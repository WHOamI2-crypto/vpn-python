#!/usr/bin/env python3
"""
VPN Client - подключается к VPN серверу и туннелирует трафик
"""

import socket
import ssl
import logging
from cryptography.fernet import Fernet

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VPNClient:
    def __init__(self, server_host='localhost', server_port=8443, encryption_key=None):
        """
        Инициализация VPN клиента
        
        Args:
            server_host: Адрес VPN сервера
            server_port: Порт сервера
            encryption_key: Ключ шифрования (должен совпадать с ключом сервера)
        """
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        
        # Инициализируем шифрование
        if encryption_key:
            self.encryption_key = encryption_key
        else:
            self.encryption_key = Fernet.generate_key()
        
        self.cipher_suite = Fernet(self.encryption_key)
        logger.info(f"VPN Client инициализирован")
    
    def connect(self):
        """
        Подключение к VPN серверу
        """
        try:
            # Создаём SSL контекст
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE  # Для тестирования (в продакшене использовать проверку)
            
            # Создаём обычный сокет
            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Оборачиваем в SSL
            self.socket = context.wrap_socket(raw_socket, server_hostname=self.server_host)
            
            # Подключаемся
            self.socket.connect((self.server_host, self.server_port))
            logger.info(f"Подключено к серверу {self.server_host}:{self.server_port}")
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка подключения: {e}")
            return False
    
    def send_message(self, message):
        """
        Отправка зашифрованного сообщения на сервер
        
        Args:
            message: Текст сообщения
        """
        try:
            # Шифруем сообщение
            encrypted_message = self.cipher_suite.encrypt(message.encode())
            
            # Отправляем
            self.socket.send(encrypted_message)
            logger.info(f"Сообщение отправлено: {message}")
            
            # Получаем ответ
            encrypted_response = self.socket.recv(1024)
            decrypted_response = self.cipher_suite.decrypt(encrypted_response)
            logger.info(f"Ответ сервера: {decrypted_response.decode()}")
            
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
    
    def disconnect(self):
        """
        Отключение от сервера
        """
        if self.socket:
            self.socket.close()
            logger.info("Отключено от сервера")


if __name__ == '__main__':
    client = VPNClient()
    if client.connect():
        client.send_message("Привет, это тестовое сообщение!")
        client.disconnect()
