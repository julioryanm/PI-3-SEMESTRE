from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from django.contrib.messages import get_messages
from django.utils.http import urlencode
from Sistema.models import Obra, Colaborador, Hotel, Restaurante, Profile
from datetime import datetime

class SistemaViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Grupos
        self.admin_group = Group.objects.create(name='Administradores')
        self.encarregado_group = Group.objects.create(name='Encarregados')

        # Usuários
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        self.admin_user.groups.add(self.admin_group)

        self.encarregado_user = User.objects.create_user(
            username='encarregado',
            password='pass123',
            is_active=True
        )
        self.encarregado_user.groups.add(self.encarregado_group)

        # Perfis
        Profile.objects.create(user=self.admin_user, tipo='admin')
        Profile.objects.create(user=self.encarregado_user, tipo='encarregado')

        # Criando dados
        self.obra = Obra.objects.create(
            nome='Obra Teste',
            empresa='Empresa X',
            endereco='Rua X, 123',
            data_inicio='2023-01-01',
            status='ANDAMENTO',
            encarregado_responsavel=self.encarregado_user
        )
        self.colaborador = Colaborador.objects.create(
            nome='Colaborador Teste',
            cpf='123.456.789-00',
            data_nascimento='1990-01-01',
            telefone='11999999999',
            endereco='Rua Y, 456',
            obra=self.obra
        )
        self.hotel = Hotel.objects.create(
            nome='Hotel Teste',
            cnpj='12.345.678/0001-99',
            cidade='São Paulo',
            endereco='Av. Hotel, 123',
            telefone='11888888888',
            responsavel='Responsável'
        )
        self.restaurante = Restaurante.objects.create(
            nome='Restaurante Teste',
            cnpj='98.765.432/0001-99',
            endereco='Av. Restaurante, 789',
            telefone='11777777777',
            responsavel='Responsável'
        )

    def test_login_redirects_to_home_if_logged(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('home'))

    def test_login_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post_valid(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'adminpass123'
        })
        self.assertRedirects(response, reverse('home'))

    def test_logout_post(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')

    def test_logout_get_redirects_home(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))

    def test_home_view_context_permissions(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertTrue(context['pode_ver_refeicoes'])
        self.assertTrue(context['pode_ver_obras'])
        self.assertTrue(context['pode_ver_dashboard'])
        self.assertEqual(context['grupo_nome'], 'ADMINISTRADORES')
        self.assertEqual(context['username_maiusculo'], 'ADMIN')

    def test_listar_colaboradores_requires_login(self):
        url = reverse('listar-colaboradores')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # redirect login

        self.client.login(username='encarregado', password='pass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Colaborador Teste')

    def test_editar_colaborador_get_and_post(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('editar-colaborador', args=[self.colaborador.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editar-colaborador.html')

        # POST com dados atualizados
        data = {
            'nome': 'Colaborador Atualizado',
            'cpf': '123.456.789-00',
            'data_nascimento': '1990-01-01',
            'telefone': '11999999999',
            'endereco': 'Rua Atualizada',
            'obra': self.obra.id,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('listar-colaboradores'))
        self.colaborador.refresh_from_db()
        self.assertEqual(self.colaborador.nome, 'Colaborador Atualizado')

    def test_excluir_colaborador_post(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('excluir-colaborador', args=[self.colaborador.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('listar-colaboradores'))
        self.assertFalse(Colaborador.objects.filter(id=self.colaborador.id).exists())

    def test_cadastro_colaborador_get_and_post(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('cadastro')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro.html')

        data = {
            'nome': 'Novo Colaborador',
            'cpf': '999.999.999-99',
            'data_nascimento': '1995-01-01',
            'telefone': '11988887777',
            'endereco': 'Rua Nova, 123',
            'obra': self.obra.id,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('listar-colaboradores'))
        self.assertTrue(Colaborador.objects.filter(nome='Novo Colaborador').exists())

    def test_cadastrar_restaurante_get_and_post(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('cadastrar-restaurante')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastrar-restaurante.html')

        data = {
            'nome': 'Novo Restaurante',
            'cnpj': '00.000.000/0001-00',
            'endereco': 'Rua Restaurante, 321',
            'telefone': '11912345678',
            'responsavel': 'Responsável X',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(Restaurante.objects.filter(nome='Novo Restaurante').exists())

    def test_editar_restaurante_get_and_post(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('editar-restaurante', args=[self.restaurante.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editar-restaurante.html')
        self.assertContains(response, self.restaurante.nome)

        data = {
            'nome': 'Restaurante Modificado',
            'cnpj': self.restaurante.cnpj,
            'endereco': 'Endereço Modificado',
            'telefone': self.restaurante.telefone,
            'responsavel': self.restaurante.responsavel,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('listar-restaurantes'))
        self.restaurante.refresh_from_db()
        self.assertEqual(self.restaurante.nome, 'Restaurante Modificado')

    def test_excluir_restaurante_post(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('excluir-restaurante', args=[self.restaurante.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('listar-restaurantes'))
        self.assertFalse(Restaurante.objects.filter(id=self.restaurante.id).exists())

    def test_cadastro_hotel_get_and_post(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('cadastrar-hotel')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastrar-hotel.html')

        data = {
            'nome': 'Hotel Novo',
            'cnpj': '00.111.222/0001-33',
            'cidade': 'Cidade Nova',
            'endereco': 'Rua Hotel, 456',
            'telefone': '11999998888',
            'responsavel': 'Responsável Y',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('listar-hoteis'))
        self.assertTrue(Hotel.objects.filter(nome='Hotel Novo').exists())

    def test_listar_hoteis_view(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('listar-hoteis')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.hotel.nome)

    def test_editar_hotel_get_and_post(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('editar-hotel', args=[self.hotel.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editar-hotel.html')
        self.assertContains(response, self.hotel.nome)

        data = {
            'nome': 'Hotel Editado',
            'cnpj': self.hotel.cnpj,
            'cidade': self.hotel.cidade,
            'endereco': self.hotel.endereco,
            'telefone': self.hotel.telefone,
            'responsavel': self.hotel.responsavel,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('listar-hoteis'))
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.nome, 'Hotel Editado')

    def test_redirecionar_edicao_hotel_post(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('redirecionar-edicao-hotel')
        response = self.client.post(url, {'hotel_id': self.hotel.id})
        self.assertRedirects(response, reverse('editar-hotel', args=[self.hotel.id]))

    def test_redirecionar_edicao_hotel_post_no_id(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('redirecionar-edicao-hotel')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)

    def test_deletar_generico_post_valid(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('deletar-generico')
        # Criar um objeto para deletar
        colab = Colaborador.objects.create(
            nome='ToDelete',
            cpf='000.000.000-00',
            data_nascimento='1990-01-01',
            telefone='11111111111',
            endereco='Rua X',
            obra=self.obra
        )
        data = {
            'model': 'Colaborador',
            'ids': [colab.id],
            'redirect_to': 'listar-colaboradores',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('listar-colaboradores'))
        self.assertFalse(Colaborador.objects.filter(id=colab.id).exists())

    def test_deletar_generico_post_invalid_model(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('deletar-generico')
        data = {
            'model': 'NaoExiste',
            'ids': ['1'],
            'redirect_to': 'home',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_cadastrar_usuario_post_valid(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('cadastrar_usuario')
        data = {
            'username': 'novo_user',
            'email': 'novo@teste.com',
            'password': '123456',
            'confirm_password': '123456',
            'tipo': 'admin',
            'admin_password': 'qualquer',
        }
        response = self.client.post(url, data, follow=True)
        self.assertContains(response, 'Usuário e perfil criados com sucesso!')
        self.assertTrue(User.objects.filter(username='novo_user').exists())

    def test_cadastrar_usuario_post_password_mismatch(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('cadastrar_usuario')
        data = {
            'username': 'user2',
            'email': 'user2@teste.com',
            'password': '123',
            'confirm_password': '321',
            'tipo': 'encarregado',
        }
        response = self.client.post(url, data, follow=True)
        self.assertContains(response, 'As senhas não coincidem!')

    def test_listar_obras_encarregado_versus_admin(self):
        # Como encarregado, deve ver só suas obras
        self.client.login(username='encarregado', password='pass123')
        response = self.client.get(reverse('listar-obras'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Obra Teste')
        # Cria uma obra para outro encarregado
        outro_user = User.objects.create_user(username='outro', password='pass')
        Profile.objects.create(user=outro_user, tipo='encarregado')
        Obra.objects.create(
            nome='Outra Obra',
            empresa='Empresa 2',
            endereco='Endereço 2',
            data_inicio='2024-01-01',
            status='ANDAMENTO',
            encarregado_responsavel=outro_user
        )
        # Ainda não deve ver 'Outra Obra'
        response = self.client.get(reverse('listar-obras'))
        self.assertNotContains(response, 'Outra Obra')

        # Como admin, deve ver todas
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('listar-obras'))
        self.assertContains(response, 'Outra Obra')

    def test_editar_obra_get_and_post(self):
        # Se data_inicio for string, converta para datetime antes
        if isinstance(self.obra.data_inicio, str):
            data_inicio_obj = datetime.strptime(self.obra.data_inicio, '%Y-%m-%d')
        else:
            data_inicio_obj = self.obra.data_inicio
        
        response = self.client.get(reverse('editar-obra', kwargs={'id': self.obra.id}), {
            'data_inicio': data_inicio_obj.strftime('%Y-%m-%d'),
            # demais dados para o post, se for o caso
        })

    def test_detalhes_obra_view(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('detalhes-obra', args=[self.obra.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.obra.nome)

    def test_relatorio_view_valid_and_invalid(self):
        self.client.login(username='admin', password='adminpass123')

        # Testa com datas inválidas
        query = urlencode({
            'data_inicio': '2023-01-01',
            'data_fim': '2023-03-15',  # > 31 dias
            'obra_id': self.obra.id,
            'colaborador_id': self.colaborador.id
        })
        response = self.client.get(reverse('relatorio') + '?' + query)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("intervalo de datas não pode ultrapassar" in m.message for m in messages))

        # Testa sem filtros (default)
        response = self.client.get(reverse('relatorio'))
        self.assertEqual(response.status_code, 200)

    # Para as views que acessam MongoDB (listar_pedidos, cadastrar_pedido, listar_registros, etc)
    # você pode criar mocks para o pedido_model se quiser testar esses fluxos.
