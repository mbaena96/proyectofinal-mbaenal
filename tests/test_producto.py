import unittest
from models.producto import Producto
from app import app
from db import db

class TestProducto(unittest.TestCase):

    def setUp(self) -> None:
        self.app_context = app.app_context()
        self.app_context.push()
        self.copa = Producto.query.filter_by(tipo='copa').order_by(Producto.id).first()
        self.malteada = Producto.query.filter_by(tipo='malteada').order_by(Producto.id).first()

    def tearDown(self):
        self.app_context.pop()
        db.session.rollback

    def test_calcular_calorias_copa(self):
        #57 * 0.95 = 54.15
        self.assertEqual(self.copa.calcular_calorias(), 54.15)

    def test_calcular_calorias_malteada(self):
        #75 + 200 = 275
        self.assertEqual(self.malteada.calcular_calorias(), 275)

    def test_calcular_costo_produccion_copa(self):
        #2600
        self.assertEqual(self.copa.calcular_costo(), 2600)

    def test_calcular_costo_produccion_malteada(self):
        #2700 + 500
        self.assertEqual(self.malteada.calcular_costo(), 3200)

    def test_calcular_rentabilidad_copa(self):
        #4900 - 2600 = 2300
        rentabilidad = self.copa.precio_publico - self.copa.calcular_costo()
        self.assertEqual(rentabilidad, 2300)

    def test_calcular_rentabilidad_malteada(self):
        #11000 - 3200 = 7800
        rentabilidad = self.malteada.precio_publico - self.malteada.calcular_costo()
        self.assertEqual(rentabilidad, 7800)

    # def test_producto_mas_rentable(self):
    #     pass

    # def test_vender(self):
    #     pass