class HELP(Exception):
    pass

class A(object):
    '''Класс для конвертации валюты'''
    # Forex 09.03.2020 23:58 GMT+03
    _coefs = {
        'euro_to_euro': 1,      # отсчет
        'euro_to_usd': 1.1443,  # сша
        'euro_to_gbp': 0.872,   # фунт
        'euro_to_chf': 1.0583,  # швейц. франк
        'euro_to_rub': 85.8631  # рубль
    }
    __possible_currencies = ['euro', 'usd', 'gbp', 'chf', 'rub']
    def __init__(self, value, currency=None):

        self.value = float(value)
        self.currency = currency
        if currency is not None:
            self.currency = currency.strip().lower()
            assert self.currency in self.__possible_currencies, f"Sorry, but you have to choose one of {self.__possible_currencies} "

    def __str__(self):
        if self.currency is None:
            return 'Currency not detected. Value {0}'.format(self.value, )
        else:
            return 'Currency is {1}. Value {0}'.format(self.value, self.currency.upper())

    def __repr__(self):
        return '{0}, {1}'.format(self.value, self.currency)

    def __add__(self, other):
        if isinstance(other, int):
            return A(self.value + other, self.currency)

        elif type(self) == type(other):
            assert self.currency is not None or other.currency is not None, 'Currencies not implemented'

            if self.currency is not None and other.currency is not None:
                return A(self.value + self.convert(other) * other.value, self.currency)

            elif other.currency is None:
                return A(self.value + other.value, self.currency)

            elif self.currency is None:
                return A(self.value + other.value, other.currency)

            else:
                raise HELP('HELP!!!')

    def __iadd__(self, other):
        return self.__add__(other)

    def convert(self, other):
        assert other.currency in self.__possible_currencies, f"Sorry, I know just {self.__possible_currencies}"
        if self.currency == other.currency:
            return 1
        else:
            return self._coefs[f'euro_to_{self.currency}'] / self._coefs[f'euro_to_{other.currency}']

    def send_to(self, to):
        assert to in self.__possible_currencies, f"Sorry, I know just {self.__possible_currencies}"
        self.value = self.value * self._coefs[f'euro_to_{to}'] / self._coefs[f'euro_to_{self.currency}']
        self.currency = to
