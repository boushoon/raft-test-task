import json

from agents.base_agent import BaseAgent
from utils.llm_client import call_llm

SYSTEM_PROMPT = """
Ты оценщик зарплат.
Твоя задача: на основе переданных навыков(skill_map) составить таблицу(salary_table) вилок по грейдам(ы Junior / Middle / Senior / Lead) и регионам(Москва / Регионы РФ / Remote USD).
Для каждой ячейки три числа: min, median, max (тыс. руб. или USD)
В ответе должно содержаться поле market_trend: trend("growing" / "stable" / "declining") + reason(краткое обоснование (1–2 предложения))
В ответе должно содержаться поле top_employers: список из 3–5 реальных компаний, нанимающих на данную роль
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
  "market_trend": {
    "trend":,
    "reason":
  },
  "top_employers": []
}
"""


class SalaryAppraiser(BaseAgent):
    """Оценщик зарплат"""

    def run(self, input_data):
        prompt = f"{json.dumps(input_data, ensure_ascii=False, indent=2)}"
        result = call_llm(prompt, SYSTEM_PROMPT)
        return result
