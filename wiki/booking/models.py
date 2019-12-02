from django.db import models

# Create your models here.
class DoctorFiles(models.Model):
    dname = models.CharField(verbose_name='医生姓名',max_length=10)
    dtitle = models.CharField(verbose_name='职称',max_length=20)
    dintroduction = models.CharField(verbose_name='介绍',max_length=1000)
    department = models.CharField(verbose_name='科室',max_length=20)
    dcount = models.BooleanField(verbose_name='是否显示',default=True)
    isActive = models.BooleanField(verbose_name='是否显示',default=True)
    def __str__(self):
        return self.dname,self.dtitle,self.department
    class Meta:
        db_table = 'doctor'


