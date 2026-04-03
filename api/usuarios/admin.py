from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioPersonalizadoAdmin(UserAdmin):
    # Ordenamos cómo se ve en el listado
    list_display = ('email', 'nombre_completo', 'rut', 'cargo', 'es_admin', 'is_staff')
    # Quitamos el username de los filtros y formularios del admin base
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombre_completo', 'rut', 'cargo')}),
        ('Permisos', {'fields': ('es_admin', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre_completo', 'rut', 'password', 'es_admin'),
        }),
    )