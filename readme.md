# Farmacia API

### Instalación:
1. Clona el repositorio
2. Crea un entorno virtual:
   ```bash o terminal de comandos
   python3 -m venv env
   .env/bin/activate 
   o
   .\env\Scripts\activate
   pip install fastapi[all] sqlalchemy psycopg2 alembic
   pip install pytest pytest-cov
   pip install fastapi[testclient]


### Inicialización 
````   uvicorn app.main:app --reload    ````

### Dependencias:
1. Python 3.9+
2. FastAPI
3. SQLAlchemy
4. PostgreSQL
5. alembic
6. pytest 
7. pytest-cov
8. testclient

# para la configuracion de la base de datos cambiar esta variable DATABASE_URL ="postgresql://postgres:1234@localhost/farmacia_db" en el archivo database.py

### Documentacion
```` http://127.0.0.1:8000/docs  o en el puerto donde se levante````
----------------------------------------------------------------

### utilice alembic para las migraciones de la base de datos

### para inizializar alembic 
1. alembic init alembic
2. esto creara un archivo env y tendran que agregar estas importaciones para la conexion a la base de datos

from app.database import Base, DATABASE_URL
from app.models import *

3. luego arriba de la variable target_metadata este codigo

config.set_main_option('sqlalchemy.url', DATABASE_URL)

4. cambiar el valor de la variable target_metadata por este

target_metadata = Base.metadata

### comando para generar una nueva migracion
1. alembic revision --autogenerate -m "Nombre de la migración"
### comando para aplicar la migracion a la base de datos
1. alembic upgrade head
### Esto ejecutará todas las migraciones pendientes y actualizará la base de datos según los cambios realizados en los modelos.

### el cors esta configurado para que solo deje acceder al localhost:4200 si desean cambiarlo deben modificar la propiedad origins por el que deseen

para el correcto funcionamiento del back se recomienda en el entorno virtual 
en el caso de las pruebas unitarias se recomienda cambiar el nombre del medicamento por cada prueba de lo contrario
causara un error debido a que insertara el nombre en la base de datos y si intententa ingresar el mismo de nuevo no podra
tambien revisar que existan medicamentos ya que es necesario para ejecutar las pruebas con las cantidades correctas para su correcto funcionamiento