from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from Sistema.models import PermissaoVirtual



class Command(BaseCommand):
    help = 'Cria permissão personalizada e atribui aos grupos'

    def handle(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(PermissaoVirtual)

        # Cria ou recupera a permissão
        perm, created = Permission.objects.get_or_create(
            codename='view_refeicao',
            content_type=content_type,
            defaults={'name': 'Pode visualizar refeições'}
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Permissão 'view_refeicao' criada."))
        else:
            self.stdout.write("Permissão 'view_refeicao' já existe.")

        # Grupos que receberão a permissão
        grupos = ['Encarregados', 'Administradores']

        for nome in grupos:
            grupo, _ = Group.objects.get_or_create(name=nome)
            grupo.permissions.add(perm)
            self.stdout.write(self.style.SUCCESS(f"Permissão atribuída ao grupo: {nome}"))
