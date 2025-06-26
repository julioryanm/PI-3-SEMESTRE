from django.test import TestCase
from django.contrib.admin.sites import site
from Sistema.models import (
    Profile, EmpresaParceira, Obra, Colaborador,
    Restaurante, Hotel, RelatorioMensal
)
from Sistema import admin as sistema_admin


class AdminRegistrationTests(TestCase):
    def test_profile_registered_in_admin(self):
        self.assertIn(Profile, site._registry)

    def test_empresa_parceira_registered_in_admin(self):
        self.assertIn(EmpresaParceira, site._registry)
    
    def test_obra_registered_in_admin(self):
        self.assertIn(Obra, site._registry)

    def test_colaborador_registered_in_admin(self):
        self.assertIn(Colaborador, site._registry)

    def test_restaurante_registered_in_admin(self):
        self.assertIn(Restaurante, site._registry)

    def test_hotel_registered_in_admin(self):
        self.assertIn(Hotel, site._registry)

    def test_relatorio_mensal_registered_in_admin(self):
        self.assertIn(RelatorioMensal, site._registry)
