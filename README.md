# Fequis

*Fequis - Porque Feisbuc y Xwitter son feos.*

Este es el programa que hicimos en el módulo de Python/Flask en [LAchirana Plat](https://www.facebook.com/LAChiranaPlat/), casi tal y como quedó al culminar.

## Instalación

Salvo un comando, estas instrucciones también debería funcionar en Windows.

```bash
# Clonas esta repo en tu equipo
git clone https://github.com/drmad/fequis.git

# Entras al directorio del proyecto
cd fequis

# Creas un entorno virtual
python -m venv .venv

# Lo activas
source .venv/bin/activate

# Instalas los paquetes que requiere el proyecto
pip install -r requirements.txt

# Necesitas una configuración inicial
mkdir instance

# Esto solo funciona en Linux. Lee las líneas hasta el 'EOF' y las guarda 
# en el fichero instance/configuración.py . En la línea de `SECRET_KEY` 
# ejecutamos un script de Python para que genere un código al azar
cat <<EOF > instance/configuración.py
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///basedatos.sqlite'
SECRET_KEY = '`python -c 'import secrets; print (secrets.token_hex())'`'
EOF


# Abres un shell de flask para inicializar la bae de datos
flask shell

# Dentro del shell ejecutas: 
#
# db.create_all()
# 
# Para que cree la base de datos. Luego sales del shell con CTRL+d

# Y corres el servidor de pruebas de Flask
flask run
```

