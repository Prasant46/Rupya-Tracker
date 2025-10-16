from app import create_app
from app.extensions import db
from flask.cli import FlaskGroup
import os

# Import models so Flask-Migrate can detect them
from app.models import User, Expense

app = create_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()