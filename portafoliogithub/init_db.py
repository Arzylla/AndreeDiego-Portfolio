from app import app, db, User
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create admin user with password
            admin_user = User(
                username='admin',
                password_hash=generate_password_hash('Admin2025!')
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists!")

if __name__ == '__main__':
    init_db()
