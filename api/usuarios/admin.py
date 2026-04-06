from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Usuario

# Formulario de creación totalmente limpio
class UsuarioCreationForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ("email", "nombre_completo", "rut", "es_admin", "is_staff")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# Formulario de edición
class UsuarioChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Contraseña", help_text="Las contraseñas se guardan encriptadas.")

    class Meta:
        model = Usuario
        fields = ("email", "nombre_completo", "rut", "cargo", "es_admin", "is_active", "is_staff")

@admin.register(Usuario)
class UsuarioPersonalizadoAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    
    model = Usuario
    list_display = ('email', 'nombre_completo', 'rut', 'cargo', 'es_admin', 'is_staff')
    list_filter = ('es_admin', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'nombre_completo', 'rut')
    ordering = ('email',)

    # Secciones para la edición
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombre_completo', 'rut', 'cargo')}),
        ('Permisos', {'fields': ('es_admin', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Secciones para la creación
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre_completo', 'rut', 'password', 'es_admin', 'is_staff'),
        }),
    )