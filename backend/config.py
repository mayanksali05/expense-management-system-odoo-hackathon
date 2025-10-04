import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/expense_db")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")  # or use S3 in prod
