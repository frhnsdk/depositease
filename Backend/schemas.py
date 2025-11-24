from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Admin Schemas
class AdminRegister(BaseModel):
    username: str
    password: str

class AdminLogin(BaseModel):
    username: str
    password: str

class Admin(BaseModel):
    id: int
    username: str
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Bank Schemas
class BankBase(BaseModel):
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool = True

class BankCreate(BankBase):
    pass

class BankUpdate(BankBase):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class Bank(BankBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Product Schemas
class ProductBase(BaseModel):
    bank_id: int
    name: str
    type: str
    interest_rate: float
    min_deposit: float
    tenure: str
    product_overview: Optional[str] = None
    key_features: Optional[str] = None
    withdrawal_rules: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    required_documents: Optional[str] = None
    max_deposit: Optional[float] = None
    compounding_frequency: Optional[str] = None
    premature_withdrawal_penalty: Optional[str] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    bank_id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    interest_rate: Optional[float] = None
    min_deposit: Optional[float] = None
    tenure: Optional[str] = None
    product_overview: Optional[str] = None
    key_features: Optional[str] = None
    withdrawal_rules: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    required_documents: Optional[str] = None
    max_deposit: Optional[float] = None
    compounding_frequency: Optional[str] = None
    premature_withdrawal_penalty: Optional[str] = None
    is_active: Optional[bool] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Application Schemas
class ApplicationBase(BaseModel):
    product_id: int
    applicant_name: str
    phone: str
    email: Optional[EmailStr] = None
    nid_number: Optional[str] = None
    address: Optional[str] = None
    deposit_amount: float
    tenure_selected: str
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    reviewed_by: Optional[str] = None

class Application(ApplicationBase):
    id: int
    status: str
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Response Schemas with Relations
class BankWithProducts(Bank):
    products: List[Product] = []

class ProductWithBank(Product):
    bank: Bank
