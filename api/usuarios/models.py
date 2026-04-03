from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinLengthValidator

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('es_admin', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    # Eliminamos el campo username para usar el email
    username = None
    email = models.EmailField('Correo electrónico', unique=True)
    
    # Campos personalizados
    nombre_completo = models.CharField('Nombre completo', max_length=255)
    rut = models.CharField('RUT', max_length=12, unique=True)
    cargo = models.CharField('Cargo', max_length=100, blank=True, null=True)
    
    # El campo 'es_admin' controlará el acceso total a los sensores en tu lógica
    es_admin = models.BooleanField('Es Administrador', default=False)

    # Configuramos el email como el campo para login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre_completo', 'rut']

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombre_completo} ({self.cargo})"