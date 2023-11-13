from fish import Fish, ListFish, create_list_fish
from pool import Pool
from copy import deepcopy


class CWSD:
    def __init__(self, number_pools: int, square: float, max_density: float, commercial_fish_mass: float, package: int):
        self.number_pools: int = number_pools
        self.max_density: float = max_density
        self.pools: list[Pool] = []
        for _ in range(number_pools):
            self.pools.append(Pool(square=square))

        self.commercial_fish_mass: float = commercial_fish_mass
        self.package: int = package
        self.square: float = square

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

    def sell_fish(self) -> float:
        """
        Метод для продажи товарной рыбы пакетами.
        :return: Биомасса проданной рыбы.
        """
        sold_fish: ListFish = ListFish([])

        # Пройдемся по каждому бассейну и посчитаем количество товарной рыбы.
        # В каждом бассейне такое количество должно быть не меньше размера пакета.
        for pool in self.pools:
            number_commercial_fish: int = pool.fishes.get_number_of_grown_fish(min_mass=self.commercial_fish_mass)
            if (number_commercial_fish >= self.package) or (number_commercial_fish == pool.get_number_fish()):
                sold_fish += pool.remove_fish(number_fish=number_commercial_fish)

        # Обновим массовые индексы
        self._update_mass_indexes()

        return sold_fish.get_biomass()

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

        # Обновим массовые индексы
        self._update_mass_indexes()
        # Вернем словарь с информацией о перемещениях
        return {next_pool: biomass_in_next_pool, previous_pool: biomass_in_previous_pool}

    def daily_growth(self) -> dict[str, float] | None:
        """
        Метод для разового однодневного выращивания рыбы во всем УЗВ.
        :return: Словарь с информацией о приросте биомассы, затраченном корме и массе проданной рыбы. Если плотность
         посадки во всем УЗВ достигла предела, то это означает, что зарыбление было ошибочным, и вернем None.
          Словарь имеет вид {'mass_increase': ..., 'required_feed': ..., 'sold_biomass': ...}
        """
        daily_cwsd_result: dict[str, float] = {'mass_increase': 0.0, 'required_feed': 0.0, 'sold_biomass': 0.0}

        # Проведем ежедневное выращивание рыбы в каждом бассейне
        for pool in self.pools:
            daily_pool_result: dict[str, float] = pool.daily_growth()
            daily_cwsd_result['mass_increase'] += daily_pool_result['mass_increase']
            daily_cwsd_result['required_feed'] += daily_pool_result['required_feed']

        # Если есть достаточно товарной рыбы - продадим ее
        daily_cwsd_result['sold_biomass'] = self.sell_fish()

        # Если плотность посадки во всех не пустых бассейнах достигла предела, то это ошибка и вернем None
        total_biomass: float = 0.0
        total_square: float = 0.0
        for pool in self.pools:
            if not pool.is_empty():
                total_biomass += pool.get_biomass()
                total_square += pool.square
        if (total_biomass != 0.0) and (total_biomass / total_square >= self.max_density):
            return None

        # Если в каком-нибудь бассейне превышена плотность посадки, то распределим рыбу
        for pool in self.pools:
            if pool.get_density() > self.max_density:
                self.separate_fish(pool)

        # Обновим массовые индексы и вернем словарь с результатами
        self._update_mass_indexes()
        return daily_cwsd_result

    def has_empty_pool(self) -> bool:
        """
        Метод, который проверяет, есть пустые бассейны в УЗВ
        :return: True, если есть, иначе - False
        """
        for pool in self.pools:
            if pool.is_empty():
                return True
        return False

    def get_biomass(self):
        """
        Метод для получения биомассы во всем УЗВ
        :return: Биомассу в УЗВ
        """
        total_biomass: float = 0.0

        for pool in self.pools:
            total_biomass += pool.get_biomass()

        return total_biomass

    def get_densities(self) -> list[float]:
        """
        Метод для получения плотностей посадки в каждом бассейне.
        :return: Список плотностей посадки в каждом бассейне.
        """
        densities: list[float] = list()

        for pool in self.pools:
            densities.append(pool.get_density())

        return densities

    def get_mass_indexes(self):
        """
        Метод для получения и отслеживания правильного распределения массовых индексов.
        :return: Список списков, в которые содержат массовый индекс и среднюю массу рыбы.
        """
        mass_indexes: list[list[int | float]] = list()

        for pool in self.pools:
            mass_indexes.append([pool.mass_index, pool.get_average_mass()])

        return mass_indexes

    def is_empty(self) -> bool:
        """
        Метод, который проверяет, не опустело ли УЗВ
        :return: True, если УЗВ стало пустым. Иначе - False.
        """
        for pool in self.pools:
            if not pool.is_empty():
                return False
        return True

    def get_total_density(self) -> float:
        """
        Метод для получения плотности посадки для всего УЗВ.
        :return: Общую плотность посадки.
        """
        biomass: float = self.get_biomass()
        return biomass / (float(self.number_pools) * self.square)
