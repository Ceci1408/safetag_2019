from django.test import TestCase
from datetime import datetime
from .models import Contacto, Cliente, Proveedor, ServicioTecnico, Domicilio, Trabajo

cliente = Cliente(1, 'Cecilia', 'Barboza', datetime.now(), 'test@test.com')
proveedor = Proveedor(1, 'Prov', 'comments', 'notes', datetime.now(), 1)
servicio_tecnico = ServicioTecnico(1, 'serv tec', datetime.now(), 1)


class ContactoTest(TestCase):
    def test_unique_contact(self):
        contacto = Contacto(cliente=cliente, proveedor=proveedor, servicio_tecnico=servicio_tecnico)
        self.assertIs(contacto.unico_tipo_cuenta(), False)


class DomicilioTest(TestCase):
    def test_unique_contact(self):
        domicilio = Domicilio(cliente=cliente, proveedor=proveedor, servicio_tecnico=servicio_tecnico)
        self.assertIs(domicilio.unico_tipo_cuenta(), False)


class TrabajoTest(TestCase):
    def test_autoadhesivo_flg_doble_cara(self):
        trabajo = Trabajo(autoadhesivo_flg=1, doble_cara_flg=1)
        self.assertIs(trabajo.adhesivo_sin_flg_doble_cara(), False)