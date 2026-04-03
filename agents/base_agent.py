import json

from utils import call_llm
from utils.logger import get_logger


class BaseAgent:
    """"Базовый агент с логированием и вызовом LLM"""

    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt
        self.logger = get_logger()

    def run(self, input_data):
        self.logger.info(f"{self.name}: Запуск агента")

        self.logger.info(f"{self.name}: Формирование запроса")
        prompt = json.dumps(input_data, ensure_ascii=False, indent=2)

        self.logger.info(f"{self.name}: Посылаем запрос в LLM")
        result = call_llm(prompt, self.system_prompt)

        self.logger.info(f"{self.name}: Получен ответ LLM, возвращаем результат")
        return result
