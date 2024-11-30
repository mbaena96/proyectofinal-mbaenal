from db import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    es_admin = db.Column(db.Boolean, nullable=False, default=False)
    es_empleado = db.Column(db.Boolean, nullable=False, default=False)

    # def __init__(self, username:str, password:str, es_admin) -> None:
    #     self.username = username
    #     self.password = password
    #     self.es_admin = es_admin

    def validar_usuario(self):
        return db.session.query(Usuario).filter_by(username=self.username).first()
    
    def validar_pass(self):
        return db.session.query(Usuario).filter_by(username=self.username, password=self.password).first()