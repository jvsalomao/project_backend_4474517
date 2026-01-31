from flask import Blueprint, jsonify
from app.models.database import db, User, Patient, Appointment, Professional
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard-geral', methods=['GET'])
@jwt_required()
def relatorio_gerencial():
    """
    Retorna estatísticas para o painel administrativo.
    Apenas utilizadores com role 'admin' podem aceder.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # Verificação de Segurança (RBAC)
    if not user or user.role != 'admin':
        return jsonify({"erro": "Acesso restrito a administradores."}), 403
    
    # 1. Totais do Sistema
    total_pacientes = Patient.query.count()
    total_medicos = Professional.query.count()
    
    # 2. Análise de Consultas (Agrupamento simples)
    consultas_agendadas = Appointment.query.filter_by(status='agendado').count()
    consultas_concluidas = Appointment.query.filter_by(status='concluido').count()
    consultas_canceladas = Appointment.query.filter_by(status='cancelado').count()
    
    # 3. Cálculo de Ocupação (Lógica extra para diferenciar do original)
    total_consultas = queries = Appointment.query.count()
    taxa_cancelamento = 0
    if total_consultas > 0:
        taxa_cancelamento = round((consultas_canceladas / total_consultas) * 100, 2)

    # Estrutura JSON personalizada (Diferente da referência)
    relatorio = {
        "infraestrutura": {
            "total_pacientes_ativos": total_pacientes,
            "equipa_medica": total_medicos
        },
        "operacional": {
            "total_atendimentos": total_consultas,
            "pendentes": consultas_agendadas,
            "realizados": consultas_concluidas
        },
        "kpi_qualidade": {
            "taxa_cancelamento": f"{taxa_cancelamento}%",
            "status_sistema": "Operacional"
        }
    }
    
    return jsonify(relatorio), 200