from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)
    full_name = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name


class Address(models.Model):
    postal_code = models.IntegerField(validators=[MinValueValidator(1)])
    municipality = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    primary = models.BooleanField()

    def clean(self):
        if self.id is None and Address.objects.filter(user_id=self.user).count() >= 3:
            raise ValidationError('User already has maximal amount of addresses (3)')

    def save(self, *args, **kwargs):
        user = getattr(self, 'user')
        if getattr(self, 'primary'):
            Address.objects.filter(user_id=user).update(primary=False)
        super(Address, self).save(*args, **kwargs)

    def __str__(self):
        return self.municipality + ' ' + self.state + ' CP: '+str(self.postal_code)

