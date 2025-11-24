"""
Database Creation and Initialization Script for DepositEase

This script will:
1. Create the PostgreSQL database if it doesn't exist
2. Create all tables based on SQLAlchemy models
3. Insert sample data for testing

Usage:
    python create_database.py
"""

import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError, OperationalError
from database import Base, DATABASE_URL
from models import Bank, Product, Application, Admin
import os
from dotenv import load_dotenv
from auth import get_password_hash

load_dotenv()

def create_database():
    """Create the database if it doesn't exist"""
    # Parse the database URL to get connection info
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/depositease")
    
    # Split the URL to get the base connection and database name
    parts = database_url.rsplit('/', 1)
    base_url = parts[0]
    db_name = parts[1] if len(parts) > 1 else 'depositease'
    
    print(f"Connecting to PostgreSQL server...")
    print(f"Database to create: {db_name}")
    
    try:
        # Connect to PostgreSQL server (default 'postgres' database)
        engine = create_engine(f"{base_url}/postgres")
        
        with engine.connect() as conn:
            # Set isolation level to autocommit to create database
            conn.execute(text("COMMIT"))
            
            # Check if database exists
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": db_name}
            )
            exists = result.fetchone()
            
            if not exists:
                print(f"Creating database '{db_name}'...")
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                print(f"✓ Database '{db_name}' created successfully!")
            else:
                print(f"✓ Database '{db_name}' already exists.")
        
        engine.dispose()
        
    except OperationalError as e:
        print(f"✗ Error connecting to PostgreSQL: {e}")
        print("\nPlease ensure:")
        print("1. PostgreSQL is installed and running")
        print("2. The connection details in .env are correct")
        print("3. The PostgreSQL user has permission to create databases")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


def create_tables():
    """Create all tables in the database"""
    try:
        database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/depositease")
        engine = create_engine(database_url)
        
        print("\nCreating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ All tables created successfully!")
        
        engine.dispose()
        return engine
        
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        sys.exit(1)


