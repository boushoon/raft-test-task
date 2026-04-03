import json
import os

from utils.logger import get_logger


def generate_markdown(report, role):
    # Заголовок и время генерации
    md = f"# Карьерный отчёт: {role}\n\n"
    md += f"_Сгенерировано: {report.get('generated_at', '')}_\n\n"

    # Навыки
    md += "## Навыки\n\n"
    for skill, items in report.get("skill_map", {}).items():
        md += f"### {skill.capitalize().replace("_", " ")}\n"
        for item in items:
            if isinstance(item, dict):
                md += f"- {item.get('name')} (Востребованность: {item.get('demand')}, Тренд: {item.get('trend')})\n"
            else:
                md += f"- {item}\n"
        md += "\n"

    # Зарплаты по грейдам и регионам
    md += "## Зарплаты\n\n"
    for grade, regions in report.get("salary_table", {}).items():
        md += f"### {grade}\n"
        for region, values in regions.items():
            unit = "USD" if region == "Remote USD" else "тыс. руб."
            md += f"- {region}: {values['min']} / {values['median']} / {values['max']} {unit}\n"
        md += "\n"

    # Рыночный тренд
    trend = report.get("market_trend", "")
    reason_trend = report.get("market_trend_reason", "")
    md += "## Рынок\n\n"
    md += f"**{trend.capitalize()}** - {reason_trend}\n\n"

    # Работодатели
    md += "## Работодатели, нанимающие на эту должность\n\n"
    employers = report.get("top_employers", [])
    if employers:
        for employer in employers:
            md += f"- {employer}\n"
    else:
        md += "Нет данных\n"
    md += "\n"

    # План обучения
    md += "## План обучения\n\n"
    for phase_key, phase in report.get("learning_path", {}).items():
        phase_name = phase.get('name', phase_key)
        md += f"### {phase_name}\n"

        # Темы
        topics = phase.get('topics', [])
        if topics:
            md += "- **Темы**:\n"
            for topic in topics:
                md += f"  - {topic}\n"
        else:
            md += "- **Темы**: нет\n"

        # Ресурсы
        resources = phase.get('resources', [])
        if resources:
            md += "- **Ресурсы**:\n"
            for res in resources:
                title = res.get('title') or res.get('name', 'Без названия')
                res_type = res.get('type', '')
                url = res.get('url', '')
                if url:
                    md += f"  - [{title}]({url}) ({res_type})\n"
                else:
                    md += f"  - {title} ({res_type})\n"
        else:
            md += "- **Ресурсы**: нет\n"

        # Ожидаемый результат после этапа
        md += f"- **Ожидаемый результат**: {phase.get('milestone', '')}\n\n"

    # Анализ пробелов
    gap = report.get("gap_analysis", {})
    md += "## GAP-анализ\n\n"

    # Быстро закрываемые пробелы
    quick_wins = gap.get('quick_wins', [])
    if quick_wins:
        md += "### Quick Wins (2-4 недели)\n"
        for qw in quick_wins:
            md += f"- {qw}\n"
        md += "\n"
    else:
        md += "### Quick Wins (2-4 недели): нет\n\n"

    # Долго закрываемые пробелы
    long_term = gap.get('long_term', [])
    if long_term:
        md += "### Long Term (3+ месяца)\n"
        for lt in long_term:
            md += f"- {lt}\n"
        md += "\n"
    else:
        md += "### Long Term (3+ месяца): нет\n\n"

    # Проект в портфолио
    proj = report.get("portfolio_project", {})
    md += "## Проект для портфолио\n\n"
    md += f"**Название**: {proj.get('name', '')}\n\n"
    md += f"**Описание**: {proj.get('description', '')}\n\n"

    # Используемые технологии
    skills = proj.get('skills_demonstrated', [])
    if skills:
        md += "**Демонстрируемые навыки**:\n"
        for skill in skills:
            md += f"- {skill}\n"
    else:
        md += "**Демонстрируемые навыки**: нет\n"
    md += "\n"

    md += "## Проверка отчета\n\n"

    # Оценка
    quality = report.get("quality_score", 0)
    md += f"- **Оценка качества**: {quality}/100\n"

    # Обоснование
    reason = report.get('reason_score', '')
    if reason:
        md += f"- **Обоснование**: {reason}\n"

    # Целостность
    is_consistent = report.get('is_consistent', False)
    md += f"- **Целостность**: {'Отчет целостный' if is_consistent else 'Отчет не целостный'}\n"

    # Предупреждения
    warnings = report.get("warnings", [])
    if warnings:
        md += "- **Предупреждения**:\n"
        for w in warnings:
            md += f"  - {w}\n"

    return md


def save_report(report, role, directory="reports"):
    logger = get_logger()
    os.makedirs(f"{directory}", exist_ok=True)  # Создаем директорию reports

    # Сохраняем JSON
    json_path = f"{directory}/report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    logger.info(f"Report: Отчет в формате JSON сохранен: {json_path}")

    # Сохраняем MD
    md_path = f"{directory}/report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(generate_markdown(report, role))
    logger.info(f"Report: Отчет в формате MD сохранен: {md_path}")
