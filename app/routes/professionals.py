from flask import Blueprint, request, jsonify
from app.models.database import db, Professional, User, Schedule, AuditLog
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

professionals_bp = Blueprint('professionals', __name__)

@professionals_bp.route('/', methods=['POST'])
@jwt_required()
def create_professional():
    # Apenas Admin pode criar profissionais (Segurança RBAC)
    current_user_id = get_jwt_identity()
    admin_user = User.query.get(current_user_id)
    
    if admin_user.role != 'admin':
        return jsonify({"msg": "Acesso não autorizado"}), 403

    data = request.get_json()
    
    # Verifica se o email já existe como usuário
    existing_user = User.query.filter_by(email=data['email']).first()
    if not existing_user:
        return jsonify({"msg": "Usuário deve ser criado antes do perfil profissional"}), 400

    new_pro = Professional(
        user_id=existing_user.id,
        nome=data['nome'],
        registro=data['registro'],
        especialidade=data['especialidade']
    )
    
    db.session.add(new_pro)
    
    # Log de Auditoria
    log = AuditLog(user_id=current_user_id, acao=f"Criou profissional: {data['nome']}")
    db.session.add(log)
    
    db.session.commit()
    return jsonify({"msg": "Profissional cadastrado com sucesso"}), 201

@professionals_bp.route('/', methods=['GET'])
@jwt_required()
def get_professionals():
    pros = Professional.query.filter_by(is_active=True).all()
    output = []
    for p in pros:
        output.append({
            "id": p.id,
            "nome": p.nome,
            "especialidade": p.especialidade
        })
    return jsonify(output), 200

# Endpoint para definir a Agenda (Horários)
@professionals_bp.route('/<int:pro_id>/schedule', methods=['POST'])
@jwt_required()
def add_schedule(pro_id):
    data = request.get_json()
    
    # Formato esperado: "09:00"
    hora_inicio = datetime.strptime(data['hora_inicio'], '%H:%M').time()
    hora_fim = datetime.strptime(data['hora_fim'], '%H:%M').time()
    
    new_schedule = Schedule(
        professional_id=pro_id,
        dia_semana=data['dia_semana'], # 0=Segunda, 4=Sexta...
        hora_inicio=hora_inicio,
        hora_fim=hora_fim
    )
    
    db.session.add(new_schedule)
    db.session.commit()
    
    return jsonify({"msg": "Horário de agenda adicionado"}), 201