from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
    true,
    false,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    role: Mapped[str] = mapped_column(
        String(10), default="customer", server_default="customer"
    )

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint("role IN ('customer', 'staff')", name="ck_users_role"),
        CheckConstraint("email LIKE '%_@_%'", name="ck_users_email"),
    )


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=true())
    avg_minutes: Mapped[int] = mapped_column(default=5, server_default="5")
    notice: Mapped[str | None] = mapped_column(Text)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")

    __table_args__ = (
        CheckConstraint("avg_minutes > 0", name="ck_services_avg_minutes"),
    )


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT")
    )
    status: Mapped[str] = mapped_column(
        String(20), default="waiting", server_default="waiting"
    )
    is_priority: Mapped[bool] = mapped_column(default=False, server_default=false())
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    called_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'left')",
            name="ck_tickets_status",
        ),
        CheckConstraint(
            "called_at IS NULL OR called_at >= created_at",
            name="ck_tickets_called_at",
        ),
        CheckConstraint(
            "closed_at IS NULL OR closed_at >= created_at",
            name="ck_tickets_closed_at",
        ),
        CheckConstraint(
            "(status IN ('waiting', 'called')) = (closed_at IS NULL)",
            name="ck_tickets_closed_matches_status",
        ),
    )