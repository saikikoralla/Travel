from django.db import models
from users.models import User
from packages.models import Packages
#from django.utils import timezone
from datetime import datetime


class User_Packages(models.Model):
    deal_id=models.AutoField(primary_key=True)
    no_of_persons=models.IntegerField(null=False)
    total_cost=models.IntegerField(default=0)
    date=models.DateTimeField(default=datetime.now)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='deals')
    package=models.ForeignKey(Packages,on_delete=models.CASCADE,related_name='deals_packages')
    
    def save(self,*args,**kwargs):
        self.total_cost=self.package.price_per_person * self.no_of_persons
        super().save(*args,**kwargs)
    
    def __str__(self):
        return f'{self.user.email} : {self.package.package_name}'
