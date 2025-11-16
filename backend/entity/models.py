from django.db import models

# Create your models here.

class CompanyInformation(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'Dollar américain (USD)'),
        ('EUR', 'Euro (EUR)'),
        ('GBP', 'Livre sterling (GBP)'),
        ('CDF', 'Franc congolais (CDF)'),
        ('XAF', 'Franc CFA (XAF)'),
        ('ZAR', 'Rand sud-africain (ZAR)'),
        ('NGN', 'Naira nigérian (NGN)'),
        ('KES', 'Shilling kényan (KES)'),
        ('TZS', 'Shilling tanzanien (TZS)'),
        ('UGX', 'Shilling ougandais (UGX)'),
        ('RWF', 'Franc rwandais (RWF)'),
        ('MAD', 'Dirham marocain (MAD)'),
        ('XOF', 'Franc CFA BCEAO (XOF)'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Nom de l'entreprise")
    city = models.CharField(max_length=100, verbose_name="Ville")
    commune = models.CharField(max_length=100, verbose_name="Commune")
    avenue = models.CharField(max_length=100, verbose_name="Avenue")
    quarter = models.CharField(max_length=100, verbose_name="Quartier")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='CDF', 
        verbose_name="Devise"
    )
    
    class Meta:
        verbose_name = "Information de l'entreprise"
        verbose_name_plural = "Informations de l'entreprise"
    
    def __str__(self):
        return self.name
