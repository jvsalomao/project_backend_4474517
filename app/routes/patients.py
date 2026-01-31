from flask import Blueprint, request, jsonify
from app.models.database import db, Patient, AuditLog
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/', methods=['POST'])
@jwt_required()
def add_patient():
    user_id = get_jwt_identity()
    data = request.get_json()

    # No modelo de referência, o CPF é tratado com segurança
    new_patient = Patient(
        user_id=user_id,
        nome=data['nome'],
        cpf=data['cpf'].encode(), # Idealmente aqui entraria a lógica de criptografia Fernet
        nascimento=data.get('nascimento'),
        historico=data.get('historico', '').encode()
    )

    db.session.add(new_patient)
    
    # Registro de Auditoria (Essencial para o projeto)
    log = AuditLog(user_id=user_id, acao=f"Cadastrou o paciente: {data['nome']}")
    db.session.add(log)
    
    db.session.commit()
    return jsonify({"msg": "Paciente cadastrado com sucesso!"}), 201

@patients_bp.route('/', methods=['GET'])
@jwt_required()
def get_patients():
    patients = Patient.query.all()
    output = []
    for p in patients:
        output.append({
            "id": p.id,
            "nome": p.nome,
            "nascimento": p.nascimento
        })
    return jsonify(output), 200