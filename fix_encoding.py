#!/usr/bin/env python3
import os
import glob

def check_file_encoding(filepath):
    """Verificar y corregir codificación de archivos"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ {filepath} - UTF-8 válido")
        return True
    except UnicodeDecodeError as e:
        print(f"❌ {filepath} - Problema de codificación: {e}")
        return False

def convert_to_utf8(filepath):
    """Convertir archivo a UTF-8"""
    try:
        # Intentar diferentes codificaciones
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
                
                # Guardar como UTF-8
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"🔄 {filepath} - Convertido de {encoding} a UTF-8")
                return True
            except UnicodeDecodeError:
                continue
        return False
    except Exception as e:
        print(f"💥 Error procesando {filepath}: {e}")
        return False

def main():
    print("🔍 Verificando codificación de archivos...")
    
    # Archivos a verificar
    files_to_check = [
        'src/views/dashboard_view.py',
        'src/views/main_window.py', 
        'src/views/login_window.py',
        'src/models/__init__.py',
        'src/services/auth_service.py',
        'src/assets/styles/style.qss',
        'main.py'
    ]
    
    problems_found = False
    for filepath in files_to_check:
        if os.path.exists(filepath):
            if not check_file_encoding(filepath):
                problems_found = True
                print(f"Intentando corregir {filepath}...")
                if convert_to_utf8(filepath):
                    print(f"✅ {filepath} - Corregido exitosamente")
                else:
                    print(f"❌ {filepath} - No se pudo corregir")
        else:
            print(f"⚠️  {filepath} - No encontrado")
    
    if not problems_found:
        print("🎉 Todos los archivos tienen codificación UTF-8 correcta")
    else:
        print("🔧 Algunos archivos fueron corregidos")

if __name__ == "__main__":
    main()
