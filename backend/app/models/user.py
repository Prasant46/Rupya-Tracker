import uuid
from datetime import datetime, timezone
from app.extensions import db

def generate_uuid():
    return str(uuid.uuid4())
  
class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.String, primary_key=True, default=generate_uuid)
  account_id = db.Column(db.String, unique=True, nullable=False, default=generate_uuid)
  name = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(255), unique=True, nullable=False, index=True)
  password_hash = db.Column(db.String(255), nullable=True)
  avatar_url = db.Column(db.String(1024), nullable=True)
  created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

  def to_dict(self):
        return {
            "id": self.id,
            "accountId": self.account_id,
            "name": self.name,
            "email": self.email,
            "avatarUrl": self.avatar_url
        }