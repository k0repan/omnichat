from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import func, ForeignKey, text
from typing import Annotated
from datetime import datetime


int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"
    
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class User(Base):
    id: Mapped[int_pk]
    phone: Mapped[str]
    full_name: Mapped[str]
    tg_id: Mapped[str_null_true]
    vk_id: Mapped[str_null_true]
    wa_id: Mapped[str_null_true]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"full_name={self.full_name}, phone={self.phone})")
    
    def __repr__(self):
        return self.__str__()


class Ticket(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    messenger: Mapped[str]
    problem_type: Mapped[str]
    status: Mapped[str] = mapped_column(server_default=text("active"))

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"user_id={self.user_id}, messenger={self.messenger}, "
                f"problem_type={self.problem_type}, status={self.status})")

    def __repr__(self):
        return self.__str__()


class Message(Base):
    id: Mapped[int_pk]
    ticket_id: Mapped[int] = mapped_column(ForeignKey("ticket.id"), nullable=False)
    text: Mapped[str_null_true]

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, text={self.text})"
    
    def __repr__(self):
        return self.__str__()
    

class Service(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    service_type: Mapped[str]
    service_name: Mapped[str]
    price: Mapped[float]
    status: Mapped[str] = mapped_column(server_default=text("active"))

    def __str__(self):
        return(f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id},"
               f"service_type={self.service_type}, service_name={self.service_name}, "
               f"status={self.status}")
    
    def __repr__(self):
        return self.__str__()
    