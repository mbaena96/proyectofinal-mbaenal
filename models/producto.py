from db import db
from sqlalchemy.orm import relationship
from models.producto_ingrediente import producto_ingrediente
from funciones import obtener_costos, obtener_calorias, obtener_rentabilidad

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable = False)
    precio_publico = db.Column(db.Integer, nullable = False)
    tipo_vaso = db.Column(db.String(50))
    volumen = db.Column(db.Float)
    tipo = db.Column(db.String(10), nullable = False)
    id_heladeria = db.Column(db.Integer, db.ForeignKey('heladerias.id'))
    # ingredientes = relationship('Ingrediente', backref='producto') uno a muchos
    ingredientes = relationship('Ingrediente',secondary=producto_ingrediente, backref='producto') #muchos a muchos

    def __init__(self, nombre:str, precio_publico:int, tipo_vaso:str, volumen:float, tipo:str) -> None:
        super().__init__()
        self.nombre = nombre
        self.precio_publico = precio_publico
        self.tipo_vaso = tipo_vaso
        self.volumen = volumen
        self.tipo = tipo

    def show(self) -> str:
        return {"id": self.id,
                "nombre": self.nombre,
                "precio_publico": self.precio_publico,
                "tipo_vaso": self.tipo_vaso,
                "volumen": self.volumen,
                "tipo": self.tipo,
                "id_heladeria": self.id_heladeria,
                }

    def calcular_costo(self) -> float:
        ingrediente1 = {
                        "nombre" : self.ingredientes[0].nombre,
                        "precio" : self.ingredientes[0].precio
                         }
        
        ingrediente2 = {
                        "nombre" : self.ingredientes[1].nombre,
                        "precio" : self.ingredientes[1].precio
                         }
        
        ingrediente3 = {
                        "nombre" : self.ingredientes[2].nombre,
                        "precio" : self.ingredientes[2].precio
                         }
        if self.tipo == 'copa':
            return obtener_costos(ingrediente1, ingrediente2, ingrediente3)
        else:
            return obtener_costos(ingrediente1, ingrediente2, ingrediente3) + 500
    
    def calcular_calorias(self) -> float:
        calorias = [self.ingredientes[0].calorias, self.ingredientes[1].calorias, self.ingredientes[2].calorias]
        if self.tipo == 'copa':
            return obtener_calorias(calorias)
        else:
            return (obtener_calorias(calorias) / 0.95) + 200
    
    def calcular_rentabilidad(self) -> float:
        ingrediente1 = {
                        "nombre" : self.ingredientes[0].nombre,
                        "precio" : self.ingredientes[0].precio
                         }
        
        ingrediente2 = {
                        "nombre" : self.ingredientes[1].nombre,
                        "precio" : self.ingredientes[1].precio
                         }
        
        ingrediente3 = {
                        "nombre" : self.ingredientes[2].nombre,
                        "precio" : self.ingredientes[2].precio
                         }
        
        return obtener_rentabilidad(self.precio_publico, ingrediente1, ingrediente2, ingrediente3)

    # def nombre(self) -> str:
    #     """ Devuelve el valor del atributo privado 'nombre' """
    #     return self.nombre
    
    # @nombre.setter
    # def nombre(self, value:str) -> None:
    #     """ 
    #     Establece un nuevo valor para el atributo privado 'nombre'
    
    #     Valida que el valor enviado corresponda al tipo de dato del atributo
    #     """ 
    #     if isinstance(value, str):
    #         self.nombre = value
    #     else:
    #         raise ValueError('Expected str')
        
    # @property
    # def precio_publico(self) -> int:
    #     """ Devuelve el valor del atributo privado 'precio_publico' """
    #     return self.precio_publico
    
    # @precio_publico.setter
    # def precio_publico(self, value:int) -> None:
    #     """ 
    #     Establece un nuevo valor para el atributo privado 'precio_publico'
    
    #     Valida que el valor enviado corresponda al tipo de dato del atributo
    #     """ 
    #     if isinstance(value, int):
    #         self.precio_publico = value
    #     else:
    #         raise ValueError('Expected int')
        
    # @property
    # def tipo_vaso(self) -> str:
    #     """ Devuelve el valor del atributo privado 'tipo_vaso' """
    #     return self.tipo_vaso
    
    # @tipo_vaso.setter
    # def tipo_vaso(self, value:str) -> None:
        
    #     self._tipo_vaso = value
        
    # @property
    # def volumen(self) -> float:
    #     """ Devuelve el valor del atributo privado 'volumen' """
    #     return self.volumen
    
    # @volumen.setter
    # def volumen(self, value:float) -> None:
    #     self.volumen = value
