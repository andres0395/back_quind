# Farmacia API

### Instalación:
1. Clona el repositorio
2. Crea un entorno virtual:
   ```bash o terminal de comandos
   python3 -m venv env
   .env/bin/activate 
   o
   .\env\Scripts\activate
   pip install fastapi[all] sqlalchemy psycopg2

### Inicialización 
````   uvicorn app.main:app --reload    ````

### Dependencias:
1. Python 3.9+
2. FastAPI
3. SQLAlchemy
4. PostgreSQL

# para la configuracion de la base de datos cambiar esta variable DATABASE_URL ="postgresql://postgres:1234@localhost/farmacia_db" en el archivo database.py

### Documentacion
```` http://127.0.0.1:8000/docs  o en el puerto donde se levante````
----------------------------------------------------------------
