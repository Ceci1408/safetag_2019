from django.test import TestCase


class TipoPersona(TestCase):
    def setUp(self):
        PersonaFisica.objects.create(persona_fisica_nombre="Cecilia", persona_fisica_apellido="Barboza",
                                     persona_fisica_tipo_doc="DNI", persona_fisica_nro_documento=1524369,
                                     persona_fisica_fecha_nac=fnd)

    def test_check_mayor_edad(self):
        pf = PersonaFisica.objects.get(persona_fisica_nro_documento=1524369)
        self.assertTrue(pf.check_mayor_edad(), 'No es mayor de edad')

    def test_check_nro_documento_len(self):
        pf = PersonaFisica.objects.get(persona_fisica_nro_documento=1524369)
        self.assertTrue(pf.check_nro_documento_len(), 'El DNI no tiene una longitud válida')