def insert_sample_data():
    """Insert sample data for testing"""
    try:
        database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/depositease")
        engine = create_engine(database_url)
        
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        print("\nInserting sample data...")
        
        # Check if data already exists
        existing_banks = db.query(Bank).count()
        if existing_banks > 0:
            print("✓ Sample data already exists. Skipping insertion.")
            db.close()
            return
        
        # Sample Banks
        banks_data = [
            {
                "name": "Dutch-Bangla Bank",
                "description": "Dutch-Bangla Bank Limited (DBBL) is a leading private sector bank in Bangladesh.",
                "website": "https://www.dutchbanglabank.com",
                "contact_number": "16216",
                "email": "info@dutchbanglabank.com",
                "is_active": True
            },
            {
                "name": "BRAC Bank",
                "description": "BRAC Bank is one of the fastest-growing commercial banks in Bangladesh.",
                "website": "https://www.bracbank.com",
                "contact_number": "16221",
                "email": "info@bracbank.com",
                "is_active": True
            },
            {
                "name": "City Bank",
                "description": "The City Bank Limited is one of the first private sector banks in Bangladesh.",
                "website": "https://www.thecitybank.com",
                "contact_number": "16234",
                "email": "contact@thecitybank.com",
                "is_active": True
            },
            {
                "name": "Eastern Bank",
                "description": "Eastern Bank Limited (EBL) is a leading private commercial bank in Bangladesh.",
                "website": "https://www.ebl.com.bd",
                "contact_number": "16235",
                "email": "info@ebl.com.bd",
                "is_active": True
            }
        ]
        
        banks = []
        for bank_data in banks_data:
            bank = Bank(**bank_data)
            db.add(bank)
            banks.append(bank)
        
        db.commit()
        print(f"✓ Inserted {len(banks)} banks")
        
        # Sample Products
        products_data = [
            {
                "bank_id": 1,  # Dutch-Bangla Bank
                "name": "DBBL Premium Fixed Deposit",
                "type": "Fixed Deposit",
                "interest_rate": 6.5,
                "min_deposit": 10000,
                "tenure": "12 months",
                "product_overview": "A secure investment option with competitive interest rates and flexible tenure options.",
                "key_features": "Competitive interest rates|Monthly/Quarterly interest payout|Premature withdrawal facility|Auto-renewal option",
                "withdrawal_rules": "Premature withdrawal allowed with penalty. 1% penalty on interest earned if withdrawn before 6 months. No penalty after 6 months.",
                "eligibility_criteria": "Minimum age 18 years|Valid NID card|Initial deposit of ৳10,000",
                "required_documents": "National ID Card (NID)|Recent Passport Size Photo|TIN Certificate (for amounts above ৳5 lac)|Nominee's NID and Photo",
                "max_deposit": 10000000,
                "compounding_frequency": "Quarterly",
                "premature_withdrawal_penalty": "1% of interest if withdrawn before 6 months"
            },
            {
                "bank_id": 1,  # Dutch-Bangla Bank
                "name": "DBBL Millionaire DPS",
                "type": "DPS",
                "interest_rate": 7.0,
                "min_deposit": 5000,
                "tenure": "24 months",
                "product_overview": "Monthly savings scheme designed to build wealth through disciplined savings with attractive returns.",
                "key_features": "Higher interest rate|Flexible monthly installment|Loan facility against DPS|Auto-debit facility available",
                "withdrawal_rules": "Early encashment allowed after 1 year with reduced interest. Full maturity amount payable after completion of tenure.",
                "eligibility_criteria": "Minimum age 18 years|Valid NID card|Regular income source",
                "required_documents": "National ID Card (NID)|Recent Passport Size Photo|Proof of Income|Nominee's NID and Photo",
                "max_deposit": 50000,
                "compounding_frequency": "Monthly",
                "premature_withdrawal_penalty": "2% reduction in interest rate"
            },
            {
                "bank_id": 2,  # BRAC Bank
                "name": "BRAC Savings Plus DPS",
                "type": "DPS",
                "interest_rate": 7.0,
                "min_deposit": 5000,
                "tenure": "24 months",
                "product_overview": "A monthly deposit scheme that helps you save systematically and earn attractive returns.",
                "key_features": "Competitive returns|Flexible deposit amount|Loan facility up to 80% of deposit|SMS alerts for payment",
                "withdrawal_rules": "Premature encashment allowed after 1 year of regular payments with reduced interest rate.",
                "eligibility_criteria": "Age 18-60 years|Valid NID|BRAC Bank account holder",
                "required_documents": "National ID Card|Passport size photos|Account opening form|Nominee information",
                "max_deposit": 100000,
                "compounding_frequency": "Monthly",
                "premature_withdrawal_penalty": "Interest reduced by 2%"
            },
            {
                "bank_id": 2,  # BRAC Bank
                "name": "BRAC Secured Fixed Deposit",
                "type": "Fixed Deposit",
                "interest_rate": 6.8,
                "min_deposit": 25000,
                "tenure": "18 months",
                "product_overview": "Fixed deposit with guaranteed returns and high security for your savings.",
                "key_features": "Guaranteed returns|Flexible tenure|Overdraft facility|Quarterly interest credit",
                "withdrawal_rules": "Premature withdrawal allowed with 1.5% penalty on interest for withdrawals before maturity.",
                "eligibility_criteria": "Minimum age 18 years|Valid identification|Minimum deposit ৳25,000",
                "required_documents": "NID/Passport|2 copies passport size photo|TIN certificate|Utility bill",
                "max_deposit": 50000000,
                "compounding_frequency": "Quarterly",
                "premature_withdrawal_penalty": "1.5% of earned interest"
            },
            {
                "bank_id": 3,  # City Bank
                "name": "City Antorik Fixed Deposit",
                "type": "Fixed Deposit",
                "interest_rate": 6.75,
                "min_deposit": 25000,
                "tenure": "36 months",
                "product_overview": "Long-term fixed deposit with excellent returns for patient investors.",
                "key_features": "High interest rate|Cumulative/Non-cumulative options|Loan against FDR|Auto-renewal facility",
                "withdrawal_rules": "Premature withdrawal permitted after 3 months with penalty. 2% penalty on interest if withdrawn before 1 year.",
                "eligibility_criteria": "Age 18 and above|Valid NID or Passport|Minimum deposit amount",
                "required_documents": "National ID/Passport|Photograph|Signature card|Nominee documents",
                "max_deposit": 20000000,
                "compounding_frequency": "Quarterly",
                "premature_withdrawal_penalty": "2% of interest for withdrawal before 1 year"
            },
            {
                "bank_id": 3,  # City Bank
                "name": "City Super Saver DPS",
                "type": "DPS",
                "interest_rate": 7.25,
                "min_deposit": 3000,
                "tenure": "12 months",
                "product_overview": "Short-term monthly deposit scheme with attractive interest rates for quick savers.",
                "key_features": "Highest interest in the market|Short tenure|Easy installment|Instant loan facility",
                "withdrawal_rules": "Maturity benefit paid at the end of tenure. Early withdrawal available after 6 months with 2.5% penalty.",
                "eligibility_criteria": "Minimum age 18 years|City Bank account required|Regular income",
                "required_documents": "NID card|Recent photos|Bank account statement|Nominee ID",
                "max_deposit": 25000,
                "compounding_frequency": "Monthly",
                "premature_withdrawal_penalty": "2.5% interest reduction"
            },
            {
                "bank_id": 4,  # Eastern Bank
                "name": "EBL Double Deposit Scheme",
                "type": "DPS",
                "interest_rate": 6.8,
                "min_deposit": 3000,
                "tenure": "12 months",
                "product_overview": "Popular DPS scheme that helps you double your money with consistent savings.",
                "key_features": "Money doubling opportunity|Low monthly installment|Flexible terms|Online payment option",
                "withdrawal_rules": "Full amount payable at maturity. Premature encashment available after 6 months with 2% interest penalty.",
                "eligibility_criteria": "Age between 18-65 years|Valid NID|EBL account holder",
                "required_documents": "National ID Card|Passport size photo|Account details|Nominee information",
                "max_deposit": 50000,
                "compounding_frequency": "Monthly",
                "premature_withdrawal_penalty": "2% penalty on interest"
            },
            {
                "bank_id": 4,  # Eastern Bank
                "name": "EBL Term Deposit",
                "type": "Fixed Deposit",
                "interest_rate": 6.9,
                "min_deposit": 50000,
                "tenure": "24 months",
                "product_overview": "Medium to long-term fixed deposit with excellent returns and flexible withdrawal options.",
                "key_features": "Competitive interest rates|Multiple tenure options|Premature withdrawal facility|Loan against deposit",
                "withdrawal_rules": "Premature withdrawal allowed anytime with 1.5% penalty on interest earned.",
                "eligibility_criteria": "Minimum age 18 years|Valid identification document|Minimum balance requirement",
                "required_documents": "NID/Passport copy|Recent photographs|TIN certificate (if applicable)|Utility bill for address proof",
                "max_deposit": 15000000,
                "compounding_frequency": "Quarterly",
                "premature_withdrawal_penalty": "1.5% of total interest"
            }
        ]
        
        products = []
        for product_data in products_data:
            product = Product(**product_data)
            db.add(product)
            products.append(product)
        
        db.commit()
        print(f"✓ Inserted {len(products)} products")
        
        # Sample Applications
        applications_data = [
            {
                "product_id": 1,
                "applicant_name": "Kamal Hassan",
                "phone": "01712345678",
                "email": "kamal@example.com",
                "nid_number": "1234567890",
                "address": "Dhaka, Bangladesh",
                "deposit_amount": 50000,
                "tenure_selected": "12 months",
                "status": "pending"
            },
            {
                "product_id": 3,
                "applicant_name": "Fatima Rahman",
                "phone": "01823456789",
                "email": "fatima@example.com",
                "nid_number": "9876543210",
                "address": "Chittagong, Bangladesh",
                "deposit_amount": 10000,
                "tenure_selected": "24 months",
                "status": "approved",
                "reviewed_by": "Admin"
            },
            {
                "product_id": 5,
                "applicant_name": "Rahim Ahmed",
                "phone": "01934567890",
                "email": "rahim@example.com",
                "nid_number": "5555555555",
                "address": "Sylhet, Bangladesh",
                "deposit_amount": 30000,
                "tenure_selected": "36 months",
                "status": "pending"
            },
            {
                "product_id": 7,
                "applicant_name": "Nusrat Jahan",
                "phone": "01645678901",
                "email": "nusrat@example.com",
                "nid_number": "7777777777",
                "address": "Khulna, Bangladesh",
                "deposit_amount": 5000,
                "tenure_selected": "12 months",
                "status": "rejected",
                "reviewed_by": "Admin",
                "notes": "Incomplete documentation"
            }
        ]
        
        applications = []
        for app_data in applications_data:
            application = Application(**app_data)
            db.add(application)
            applications.append(application)
        
        db.commit()
        print(f"✓ Inserted {len(applications)} applications")
        
        print("\n✓ Sample data inserted successfully!")
        
        db.close()
        engine.dispose()
        
    except Exception as e:
        print(f"✗ Error inserting sample data: {e}")
        sys.exit(1)


def main():
    """Main function to run the database setup"""
    print("=" * 60)
    print("DepositEase Database Setup Script")
    print("=" * 60)
    
    # Step 1: Create database
    create_database()
    
    # Step 2: Create tables
    create_tables()
    
    # Step 3: Ask user if they want sample data
    print("\nDo you want to insert sample data? (y/n): ", end="")
    choice = input().strip().lower()
    if choice == 'y':
        insert_sample_data()
    else:
        print("✓ Skipping sample data insertion. Database is empty and ready for your data.")
    
    print("\n" + "=" * 60)
    print("✓ Database setup completed successfully!")
    print("=" * 60)
    print("\nYou can now start the FastAPI server with:")
    print("  uvicorn main:app --reload")
    print("\nDatabase Details:")
    print(f"  URL: {os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/depositease')}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
