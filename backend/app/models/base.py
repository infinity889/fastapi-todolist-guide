from uuid import uuid4

from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column



class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=lambda: str(uuid4()))
