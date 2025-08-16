# Form Service API

A dynamic form schema and submission service with validation and verification.

## Features

- Dynamic form schema management
- Form submission with validation
- Conditional field visibility
- Computed fields
- Email OTP verification (mock)
- PAN verification (mock)
- Admin endpoints for management

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate


### Install Dependencies
  pip install fastapi uvicorn sqlalchemy python-multipart
### Initialize Database
Add this to app/main.py
from app.models.database import Base, engine
Base.metadata.create_all(bind=engine)

### Run the Application

uvicorn app.main:app --reload

