import uuid
from datetime import datetime, timezone
from app.extensions import db

def generate_uuid():
    return str(uuid.uuid4())
  
class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey("users.account_id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    amount = db.Column(db.Numeric(12,2), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    expense_type = db.Column(db.String(50), nullable=True, default="Public")  # Add expense_type field
    is_trashed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    

    def to_dict(self):
        return {
            "$id": self.id,  # Frontend expects $id
            "id": self.id,   # Also include id for compatibility
            "owner": self.user_id,  # Frontend expects owner
            "user_id": self.user_id,  # Also keep user_id for backend
            "title": self.title,
            "description": self.description,
            "amount": float(self.amount),
            "date": self.date.isoformat(),
            "expenseType": self.expense_type,  # Add expenseType field
            "isTrashed": bool(self.is_trashed),
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }