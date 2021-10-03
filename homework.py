import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = date
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.week_ago = self.today - dt.timedelta(days=7)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = []
        for record in self.records:
            if record.date == self.today:
                today_stats.append(record.amount)
        return sum(today_stats)

    def get_week_stats(self):
        week_stats = []
        for record in self.records:
            if self.week_ago <= record.date <= self.today:
                week_stats.append(record.amount)
        return sum(week_stats)

    def get_cash_limit(self):
        balance = self.limit - self.get_today_stats()
        return balance


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_remained = self.get_cash_limit()
        if calories_remained > 0:
            message = (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                       f'калорийностью не более {calories_remained} кКал')
        else:
            message = 'Хватит есть!'
        return message


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency='rub'):
        currencies = {'usd': ('USD', self.USD_RATE),
                      'eur': ('Euro', self.EURO_RATE),
                      'rub': ('руб', self.RUB_RATE)}
        cash_remained = self.get_cash_limit()
        if currency not in currencies:
            return f'Валюта {currency} отсуствует'
        if cash_remained == 0:
            return 'Денег нет, держись'
        name, valyuta = currencies[currency]
        cash_remained = round(cash_remained / valyuta, 2)
        if cash_remained > 0:
            message = f'На сегодня осталось {cash_remained} {name}'
        else:
            cash_remained = abs(cash_remained)
            message = (f'Денег нет, держись: твой долг - {cash_remained} '
                       f'{name}')
        return message


cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('rub'))
