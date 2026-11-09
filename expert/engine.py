"""CLIPS-based inference engine. No Python fallback: real CLIPS rules decide."""
from pathlib import Path

import clips

RULES_PATH = Path(__file__).with_name("rules.clp")

PRODUCTS = {
    "web_app": {
        "title": "Веб-приложение",
        "subtitle": "Индивидуальная цифровая платформа",
        "description": "Подходит для проектов с личными кабинетами, доступом пользователей и специальными бизнес-процессами.",
        "features": ["Личные кабинеты", "Индивидуальная логика", "Масштабируемая архитектура"],
        "reason": "Вы указали, что пользователям нужны личные кабинеты. Поэтому приоритет получает веб-приложение, даже если проект также связан с продажами или презентацией компании.",
    },
    "online_store": {
        "title": "Интернет-магазин",
        "subtitle": "Продажи с оплатой на сайте",
        "description": "Подходит для онлайн-продаж с корзиной, оформлением заказа и интеграцией платёжного сервиса.",
        "features": ["Каталог товаров", "Корзина и заказы", "Онлайн-оплата"],
        "reason": "Вы планируете продавать товары и принимать оплату онлайн, при этом личные кабинеты не требуются.",
    },
    "catalog": {
        "title": "Сайт-каталог",
        "subtitle": "Витрина товаров без онлайн-оплаты",
        "description": "Позволяет показать ассортимент, характеристики и контакты для связи с менеджером.",
        "features": ["Каталог продукции", "Карточки товаров", "Заявки и контакты"],
        "reason": "Ваша цель — показать товары, но встроенная онлайн-оплата не требуется.",
    },
    "corporate": {
        "title": "Корпоративный сайт",
        "subtitle": "Профессиональное представление компании",
        "description": "Объединяет информацию о компании, услугах, кейсах, команде и контактах.",
        "features": ["Страницы услуг", "Портфолио и кейсы", "Форма обращения"],
        "reason": "Ваша основная задача — представить компанию и её услуги; отдельные кабинеты пользователей не нужны.",
    },
    "landing": {
        "title": "Лендинг",
        "subtitle": "Одна услуга — одно целевое действие",
        "description": "Одностраничный сайт для презентации предложения, рекламной кампании или сбора заявок.",
        "features": ["Чёткий оффер", "Форма заявки", "Адаптивная страница"],
        "reason": "Вам нужно продвигать одну услугу или предложение, без сложных функций личного кабинета.",
    },
}

VALID_VALUES = {
    "goal": {"products", "company", "campaign"},
    "payment": {"yes", "no"},
    "accounts": {"yes", "no"},
}

RULE_DESCRIPTIONS = {
    "R01": "ЕСЛИ нужны личные кабинеты, ТО веб-приложение.",
    "R02": "ЕСЛИ цель — продажа товаров И нужна оплата И нет кабинетов, ТО интернет-магазин.",
    "R03": "ЕСЛИ цель — продажа товаров И оплата не нужна И нет кабинетов, ТО сайт-каталог.",
    "R04": "ЕСЛИ цель — представить компанию И нет кабинетов, ТО корпоративный сайт.",
    "R05": "ЕСЛИ цель — продвинуть одну услугу И нет кабинетов, ТО лендинг.",
}


def evaluate(answers: dict) -> dict:
    """Validate inputs, run CLIPS and return recommendation with explanation."""
    if not isinstance(answers, dict):
        raise ValueError("Ожидается объект с ответами на вопросы.")
    if set(answers) != set(VALID_VALUES) or any(
        not isinstance(answers[key], str) or answers[key] not in values
        for key, values in VALID_VALUES.items()
    ):
        raise ValueError("Проверьте ответы: goal, payment и accounts обязательны.")

    # Separate environment for each request: safe, independent consultations.
    env = clips.Environment()
    env.load(str(RULES_PATH))
    template = env.find_template("request")
    template.assert_fact(**{key: clips.Symbol(answers[key]) for key in VALID_VALUES})
    fired = env.run()
    recommendations = [f for f in env.facts() if f.template.name == "recommendation"]
    if fired != 1 or len(recommendations) != 1:
        raise RuntimeError("Экспертная система не смогла выбрать единственную рекомендацию.")

    selected = recommendations[0]
    code = str(selected["code"])
    rule_id = str(selected["rule-id"])
    product = PRODUCTS[code]
    return {
        "code": code,
        **product,
        "rule_id": rule_id,
        "rule": RULE_DESCRIPTIONS[rule_id],
        "facts": answers.copy(),
        "rules_fired": fired,
        "disclaimer": "Учебная рекомендация. Окончательный выбор зависит от технического задания и консультации разработчика.",
    }
