from django.db import models
from  django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField

class members(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    member_id = models.BigAutoField(primary_key=True)
    phone=models.IntegerField(default=0)
    # block_ch=(('L1','L1'),('L2','L2'))
    block=models.CharField(max_length=5)

    flat=models.IntegerField(default=0)
    # types=(('O','owner'),('R','Rent'),('E','Empty'))
    flat_type=models.CharField(max_length=20)
    designation=models.CharField(max_length=20,default="")
class transactions(models.Model):
    
    room_id=models.ForeignKey(members,on_delete=models.CASCADE)
    transact_id=models.CharField(max_length=1000,null=True)
    order_id=models.CharField(max_length=1000,null=True,unique=True)
    amount=models.BigIntegerField(null=True)

    currency=models.CharField(max_length=20,null=True)
    timestamp=models.DateTimeField(null=True)
    type=models.CharField(max_length=8,null=True,choices=(('O','online'),('F','offline')))
    status=models.CharField(max_length=15,null=True)
    From_mon=models.IntegerField(null=True)
    From_year=models.IntegerField(null=True)
    To_year=models.IntegerField(null=True)

    To_mon=models.IntegerField(null=True)
    path=models.CharField(max_length=100,null=True)

class employe(models.Model):
    emp_id=models.IntegerField(primary_key=True)
    emp_name=models.CharField(max_length=50)
    type=(('Y','Yes'),('N','No'))
    Present=models.CharField(max_length=1,choices=type)
    Available=models.CharField(max_length=1,choices=type)
    phone=models.IntegerField(default=None)
    dept_type=(('cleaning','cleaning'),('security','security'))
    dept=models.CharField(max_length=20, choices=dept_type)
class schedule(models.Model):
    schedule_id=models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300)
    date=models.DateField(default=None)
    from_time= models.TimeField()
    to_time=models.TimeField()





