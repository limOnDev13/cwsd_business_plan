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

    def _update_mass_indexes(self):
        """
        Метод для обновления значений массовых индексов. Массовый индекс показывает порядковый номер бассейна в
         зависимости от средней массы рыбы в данном бассейне.
        :return: Ничего.
        """
        # Создадим список средних масс в бассейнах
        average_masses: list[float] = list()

        for pool in self.pools:
            average_masses.append(pool.get_average_mass())

        # Отсортируем список средних масс по возрастанию, и, в зависимости от порядкового номера средней массы,
        # определим массовые индексы
        average_masses.sort()
        for index in range(self.number_pools):
            for pool in self.pools:
                if average_masses[index] == pool.get_average_mass():
                    pool.mass_index = index
                    break

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

        # Обновим массовые индексы
        self._update_mass_indexes()

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

        # Обновим массовые индексы
        self._update_mass_indexes()

        return sold_fish

    def _find_pool_with_mass_index(self, mass_index: int) -> Pool:
        """
        Метод для поиска бассейна с данным массовым индексом.
        :param mass_index: Массовый индекс искомого бассейна.
        :return: Искомый бассейн.
        """
        for pool in self.pools:
            if pool.mass_index == mass_index:
                return pool

    def separate_fish(self, pool: Pool) -> dict[Pool, float]:
        """
        Метод для разделения рыб в бассейне, в котором плотность посадки достигла предела, по соседним
         (по массовым индексам) бассейнам. Рыба не будет перемещаться в ПУСТЫЕ бассейны. Рыба будет перемещаться
          пакетами.
        :return: Словарь с информацией о перемещениий рыбы. Словарь будет иметь два значения - в какой бассейн
         переместилась быстрорастущая рыба, а в какой - медленнорастущая. В качестве ключа будет бассейн,
          в качестве значения - перемещенная биомасса. Словарь имеет вид:
           {next_pool: biomass_in_next_pool, previous_pool: biomass_in_previous_pool}
        """
        # Найдем соседние по массовым индексам бассейны. Они не должны быть пустыми.
        next_pool: Pool | None = None
        previous_pool: Pool | None = None
        current_mass_index: int = pool.mass_index
        next_mass_index: int = current_mass_index + 1
        previous_mass_index: int = current_mass_index - 1
        biomass_in_next_pool: float = 0.0
        biomass_in_previous_pool: float = 0.0

        # Ищем следующий бассейн. Все пустые бассейны будут иметь наименьший массовый индекс,
        # поэтому следующий бассейн (если текущий не крайний) не может быть пустым.
        if next_mass_index < self.number_pools:
            next_pool = self._find_pool_with_mass_index(next_mass_index)

        # Ищем предыдущий бассейн. Предыдущий может оказаться пустым, при этом все бассейны с меньшими массовыми
        # индексами также будут пустыми. Поэтому, если предыдущий бассейн окажется пустым, то искать далее
        # не имеет смысла.
        if previous_mass_index >= 0:
            previous_pool = self._find_pool_with_mass_index(previous_mass_index)
            if previous_pool.is_empty():
                previous_pool = None

        # В следующий бассейн (если таковой имеется) переместим быстрорастущую рыбу
        if next_pool is not None:
            fast_growing_fish: ListFish = pool.remove_fish(number_fish=self.package)
            biomass_in_next_pool: float = fast_growing_fish.get_biomass()
            next_pool.add_fish(fast_growing_fish)

        # В предыдущий бассейн (если таковой имеется) переместим медленнорастущую рыбу
        if previous_pool is not None:
            slow_growing_fish: ListFish = pool.remove_fish(number_fish=self.package)
            biomass_in_previous_pool: float = slow_growing_fish.get_biomass()
            previous_pool.add_fish(slow_growing_fish)

        # Вернем словарь с информацией о перемещениях
        return {next_pool: biomass_in_next_pool, previous_pool: biomass_in_previous_pool}
