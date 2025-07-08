from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.Database import get_db
from app.models.User import User
from jose import jwt
from fastapi_jwt_auth import AuthJWT

# Constants for JWT encoding and decoding
SECRET_KEY = "my_super_secret_key_123"
ALGORITHM = "HS256"

# OAuth2 scheme to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Function to create a JWT access token for the given user identity
def create_access_token(identity: str):
    from datetime import datetime, timedelta
    payload = {
        # Subject of the token (user ID or email)
        "sub": identity, 
         # Token expiry time
        "exp": datetime.utcnow() + timedelta(minutes=30)  
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Dependency to get the currently authenticated user from the token
def get_current_user(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
) -> User:
    try:
        # Verifies the token is present and valid
        Authorize.jwt_required()  
        # Extracts user ID from token
        user_id = Authorize.get_jwt_subject() 
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
# Fetching user from database
    user = db.query(User).get(int(user_id))  
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

# Dependency factory to restrict access to users with specific roles
def get_current_user_with_roles(roles: list[str]):
    def dependency(user: User = Depends(get_current_user)):
        if user.role.name not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Requires one of roles {roles}"
            )
        return user
    return dependency
