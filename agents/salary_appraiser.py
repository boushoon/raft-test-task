import json

from agents.base_agent import BaseAgent
from utils.llm_client import call_llm

SYSTEM_PROMPT = """
ОТВЕЧАЙ ТОЛЬКО НА РУССКОМ ЯЗЫКЕ.
Ты оценщик зарплат.
Твоя задача: на основе переданных навыков(skill_map) составить таблицу(salary_table) вилок по грейдам и регионам.
    * Грейды: Junior / Middle / Senior / Lead
    * Регионы: Москва(тыс. руб.) / Регионы РФ(тыс. руб.) / Remote USD(в USD)
Для каждой ячейки таблицы три числа: min < median < max

В ответе также должны содержаться следующие поля:
    * market_trend:
        growing - растущий спрос
        stable - стабильный спрос
        declining - падающий спрос
    * market_trend_reason(краткое обоснование такого тренда на 1–2 предложения):
        - Объясни, почему тренд такой, учитывая востребованность навыков из skill_map.
    * top_employers: 
        - Список из 3–5 реальных компаний, которые активно нанимают специалистов с указанными навыками в skill_map
Структурируй свой ответ в виде JSON без лишних объяснений в формате:

{
  "salary_table": {
    "Junior": {
      "Москва": {},
      "Регионы РФ": {},
      "Remote USD": {}
    },
    "Middle": {
      "Москва": {},
      "Регионы РФ": {},
      "Remote USD": {}  
    },
    "Senior": {
      "Москва": {},
      "Регионы РФ": {},
      "Remote USD": {}
    },
    "Lead": {
      "Москва": {},
      "Регионы РФ": {},
      "Remote USD": {}
    }
  },
  "market_trend": ,
  "market_trend_reason": ,
  "top_employers": []
}
"""


class SalaryAppraiser(BaseAgent):
    """Оценщик зарплат"""

    def run(self, input_data):
        prompt = f"{json.dumps(input_data, ensure_ascii=False, indent=2)}"
        result = call_llm(prompt, SYSTEM_PROMPT)
        return result
