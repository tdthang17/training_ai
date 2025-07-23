from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
from app.core.security import get_password_hash


def create_initial_data():
    db: Session = SessionLocal()
    try:
        # --- Seed Roles ---
        roles = [
            schemas.RoleCreate(name="admin", description="Administrator role with full permissions"),
            schemas.RoleCreate(name="user", description="Default role for standard users")
        ]
        for role_in in roles:
            existing = crud.role.get_by_name(db, name=role_in.name)
            if not existing:
                crud.role.create(db, obj_in=role_in)
                print(f"Created role: {role_in.name}")
            else:
                print(f"Role already exists: {role_in.name}")

        # --- Seed Superuser ---
        # You can customize these credentials or read from environment
        admin_username = "admin"
        admin_email = "admin@example.com"
        admin_password = "admin123"  # change this in production!
        
        existing_user = crud.user.get_by_username(db, username=admin_username)
        if not existing_user:
            # Find admin role
            admin_role = crud.role.get_by_name(db, name="admin")
            user_in = schemas.UserCreate(
                username=admin_username,
                email=admin_email,
                fullname="System Administrator",
                password=admin_password,
                role_id=admin_role.id if admin_role else None
            )
            admin = crud.user.create(db, obj_in=user_in)
            # Elevate to superuser
            admin.is_superuser = True
            admin.is_active = True
            db.add(admin)
            db.commit()
            print(f"Created superuser: {admin_username}")
        else:
            print(f"Superuser already exists: {admin_username}")
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_data()
