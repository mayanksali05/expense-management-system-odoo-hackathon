from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database.db_connection import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Allow requests from your React app
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    JWTManager(app)
    init_db(app)

    # --- Register Blueprints ---
    try:
        from routes.auth import auth_bp
        from routes.expenses import expense_bp
        from routes.approvals import approvals_bp
        # from routes.users import users_bp
        # from routes.ocr import ocr_bp
    except ImportError as e:
        print("Blueprint import failed:", e)
        raise

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(expense_bp, url_prefix="/api/expenses")
    app.register_blueprint(approvals_bp, url_prefix="/api/approvals")
    # app.register_blueprint(users_bp, url_prefix="/api/users")
    # app.register_blueprint(ocr_bp, url_prefix="/api/ocr")

    print(app.url_map)
    print("Registered Blueprints:", app.blueprints)
    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
