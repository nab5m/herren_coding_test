# 헤렌 코딩 테스트

작성자: 김준영

## 명세
pipenv, postgresql, celery, docker <br><br>
<문서 작성하기> <br>
[swagger 보러가기](http://api.localhost:8000/api-auth/login/?next=/api/v1/swagger) <br>
[redoc 보러가기](http://api.localhost:8000/api-auth/login/?next=/api/v1/redoc)


## 브랜치 관리
- master(=main) <br>
: 프로덕션 서버, 실제 배포에 사용할 브랜치 <br>

- develop <br>
: 개발 서버 <br>

## 목표
1. API TDD 적용해보기
2. black이라는 파이썬 코드 포매터 사용해보기 
3. swagger로 문서화하기
4. 코테 합격하기

## ToDo료
1. subscribe, unsubscribe (완료)
2. mail, inbox, mail_all
3. mail_v2, mail_all_v2
4. 도커 설정

## 실행방법
```shell script
pipenv install

python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
python manage.py runserver
```
