from flask_sqlalchemy import SQLAlchemy

# flask-sqlalchemy 를 사용하면 기존 sqlachemy보다 간단하게 db를 설정할 수 있음
# >> 원래라면 engine도 설정하고 declareDB 상속받고 등등을 진행해야 함
db = SQLAlchemy()
