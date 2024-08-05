from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): #Creating our Base model that all other models will inherit from
    pass

db = SQLAlchemy(model_class=Base)

class Bakery(Base):
    __tablename__ = 'bakery'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255))
    category: Mapped[str] = mapped_column(db.String(255))
    price: Mapped[float] = mapped_column(db.Integer)


