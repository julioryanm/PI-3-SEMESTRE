from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Profile, EmpresaParceira, Obra, Colaborador, 
    Restaurante, RelatorioMensal, Hotel
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo')
    list_filter = ('tipo', )
    search_fields = ('user__username', 'user__email')


class EmpresaParceiraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'telefone', 'email', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'cnpj')
    list_per_page = 20
    ordering = ('nome',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'cnpj', 'ativo')
        }),
        ('Contato', {
            'fields': ('telefone', 'email')
        }),
    )


class ObraAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'empresa', 'status', 'data_inicio', 
        'data_prevista_termino', 'dias_atraso_display'
    )
    list_filter = ('status', 'empresa', 'data_inicio')
    search_fields = ('nome', 'empresa__nome')
    date_hierarchy = 'data_inicio'
    #raw_id_fields = ('empresa',)
    list_per_page = 30
    ordering = ('-data_inicio',)

    fieldsets = (
        ('Identificação', {
            'fields': ('nome', 'empresa', 'status', 'encarregado_responsavel', 'restaurante_vinculado', 'hotel_vinculado')
        }),
        ('Datas', {
            'fields': ('data_inicio', 'data_prevista_termino', 'data_real_termino')
        }),
        ('Localização', {
            'fields': ('endereco',)
        }),
        ('Detalhes', {
            'fields': ('descricao',)
        }),
    )

    def dias_atraso_display(self, obj):
        return obj.dias_atraso or '-'
    dias_atraso_display.short_description = 'Dias de Atraso'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'encarregado_responsavel':
            from django.contrib.auth.models import User
            kwargs["queryset"] = User.objects.filter(profile__tipo='encarregado')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'obra')
    list_filter = ('obra',)
    search_fields = ('nome', 'cpf')
    raw_id_fields = ('obra',)
    list_per_page = 50
    ordering = ('nome',)
    #readonly_fields = ('foto_display',)

    fieldsets = (
        ('Dados Pessoais', {
            'fields': (
                'nome', 'cpf',
                'data_nascimento'
            )
        }),
        ('Contato', {
            'fields': ['telefone']
        }),
        ('Endereço', {
            'fields': ('endereco',)
        }),
        ('Dados Profissionais', {
            'fields': (
                'obra',
            )
        }),
    )

    def foto_display(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="50" height="50" />', obj.foto.url)
        return "-"
    foto_display.short_description = 'Foto Atual'


class RestauranteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'responsavel', 'telefone',)
    search_fields = ('nome', 'cnpj', 'responsavel',)
    list_per_page = 20

    fieldsets = (
        ('Identificação', {
            'fields': ('nome', 'cnpj',)
        }),
        ('Informações', {
            'fields': ('responsavel',)
        }),
        ('Contato', {
            'fields': ('telefone', 'endereco',)
        }),
    )


class HotelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'responsavel', 'telefone',)
    search_fields = ('nome', 'cnpj', 'responsavel',)
    list_per_page = 20

    fieldsets = (
        ('Identificação', {
            'fields': ('nome', 'cnpj',)
        }),
        ('Informações', {
            'fields': ('responsavel',)
        }),
        ('Contato', {
            'fields': ('telefone', 'cidade', 'endereco',)
        }),
    )


class RelatorioMensalAdmin(admin.ModelAdmin):
    list_display = (
        'colaborador', 'mes_referencia', 'total_refeicoes', 
        'valor_total', 'data_geracao'
    )
    list_filter = ('mes_referencia',)
    search_fields = ('colaborador__nome',)
    date_hierarchy = 'data_geracao'
    raw_id_fields = ('colaborador',)
    readonly_fields = ('data_geracao',)

    fieldsets = (
        ('Identificação', {
            'fields': ('colaborador', 'mes_referencia')
        }),
        ('Quantitativos', {
            'fields': (
                'cafe_manha', 'almocos', 'jantares', 'lanches',
                'total_refeicoes', 'valor_total'
            )
        }),
        ('Detalhes', {
            'fields': ('data_geracao', 'observacoes')
        }),
    )


# Registro dos modelos no admin
admin.site.register(EmpresaParceira, EmpresaParceiraAdmin)
admin.site.register(Obra, ObraAdmin)
admin.site.register(Colaborador, ColaboradorAdmin)
admin.site.register(Restaurante, RestauranteAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(RelatorioMensal, RelatorioMensalAdmin)
