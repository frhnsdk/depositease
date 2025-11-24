from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

class Bank(Base):
    __tablename__ = "banks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    logo_url = Column(String(500), nullable=True)
    website = Column(String(500), nullable=True)
    contact_number = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with products
    products = relationship("Product", back_populates="bank", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    bank_id = Column(Integer, ForeignKey("banks.id", ondelete="CASCADE"), nullable=False)
    
    # Basic Information
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)  # Fixed Deposit, DPS, etc.
    interest_rate = Column(Float, nullable=False)  # Interest rate in percentage
    min_deposit = Column(Float, nullable=False)  # Minimum deposit amount
    tenure = Column(String(100), nullable=False)  # e.g., "12 months", "24 months"
    
    # Detailed Information
    product_overview = Column(Text, nullable=True)
    key_features = Column(Text, nullable=True)  # Store as JSON string or comma-separated
    withdrawal_rules = Column(Text, nullable=True)
    eligibility_criteria = Column(Text, nullable=True)
    required_documents = Column(Text, nullable=True)  # Store as JSON string or comma-separated
    
    # Additional Fields
    max_deposit = Column(Float, nullable=True)
    compounding_frequency = Column(String(50), nullable=True)  # Monthly, Quarterly, Yearly
    premature_withdrawal_penalty = Column(String(255), nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with bank
    bank = relationship("Bank", back_populates="products")


class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    
    # Applicant Information
    applicant_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=True)
    nid_number = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    
    # Application Details
    deposit_amount = Column(Float, nullable=False)
    tenure_selected = Column(String(100), nullable=False)
    status = Column(String(50), default="pending")  # pending, approved, rejected
    notes = Column(Text, nullable=True)
    
    # Admin fields
    reviewed_by = Column(String(255), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with product
    product = relationship("Product")
