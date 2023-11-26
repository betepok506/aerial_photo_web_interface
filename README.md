# Описание

# Запуск

Для запуска приложения используйте команду:

```commandline
bash tools/run.sh
```
## Настройка

Все переменные окружения находтся в файле `.env`

Запуск осуществляется с каталога `app`
Linux
```commandline
gunicorn -w 4 --bind 0.0.0.0:8000 wsgi:app
```

# Настройка NGINX

Установка Nginx
```commandline
sudo apt update
sudo apt install nginx
```

Запуск Nginx
```commandline
sudo service nginx start
```

Проверка статуса Nginx
```commandline
sudo service nginx status
```

Просмотрите статус службы Nginx:
```commandline
systemctl status nginx.service
```

Проверка корректности конфигурационного файла nginx
```commandline
nginx -t
```

Настройка Nginx:

- Редактируем конфигурационный файл: `sudo nano /etc/nginx/sites-available/default`

- Добавьте или измените блок server, чтобы настроить перенаправление:
```commandline
server {
    listen 80;
    server_name waytorest.ru www.waytorest.ru;

    location / {
        proxy_pass http://localhost:8000;  # Перенаправление на порт 8000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
- Перезапустите сервис Nginx, чтобы изменения вступили в силу: