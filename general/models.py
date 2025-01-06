from django.db import models

# Create your models here.

class AbstractCommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Address(AbstractCommonModel):
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255 , blank=True , null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.ForeignKey('general.Country', on_delete=models.SET_NULL , null=True)

    def __str__(self):
        return f"{self.line_1} , {self.city} , {self.state} , {self.country}"


class BankDetails(AbstractCommonModel):
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
    

class Country(AbstractCommonModel):
    continent = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.country

