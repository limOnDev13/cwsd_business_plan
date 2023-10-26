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
