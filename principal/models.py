from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Service(models.Model):
    CATEGORY_CHOICES = (
        ('Cuidado parcial', 'Cuidado parcial'),
        ('Cuidado completo', 'Cuidado completo'),
        ('Cuidado nocturno', 'Cuidado nocturno'),
        ('Cuidado hospitalario', 'Cuidado hospitalario'),
        ('Recados', 'Recados'),
        ('Sin especificar', 'Sin especificar'),
    )
    name = models.CharField(verbose_name=('Nombre'), max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=('Autor'))
    description = models.TextField(verbose_name=('Descripción'))
    created = models.DateField(verbose_name=('Fecha de creación'), auto_now_add=True)
    price = models.DecimalField(verbose_name=('Precio'), max_digits=20, decimal_places=2)
    avaliability = models.IntegerField(verbose_name=('Disponibilidad'))
    category = models.CharField(verbose_name=('Categoría'), max_length=50, choices=CATEGORY_CHOICES)
    offerer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offerer", null=True, blank=True, verbose_name=('Solicitante'))

    def __str__(self):
        return f'{self.name}'

    def short_description(self):
        return self.description[:15]

    def get_absolute_url(self):
        return u'/oldkareall'

class UserDetails(models.Model):
    GENDER_CHOICES = (
        ('M', 'Mujer'),
        ('H', 'Hombre'),
        ('O', 'Otro'),
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El número debe seguir el siguiente patrón: '+999999999'. Máximo 15 dígitos.")

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=('Usuario'))
    birthday = models.DateField(verbose_name=('Fecha de nacimiento'))
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name=('Teléfono'))
    postalAddress = models.CharField(max_length=100, verbose_name=('Domicilio'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=('Género'))
    occupation = models.CharField(max_length=100, verbose_name=('Profesión'))
    photo = models.URLField(max_length=600, verbose_name=('Foto'))
    socialReferences = models.CharField(null=True,blank=True,max_length=600, verbose_name=('Redes Sociales'))

    def __str__(self):
        return f'{self.user.username}'
    def get_absolute_url(self):
        return u'/oldkare'