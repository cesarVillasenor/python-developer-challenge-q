from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)
    full_name = models.CharField(max_length=50)

    class Comment:
        def __init__(self, email, password, full_name):
            self.email = email
            self.password = password
            self.full_name = full_name

    def __str__(self):
        return self.full_name


class Address(models.Model):
    postal_code = models.IntegerField(validators=[MinValueValidator(1)])
    municipality = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    user = models.ForeignKey(to=User, related_name='addresses', on_delete=models.PROTECT)
    primary = models.BooleanField()

    def clean(self):
        addresses = Address.objects.filter(user_id=self.user)
        if self.id is None and addresses.count() >= 3:
            raise ValidationError('User already has maximal amount of addresses (3)')
        if not self.primary:
            primary = False
            if self.id is not None:
                addresses = Address.objects.filter(user_id=self.user).exclude(id=self.id)
            for address in addresses:
                if address.primary:
                    primary = True
                    break
            if not primary :
                if self.id is None:
                    raise ValidationError('There Is Not A Primary Please Create A Primary Address')
                else:
                    raise ValidationError('Cannot Update You Should Have At Least One Primary Address')


    def save(self, *args, **kwargs):
        user = getattr(self, 'user')
        if getattr(self, 'primary'):
            Address.objects.filter(user_id=user).update(primary=False)
        super(Address, self).save(*args, **kwargs)

    def __str__(self):
        return self.municipality + ' ' + self.state + ' CP: '+str(self.postal_code)

