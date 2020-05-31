# 백엔드 서버 사용법

## 가상환경 virtualenv 써야함

virtualenv -p python3.6 <가상환경 폴더명>

## 가상환경 접속

Linux/Max OS 기준 : source <가상환경 폴더명>/bin/activate
Window OS 기준 : <가상환경 폴더명>/Scripts/activate

## 접속 후 코드 폴더로 이동

pip install -r requirements.txt -I

## 설치 후 서버 열기

uvicorn main:app --host 0.0.0.0 --port 2052


