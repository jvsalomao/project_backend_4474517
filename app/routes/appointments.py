from flask import Blueprint, request, jsonify
from app.models.database import db, Appointment, Schedule, AuditLog
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/', methods=['POST'])
@jwt_required()
def create_appointment():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Converter string "2024-12-01 14:00" para objeto datetime
    data_consulta = datetime.strptime(data['data_hora'], '%Y-%m-%d %H:%M')
    
    # Verificação simples de disponibilidade
    dia_semana = data_consulta.weekday()
    
    # Busca se o médico atende nesse dia da semana
    agenda = Schedule.query.filter_by(
        professional_id=data['professional_id'], 
        dia_semana=dia_semana
    ).first()
    
    if not agenda:
        return jsonify({"msg": "O médico não atende neste dia da semana."}), 400
        
    # Lógica de criação da consulta
    new_appt = Appointment(
        patient_id=data['patient_id'],
        professional_id=data['professional_id'],
        data_hora=data_consulta,
        status='agendado'
    )
    
    db.session.add(new_appt)
    
    # Auditoria
    log = AuditLog(user_id=user_id, acao=f"Agendou consulta ID {new_appt.id}")
    db.session.add(log)
    
    db.session.commit()
    
    return jsonify({"msg": "Consulta agendada com sucesso!"}), 201

@appointments_bp.route('/', methods=['GET'])
@jwt_required()
def list_appointments():
    # Lista consultas do usuário logado
    appointments = Appointment.query.all()
    output = []
    for a in appointments:
        output.append({
            "id": a.id,
            "data": a.data_hora.strftime('%Y-%m-%d %H:%M'),
            "status": a.status
        })
    return jsonify(output), 200