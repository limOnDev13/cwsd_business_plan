import random


class Fish:
    """
    Класс для хранения информации о каждой рыбке
    """

    @staticmethod
    def _calculate_random_mac() -> float:
        """
        Расчет случайного значения коэффициента массонакопления
        по нормальному распределению.
        :return: Коэффициент массонакопления (mass accumulation coefficient)
        """
        min_mass_accumulation: float = 0.07
        max_mass_accumulation: float = 0.087

        medium: float = (max_mass_accumulation + min_mass_accumulation) / 2
        # Стандартное отклонение возьмем из расчета, что 68% выпадает
        # на вторую треть промежутка между min_mass_accumulation
        # и max_mass_accumulation
        standard_deviation: float = \
            ((max_mass_accumulation - min_mass_accumulation) / 3) / 2

        mass_accumulation_coefficient: float = random.gauss(medium,
                                                            standard_deviation)
        return mass_accumulation_coefficient

    def __init__(self, start_mass: float, feed_ratio: float = 1.5):
        self.mass: float = start_mass  # текущая масса
        self.feed_ratio: float = feed_ratio  # кормовой коэффициент
        self._mac: float = self._calculate_random_mac()  # коэффициент массонакопления

    def daily_growth(self) -> dict[str, float]:
        """
        Метод для расчета суточного выращивания данной рыбы.
        :return: Возвращает словарь с информацией об абсолютном значении прироста
        и затраченного корма.
        Словарь имеет вид {'mass_increase': ...,
        'required_feed': ...}
        """
        # Масса в начале суток
        previous_mass: float = self.mass
        # Масса в конце суток
        next_mass: float = \
            (previous_mass ** (1 / 3) + self._mac / 3) ** 3
        # Относительный суточный прирост
        relative_daily_increase: float =\
            (next_mass - previous_mass) * 100 / previous_mass
        # Абсолютный суточный прирост
        mass_increase: float = next_mass - previous_mass
        # Норма кормления
        feeding_rate: float = relative_daily_increase * self.feed_ratio
        # масса затраченного корма
        required_feed: float = previous_mass * feeding_rate / 100

        self.mass = next_mass

        return {'mass_increase': mass_increase,
                'required_feed': required_feed}

    def print(self):
        """
        Метод для печати массы рыбки.
        :return: Ничего
        """
        print(f'Масса рыбки: {self.mass}')


class ListFish:
    """
    Класс для работы со списком объектов Fish
    """
    def __init__(self, list_fish: list[Fish]):
        self.list_fish: list[Fish] = list_fish

    def __add__(self, other):
        """
        Метод для операнда self + other (Fish | ListFish)
        :param other: Правый операнд
        :return: Результат сложения двух списков.
        """
        if isinstance(other, ListFish):
            return ListFish(self.list_fish + other.list_fish)
        elif isinstance(other, Fish):
            return ListFish(self.list_fish + [other])
        else:
            raise ArithmeticError('Правый операнд должен быть либо ListFish, либо Fish')

    def __iadd__(self, other):
        """
        Метод для операнда self += other (Fish | ListFish)
        :param other: Правый операнд
        :return: Результат итерации.
        """
        if isinstance(other, ListFish):
            self.list_fish += other
            return self
        elif isinstance(other, Fish):
            self.list_fish.append(other)
            return self
        else:
            raise ArithmeticError('Правый операнд должен быть либо ListFish, либо Fish')

    def sort(self, reverse: bool = False):
        self.list_fish.sort(key=lambda fish: fish.mass, reverse=reverse)

    def pop(self) -> Fish:
        return self.list_fish.pop()

    def get_biomass(self) -> float:
        """
        Метод для расчета биомассы списка рыб.
        :return: Биомасса списка рыб
        """
        biomass: float = 0.0
        for fish in self.list_fish:
            biomass += fish.mass
        return biomass / 1000.0

    def get_number_fish(self) -> int:
        """
        Метод для получения количества рыб в списке.
        :return: Количество рыб в списке
        """
        return len(self.list_fish)

    def get_mass(self, min: bool = False, max: bool = False, average: bool = False) -> float:
        """
        Метод для получения минимальной, максимальной и средней массы.
        :param min: Вывести минимум.
        :param max: Вывести максимум.
        :param average: Вывести среднюю.
        :return: Минимальная или максимальная, или средняя масса.
        """
        self.list_fish.sort(key=lambda fish: fish.mass)
        if min:
            return self.list_fish[0].mass
        elif max:
            return self.list_fish[-1].mass
        elif average:
            mass: float = 0.0
            for fish in self.list_fish:
                mass += fish.mass
            return mass / len(self.list_fish)


def create_list_fish(number_fish: int, mass: float) -> ListFish:
    fishes: list[Fish] = [Fish(mass) for _ in range(number_fish)]
    return ListFish(fishes)
