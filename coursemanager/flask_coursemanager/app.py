from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Create database object
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Create Flask app
    app = Flask(__name__)

    # Load config settings
    app.config.from_object(Config)

    # Connect database to app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprint
    from courses.routes import courses_bp
    app.register_blueprint(courses_bp)

    # Hands-On 4, Task 2 - JSON error handlers (not HTML!)
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'status': 'error', 'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

    return app


# Create the app ONCE at module level
# This is what 'flask run' and 'flask db' commands look for
app = create_app()


# Run the app only when this file is run directly
if __name__ == '__main__':
    app.run(debug=True)