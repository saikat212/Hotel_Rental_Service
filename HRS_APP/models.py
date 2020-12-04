

# Create your models here.
from django.db import models
from django.conf import settings
from django.urls import reverse_lazy

# Create your models here.
class Room(models.Model):
    ROOM_AVAILABILITY = (
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUXE'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
    )
    HOTEL_ID = models.IntegerField()
    ROOM_ID  = models.IntegerField()
    FLOOR  = models.IntegerField()
    PRICE  = models.IntegerField()
    BUILDING = models.CharField(max_length=3, choices=ROOM_AVAILABILITY)
    NUMBER_OF_BED = models.IntegerField()
    CAPACITY = models.IntegerField()
#catagory = BUILDING ,, ROOM_CATAGORY=ROOM_AVIALABILITY
    def __str__(self):
        return f'{self.HOTEL_ID}. {dict(self.ROOM_AVAILABILITY)[self.BUILDING]} NUMBER_OF_BED = {self.beds} People = {self.capacity}'


