from django.shortcuts import render
from .models import Cloud
import json
from django.views import View
from django.http  import JsonResponse
from .serializers import ListSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'],['POST'])
def index(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        cloud = Cloud.objects.get(subject = subject)
        cloud.now_fund += cloud.per_fund
        cloud.save()
        return JsonResponse({'message': 'SUCCESS'}, status=200)
    else:
        return JsonResponse({'message': 'HELLO'}, status=200)

@api_view(['POST'])
def register_cloud(request): #등록
    data = json.load(request.body) #post요청받은 json 추출
    subject = data.get('subject',None)
    writer = data.get('writer',None)
    text = data.get('text',None)
    goal_money = data.get('goal_money',None)
    end_day = data.get('end_day',None)
    per_fund = data.get('per_fund',None)

    cloud = Cloud( 
        subject = subject,
        writer = writer,
        text = text,
        goal_money = goal_money,
        end_day = end_day,
        per_fund = per_fund
    )
    cloud.save()
    return JsonResponse({'message': 'SUCCESS'}, status=200)

@api_view(['POST'])
def delete(request): #삭제
    data = json.load(request.body) #post요청받은 json 추출
    subject = data.get('subject',None) #삭제할 게시물의 제목을 가져옴
    cloud = Cloud.objects.get(subject = subject)
    cloud.delete()
    return JsonResponse({'message': 'SUCCESS'}, status=200)

@api_view(['POST'])
def revice(request): #수정
    data = json.load(request.body) #post요청받은 json 추출
    before_sub = data.get('before_sub')
    subject = data.get('subject',None)
    writer = data.get('writer',None)
    text = data.get('text',None) 
    end_day = data.get('end_day',None)
    per_fund = data.get('per_fund',None) 

    id = Cloud.objects.get(subject = before_sub)['id']
    cloud = Cloud(
        id = id,
        subject = subject,
        writer = writer,
        text = text,
        end_day = end_day,
        per_fund = per_fund
    )
    cloud.save()
    return JsonResponse({'message': 'SUCCESS'}, status=200)


@api_view(['get'])
def cloud_list(request): #리스트 출력
    try:
        search = request.get['search']
        cloud_list = Cloud.objects.filter(name__icontains=search)
        serailized_list= ListSerializer(cloud_list, many=True)
        return Response(serailized_list.data, status=200)
    except:
        try:
            search = request.get['order_by']
            if search == '생성일':
                cloud_list = Cloud.objects.filter(name__icontains=search).order_by('start_day')
                serailized_list= ListSerializer(cloud_list, many=True)
                return Response(serailized_list.data, status=200)
            elif search == '총펀딩금액':
                cloud_list = Cloud.objects.filter(name__icontains=search).order_by('now_fund')
                serailized_list= ListSerializer(cloud_list, many=True)
                return Response(serailized_list.data, status=200)
        except:
            cloud_list = Cloud.objects.all()
            serailized_list= ListSerializer(cloud_list, many=True)
            return Response(serailized_list.data, status=200)
        
