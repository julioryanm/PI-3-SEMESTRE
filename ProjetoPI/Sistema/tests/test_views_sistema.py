from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from Sistema.models import Obra, Colaborador, Hotel, Restaurante, Profile

class SistemaViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin_group = Group.objects.create(name='Admin')
        self.encarregado_group = Group.objects.create(name='Encarregado')

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.user.groups.add(self.encarregado_group)

        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            email='admin@example.com',
            is_staff=True
        )
        self.admin_user.groups.add(self.admin_group)

        Profile.objects.create(user=self.user, tipo='encarregado', telefone='11999999999')
        Profile.objects.create(user=self.admin_user, tipo='admin', telefone='11888888888')

        self.obra = Obra.objects.create(
            nome='Obra Teste',
            empresa='Empresa Teste',
            endereco='Endereço Teste, 123',
            data_inicio='2023-01-01',
            status='ANDAMENTO',
            encarregado_responsavel=self.user
        )

        self.colaborador = Colaborador.objects.create(
            nome='Colaborador Teste',
            cpf='123.456.789-09',
            data_nascimento='1990-01-01',
            telefone='11999999999',
            endereco='Endereço Teste',
            obra=self.obra
        )

        self.hotel = Hotel.objects.create(
            nome='Hotel Teste',
            cnpj='12.345.678/0001-99',
            cidade='São Paulo',
            endereco='Endereço Hotel Teste',
            telefone='11888888888',
            responsavel='Responsável Teste'
        )

        self.restaurante = Restaurante.objects.create(
            nome='Restaurante Teste',
            cnpj='98.765.432/0001-99',
            endereco='Endereço Restaurante Teste',
            telefone='11777777777',
            responsavel='Responsável Teste'
        )

    def test_home_view_requires_login(self):
        response = self.client.get(reverse('home'))
        self.assertIn(response.status_code, [302, 403])

    def test_home_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_success(self):
        login_successful = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_successful)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_listar_obras_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('listar-obras'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Obra Teste')

    def test_listar_colaboradores_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('listar-colaboradores'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Colaborador Teste')

    def test_listar_hoteis_view(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('listar-hoteis'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hotel Teste')

    def test_listar_restaurantes_view(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('listar-restaurantes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Restaurante Teste')

    def test_editar_hotel_view(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('editar-hotel', args=[self.hotel.id]))
        self.assertEqual(response.status_code, 200)

    def test_editar_hotel_post(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('editar-hotel', args=[self.hotel.id]), {
            'nome': 'Hotel Modificado',
            'cnpj': self.hotel.cnpj,
            'cidade': self.hotel.cidade,
            'endereco': self.hotel.endereco,
            'telefone': self.hotel.telefone,
            'responsavel': self.hotel.responsavel
        })
        self.assertEqual(response.status_code, 302)
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.nome, 'Hotel Modificado')

    def test_cadastrar_hotel_view(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('cadastrar-hotel'))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_colaborador_view(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SEJA BEM-VINDO')

    def test_excluir_restaurante_post(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('excluir-restaurante', args=[self.restaurante.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Restaurante.objects.filter(id=self.restaurante.id).exists())

    def test_editar_restaurante_view_get(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('editar-restaurante', args=[self.restaurante.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Restaurante Teste')

    def test_logout_get_redirect(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_logout_post(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')

    def test_cadastro_obra_post(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('cadastrar-obra'), {
            'nome': 'Nova Obra',
            'empresa': 'Empresa Nova',
            'status': 'ANDAMENTO',
            'endereco': 'Rua Nova, 123',
            'data_inicio': '2023-05-01',
            'encarregado_responsavel': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Obra.objects.filter(nome='Nova Obra').exists())
