from flask import Blueprint, jsonify, request
from app.models.database import db, Patient, AuditLog, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

security_bp = Blueprint('security', __name__)

# Rota para o Admin visualizar logs de auditoria
@security_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    # Verifica se quem está pedindo é Admin
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'admin':
        return jsonify({"msg": "Acesso não autorizado"}), 403
        
    logs = AuditLog.query.order_by(AuditLog.data_hora.desc()).all()
    output = []
    for log in logs:
        output.append({
            "id": log.id,
            "usuario": log.user_id,
            "acao": log.acao,
            "data": log.data_hora.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(output), 200

# Rota LGPD: Exportação de Dados (Portabilidade)
@security_bp.route('/export-data', methods=['GET'])
@jwt_required()
def export_data():
    user_id = get_jwt_identity()
    patient = Patient.query.filter_by(user_id=user_id).first()
    
    if not patient:
        return jsonify({"msg": "Paciente não encontrado"}), 404
        
    # Aqui descriptografaríamos os dados se estivessem com Fernet
    # Como simplificamos no passo anterior, retornamos direto
    dados = {
        "nome": patient.nome,
        "nascimento": patient.nascimento,
        "cpf": str(patient.cpf), # Convertendo bytes para string visual
        "historico": str(patient.historico)
    }
    
    # Registra que o usuário exportou seus dados
    log = AuditLog(user_id=user_id, acao="Exportou dados pessoais (LGPD)")
    db.session.add(log)
    db.session.commit()
    
    return jsonify(dados), 200

# Rota LGPD: Direito ao Esquecimento (Anonimização)
@security_bp.route('/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    patient = Patient.query.filter_by(user_id=user_id).first()
    
    if not patient:
        return jsonify({"msg": "Paciente não encontrado"}), 404
        
    # Anonimização dos dados sensíveis
    patient.nome = "ANONIMIZADO"
    patient.cpf = b"ANONIMIZADO"
    patient.historico = b"DADOS EXCLUIDOS PELO TITULAR"
    
    log = AuditLog(user_id=user_id, acao="Solicitou exclusão de conta (LGPD)")
    db.session.add(log)
    db.session.commit()
    
    return jsonify({"msg": "Dados pessoais removidos e anonimizados com sucesso."}), 200