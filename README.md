# simple-dns-server


# Запуск
1. Клонирование репозитория
```bash
git clone https://github.com/dezzerlol/simple-dns-server.git
```

2. Запуск docker контейнера с сервером
```bash
docker compose up
```

3. Запуск docker контейнера с указанием DNS резолвера (пример 8.8.8.8)
```bash
docker compose run --service-ports dns-server --resolver 8.8.8.8
```

## Пример работы
Проверка работы DNS сервера линукс утилитой dig:
```bash
dig @0.0.0.0 -p 2053 +noedns yandex.com
```

Пример ответа без использования DNS резолвера:
```bash
; <<>> DiG 9.18.18-0ubuntu0.23.04.1-Ubuntu <<>> @0.0.0.0 -p 2053 +noedns yandex.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 37359
;; flags: qr rd ad; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 0
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;yandex.com.			IN	A

;; Query time: 0 msec
;; SERVER: 0.0.0.0#2053(0.0.0.0) (UDP)
;; WHEN: Fri Jan 05 12:28:28 +05 2024
;; MSG SIZE  rcvd: 28

```

Пример ответа в случае использования DNS резолвера:
```bash
; <<>> DiG 9.18.18-0ubuntu0.23.04.1-Ubuntu <<>> @0.0.0.0 -p 2053 +noedns yandex.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 16546
;; flags: qr rd ad; QUERY: 1, ANSWER: 4, AUTHORITY: 0, ADDITIONAL: 0
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;yandex.com.			IN	A

;; ANSWER SECTION:
yandex.com.		1077	IN	A	77.88.55.80
yandex.com.		1077	IN	A	5.255.255.80
yandex.com.		1077	IN	A	5.255.255.88
yandex.com.		1077	IN	A	77.88.55.77

;; Query time: 4 msec
;; SERVER: 0.0.0.0#2053(0.0.0.0) (UDP)
;; WHEN: Fri Jan 05 12:28:00 +05 2024
;; MSG SIZE  rcvd: 132

```