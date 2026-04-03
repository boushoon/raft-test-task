import logging
import os

_logger = None


def setup_logger(log_dir="logs"):
    global _logger

    if _logger is not None:
        return _logger

    _logger = logging.getLogger("MultiAgent")
    _logger.setLevel(logging.INFO)  # Устанавливаем уровень логгироавния INFO

    # Создаём папку для логов, если её нет
    os.makedirs(log_dir, exist_ok=True)

    # Файловый обработчик
    file_handler = logging.FileHandler(
        os.path.join(log_dir, "execution.log"),
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)

    return _logger


def get_logger():
    global _logger
    if _logger is None:
        return None
    return _logger
