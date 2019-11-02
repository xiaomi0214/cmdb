from django.db import models

# Create your models here.
class People(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nichen = models.CharField(unique=True, max_length=30)
    email = models.CharField(unique=True, max_length=30)
    passwd = models.CharField(max_length=50)
    isready = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'people'
    def __str__(self):
        return self.nichen


class Server(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    cpu_jg = models.CharField(max_length=10)
    czxt = models.CharField(max_length=200)
    cpu_count = models.IntegerField()
    cpu_type = models.CharField(max_length=100)
    memory_size = models.CharField(max_length=10)
    root_size = models.CharField(max_length=10)
    ipv4 = models.CharField(max_length=50)
    mac = models.CharField(max_length=50)
    hostname = models.CharField(max_length=50)
    create_time = models.DateTimeField()
    localtion = models.CharField(max_length=50, blank=True, null=True,default="机柜1")
    # use_people = models.ForeignKey(People, models.DO_NOTHING, db_column='use_people', blank=True, null=True)
    use_people = models.CharField(max_length=20, blank=True, null=True,default="开发")
    application = models.CharField(max_length=30, blank=True, null=True,default="部署pro3")
    admin = models.ForeignKey(People, models.DO_NOTHING, db_column='admin', blank=True, null=True,default=1)

    class Meta:
        managed = False
        db_table = 'server'


class Applyip(models.Model):
    uid = models.ForeignKey('People', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    applytime = models.DateTimeField(db_column='applyTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'applyIp'