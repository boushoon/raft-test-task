import json

from agents.base_agent import BaseAgent
from utils.llm_client import call_llm

SYSTEM_PROMPT = """
Ты критик и верификатор карьерных планов.
Твоя задача: на основе переданных навыков(skill_map), таблицы вилок по грейдам и регионам(salary_table), 
плана обучения(learning_path), анализа пробелов в знаниях(gap_analysis) и проекта для портфолио(portfolio_project):
    1) Проверить согласованность: соответствуют ли зарплаты уровню навыков? Если есть сильные различия, то указать это в warnings
    2) Найти противоречия: Проверка трендов навыков из skill_map и их наличие в learning_path
    3) Обнаружение технологий, используемых в проекте для портфолио, но не из skill_map
    ! Если warnings нет, то их не нужно выдумывать
В ответе должно содержаться поле quality_score: score(Целое число от 0 до 100) + reason(Обоснование).
Выставляй quality_score на основе согласованности зарплат, наличии противоречий и их серьезности и полноты
В ответе должно содержаться поле is_consistent: Булевое значение - итоговый вердикт о целостности
Структурируй свой ответ в виде JSON без лишних объяснений в формате:
{
  "quality_score":,
  "reason_score": 
  "warnings": [],
  "is_consistent":
}
"""


class Critic(BaseAgent):
    """Критик и верификатор"""

    def run(self, input_data):
        prompt = f"{json.dumps(input_data, ensure_ascii=False, indent=2)}"
        result = call_llm(prompt, SYSTEM_PROMPT)
        return result
