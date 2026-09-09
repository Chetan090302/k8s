from sqlalchemy.orm import Mapped, mapped_column
from db import Base,engine

class User(Base):
    __tablename__ = "users544"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email:Mapped[str]=mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(unique=True,nullable=False,index=True)

Base.metadata.create_all(bind=engine)