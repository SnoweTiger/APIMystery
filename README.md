# API Mystery

**API Mystery** - это увлекательная детективная игра по раскрытию преступлений и тренажер по работе с **Web API, RPC, GraphQL**.

## Предисловие от автора

Всем привет! С самого первого момента, как я увидел [The SQL Murder Mystery](https://mystery.knightlab.com/), я не мог поверить, что не было продолжения или похожей игры с **Web API**-решением. Когда у меня появилось время, я решил создать такую игру, и **The API Mystery** родилась!

Игра состоит из нескольких независимых частей. В каждой из них вам предстоит разгадать детективную загадку и найти преступника. Вы играете за стажера-криминалиста по имени Апи. Единственные доступные вам инструменты - это API нескольких сервисов и, конечно же, ваша смекалка и дедукция!

## Установка и начало работы

Самый простой способ использовать предварительно подготовленный контейнер. Для этого у вас на компьютере должен быть установлен Docker Desktop или docker-engine и они должны быть прописаны в path.

Открываем консоль от вашего пользователя и вводим:

```
docker pull xxxx
docker run xxxx
```

## Часть 0: Погружение в чистый API

В городе N city ночью 29 октября 2025 года из накануне открытия музея кафедры Информационных технологий была разбита витрина и похищен талисман Золотой Гоффер. Полиция пытается найти преступника и похищенный талисман.

Вам как стажеру-криминалисту поручают расследование этого дела.
Требуется найти похитетеля и у кого находится Гоффер. Ваши доступы к служебному API выслан вам 30 октября 2025 личным сообщением в **Cakebook**. По завершению расследование передайте результат с помощью API суда. Желаем удачи!

### С чего начать

Как получить доступ к документации на Web API описано в [Установка и начало работы](#установка-и-начало-работы).

Так же 30 октября 2025 вам передали ключи для доступа к API местного финтнес центра и социальной сети **Cakebook** и ваш индентификатор пользователя:

```
GETFITNOW_API_TOKEN = 'd901050d-07ec-4990-a05c-ab2178e2e09c'
CAKEBOOK_API_TOKEN = 'd901050d-07ec-4990-a05c-ab2178e2e09c'
PERSON_ID = 12345
```

Используя токен от Cakebook API и зная когда и от кого было сообщение с доступами запросите сообщения. Можете использовать свой любимый инструмент для работы с WebAPI. Я рекомендую **Bruno** или **REST Client Extension** для VS Code Например с помощью REST Client:

```
@host = http://localhost:5000/cakebook/api
@token = d901050d-07ec-4990-a05c-ab2178e2e09c

POST {{host}}/events HTTP/1.1
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "person_id": 12345,
    "start_date": 20251030,
    "end_date": 20251030
}
```

В ответ вы получете JSON, содержащий текст сообщения с доступами к служебному API. Далее с помощью служебного апи получите отчет о преступлении и приступайте к расследованию.

### Как проверить результат расследования

Воспользуйтесь API суда. Например так:

```

```

В ответе судья сообщит правы ли вы.

# В будущих обновлениях (Дорожная карта)

1. Новые части
2. Сюжетный режим
3. Загадки решаемые при помощи RPC и GraphQL
4. Загадки решаемые при помощи Web UI
