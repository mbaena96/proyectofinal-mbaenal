from db import db
from funciones import esto_es_sano

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable = False)
    precio = db.Column(db.Integer, nullable = False)
    calorias = db.Column(db.Integer, nullable = False)
    inventario = db.Column(db.Float, nullable = False)
    es_vegetariano = db.Column(db.Boolean, nullable = False)
    sabor = db.Column(db.String(50))
    tipo = db.Column(db.String(20), nullable = False)
    id_heladeria = db.Column(db.Integer, db.ForeignKey('heladerias.id'))
    # id_producto = db.Column(db.Integer, db.ForeignKey('productos.id')) #uno a muchos

    def show(self) -> str:
        return {"id": self.id,
                "nombre": self.nombre,
                "precio": self.precio,
                "calorias": self.calorias,
                "inventario": self.inventario,
                "es_vegetariano": self.es_vegetariano,
                "sabor": self.sabor,
                "tipo": self.tipo,
                "id_heladeria": self.id_heladeria
                }

    def es_sano(self) -> bool:
        return esto_es_sano(self.calorias, self.es_vegetariano)
    
    def abastecer(self):
        if self.tipo == 'base':
            self.inventario += 5
        else:
            self.inventario += 10

    def renovar_inventario(self):
        if self.tipo == 'complemento':
            self.inventario = 0.0

