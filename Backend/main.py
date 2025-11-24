from fastapi import FastAPI, Depends, HTTPException, status, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import models
import schemas
import auth
from database import engine, get_db
from pathlib import Path

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DepositEase API",
    description="API for managing banks, products, and applications",
    version="1.0.0"
)

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the frontend directory path
frontend_dir = Path(__file__).parent.parent / "Frontend"

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# ==================== FRONTEND ROUTES ====================

@app.get("/")
def serve_home():
    """Serve the home page"""
    return FileResponse(frontend_dir / "index.html")

@app.get("/login")
def serve_login():
    """Serve the login page"""
    return FileResponse(frontend_dir / "login.html")

@app.get("/admin")
def serve_admin(access_token: Optional[str] = Cookie(None)):
    """Serve the admin page (protected)"""
    if not access_token or not auth.verify_token(access_token):
        return RedirectResponse(url="/login", status_code=303)
    return FileResponse(frontend_dir / "admin.html")

@app.get("/admin.html")
def serve_admin_html(access_token: Optional[str] = Cookie(None)):
    """Serve the admin page (protected)"""
    if not access_token or not auth.verify_token(access_token):
        return RedirectResponse(url="/login", status_code=303)
    return FileResponse(frontend_dir / "admin.html")

@app.get("/index.html")
def serve_index_html():
    """Serve the home page"""
    return FileResponse(frontend_dir / "index.html")

@app.get("/styles.css")
def serve_styles():
    """Serve the CSS file"""
    return FileResponse(frontend_dir / "styles.css")

@app.get("/script.js")
def serve_script():
    """Serve the JavaScript file"""
    return FileResponse(frontend_dir / "script.js")

@app.get("/product-details.html")
def serve_product_details():
    """Serve the product details page"""
    return FileResponse(frontend_dir / "product-details.html")

@app.get("/application.html")
def serve_application():
    """Serve the application page"""
    return FileResponse(frontend_dir / "application.html")

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/auth/register", response_model=schemas.Admin, status_code=status.HTTP_201_CREATED)
def register_admin(admin: schemas.AdminRegister, db: Session = Depends(get_db)):
    """Register a new admin"""
    # Check if username already exists
    existing_admin = db.query(models.Admin).filter(models.Admin.username == admin.username).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create new admin with hashed password
    hashed_password = auth.get_password_hash(admin.password)
    new_admin = models.Admin(
        username=admin.username,
        password_hash=hashed_password
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

@app.post("/auth/login")
def login_admin(response: Response, admin: schemas.AdminLogin, db: Session = Depends(get_db)):
    """Login admin and set cookie"""
    # Find admin by username
    db_admin = db.query(models.Admin).filter(models.Admin.username == admin.username).first()
    if not db_admin or not auth.verify_password(admin.password, db_admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Update last login
    db_admin.last_login = datetime.now()
    db.commit()
    
    # Create access token
    access_token = auth.create_access_token(data={"sub": admin.username})
    
    # Set cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60 * 60 * 24,  # 24 hours
        samesite="lax"
    )
    
    return {"message": "Login successful"}

@app.post("/auth/logout")
def logout_admin(response: Response):
    """Logout admin by clearing cookie"""
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}

@app.get("/auth/me", response_model=schemas.Admin)
def get_current_admin_info(current_admin: models.Admin = Depends(auth.get_current_admin)):
    """Get current logged-in admin info"""
    return current_admin

# ==================== API ENDPOINTS ====================

@app.get("/api")
def read_root():
    return {"message": "Welcome to DepositEase API", "status": "active"}


@app.post("/banks", response_model=schemas.Bank, status_code=status.HTTP_201_CREATED)
def create_bank(bank: schemas.BankCreate, db: Session = Depends(get_db)):
    """Create a new bank"""
    # Check if bank name already exists
    db_bank = db.query(models.Bank).filter(models.Bank.name == bank.name).first()
    if db_bank:
        raise HTTPException(status_code=400, detail="Bank name already exists")
    
    new_bank = models.Bank(**bank.model_dump())
    db.add(new_bank)
    db.commit()
    db.refresh(new_bank)
    return new_bank


