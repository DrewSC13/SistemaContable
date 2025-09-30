#!/usr/bin/env python3
import sys
import os

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def check_dependencies():
    print("🔍 Verificando dependencias...")
    dependencies = [
        'PySide6', 'sqlalchemy', 'psycopg2', 'alembic', 
        'bcrypt', 'dotenv', 'reportlab', 'openpyxl'  # Cambiado python-dotenv a dotenv
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError as e:
            missing.append(dep)
            print(f"❌ {dep} - Error: {e}")
    
    return missing

def check_database():
    print("\n🔍 Verificando base de datos...")
    try:
        from src.models import init_db
        engine = init_db()
        
        # Verificar que podemos crear sesión
        from src.models import get_session, create_default_user
        session = get_session(engine)
        create_default_user(session)
        session.close()
        
        print("✅ Conexión a PostgreSQL exitosa y usuario creado")
        return True
    except Exception as e:
        print(f"❌ Error de base de datos: {e}")
        return False

def main():
    print("🦇 NECROLEDGER - VERIFICACIÓN DE INSTALACIÓN")
    print("=" * 50)
    
    # Verificar dependencias
    missing = check_dependencies()
    
    # Verificar base de datos
    db_ok = check_database()
    
    print("\n" + "=" * 50)
    if not missing and db_ok:
        print("🎉 ¡Todo está listo! Puedes ejecutar: python main.py")
    else:
        if missing:
            print(f"⚠️  Faltan dependencias: {', '.join(missing)}")
            print("   Ejecuta: pip install " + " ".join(missing))
        if not db_ok:
            print("⚠️  Problemas con la base de datos")
            print("   Verifica que Docker esté corriendo en puerto 5433")

if __name__ == "__main__":
    main()
