import unittest
from models.ingrediente import Ingrediente
from app import app
from db import db

class TestIngrediente(unittest.TestCase):

    def setUp(self) -> None:
        self.app_context = app.app_context()
        self.app_context.push()
        self.ingrediente_sano = Ingrediente.query.get(6)
        self.ingrediente_no_sano = Ingrediente.query.get(4)
        self.complemento = Ingrediente.query.filter_by(tipo='complemento').filter(Ingrediente.inventario>0).first()
        self.base = Ingrediente.query.filter_by(tipo='base').first()

    def tearDown(self):
        self.app_context.pop()
        db.session.rollback

    def test_es_sano_should_return_true(self):
        self.assertTrue(self.ingrediente_sano)

    def test_es_sano_should_return_false(self):
        self.assertTrue(self.ingrediente_no_sano)

    def test_abastecer_complemento(self):
        inventario_actual = self.complemento.inventario
        self.complemento.abastecer()
        inventario_abastecido = self.complemento.inventario
        self.assertEqual(inventario_abastecido, inventario_actual + 10)

    def test_abastecer_base(self):
        inventario_actual = self.base.inventario
        self.base.abastecer()
        inventario_abastecido = self.base.inventario
        self.assertEqual(inventario_abastecido, inventario_actual + 5)

    def test_renovar_inventario(self):
        self.complemento.renovar_inventario()
        self.assertEqual(self.complemento.inventario, 0)


