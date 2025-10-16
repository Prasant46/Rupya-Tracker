from flask import Flask
from .config import get_config
from .extensions import db, migrate, jwt, cors
from .auth.routes import bp as auth_bp
from .users.routes import bp as users_bp
from .expenses.routes import bp as expenses_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    # allow access to OAuth client ids
    app.config["GITHUB_CLIENT_ID"] = os.getenv("GITHUB_CLIENT_ID")
    app.config["GOOGLE_CLIENT_ID"] = os.getenv("GOOGLE_CLIENT_ID")
    app.config["FRONTEND_URL"] = os.getenv("FRONTEND_URL", "http://localhost:3000")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={
            r"/*": {
                "origins": ["http://localhost:3000"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
                "supports_credentials": True,
                "expose_headers": ["Content-Type", "Authorization"]
            }
        }
    )

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(expenses_bp)

    @app.route("/")
    def index():
        return {"ok": True, "message": "ExpenseTracker API"}
    
    
    
    return app