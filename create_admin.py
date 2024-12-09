from src.services.auth_service import AuthService
from src.database.database import init_db

def main():
    # Initialize database first
    init_db()
    
    # Create admin user
    try:
        admin = AuthService.create_user(
            username="admin",
            password="admin123",
            email="admin@example.com",
            role="admin"
        )
        print("Admin-Benutzer erfolgreich erstellt!")
        print("Benutzername: admin")
        print("Passwort: admin123")
    except Exception as e:
        print(f"Fehler beim Erstellen des Admin-Benutzers: {str(e)}")

if __name__ == "__main__":
    main()
