from django.db import models
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def criar_token_para_novo_usuario(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance) 


@receiver(post_migrate)
def permissoes_grupo(sender, **kwargs):
  permissoes_admin = Permission.objects.filter(
        codename__in=["add_user", "change_user", "delete_user"]
    )
   


@receiver(post_save, sender=User)
def criar_profile_automanticamente(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class EmpresaParceira(models.Model):
    """Modelo para empresas parceiras com validações aprimoradas"""
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome da Empresa",
        help_text="Nome completo da empresa parceira"
    )
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ",
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message="CNPJ deve estar no formato: 99.999.999/9999-99"
            )
        ]
    )
    
    telefone = models.CharField(
        max_length=15,
        verbose_name="Telefone",
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Telefone deve estar no formato: '+999999999'"
            )
        ]
    )
    email = models.EmailField(
        verbose_name="E-mail",
        blank=True
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativa"
    )

    class Meta:
        verbose_name = "Empresa Parceira"
        verbose_name_plural = "Empresas Parceiras"
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['cnpj']),
        ]

    def __str__(self):
        return self.nome

class Obra(models.Model):
    """Modelo para obras de construção com status e controle melhorado"""
    STATUS_CHOICES = [
        ('PLANEJAMENTO', 'Planejamento'),
        ('ANDAMENTO', 'Em Andamento'),
        ('PARADA', 'Parada'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]

    nome = models.CharField(
        max_length=100,
        verbose_name="Nome da Obra"
    )
    empresa = models.CharField(
        max_length=100,
        verbose_name="Empresa Responsável"
    )
    
    endereco = models.TextField(
        verbose_name="Endereço Completo"
    )
    data_inicio = models.DateField(
        verbose_name="Data de Início"
    )
    data_prevista_termino = models.DateField(
        verbose_name="Previsão de Término",
        blank=True,
        null=True
    )
    data_real_termino = models.DateField(
        verbose_name="Data Real de Término",
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='PLANEJAMENTO',
        verbose_name="Status da Obra"
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        blank=True
    )

    class Meta:
        verbose_name = "Obra"
        verbose_name_plural = "Obras"
        ordering = ['-data_inicio']
        permissions = [
            ('view_obra_report', 'Pode visualizar relatórios de obra'),
        ]

    def __str__(self):
        return f"{self.nome} ({self.empresa})"

    @property
    def dias_atraso(self):
        if self.status == 'CONCLUIDA' and self.data_real_termino and self.data_prevista_termino:
            return (self.data_real_termino - self.data_prevista_termino).days
        return 0

class Colaborador(models.Model):
    """Modelo completo para colaboradores da construção"""

    # Dados Pessoais
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome Completo"
    )
        
    cpf = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="CPF",
        validators=[RegexValidator(
            regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
            message="CPF deve estar no formato: 999.999.999-99"
        )]
    )


    
    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento"
    )
    
    
    telefone = models.CharField(
        max_length=15,
        verbose_name="Telefone"
    )
    
    
    
    # Endereço
    
    endereco = models.CharField(
        max_length=50,
        verbose_name="Endereço"
    )
    

    # Dados Profissionais
    
    obra = models.ForeignKey(
        Obra,
        on_delete=models.CASCADE,
        verbose_name="Obra Vinculada",
        related_name='colaboradores'
    )

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['cpf']),
        ]
        permissions = [
            ('view_colaborador_report', 'Pode visualizar relatórios de colaboradores'),
        ]

    def __str__(self):
        return f"{self.nome}"


class Restaurante(models.Model):
    """Modelo para restaurantes parceiros com avaliação"""
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Restaurante"
    )
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ"
    )
    endereco = models.TextField(
        verbose_name="Endereço Completo"
    )
    telefone = models.CharField(
        max_length=15,
        verbose_name="Telefone"
    )
    responsavel = models.CharField(
        max_length=100,
        verbose_name="Responsável"
    )
    

 
class Hotel(models.Model):
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Hotel"
    )
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ"
    )
    cidade = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="Cidade"
    )
    endereco = models.TextField(
        verbose_name="Endereço Completo"
    )
    telefone = models.CharField(
        max_length=15,
        verbose_name="Telefone"
    )
    responsavel = models.CharField(
        max_length=100,
        verbose_name="Responsável"
    )

class RelatorioMensal(models.Model):
    """Modelo para relatórios mensais de refeições com detalhamento"""
    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.CASCADE,
        verbose_name="Colaborador",
        related_name='relatorios'
    )
    mes_referencia = models.CharField(
        max_length=7,
        verbose_name="Mês de Referência",
        help_text="Formato: AAAA-MM"
    )
    total_refeicoes = models.IntegerField(
        verbose_name="Total de Refeições"
    )
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Total"
    )
    cafe_manha = models.IntegerField(
        verbose_name="Cafés da Manhã",
        default=0
    )
    almocos = models.IntegerField(
        verbose_name="Almoços",
        default=0
    )
    jantares = models.IntegerField(
        verbose_name="Jantares",
        default=0
    )
    lanches = models.IntegerField(
        verbose_name="Lanches",
        default=0
    )
    data_geracao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Geração"
    )
    observacoes = models.TextField(
        verbose_name="Observações",
        blank=True
    )

    class Meta:
        verbose_name = "Relatório Mensal"
        verbose_name_plural = "Relatórios Mensais"
        ordering = ['-mes_referencia']
        unique_together = ['colaborador', 'mes_referencia']

    def __str__(self):
        return f"Relatório de {self.mes_referencia} - {self.colaborador}"

    def save(self, *args, **kwargs):
        self.total_refeicoes = self.cafe_manha + self.almocos + self.jantares + self.lanches
        super().save(*args, **kwargs)
        
class Profile(models.Model):
    TIPOS_USUARIO = [
        ('admin', 'Administrador'),
        ('encarregado', 'Encarregado de Obra'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    obra = models.ForeignKey(Obra, on_delete=models.SET_NULL, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ({self.get_tipo_display()})'
 
