from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
import decimal
from localflavor.es.forms import ESIdentityCardNumberField

class Feedback(models.Model):
    rate = models.PositiveIntegerField(verbose_name=_('Rate'), validators=[MaxValueValidator(5)])
    description = models.TextField(verbose_name=_('Description'))

    def __str__(self):
        return f'{self.rate}'

    def get_absolute_url(self):
        return u'/'

class Service(models.Model):
    CATEGORY_CHOICES = (
        ('Cuidado parcial', 'Cuidado parcial'),
        ('Cuidado completo', 'Cuidado completo'),
        ('Cuidado nocturno', 'Cuidado nocturno'),
        ('Cuidado hospitalario', 'Cuidado hospitalario'),
        ('Recados', 'Recados'),
        ('Sin especificar', 'Sin especificar'),
    )
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Author'))
    description = models.TextField(verbose_name=_('Description'))
    created = models.DateField(verbose_name=_('Created'), auto_now_add=True)
    price = models.DecimalField(verbose_name=_('Price'), max_digits=20, decimal_places=2)
    avaliability =  models.BooleanField(default=1)
    category = models.CharField(verbose_name=_('Category'), max_length=50, choices=CATEGORY_CHOICES)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='solicitante')
    offerer = models.ManyToManyField(User, related_name="offerer", blank=True, verbose_name=_('Offerers'))
    feedback = models.ManyToManyField(Feedback)


    def __str__(self):
        return f'{self.name}'

    def short_description(self):
        return self.description[:15]

    def get_absolute_url(self):
        return u'/services/all'

    def priceOverFifty(self):
        res = decimal.Decimal(self.price) * decimal.Decimal(.8)
        return "{0:.2f}".format(res)

class UserDetails(models.Model):
    GENDER_CHOICES = (
        ('M', 'Mujer'),
        ('H', 'Hombre'),
        ('O', 'Otro'),
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El número debe seguir el siguiente patrón: '+999999999'. Máximo 15 dígitos.")
    dni_regex = RegexValidator(regex=r'^[0-9]{8,8}[A-Za-z]$', message="DNI inválido")

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name=_('User'))
    birthday = models.DateField(verbose_name=_('Birthday'))
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name=_('Phone'))
    postalAddress = models.CharField(max_length=100, verbose_name=_('Postal address'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_('Gender'))
    occupation = models.CharField(max_length=100, verbose_name=_('Occupation'))
    photo = models.URLField(max_length=600, verbose_name=_('Photo'))
    socialReferences = models.CharField(null=True,blank=True,max_length=600, verbose_name=_('Social references'))
    dni = models.CharField(validators=[dni_regex], max_length=9)
    

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return u'/userdetails/'+str(self.id)


class Curriculum(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name=_('User'))
    personalData = models.CharField(max_length=1000, blank=True, verbose_name=_('Personal data'))
    experience = models.CharField(max_length=300, blank=True, verbose_name=_('Experience'))
    education = models.CharField(max_length=100, blank=True, verbose_name=_('Education'))
    misc = models.CharField(max_length=300, blank=True, verbose_name=_('Miscellaneous'))

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return u'/curriculum/'+str(self.id)

class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=_('First name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last name'))
    email = models.EmailField()
    address = models.CharField(max_length=250, verbose_name=_('Address'))
    postal_code = models.CharField(max_length=20, verbose_name=_('Postal code'))
    city = models.CharField(max_length=100, verbose_name=_('City'))
    service = models.ForeignKey(Service, null=True, blank=False,on_delete=models.CASCADE, verbose_name=_('Service'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return 'Order {}'.format(self.id)