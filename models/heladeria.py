from db import db
from sqlalchemy.orm import relationship
from funciones import producto_mas_rentable
from flask import flash

class Heladeria(db.Model):
    __tablename__ = 'heladerias'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50))
    venta_dia = db.Column(db.Integer, default=0)
    productos = relationship('Producto', backref='heladeria')
    ingredientes = relationship('Ingrediente', backref='heladeria')

    def __init__(self, nombre:str) -> None:
        super().__init__()
        self.nombre = nombre

    def producto_mas_rentable(self):
        producto1 = {
                        "nombre" : self.productos[0].nombre,
                        "rentabilidad" : self.productos[0].calcular_rentabilidad()
                         }
        
        producto2 = {
                        "nombre" : self.productos[1].nombre,
                        "rentabilidad" : self.productos[1].calcular_rentabilidad()
                         }
        
        producto3 = {
                        "nombre" : self.productos[2].nombre,
                        "rentabilidad" : self.productos[2].calcular_rentabilidad()
                         }
        
        producto4 = {
                        "nombre" : self.productos[3].nombre,
                        "rentabilidad" : self.productos[3].calcular_rentabilidad()
                         }

        return producto_mas_rentable(producto1, producto2, producto3, producto4)
    
    def vender(self, producto_vender:str) -> bool:
        existe_producto = ""
        for producto in self.productos:
            if producto.nombre == producto_vender:
                existe_producto = producto
        
        if not existe_producto:
            raise ValueError('No existe el producto')
        
        for ingrediente in existe_producto.ingredientes:
            if ingrediente.tipo == 'base':
                if ingrediente.inventario < 0.2:
                    raise ValueError(f"Oh no! Nos hemos quedado sin {ingrediente.nombre}")
            elif ingrediente.tipo == 'complemento':
                if ingrediente.inventario < 1:
                    raise ValueError(f"Oh no! Nos hemos quedado sin {ingrediente.nombre}")
                
        for ingrediente in existe_producto.ingredientes:
            if ingrediente.tipo == 'base':
                ingrediente.inventario -= 0.2
            elif ingrediente.tipo == 'complemento':
                ingrediente.inventario -= 1

        self.venta_dia += existe_producto.precio_publico
        return True

