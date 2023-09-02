from django.test import TestCase

from yektanet import models


class CarTest(TestCase):
    """Car Model Test"""
    
    def test_car_model_should_work_properly(self):
        """Test Car Model"""
        fields = {
            "source" : "test car",
            "code" : "test car code",
            # "phone" : "09151498722" 
        }
        car = models.Car.objects.create(**fields)
        
        for (key, value) in fields.items():
            self.assertEqual(getattr(car, key),value)
            
            
class PhoneTest(TestCase):
    """Phone Model Test"""
    
    def test_phone_model_should_work_properly(self):
        """Test Phone Model"""
        car_fields = {
            "source" : "test car",
            "code" : "test car code",
            # "phone" : "09151498722" 
        }
        car = models.Car.objects.create(**car_fields)
        
        fields = {
            "phone" : "09151498722" 
        }
        
        phone = models.Phone.objects.create(car=car,**fields)
        
        for (key, value) in fields.items():
            self.assertEqual(getattr(phone, key),value)
        
        self.assertEqual(phone.car.id, car.id)