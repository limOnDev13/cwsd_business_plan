from fish import Fish, ListFish


class Pool:
    def __init__(self, square: float, max_density: float, mass_index: int = 0):
        self.square: float = square
        self.max_density: float = max_density

        self.fishes: ListFish = ListFish([])
        self.mass_index: int = mass_index

    def add_fish(self, new_fish: Fish | ListFish):
        self.fishes += new_fish

    def remove_fish(self, number_fish: int, biggest_fish: bool = True) -> ListFish:
        """
        Метод для удаления самых больших или самых маленьких рыб.
        :param number_fish: Количество удаляемых рыб.
        :param biggest_fish: Если True, то удаляются самые больше, иначе - самые маленькие.
        :return: ListFish удаленных рыб
        """
        # Отсортируем список рыб. Если удалить нужно большие, то сортируем по возрастанию.
        self.fishes.sort(reverse=not biggest_fish)
        # Создадим список удаляемых рыб.
        removed_fish: list[Fish] = list()
        amount: int
        length: int = self.fishes.get_number_fish()

        # Если введенное число больше количества рыбы в бассейне, то удалим всю рыбу
        if number_fish > length:
            amount = length
        else:
            amount = number_fish
        # Так как массив отсортирован, удаляем необходимое количество раз последний элемент.
        for _ in range(amount):
            removed_fish.append(self.fishes.pop())

        return ListFish(removed_fish)

    def daily_growth(self) -> dict[str, float | bool]:
        """
        Метод, производящий разовое дневное выращивание рыбы в данном бассейне.
        :return: Словарь с информацией о затраченном корме, приросте биомассы и превышении плотности посадки.
        Словарь имеет вид {'mass_increase': ..., 'required_feed': ..., 'overflow': ...}
        """
        daily_result: dict[str, float] = self.fishes.daily_growth()

        density: float = self.fishes.get_biomass() / self.square
        overflow: bool = False
        if density >= self.max_density:
            overflow = True

        daily_result['overflow'] = overflow
        return daily_result

    def is_empty(self) -> bool:
        """
        Метод, который определяет, является бассейн пустым.
        :return: True, если бассейн пуст.
        """
        if self.fishes.get_number_fish() == 0:
            return True
        return False

    def get_biomass(self) -> float:
        """
        Метод для получения биомассы в бассейне.
        :return: биомасса.
        """
        return self.fishes.get_biomass()

    def get_density(self) -> float:
        """
        Метод для получения плотности посадки.
        :return: плотность посадки.
        """
        return self.fishes.get_biomass() / self.square

    def get_number_fish(self) -> int:
        """
        Метод для получения количества рыбы в бассейне.
        :return: количество рыбы в бассейне.
        """
        return self.fishes.get_number_fish()

    def get_average_mass(self) -> float:
        """
        Метод для получения средней массы в бассейне.
        :return: Средняя масса рыбы в бассейне.
        """
        return self.fishes.get_mass(average=True)
