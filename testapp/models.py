
from django.db import models


class Cloud(models.Model):
    subject = models.CharField(max_length=100)
    writer = models.CharField(max_length=20)
    text = models.CharField(max_length=1000)
    goal_money = models.IntegerField()
    end_day = models.DateTimeField()
    per_fund = models.IntegerField()
    start_day = models.DateTimeField(blank=True, null=True)
    now_fund = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cloud'
        ordering = ['-id']
