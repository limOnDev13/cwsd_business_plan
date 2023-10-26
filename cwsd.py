from fish import Fish, ListFish
from pool import Pool


class CWSD:
    def __init__(self, number_pools: int, square: float, max_density: float, commercial_fish_mass: float, package: int):
        self.number_pools: int = number_pools
        self.pools: list[Pool] = []
        for _ in range(number_pools):
            self.pools.append(Pool(square=square, max_density=max_density))

        self.commercial_fish_mass: float = commercial_fish_mass
        self.package: int = package

    def add_fish(self, new_fish: ListFish) -> bool:
        """
        Метод для добавления новой рыбы в ПУСТОЙ бассейн.
        :param new_fish: Список новой рыбы.
        :return: True, если был пустой бассейн и в него добавилась рыба, иначе - False.
        """
        # Найдем пустой бассейн
        fish_were_added: bool = False

        for pool in self.pools:
            if pool.is_empty():
                pool.add_fish(new_fish)
                fish_were_added = True
                break

        return fish_were_added

    def sell_fish(self) -> ListFish:
        """
        Метод для продажи товарной рыбы пакетами.
        :return: Список проданных рыб.
        """
        sold_fish: ListFish = ListFish([])

        # Пройдемся по каждому бассейну и посчитаем количество товарной рыбы.
        # В каждом бассейне такое количество должно быть не меньше размера пакета.
        for pool in self.pools:
            number_commercial_fish: int = pool.fishes.get_number_of_grown_fish(min_mass=self.commercial_fish_mass)
            if number_commercial_fish >= self.package:
                sold_fish += pool.remove_fish(number_fish=number_commercial_fish)

        return sold_fish
