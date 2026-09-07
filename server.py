#!/usr/bin/env python3
"""
VPN Server - принимает подключения клиентов и туннелирует трафик
"""

import socket
import ssl
import threading
import logging
from cryptography.fernet import Fernet

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VPNServer:
    def __init__(self, host='localhost', port=8443):
        """
        Инициализация VPN сервера
        
        Args:
            host: IP адрес сервера
            port: Порт для подключения
        """
        self.host = host
        self.port = port
        self.clients = []  # Список подключённых клиентов
        self.server_socket = None
        
        # Генерируем ключ шифрования (в продакшене использовать безопасное хранилище)
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        logger.info(f"VPN Server инициализирован на {host}:{port}")
    
    def start(self):
        """
        Запуск VPN сервера
        """
        try:
            # Создаём SSL контекст
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(
                certfile='server.crt',
                keyfile='server.key'
            )
            
            # Создаём сокет
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            logger.info("VPN Server запущен и ожидает подключений...")
            
            # Принимаем подключения в бесконечном цикле
            while True:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    logger.info(f"Новое подключение от {client_address}")
                    
                    # Запускаем обработку клиента в отдельном потоке
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except Exception as e:
                    logger.error(f"Ошибка при принятии подключения: {e}")
                    
        except Exception as e:
            logger.error(f"Ошибка сервера: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def handle_client(self, client_socket, client_address):
        """
        Обработка клиента
        
        Args:
            client_socket: Сокет клиента
            client_address: Адрес клиента
        """
        try:
            # Получаем данные от клиента
            encrypted_data = client_socket.recv(1024)
            
            # Расшифровываем
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            logger.info(f"От {client_address}: {decrypted_data.decode()}")
            
            # Отправляем ответ (зашифрованный)
            response = b"Сообщение получено на сервере"
            encrypted_response = self.cipher_suite.encrypt(response)
            client_socket.send(encrypted_response)
            
        except Exception as e:
            logger.error(f"Ошибка при работе с клиентом {client_address}: {e}")
        finally:
            client_socket.close()
            logger.info(f"Клиент {client_address} отключён")


if __name__ == '__main__':
    server = VPNServer()
    server.start()
