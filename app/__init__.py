from flask import Flask
from .models import db, bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restx import Api, Resource, fields

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret'

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)
    CORS(app)

    # Import and register blueprint
    from .routes.main import ns
    api = Api(app,
              version='1.0',
              title='Todo API',
              description='Full JWT + Todo API with Swagger',
              doc='/docs')
    api.add_namespace(ns, path='/api')

    # Create tables
    with app.app_context():
        db.create_all()

    return app
