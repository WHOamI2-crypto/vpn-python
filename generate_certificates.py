#!/usr/bin/env python3
"""
Скрипт для генерации самоподписанных SSL сертификатов
(Используется только для разработки и тестирования!)
"""

import subprocess
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_certificates():
    """
    Генерирует самоподписанные сертификаты для тестирования
    """
    logger.info("Генерирую самоподписанные сертификаты...")
    
    # Команда для генерации приватного ключа и сертификата
    command = [
        'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
        '-keyout', 'server.key',
        '-out', 'server.crt',
        '-days', '365',
        '-nodes',
        '-subj', '/CN=localhost'
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✓ Сертификаты успешно созданы:")
            logger.info("  - server.key (приватный ключ)")
            logger.info("  - server.crt (сертификат)")
        else:
            logger.error(f"Ошибка при генерации сертификатов: {result.stderr}")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        logger.info("Убедитесь, что OpenSSL установлен на вашей системе")


if __name__ == '__main__':
    generate_certificates()
