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
