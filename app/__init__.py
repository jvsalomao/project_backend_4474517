from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.models.database import db
import os

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'hospital.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'chave-secreta-hospital-vidaplus' # Em produção, use algo seguro
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Registro de Blueprints (faremos as rotas no próximo passo)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    from app.routes.patients import patients_bp
    app.register_blueprint(patients_bp, url_prefix='/api/patients')
    from app.routes.security import security_bp
    app.register_blueprint(security_bp, url_prefix='/api/security')
    from app.routes.professionals import professionals_bp
    app.register_blueprint(professionals_bp, url_prefix='/api/professionals')
    from app.routes.appointments import appointments_bp
    app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    @app.route('/')
    def index():
        return "API SGHSS VidaPlus está rodando com sucesso! RU: 4474517 🚀", 200

    
    return app