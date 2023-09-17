### Обновить
Локально:
```
docker build -t ghcr.io/denisov/guess-changbin .
docker push ghcr.io/denisov/guess-changbin
```

На сервере:
```
./update-guess-changbin.sh
```
или
```
docker stop guess-changbin
docker rm guess-changbin
docker rmi ghcr.io/denisov/guess-changbin
docker run \
    -d \
    --name guess-changbin \
    -e TELEGRAM_BOT_TOKEN=<..> \
    ghcr.io/denisov/guess-changbin:latest
```
