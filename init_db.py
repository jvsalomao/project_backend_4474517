from app import create_app, db
from app.models.database import User, Patient
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt()

def init():
    with app.app_context():
        # Cria o arquivo do banco de dados e as tabelas
        db.create_all()
        
        # Verifica se já existe um admin para não duplicar
        if not User.query.filter_by(email='admin@vidaplus.com').first():
            hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = User(email='admin@vidaplus.com', password=hashed_pw, role='admin')
            db.session.add(admin)
            db.session.commit()
            print("✓ Banco de dados inicializado e usuário Admin criado!")
        else:
            print("! O banco de dados já contém informações.")

if __name__ == '__main__':
    init()