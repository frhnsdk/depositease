# DepositEase - Quick Start Guide

## Prerequisites
1. Install Python 3.9+ from https://www.python.org/downloads/
2. Install PostgreSQL from https://www.postgresql.org/download/windows/

## Setup Steps

### 1. Install Backend Dependencies
```powershell
cd Z:\Depositease\backend
pip install -r requirements.txt
```

### 2. Configure Database
Edit `backend\.env` and update your PostgreSQL password:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/depositease
```

### 3. Create Database
```powershell
cd Z:\Depositease\backend
python create_database.py
```
When prompted "Do you want to insert sample data? (y/n):", type **n** to start with an empty database.

### 4. Start Backend Server
```powershell
cd Z:\Depositease\backend
Create and Activate venv
uvicorn main:app --reload
```
Backend will run on: http://localhost:8000

### 5. Open Frontend
Open `Z:\Depositease\Frontend\admin.html` in your browser.

## Features

### ✅ Add Banks
- Click "Add Bank" button
- Enter bank name, website, contact details
- Data saves to PostgreSQL automatically

### ✅ Add Products
- Click "Add Product" button
- Select bank, enter product details
- Includes: type, interest rate, min deposit, tenure, overview, features, rules, eligibility, documents

### ✅ View & Manage
- Switch tabs to view Banks, Products, Applications
- Edit button: Update existing records
- Delete button: Remove records from database
- All data syncs with PostgreSQL in real-time

### ✅ Applications
- View all applications
- Approve/Reject pending applications
- Status updates save to database

## API Endpoints
- **GET** `/banks` - Get all banks
- **POST** `/banks` - Add new bank
- **PUT** `/banks/{id}` - Update bank
- **DELETE** `/banks/{id}` - Delete bank
- **GET** `/products` - Get all products
- **POST** `/products` - Add new product
- **PUT** `/products/{id}` - Update product
- **DELETE** `/products/{id}` - Delete product
- **GET** `/applications` - Get all applications
- **PUT** `/applications/{id}` - Update application status
- **GET** `/stats/dashboard` - Get dashboard statistics

View full API docs: http://localhost:8000/docs

## Database Access
Use pgAdmin or psql to view data:
```powershell
psql -U postgres -d depositease
```

## Troubleshooting
- If API errors occur, ensure backend server is running
- Check browser console (F12) for errors
- Verify PostgreSQL is running (services.msc)
