from fish import Fish, ListFish


class Pool:
    def __init__(self, square: float, max_density: float):
        self.square: float = square
        self.max_density: float = max_density

        self.fishes: ListFish | None = None

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
