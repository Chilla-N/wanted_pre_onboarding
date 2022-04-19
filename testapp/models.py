# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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
