import uuid
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from src.core.database import Base

class User(Base):
    """
    User Database Model.
    
    Attributes:
        id (str): UUID primary key (more secure than integer IDs).
        email (str): Unique email address (indexed).
        hashed_password (str): Bcrypt hashed string.
        is_active (bool): Soft delete flag.
        created_at (datetime): Timestamp.
    """

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String,primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(
        String,unique=True,index=True,nullable=False
        )
    
    hashed_password: Mapped[str] = mapped_column(
        String,nullable=False
        )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,default=True
        )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),server_default=func.now()
        )
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"


