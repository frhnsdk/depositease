# DepositEase Backend API

FastAPI backend for the DepositEase application with PostgreSQL database.

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher

## Setup Instructions

### 1. Install PostgreSQL

Download and install PostgreSQL from: https://www.postgresql.org/download/

During installation, remember the password you set for the `postgres` user.

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit the `.env` file and update the database credentials:

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/depositease
SECRET_KEY=your-secret-key-change-this
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

### 4. Create Database and Tables

Run the database creation script:

```bash
python create_database.py
```

This script will:
- Create the `depositease` database
- Create all necessary tables (banks, products, applications)
- Insert sample data for testing

### 5. Start the FastAPI Server

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Database Schema

### Banks Table
- id (Primary Key)
- name (Unique)
- description
- logo_url
- website
- contact_number
- email
- is_active
- created_at
- updated_at

### Products Table
- id (Primary Key)
- bank_id (Foreign Key → banks.id)
- name
- type (Fixed Deposit, DPS, etc.)
- interest_rate
- min_deposit
- tenure
- product_overview
- key_features
- withdrawal_rules
- eligibility_criteria
- required_documents
- max_deposit
- compounding_frequency
- premature_withdrawal_penalty
- is_active
- created_at
- updated_at

### Applications Table
- id (Primary Key)
- product_id (Foreign Key → products.id)
- applicant_name
- phone
- email
- nid_number
- address
- deposit_amount
- tenure_selected
- status (pending, approved, rejected)
- notes
- reviewed_by
- reviewed_at
- created_at
- updated_at

## API Endpoints

### Banks
- `GET /banks` - List all banks
- `GET /banks/{id}` - Get bank by ID
- `POST /banks` - Create new bank
- `PUT /banks/{id}` - Update bank
- `DELETE /banks/{id}` - Delete bank

### Products
- `GET /products` - List all products
- `GET /products/{id}` - Get product by ID
- `GET /banks/{bank_id}/products` - Get products by bank
- `POST /products` - Create new product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

### Applications
- `GET /applications` - List all applications
- `GET /applications/{id}` - Get application by ID
- `POST /applications` - Create new application
- `PUT /applications/{id}` - Update application (change status)
- `DELETE /applications/{id}` - Delete application

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check if the credentials in `.env` are correct
- Verify the database exists: `psql -U postgres -l`

### Port Already in Use
If port 8000 is already in use, run on a different port:
```bash
uvicorn main:app --reload --port 8001
```

## Development

To reset the database:
```bash
python create_database.py
```

To add more sample data, edit the `insert_sample_data()` function in `create_database.py`.
