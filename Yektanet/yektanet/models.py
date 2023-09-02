from django.db import models

class AuthCode(models.Model):
    """Authorization Code Model"""
    
    phone = models.CharField(max_length=11, null=False, blank=False)
    code = models.TextField(null=False, blank=False)
    
    def __str__(self) -> str:
        return self.phone

class Car(models.Model):
    """Car Model"""
    
    source = models.CharField(max_length=85)
    code = models.CharField(max_length=85)
    
    def __str__(self) -> str:
        return f"{self.source}-{self.code}"
    
    
class Phone(models.Model):
    """Phone Model"""
    
    phone = models.CharField(max_length=11, null=True, blank=True)
    
    car = models.ForeignKey(Car, null=True, blank=True, on_delete=models.SET_NULL, related_name="phones")
    
    def __str__(self) -> str:
        return f"{self.car}-{self.phone}"