@app.get("/banks", response_model=List[schemas.BankWithProducts])
def get_banks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all banks with their products"""
    banks = db.query(models.Bank).offset(skip).limit(limit).all()
    return banks


@app.get("/banks/{bank_id}", response_model=schemas.BankWithProducts)
def get_bank(bank_id: int, db: Session = Depends(get_db)):
    """Get a specific bank with its products"""
    bank = db.query(models.Bank).filter(models.Bank.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank


@app.put("/banks/{bank_id}", response_model=schemas.Bank)
def update_bank(bank_id: int, bank: schemas.BankUpdate, db: Session = Depends(get_db)):
    """Update a bank"""
    db_bank = db.query(models.Bank).filter(models.Bank.id == bank_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    
    update_data = bank.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_bank, key, value)
    
    db.commit()
    db.refresh(db_bank)
    return db_bank


@app.delete("/banks/{bank_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bank(bank_id: int, db: Session = Depends(get_db)):
    """Delete a bank (will also delete all associated products)"""
    db_bank = db.query(models.Bank).filter(models.Bank.id == bank_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    
    db.delete(db_bank)
    db.commit()
    return None


# ==================== PRODUCT ENDPOINTS ====================

@app.post("/products", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    # Check if bank exists
    bank = db.query(models.Bank).filter(models.Bank.id == product.bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/products", response_model=List[schemas.ProductWithBank])
def get_products(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    bank_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all products with optional filters"""
    query = db.query(models.Product)
    
    if type:
        query = query.filter(models.Product.type == type)
    if bank_id:
        query = query.filter(models.Product.bank_id == bank_id)
    
    products = query.offset(skip).limit(limit).all()
    return products


@app.get("/products/{product_id}", response_model=schemas.ProductWithBank)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product with bank details"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/banks/{bank_id}/products", response_model=List[schemas.Product])
def get_bank_products(bank_id: int, db: Session = Depends(get_db)):
    """Get all products for a specific bank"""
    bank = db.query(models.Bank).filter(models.Bank.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    
    products = db.query(models.Product).filter(models.Product.bank_id == bank_id).all()
    return products


@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """Update a product"""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return None


# ==================== APPLICATION ENDPOINTS ====================

@app.post("/applications", response_model=schemas.Application, status_code=status.HTTP_201_CREATED)
def create_application(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    """Create a new application"""
    # Check if product exists
    product = db.query(models.Product).filter(models.Product.id == application.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    new_application = models.Application(**application.model_dump())
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application


@app.get("/applications", response_model=List[schemas.Application])
def get_applications(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all applications with optional status filter"""
    query = db.query(models.Application)
    
    if status_filter:
        query = query.filter(models.Application.status == status_filter)
    
    applications = query.order_by(models.Application.created_at.desc()).offset(skip).limit(limit).all()
    return applications


@app.get("/applications/{application_id}", response_model=schemas.Application)
def get_application(application_id: int, db: Session = Depends(get_db)):
    """Get a specific application"""
    application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@app.put("/applications/{application_id}", response_model=schemas.Application)
def update_application(
    application_id: int,
    application: schemas.ApplicationUpdate,
    db: Session = Depends(get_db)
):
    """Update an application (mainly for status changes)"""
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    update_data = application.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_application, key, value)
    
    # Set reviewed_at if status is being updated
    if application.status:
        from datetime import datetime
        db_application.reviewed_at = datetime.now()
    
    db.commit()
    db.refresh(db_application)
    return db_application


@app.delete("/applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    """Delete an application"""
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.delete(db_application)
    db.commit()
    return None


# ==================== STATISTICS ENDPOINTS ====================

@app.get("/stats/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin)
):
    """Get dashboard statistics (protected)"""
    total_banks = db.query(models.Bank).count()
    total_products = db.query(models.Product).count()
    pending_applications = db.query(models.Application).filter(models.Application.status == "pending").count()
    
    # Get approved today
    from datetime import datetime, timedelta
    today = datetime.now().date()
    approved_today = db.query(models.Application).filter(
        models.Application.status == "approved",
        models.Application.reviewed_at >= today
    ).count()
    
    return {
        "total_banks": total_banks,
        "total_products": total_products,
        "pending_applications": pending_applications,
        "approved_today": approved_today
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
