from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

class User_info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    groupname = models.CharField(max_length=20, null=True)
    class Meta:
        db_table = 'user_info'

class Order(models.Model):
    status = models.CharField(max_length=30)
    date_recieved = models.DateField()
    date_completed = models.DateField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table='order'
      
class Spot(models.Model):
    page = models.IntegerField()
    status = models.CharField(max_length=30)
    cost = models.FloatField()
    position = models.CharField(max_length=30)
    width = models.IntegerField()
    height = models.IntegerField()
    order = models.ForeignKey('Order', null=True)
    class Meta:
        db_table='spot'
    
class Prototype(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    layout = models.CharField(max_length=100)
    text = models.CharField(max_length=200)
    desc_graphical = models.CharField(max_length=100)
    order = models.ForeignKey('Order')
    class Meta:
        db_table='prototype'

def generate_filename(instance, filename):
    url = 'prototypes/orders/%s/%s/%s' % (instance.order_id, instance.author.username, filename)
    return url
        
class Prototype_pic(models.Model):
    status = models.CharField(max_length=30, default=u'Запропонований')
    img = models.FileField(upload_to=generate_filename)
    width = models.IntegerField()
    height = models.IntegerField()
    order = models.ForeignKey('Order')
    class Meta:
        db_table='prototype_pic'