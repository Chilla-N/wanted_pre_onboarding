작성자:남기윤

```python

```
* 깃 튜토리얼
  * 깃 Clone
  * 깃 Pull
  * 깃 Commit
    * 깃 Commit 1)
    * 깃 Commit 2)


이름|영어|정보|수학
---|---|---|---|
나동빈|98점|87점|100점|
홍길동|97점|78점|93점|
이순신|89점|93점|97점|

 
**치킨** 먹다가 ~~두드리기~~났어요. ㅠㅠ

> '공부합시다.' - 나동빈 - 

[블로그 주소](https://blog.naver.com/ndb796)

* 사용 기술 선정

devops|기술명|선정 이유|
---|---|---|
언어|python|기존에 숙련되어있던 언어|
WebFrameWork|Django|학습 목적(기존 웹프로젝트는 flask만 경험함)|
DB|mysql|간단한 ORM쿼리를 지원하며 shell상에서 컨트롤 하기 쉬움|



* DB 구현

  1. DB설계
  
  컬럼명|속성|제한사항|내용
  ---|---|---|---|
  id|int(10)|prymary key, not null, auto_increment|제목|
  subject|varchar(100)|not null, unique key|제목|
  writer|varchar(20)|not null|게시자명|
  text|varchar(1000)|not null|상품설명|
  goal_money|int(10)|not null|목표금액|
  end_day|datetime|not null|펀딩종료일|
  per_fund|int(10)|not null|1회펀딩금액|
  start_day|datetime|not null|펀딩시작일자|
  now_fund|int(10)|default = 0|현재펀딩받은금액|

  2. models.py 작성
  
```python
#models.py

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
        ordering = ['-id']#id를 기준으로 내림차순 정렬을 기본값으로 함

```

*  **요구사항 구현**

  * 요구사항 1
  
    > '상품을 등록합니다. 제목, 게시자명, 상품설명, 목표금액, 펀딩종료일, 1회펀딩금액로 구성'
    
    분석: 
    1.상품등록에 필요한 정보를 json형태로 받아온다고 가정합니다.(for rest API)
    2.가져온 정보를 model객체로 만들어 DB에 저장합니다.
   
```python
#veiws.py

#사용할 모듈을 임포트
from django.shortcuts import render #django 기본 툴
from .models import Cloud #모델
import json
from django.views import View
from django.http  import JsonResponse #json형태로 통신
from .serializers import ListSerializer #json 변환 및 데이터 가공
from rest_framework.response import Response #일반 응답
from rest_framework.decorators import api_view #데코레이터

@api_view(['POST'])
def register_cloud(request):      #등록기능
    data = json.load(request.body) #json을 post형식으로 받아옴
    subject = data.get('subject',None)
    writer = data.get('writer',None)
    text = data.get('text',None)
    goal_money = data.get('goal_money',None)
    end_day = data.get('end_day',None)
    per_fund = data.get('per_fund',None)

    cloud = Cloud( #객체생성
        subject = subject,
        writer = writer,
        text = text,
        goal_money = goal_money,
        end_day = end_day,
        per_fund = per_fund
    )
    cloud.save() #저장
    return JsonResponse({'message': 'SUCCESS'}, status=200) #성공 메세지
```




  * 요구사항 2
  
  > '상품을 수정합니다.단, 모든 내용이 수정 가능하나 '목표금액'은 수정이 불가능합니다.'
  
    분석: 
    1.목표금액을 제외한 모든 데이터를 담고있는 json파일을 가져옵니다.
    2.가져온 정보를 model객체로 만들어 DB에 저장합니다.
      -이때 unique key인 subject(상품제목)으로 상품을 검색하여 primar key인 id값을 조회하고, 같은 id로 객체로 만들어 저장합니다.
      -mysql자체에서 DB에 이미 존재하는 primary key를 가진 객체의 저장은 수정으로 판단하기 때문입니다.
  
```python
#veiws.py

def revice(request):
    data = json.load(request.body)
    before_sub = data.get('before_sub') #기존 제목
    subject = data.get('subject',None)  #변경된 제목
    writer = data.get('writer',None)
    text = data.get('text',None) 
    end_day = data.get('end_day',None)
    per_fund = data.get('per_fund',None) 

    id = Cloud.objects.get(subject = before_sub)['id'] #기존 제목을 가진 데이터의 id값 조회
    cloud = Cloud(
        id = id,
        subject = subject,
        writer = writer,
        text = text,
        end_day = end_day,
        per_fund = per_fund
    )
    cloud.save() #수정
    return JsonResponse({'message': 'SUCCESS'}, status=200)

```

  * 요구사항 3
  
  > '상품을 삭제합니다. DB에서 삭제됩니다.'
  
 
    분석: 
    1.unique key인 subject(상품제목)으로 상품을 검색합니다.
    2.조회한 객체를 대상으로 삭제합니다.
      
      
```python
#veiws.py

def delete(request): 
    data = json.load(request.body) 
    subject = data.get('subject',None) #삭제할 게시물의 제목을 가져옴
    cloud = Cloud.objects.get(subject = subject)
    cloud.delete() #삭제
    return JsonResponse({'message': 'SUCCESS'}, status=200)
```

  * 요구사항 4


  > '상품 목록을 가져옵니다.제목, 게시자명, 총펀딩금액, 달성률 및 D-day(펀딩 종료일까지) 가 포함되어야 합니다.
  >상품 검색 기능 구현 (상품 리스트 API 에 ?search=취미 조회 시 ,제목에  ‘내 취미 만들..’  ‘취미를 위한 ..’ 등 검색한 문자 포함된 상품 리스트만 조회)
  >상품 정렬 기능 구현 생성일기준, 총펀딩금액 두 가지 정렬이 가능해야합니다. 
  >?order_by=생성일 / ?order_by=총펀딩금액
  >(달성률: 1,000,000원 목표금액 일때,  총 펀딩금액이 5,000,000원 이면 500%, 소수점 무시)'

    분석: 
    1.GET형태로 조건에 필요한 변수를 가져옵니다.
    2.조건에 해당하는 데이터를 모두 찾아옵니다. (검색기능 사용 시에만 검색에 해당하는 데이터만 찾아옴)
    3.json 형식으로 response 하기 위하여 직렬화(serialize)합니다. (serializers.py 참조)
    4.serialize기능이 제공하는 SerializerMethodField(SMF)기능을 사용합니다.
    -이유: 쿼리를 최소화하여 응답시간을 줄입니다.
    -데이터 자체 구조를 수정하지 않고도 기존 데이터에서 파생된 컬럼을 만들어 낼 수 있습니다.

```python
#views.py
def cloud_list(request):
    try:
        search = request.get['search'] # 검색기능 구현
        cloud_list = Cloud.objects.filter(name__icontains=search)
        serailized_list= ListSerializer(cloud_list, many=True)
        return Response(serailized_list.data, status=200)
    except:
        try:
            search = request.get['order_by'] #정렬 기능 구현
            if search == '생성일':
                cloud_list = Cloud.objects.filter(name__icontains=search).order_by('start_day')
                serailized_list= ListSerializer(cloud_list, many=True)
                return Response(serailized_list.data, status=200)
            elif search == '총펀딩금액':
                cloud_list = Cloud.objects.filter(name__icontains=search).order_by('now_fund')
                serailized_list= ListSerializer(cloud_list, many=True)
                return Response(serailized_list.data, status=200)
        except:
            cloud_list = Cloud.objects.all() #GET 파라미터가 존재하지 않으면 최근 만들어 진 순으로 정렬
            serailized_list= ListSerializer(cloud_list, many=True)
            return Response(serailized_list.data, status=200)
        
```

```python
#serializers.py
from django.core import serializers
from rest_framework import serializers #모듈 임포트
from .models import Cloud 

class ListSerializer(serializers.ModelSerializer): 
    subject = serializers.CharField(max_length=100)
    writer = serializers.CharField(max_length=20)
    goal_money = serializers.IntegerField()
    goal_percent = serializers.SerializerMethodField() #SMF기능 사용할 파생컬럼 달성률
    d_day = serializers.SerializerMethodField()        #SMF기능 사용할 파생컬럼 디데이
    start_day = serializers.DateTimeField()
    now_fund = serializers.IntegerField()


    class Meta: 
        model = Cloud
        fields = '__all__'

    def get_goal_percent(self, obj): #달성률 연산 (이 기능을 통해 자동으로 채워짐)
        return int((obj.now_fund/obj.goal_money)*100) #소숫점 무시
    
    def get_d_day(self, obj): #디데이 연산
        return (obj.end_day - obj.start_day).days
        
```
> 출력된 json 데이터 예:
> [{"id":1,
> "subject":"제목",
> "writer":"작성자",
> "goal_money":1000000,
> "goal_percent":0,
> "d_day":166,
> "start_day":"2022-04-18T23:55:59Z",
> "now_fund":0,
> "text":"내용",
> "end_day":"2022-10-02T00:00:00Z",
> "per_fund":1000}]

이처럼 정상적으로 작동됨을 볼 수 있습니다.






