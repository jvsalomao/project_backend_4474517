from flask import Blueprint, request, jsonify
from app.models.database import db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Verifica se o usuário já existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email já cadastrado"}), 400
    
    # Criptografa a senha
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    new_user = User(
        email=data['email'],
        password=hashed_password,
        role=data.get('role', 'paciente') # Padrão é paciente
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "Usuário criado com sucesso"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        # Cria o token de acesso (JWT)
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token, role=user.role), 200
    
    return jsonify({"msg": "E-mail ou senha incorretos"}), 401