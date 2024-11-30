import unittest
from models.heladeria import Heladeria
from models.producto import Producto
from app import app
from db import db

class TestHeladeria(unittest.TestCase):

    def setUp(self) -> None:
        self.app_context = app.app_context()
        self.app_context.push()
        self.heladeria = Heladeria.query.get(1)
        self.producto = Producto.query.get(1)

    def tearDown(self):
        self.app_context.pop()
        db.session.rollback

    def test_producto_mas_rentable(self):
        # rentable = self.heladeria.producto_mas_rentable()
        rentable = ''
        rentabilidad = 0
        for producto in self.heladeria.productos:
            if producto.calcular_rentabilidad() > rentabilidad:
                rentabilidad = producto.calcular_rentabilidad()
                rentable = producto.nombre
        self.assertEqual(self.heladeria.producto_mas_rentable(), rentable)

    def test_vender_exitoso(self):
        for ingrediente in self.producto.ingredientes:
            ingrediente.inventario = 100000

        self.assertTrue(self.heladeria.vender(self.producto.nombre))

    def test_vender_producto_no_existe(self):
        self.assertRaises(ValueError,  self.heladeria.vender, 'nombre que no existe')

    def test_vender_ingrediente_insuficiente(self):
        ingrediente = self.producto.ingredientes[0]
        ingrediente.inventario = 0
        self.assertRaises(ValueError, self.heladeria.vender, self.producto.nombre)