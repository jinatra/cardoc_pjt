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
- 거래내역 조회 GET API
- 입금 POST API
- 출금 POST API

## 🟡 구현 기능/구현 방법
🔵  거래내역 조회 GET API
 
- 검색 시작 날짜(`start_date`), 검색 종료 날짜(`end_date`), 입/출금 타입(`type`) 및 pagination data(`offset`, `limit`)을 쿼리 스트링으로 전달받습니다.
- 각각의 쿼리스트링이 전달되지 않으 경우, 기존에 지정해두 default value를 통해 filtering하게 됩니다.
- filtering method로는 q객체를 사용하였습니다.
- 인증되지 않은 유저(다른 유저)의 접근을 제한하기 위해 토큰을 이용하여 사용자르 식별합니다.
- Key Error, Value Error(잘못된 type 형식 등), Validation Error(잘못된 날짜 형식 등)에 대한 예외처리를 주었습니다.

🔵 입금 POST API

- json을 통해 입금할 금액, account_id, 적요를 받아온 후, account_id가 존재하는지 확인합니다. id가 없다면 계좌 없음 에러를 반환합니다.
- 그 후 계좌 잔액과 입금 금액을 더해 전체 금액을 저장해주고, account_id와 account_balance, brief를 결과값으로 받아옵니다.

🔵 출금 POST API

- json을 통해 출금할 금액, account_id, 적요를 받아온 후, account_id가 존재하는지 확인합니다. id가 없다면 계좌 없음 에러를 반환합니다.
- 그 후 계좌 잔액과 출금 금액을 빼 전체 금액을 저장해주고, 뺀 금액이 0보다 큰지 확인합니다. 0보다 작다면 잔고 부족으로 에러를 반환합니다.
- account_id와 account_balance, brief를 결과값으로 받아옵니다.



## 🟡 배포 서버
- 아래 OPEN API 링크를 통해 엔드포인트 및 API TEST를 진행할 수 있습니다.
- http://3.35.0.116:8000/


## 🟡 엔드포인트 설명
|METHOD| ENDPOINT| body | 수행목적 |
|------|---|---|----|
| GET	| /accounts/history?start_date&?end_date?type	| query string	| 거래 내역 조회 |
| POST | /accounts/deposit  |  | 입금 |
| POST | /accouts/withdraw  |  | 출금 |


## 🟡 아쉬웠던 점

- 성우진
<img width="669" alt="image" src="https://user-images.githubusercontent.com/85162752/141450304-0eff9404-3ff4-49b3-b099-81a91a4c2b0a.png">

  - 위 조회 화면에서는 특정 기간(일주일, 한달 등)을 조회할 수 있는 버튼을 주었는데, 해당 post request에 대해 즉각적으로 반환해줄 수 있는 API를 짜지 못했더 점이 못내 아쉽습니다.
  - DB join을 최소화하기 위해 하나의 쿼리문을 통해 객체르 가져올 수 있도로 하였는데, 각 객체의 user_id에 접근하여 token의 user_id와 비교할 수 있는 방법을 제출 기한 내에 생각하지 못해 첫 객체를
    기준으로 잡아 인증 검사를 하였던 것이 아쉬웠습니다.

- 김도담
  - user가 하나의 account를 가질 수 있게 unique=true 조건을 주었음에도 account_id를 통해 입금/출금 기능을 구현할 생각을 보다 늦게 한 것이 아쉬웠습니다.
  - 보다 간결하게 코드를 작성하기 위해 어떻게 해야하는가? 고민할 수 있었던 시간이었습니다. 로직을 깔끔하게 코드에 담아내고, 작동될 수 있게 작성하는 것이 중요하다는 것을 다시 한 번 배웠습니다. 

## 🟡 프로젝트 회고

- 이정우: [블로그](https://mytech123.tistory.com/)
- 성우진: [블로그](https://velog.io/@jinatra)
- 김도담: [블로그](http://velog.io/@damdreammm)
