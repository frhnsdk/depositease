import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Try different connection strings
passwords = ['rootfarhan', 'root', 'postgres', 'admin']

for pwd in passwords:
    try:
        conn_string = f"postgresql://postgres:{pwd}@localhost:5432/postgres"
        print(f"Trying password: {pwd}")
        conn = psycopg2.connect(conn_string)
        print(f"✓ SUCCESS! Password is: {pwd}")
        conn.close()
        print(f"\nUpdate your .env file with:")
        print(f"DATABASE_URL=postgresql://postgres:{pwd}@localhost:5432/depositease")
        break
    except Exception as e:
        print(f"✗ Failed with password '{pwd}'")
        continue
else:
    print("\nNone of the common passwords worked.")
    print("Please check your PostgreSQL password in pgAdmin or when you installed it.")
