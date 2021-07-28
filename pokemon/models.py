from django.db import models

# Create your models here.


class Type(models.Model):
    type_name = models.CharField(max_length=8)
    image = models.URLField(default="")
    color = models.CharField(default="", max_length=7)
    def __str__(self) -> str:
        return self.type_name.capitalize()
    
class Regen(models.Model):
    gen = models.IntegerField(null=True, unique=True)
    reg = models.CharField(max_length=6)
    
    def __str__(self) -> str:
        return str(self.gen) + " - " + self.reg
    

class Pokemon(models.Model):
    id = models.IntegerField(primary_key=True , unique=True)
    name = models.CharField(max_length=50)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.URLField()
    type_name = models.ManyToManyField(Type)
    regen = models.ManyToManyField(Regen)

    def __str__(self) -> str:
        return str(self.id) + " - " + self.name + " - " + str(self.height) + " - " + str(self.weight) + " - " + str(list(self.type_name.all()))  + " - " + str(self.regen.first())