from django.urls import path
from testapp.views import index, register_cloud,delete,revice,cloud_list

urlpatterns = [
    path('index', index), 
    path('register_cloud', register_cloud), 
    path('delete', delete), 
    path('revice', revice), 
    path('cloud_list/', cloud_list), 
]