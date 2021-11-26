# 🔴 [위코드 x 원티드] 카닥 기업 협업 과제

## 🟡 구현 기술 스택
- Language  : Python

- Framework :  Django

- Postman

- DB  : MySQL

- 배포 :AWS EC2

## 🟡 Contributors
|이름 |담당 기능| GitHub 주소|
|------|---|---|
|성우진| 전체 프로젝트 | [jinatra](http://github.com/jinatra)|

## 🟡 빌드 및 실행 방법
- requirements.text 파일을 install 한다.
pip install -r requirements.txt
- python manage.py runserver를 통해 서버를 실행한다.
<br>
- [POSTMAN API 문서](https://documenter.getpostman.com/view/17234940/UVJbGwv6) 를 통해 확인 가능합니다.
<br>

## 🟡 기본 설계
<img width="951" alt="스크린샷 2021-11-23 오후 5 10 33" src="https://user-images.githubusercontent.com/85162752/143542040-ecf5b637-52e9-42b9-acff-3e14e7aac96f.png">



- User, Vehicle, FrontTire, RearTire 총 네개의 테이블로 구성하였습니다.

- 모델링 시 고려했던 사항
  - 유저의 경우 이메일에 `unique`를 부여하였습니다.
  - 한 유저가 여러 차량을 가질 수 있도록 하였고, 본 모델링에서는 주어진 dev data 중 `model_name`을 기반으로 차량의 고유성을 설정하였습니다.
  - 서로 다른 차량의 경우에도 동일한 타이어 스펙을 가질 수 있다고 판단하여, 차량 테이블에 타이어 정보를 합치지 않고 분할하여 고유성을 갖도록 하였습니다. (같은 스펙의 타이어의 경우 데이터 하나로 관리 가능)


## 🟡 구현 내용
- 유저 회원가입 / 로그인 API
- 사용자가 소유한 타이어 정보를 저장하는 API
- 사용자가 소유한 타이어 정보 조회 API

## 🟡 구현 기능/구현 방법
🔵 회원가입 API
- 회원가입 시 사용자로부터 이메일과 비밀번호, 닉네임을 전달받습니다.
- (이메일은 각 사용자마다 고유한 값을 가진다고 생각하기에 id와 같은 개념으로 사용하였습니다.)
- 이메일, 비밀번호, 닉네임 등은 각각 지정한 정규표현식에 의해 예외처리가 수행됩니다.

🔵 로그인 API
- 사용자는 이메일, 비밀번호를 통해 로그인합니다.
- 사용자가 이메일, 비밀번호 등을 틀릴 경우 적절한 메시지가 반환되어집니다.

🔵 인증, 인가
- 사용자가 회원가입 시 비밀번호는 bcrypt를 통해 hashing되어 db에 저장됩니다.
- 사용자가 로그인 시 jwt 토큰이 발급되어집니다. 

🔵 타이어 정보 저장 API
- `id`와 `trimId`를 전달받아 해당 유저의 차량 정보에, `trimId`를 통해 알 수 있는 타이어 스펙을 저장합니다.
- request 건수가 5개를 넘어갈 경우 에러가 반환됩니다.
- 이미 등록된 유저-타이어 정보와 등록되어야할 정보가 동시에 request될 경우 미등록 건은 정상적으로 처리되고, 기등록 건은 적절한 에러메시지가 반환됩니다. 
- 유저가 존재하지 않을 경우 에러가 반환됩니다.
- 타이어 포맷이 지정된 형식에 어긋날 경우 에러가 반환되며 db에 저장이 되지 않습니다.

🔵 타이어 정보 조회 API
- `id`를 전달받아 해당 유저의 차량 및 타이어 정보를 반환합니다.
- 유저는 자기 자신의 타이어 정보만을 볼 수 있으며, 토큰과 `id`가 일치하지 않을 경우 에러가 반환됩니다.



## 🟡 배포 서버
- 아래 링크를 통해 엔드포인트 및 API TEST를 진행할 수 있습니다.
- http://3.128.190.45:8000


## 🟡 엔드포인트 설명
|METHOD| ENDPOINT| body | 수행목적 |
|------|---|---|----|
| POST   | /users/signup | email, password, nickname | 회원가입    |
| POST   | /users/signin  | email, password       | 로그인        |
| POST | /vehicles/tires  | id, trimId | 타이어 정보 등록 |
| GET | /vehicles/tires   | id | 타이어 정보 조회 |



## 🟡 프로젝트 회고

- 성우진: [블로그](https://velog.io/@jinatra)
