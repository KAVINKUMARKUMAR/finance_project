from django.db import models

# Create your models here.
SERVICE_CHOICES = [
    ('home_loan', 'Home Loan'),
    ('personal_loan', 'Personal Loan'),
    ('car_loan', 'Car Loan'),
    ('insurance', 'Insurance'),
    ('other', 'Other'),
]

WORLD_PHONE_CODES = [
    ('+1', 'USA, Canada, and other countries'),
    ('+44', 'United Kingdom'),
    ('+91', 'India'),
    ('+61', 'Australia'),
    ('+81', 'Japan'),
    ('+33', 'France'),
    ('+49', 'Germany'),
    ('+39', 'Italy'),
    ('+55', 'Brazil'),
    ('+34', 'Spain'),
    ('+52', 'Mexico'),
    ('+7', 'Russia, Kazakhstan'),
    ('+86', 'China'),
    ('+27', 'South Africa'),
    ('+971', 'United Arab Emirates'),
    ('+66', 'Thailand'),
    ('+27', 'South Africa'),
    ('+61', 'Australia'),
    ('+20', 'Egypt'),
    ('+32', 'Belgium'),
    ('+31', 'Netherlands'),
    ('+34', 'Spain'),
    ('+45', 'Denmark'),
    ('+46', 'Sweden'),
    ('+48', 'Poland'),
    ('+49', 'Germany'),
    ('+53', 'Cuba'),
    ('+54', 'Argentina'),
    ('+60', 'Malaysia'),
    ('+63', 'Philippines'),
    ('+64', 'New Zealand'),
    ('+65', 'Singapore'),
    ('+81', 'Japan'),
    ('+82', 'South Korea'),
    ('+91', 'India'),
    ('+92', 'Pakistan'),
    ('+93', 'Afghanistan'),
    # You can add more countries and codes as needed
]


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_code = models.CharField(max_length=10, choices=WORLD_PHONE_CODES,default='+91')
    phone = models.CharField(max_length=15)
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES,default='home_loan')
    desc = models.TextField()

class Boxes(models.Model):
    name=models.CharField(max_length=250)
    abo=models.CharField(max_length=250)
    desc=models.CharField(max_length=500)
    img=models.ImageField(upload_to='box/',null=True)

    def __str__(self):
        return f"box: {self.name}"
