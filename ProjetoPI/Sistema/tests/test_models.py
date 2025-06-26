from django.test import TestCase
from django.contrib.auth.models import User
from Sistema.models import Obra, Colaborador, Hotel, Restaurante, Profile
from datetime import date

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='123456')

        self.obra = Obra.objects.create(
            nome="Obra Exemplo",
            empresa="Construtora XYZ",
            endereco="Rua das Pedras, 123",
            data_inicio=date(2023, 1, 1),
            data_prevista_termino=date(2023, 2, 1),
            data_real_termino=date(2023, 2, 10),
            status="CONCLUIDA",
            encarregado_responsavel=self.user
        )

        self.colaborador = Colaborador.objects.create(
            nome="João Silva",
            cpf="123.456.789-09",
            data_nascimento="1990-01-01",
            telefone="11999999999",
            endereco="Rua Exemplo, 100",
            obra=self.obra
        )

        self.hotel = Hotel.objects.create(
            nome="Hotel Sol",
            cnpj="12.345.678/0001-99",
            cidade="São Paulo",
            endereco="Rua do Hotel, 50",
            telefone="11888888888",
            responsavel="Maria Hotel"
        )

        self.restaurante = Restaurante.objects.create(
            nome="Restaurante Bom Sabor",
            cnpj="98.765.432/0001-99",
            endereco="Rua do Restaurante, 77",
            telefone="11777777777",
            responsavel="Carlos Restaurante"
        )

        self.profile = Profile.objects.create(
            user=self.user,
            tipo="encarregado"
        )

    def test_str_methods(self):
        self.assertEqual(str(self.obra), "Obra Exemplo (Construtora XYZ)")
        self.assertEqual(str(self.colaborador), "João Silva")
        self.assertEqual(str(self.profile), "teste (Encarregado de Obra)")
        self.assertEqual(str(self.hotel), "Hotel Sol")
        self.assertEqual(str(self.restaurante), "Restaurante Bom Sabor")

    def test_dias_atraso(self):
        self.assertEqual(self.obra.dias_atraso, 9)

    def test_profile_usuario(self):
        self.assertEqual(self.profile.user.username, 'teste')
        self.assertEqual(self.profile.get_tipo_display(), 'Encarregado de Obra')
