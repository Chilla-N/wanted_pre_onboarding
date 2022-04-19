from django.core import serializers
from rest_framework import serializers 
from .models import Cloud 

class ListSerializer(serializers.ModelSerializer): 
    subject = serializers.CharField(max_length=100)
    writer = serializers.CharField(max_length=20)
    goal_money = serializers.IntegerField()
    goal_percent = serializers.SerializerMethodField()
    d_day = serializers.SerializerMethodField()
    start_day = serializers.DateTimeField()
    now_fund = serializers.IntegerField()


    class Meta: 
        model = Cloud
        fields = '__all__'

    def get_goal_percent(self, obj): 
        return int((obj.now_fund/obj.goal_money)*100)
    
    def get_d_day(self, obj): 
        return (obj.end_day - obj.start_day).days