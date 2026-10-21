from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column
from dependencies.database import Base, SessionLocal

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

def get_user_by_id(user_id: int):
    with SessionLocal() as db:
        statement = select(User).where(User.id == user_id)
        return db.scalar(statement)