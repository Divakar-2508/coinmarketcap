import uuid
from django.db import models

# Create your models here.
class Job(models.Model):
    job_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

class Task(models.Model):
    job = models.ForeignKey(Job, related_name='tasks', on_delete=models.CASCADE)
    coin = models.CharField(max_length=100)

class Output(models.Model):
    task = models.OneToOneField(Task, related_name='output', on_delete=models.CASCADE) 
    price = models.DecimalField(max_digits=10, decimal_places=6)
    price_change = models.DecimalField(max_digits=10, decimal_places=6)
    market_cap = models.DecimalField(max_digits=10, decimal_places=6)
    market_cap_rank = models.IntegerField()
    volume = models.BigIntegerField()
    volume_rank = models.IntegerField()
    volume_change = models.DecimalField(max_digits=10, decimal_places=6)
    circulating_supply = models.BigIntegerField()
    total_supply = models.BigIntegerField()
    diluted_market_cap = models.BigIntegerField()

class Contract(models.Model):
    output = models.ForeignKey(Output, related_name='contracts', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

class OfficialLink(models.Model):
    output = models.ForeignKey(Output, related_name='official_links', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    link = models.URLField()

class Social(models.Model):
    output = models.ForeignKey(Output, related_name='socials', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField()
