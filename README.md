# django-server

- Django 를 이용하여 DB 관리 및 api 개발
- 추후 필요한 기능들을 Django app 으로 모듈화 하여 추가
```
프레임 워크: Django (Python)
DB: Aamazon RDS MySQL
서버 인스턴스: Amamzon ECS
Web Server: Nginx
WSGI Server: Gunicorn
```
- 시작
```
cd backend
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
- 로컬 실행
```
python manage.py runserver
# .env 파일 (중요 환경 변수) 필요
```
- 서버 배포 (파이프라인 구축 작업 진행중)
```
fab build
```