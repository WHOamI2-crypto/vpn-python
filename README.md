# VPN Application на Python

Полноценное VPN приложение с клиентом и сервером, использующее SSL/TLS шифрование и криптографию.

## Структура проекта

```
vpn-python/
├── server.py                    # VPN Сервер
├── client.py                    # VPN Клиент
├── generate_certificates.py     # Генерация SSL сертификатов
├── requirements.txt             # Python зависимости
└── README.md                    # Этот файл
```

## Требования

- Python 3.7+
- OpenSSL (для генерации сертификатов)

## Установка

### 1. Клонируем репозиторий
```bash
git clone https://github.com/WHOamI2-crypto/vpn-python.git
cd vpn-python
```

### 2. Устанавливаем зависимости
```bash
pip install -r requirements.txt
```

### 3. Генерируем SSL сертификаты
```bash
python generate_certificates.py
```

Это создаст:
- `server.key` - приватный ключ сервера
- `server.crt` - сертификат сервера

## Использование

### Запуск сервера

```bash
python server.py
```

Вы увидите:
```
2026-01-15 10:30:45,123 - INFO - VPN Server инициализирован на localhost:8443
2026-01-15 10:30:45,124 - INFO - VPN Server запущен и ожидает подключений...
```

### Запуск клиента (в другом терминале)

```bash
python client.py
```

Вы увидите:
```
2026-01-15 10:30:50,456 - INFO - VPN Client инициализирован
2026-01-15 10:30:50,457 - INFO - Подключено к серверу localhost:8443
2026-01-15 10:30:50,458 - INFO - Сообщение отправлено: Привет, это тестовое сообщение!
2026-01-15 10:30:50,459 - INFO - Ответ сервера: Сообщение получено на сервере
```

## Как это работает?

### Шифрование (Fernet)

Мы используем симметричное шифрование Fernet для защиты данных:

```python
from cryptography.fernet import Fernet

# Генерируем ключ
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Шифруем
encrypted = cipher_suite.encrypt(b"Мое сообщение")

# Расшифровываем
decrypted = cipher_suite.decrypt(encrypted)
```

### SSL/TLS

Сервер использует SSL сертификат для безопасного соединения:

```python
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')
```

## Дальнейшее развитие

- [ ] Аутентификация пользователей (username/password)
- [ ] Управление IP адресами в виртуальной сети
- [ ] Туннелирование реального сетевого трафика
- [ ] Асимметричное шифрование (RSA) для обмена ключами
- [ ] Поддержка нескольких протоколов (TCP/UDP)
- [ ] Веб-интерфейс для управления
- [ ] Логирование и мониторинг
- [ ] Тесты (unittest/pytest)

## ⚠️ Безопасность

**ЭТО УЧЕБНЫЙ ПРОЕКТ!** Не используйте в продакшене без:

1. Правильной генерации и хранения ключей
2. Проверки сертификатов
3. Аутентификации
4. Аудита безопасности
5. Использования проверенных библиотек

## Лицензия

MIT

## Автор

WHOamI2-crypto
