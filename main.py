# AS Обшие замечания
# не расставлены пустые строки по pep8 (исправлено автоматически)
# нет пробелов вокруг операций по pep8 (исправлено автоматически)

import datetime as dt
# AS Неиспользуемый импорт
import json


class Record:
    # AS для "пустого значения лучше использовать None а не ''
    # def __init__(self, amount, comment, date=None):
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = dt.datetime.now().date() if not date else dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # AS переменная должна называться с маленькой буквы.
        # тем более что уже есть "class Record"
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # AS в данном случае правильнее использовать
                # AS today_stats += Record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # AS в данном случае правильнее использовать
            # AS цепочку сравнений
            # AS if 0 <= (today - record.date).days < 7:
            if (today - record.date).days < 7 and (today - record.date).days >= 0:
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # AS комментарии к функции должны указываться в виде Docstrings
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    # AS комментарии не должны использоваться
    # AS можно сразу использовать константу float а не приводить тип
    # АЫ хотя возможно компилятор умный и поймет это "как надо"
    USD_RATE = float(60)  # Курс доллар США.
    # AS комментарии не должны использоваться
    # AS можно сразу использовать константу float а не приводить тип
    # AS хотя возможно компилятор умный и поймет это "как надо"
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency, USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # AS бесполезная строка, непонятно что она тут делает (и что должна делать по замыслу)
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return f'На сегодня осталось {round(cash_remained, 2)} {currency_type}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # AS лишний elif, в этой точке
        elif cash_remained < 0:
            return 'Денег нет, держись: твой долг - {0:.2f} {1}'.format(-cash_remained, currency_type)

    # AS ненужная функция. не делает ничего, только теряет результат
    def get_week_stats(self):
        super().get_week_stats()
