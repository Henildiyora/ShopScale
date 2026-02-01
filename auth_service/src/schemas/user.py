from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    """Schema for receiving registration data."""
    password: str

class UserResponse(UserBase):
    """
    Schema for returning user data.
    
    Optimization: 'from_attributes=True' (formerly orm_mode) allows 
    Pydantic to read directly from the SQLAlchemy object.
    """
    id: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)