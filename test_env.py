from dotenv import load_dotenv
import os

load_dotenv()

print("DB URI:", os.getenv("SQLALCHEMY_DATABASE_URI"))
