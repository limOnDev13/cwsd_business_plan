from cwsd import CWSD
from copy import deepcopy
from fish import create_list_fish
from random import randint
import os.path


class Optimization:
    @staticmethod
    def calculate_optimal_number_new_fish_in_empty_pool(cwsd: CWSD, mass: float,
                                                        start_number: int, step_number: int, end_number: int,
                                                        attempts: int = 10, error_rate: float = 90.0,
                                                        print_info: bool = False) -> int:
        """
        Метод для расчета оптимального количества новой рыбы для добавления в существующий УЗВ. УЗВ должен иметь пустой
         бассейн. Расчет будет вестись для добавления только в этот пустой бассейн. Если в УЗВ есть не один пустой
          бассейн, то необходимо повторно вызывать данный метод.
        :param cwsd: Существующее УЗВ с пустым бассейном.
        :param mass: Масса добавляемой рыбы.
        :param start_number: Начальное количество рыбы.
        :param step_number: Шаг вариации количества.
        :param end_number: Конечное количество рыбы.
        :param attempts: Количество проверок.
        :param error_rate: Погрешность вычислений в процентах. Результат будет выводиться, если количество успешных
         проверок попадет в указанную погрешность.
        :param print_info: Если True, то метод будет писать о процессе выполнения рыботы.
        :return: Оптимально количество.
        """
        number: int = start_number
        result_number: int = number

        # Проварьируем количество новой рыбы
        while number <= end_number:
            successful_attempts: int = 0
            if print_info:
                print(f'Тестируемое количество: {number}')
            # Для точности проведем несколько проверок
            for attempt in range(attempts):
                test_cwsd: CWSD = deepcopy(cwsd)

                test_cwsd.add_fish(create_list_fish(number_fish=number,
                                                    mass=mass))
                # Будем производить ежедневное выращивание, пока УЗВ не опустеет (придумать более короткую проверку)
                success: bool = True
                while test_cwsd.get_biomass() > 1.0:
                    daily_result: dict[str | float] | None = test_cwsd.daily_growth()
                    if daily_result is None:
                        success = False
                        break
                if success:
                    if print_info:
                        print(f'{attempt} попытка из {attempts} - Успешно!')
                    successful_attempts += 1
                else:
                    if print_info:
                        print(f'{attempt} попытка из {attempts} - Провал!')

            if successful_attempts * 100 / attempts >= error_rate:
                if print_info:
                    print(f'{successful_attempts} успешных попыток из {attempts}')
                result_number = number
                number += step_number
            else:
                break

        return result_number

    @staticmethod
    def calculate_new_fish_mass(cwsd: CWSD, masses: list[float], delta_mass: float) -> float:
        """
        Метод, который рассчитывает массу новых мальков в пустой бассейн.
        :param cwsd: Работающее УЗВ.
        :param masses: Список масс, которые можно зарыблить в пустой бассейн.
        :param delta_mass: Половина длины промежутка, в котором не должно быть средних масс. Это будет критерием
         определения необходимой массы новой рыбы.
        :return: Массу из списка масс.
        """
        average_masses: list[float] = list()
        for pool in cwsd.pools:
            average_masses.append(pool.get_average_mass())
        average_masses.sort(reverse=True)
        masses.sort(reverse=True)

        for i in range(len(average_masses) - 1):
            for mass in masses:
                if (average_masses[i] <= mass + delta_mass) and (mass - delta_mass < average_masses[i + 1]):
                    return mass

        return masses[0]


class BusinessPlan:
    def __init__(self, prices: list[list[float | int]], fish_price: float, feed_price: float, price_per_kg: bool):
        """
        Метод __init__
        :param prices: Список списков с массой и ценой зарыбляемой рыбы. Сначала идет масса, после - цена.
         Списки расположены по возрастанию масс.
        :param fish_price: Цена товарной рыбы за 1 кг.
        :param feed_price: Цена за 1 кг корма.
        """
        self.prices: list[list[float | int]] = prices
        self.fish_price: float = fish_price
        self.feed_price: float = feed_price
        self.price_per_kg: bool = price_per_kg

    def calculate_daily_income(self, daily_result: dict[str, float]) -> float:
        """
        Метод для расчета ежедневных доходов.
        :param daily_result: Словарь с дневным результатом работы УЗВ.
        :return: Дневную прибыль.
        """
        daily_income: float = daily_result['sold_biomass'] * self.fish_price
        return daily_income

    def calculate_daily_expenses(self, daily_result: dict[str, float]) -> float:
        """
        Метод для расчета ежедневных затрат.
        :param daily_result: Словарь с дневным результатом работы УЗВ.
        :return: Дневные затраты.
        """
        daily_expenses: float = daily_result['required_feed'] * self.feed_price / 1000
        return daily_expenses

    def calculate_cost_fry(self, numbers_fish: list[int]) -> float:
        """
        Метод для расчета затрат на малька.
        :param numbers_fish: Список количеств рыб. Их порядок соответствует порядку расположения масс в поле self.prices.
        :param price_per_kg: Если True, то цена указана за килограмм. Иначе - за штуку.
        :return: Затраты на малька.
        """
        result_expenses: float = 0.0
        for i in range(len(self.prices)):
            if self.price_per_kg:
                result_expenses += float(numbers_fish[i]) * self.prices[i][0] * self.prices[i][1] / 1000
            else:
                result_expenses += float(numbers_fish[i]) * self.prices[i][1]
        return result_expenses

    def daily_growth(self, cwsd: CWSD, print_info: bool = False) -> dict[str, float] | None:
        """
        Метод, который производит разовое дневное выращивание.
        :param cwsd: Действующее УЗВ.
        :param print_info: Если True, то метод будет сообщать о переполнении.
        :return: Словарь с необходимой информацией. Словарь имеет вид {'mass_increase': ..., 'required_feed': ...,
         'sold_biomass': ..., 'income': ..., 'expenses': ...}
        """
        daily_result: dict[str, float] | None = cwsd.daily_growth()

        if daily_result is None:
            if print_info:
                print('Переполнение УЗВ!!!!')
            return None
        else:
            daily_result['income'] = self.calculate_daily_income(daily_result)
            daily_result['expenses'] = self.calculate_daily_expenses(daily_result)
            return daily_result

    def calculate_profit(self, cwsd: CWSD, days: int, initial_capital: float, cost_fry: float,
                         delta_mass: float | None = None, step_number: int | None = None, end_number: int | None = None,
                         print_info: bool = False) -> dict[str, float | dict[int, float]] | None:
        """
        Метод для расчета прибыли с УЗВ.
        :param cwsd: Действующее УЗВ.
        :param days: Количество дней, которое УЗВ должно отработать. Если days == 0, то метод будет считать,
         пока УЗВ не опустеет.
        :param initial_capital: Стартовый капитал на момент запуска.
        :param cost_fry: Стоимость мальков.
        :param delta_mass: Минимальная длина промежутка между средней массой и массой новой рыбы.
        :param step_number: Шаг для перебора значений количества новой рыбы.
        :param end_number: Верхняя граница значений количества новой рыбы.
        :param price_per_kg: True, если цена за кг. False, если цена за шт.
        :param print_info: Если True, то будет писать о переполнении.
        :return: Словарь с необходимой информацией. Словарь имеет вид {'sold_biomass': ..., 'spent_feed_mass': ...,
        'income': ..., 'expenses': ..., 'profit': ..., 'budget': ...}
        """
        sold_biomass: float = 0.0
        spent_feed_mass: float = 0.0
        income: float = 0.0
        expenses: float = 0.0
        profit: float = 0.0
        budget: dict[int, float] = {0: initial_capital}
        result_info: dict[str, float | dict[int, float]] = dict()
        day: int = 0

        if days == 0:
            while not cwsd.is_empty():
                day += 1
                daily_result: dict[str, float] | None = self.daily_growth(cwsd, print_info)
                if daily_result is None:
                    return None
                sold_biomass += daily_result['sold_biomass']
                spent_feed_mass += daily_result['required_feed']
                income += daily_result['income']
                expenses += daily_result['expenses']
                profit = income - expenses
                budget[day] = budget[day - 1] + daily_result['income'] - daily_result['expenses']
        else:
            opt: Optimization = Optimization()
            bought_fish: list[int] = [0 for _ in range(len(self.prices))]
            while day < days:
                if cwsd.has_empty_pool():
                    new_fish_mass: float = opt.calculate_new_fish_mass(
                        cwsd=cwsd,
                        masses=sorted([self.prices[i][0] for i in range(len(self.prices))], reverse=True),
                        delta_mass=delta_mass
                    )
                    number_new_fish: int = opt.calculate_optimal_number_new_fish_in_empty_pool(
                        cwsd=cwsd,
                        mass=new_fish_mass,
                        start_number=0,
                        step_number=step_number,
                        end_number=end_number
                    )
                    for i in range(len(self.prices)):
                        if self.prices[i][0] == new_fish_mass:
                            bought_fish[i] += number_new_fish
                    cwsd.add_fish(create_list_fish(number_new_fish, new_fish_mass))

                daily_result: dict[str, float] | None = self.daily_growth(cwsd, print_info)
                if daily_result is None:
                    return None
                print(f'День {day}')
                day += 1
                sold_biomass += daily_result['sold_biomass']
                spent_feed_mass += daily_result['required_feed']
                income += daily_result['income']
                expenses += daily_result['expenses']
                budget[day] = budget[day - 1] + daily_result['income'] - daily_result['expenses']
            expenses += self.calculate_cost_fry(bought_fish)
            profit = income - expenses

        result_info['sold_biomass'] = sold_biomass
        result_info['spent_feed_mass'] = spent_feed_mass
        result_info['income'] = income
        result_info['expenses'] = expenses
        result_info['profit'] = profit - cost_fry
        result_info['budget'] = budget

        return result_info

    @staticmethod
    def _calculate_number_possible_vectors(min_limits: list[int] | int, max_limits: list[int] | int,
                                           number_pools: int) -> int:
        if isinstance(min_limits, int) and isinstance(max_limits, int):
            return (max_limits - min_limits + 1) ** number_pools
        elif not isinstance(min_limits, int) and isinstance(max_limits, int):
            result: int = 1
            for i in range(len(min_limits)):
                result *= (max_limits - min_limits[i] + 1)
            return result
        elif isinstance(min_limits, int) and not isinstance(max_limits, int):
            result: int = 1
            for i in range(len(max_limits)):
                result *= (max_limits[i] - min_limits + 1)
            return result
        else:
            result: int = 1
            for i in range(len(min_limits)):
                result *= (max_limits[i] - min_limits[i] + 1)
            return result

    @staticmethod
    def _random_values(min_limits: list[int] | int, max_limits: list[int] | int, step: int) -> list[int]:
        result_vector: list[int] = list()

        for i in range(len(min_limits)):
            min_value: int
            max_value: int

            if isinstance(min_limits, int):
                min_value = min_limits
            else:
                min_value = min_limits[i]
            if isinstance(max_limits, int):
                max_value = max_limits
            else:
                max_value = max_limits[i]
            result_vector.append(randint(min_value, max_value) * step)

        return result_vector

    def calculate_profitable_first_stocking(self, number_pools: int, square: float, max_density: float,
                                            commercial_fish_mass: float, package: int,
                                            min_limits: list[int] | int, max_limits: list[int] | int,
                                            number_vectors: int, step: int, attempts: int, print_info: bool = False
                                            ) -> list[list[int]]:
        """
        Метод для решения оптимизации первого зарыбления. Пока метод создает рандомные вектора
         (координаты - количества зарыбляемой рыбы) и рассчитывает прибыль данного зарыбления. Для каждого вектора будет
          проводиться несколько попыток, так как каждый раз будет зарыбляться рыба со случайным коэффициентом
           массонакопления. Из этих попыток будет браться наихудший сценарий (с наименьшей прибылью). Из всех векторов
            выбираться будет с наибольшей прибылью.
        :param number_pools: Количество бассейнов. Чем больше бассейнов, тем больше необходимо векторов, тем намного
         дольше будет производиться расчет.
        :param square: Площадь бассейна.
        :param max_density: Максимальная плотность посадки.
        :param commercial_fish_mass: Масса товарной рыбы.
        :param package: Минимальный размер пакета.
        :param vector_min_value: Минимальное значение координаты вектора, деленное на step.
        :param max_limits: Границы количеств для каждой масс. Если передан список, то границы устанавливаются для каждой
         массы отдельно. Если передано int, то для всех устанавливается одинаковая граница.
        :param min_limits: Минимальные границы.
        :param number_vectors: Количество успешных векторов. Если передано число, большее чем 50% от количества
         возможных векторов, то будет вестись расчет для 20%.
        :param step: Шаг изменения координаты вектора.
        :param attempts: Количество попыток (тестов) для каждого вектора. Не стоит брать слишком много.
        :param print_info: Если True, то будет писаться подробная информация о процессе работы.
        :return: Список списков масс рыб и их количества.
        """
        # Результатом работы метода будет список количеств, они расположены в соответствии.
        stockings: set[tuple[int]] = set()
        result_stocking: list[int] = list()
        tested_vectors: list[list[int]] = list()
        total_profit: float = 0.0

        for vector_number in range(number_vectors):
            if print_info:
                print(f'\nПроисходит тестирование № {vector_number} из {number_vectors}\n')
            new_vector_is_needed: bool = True
            while new_vector_is_needed:
                # 1) Создадим случайный вектор
                stocking: list[int] = self._random_values(min_limits, max_limits, step)
                # 2) Если созданный вектор уже тестировался, то пропустим итерацию
                if tuple(stocking) in stockings:
                    continue
                else:
                    stockings.add(tuple(stocking))
                if print_info:
                    print(f'Тестируем вектор {stocking}')
                # 3) Проведем несколько попыток для точности
                min_profit_one_test: float = 99999999.9
                for attempt in range(attempts):
                    # 4) Создадим тестовое УЗВ и добавим в него рыбу в количествах в соответствии с созданным вектором
                    if print_info:
                        print(f'Происходит попытка {attempt} из {attempts}')
                    cwsd: CWSD = CWSD(number_pools, square, max_density, commercial_fish_mass, package)
                    for i in range(len(self.prices)):
                        cwsd.add_fish(create_list_fish(number_fish=stocking[i],
                                                       mass=self.prices[i][0]))
                    cost_fry: float = self.calculate_cost_fry(numbers_fish=stocking)
                    print(f'Затрачено на мальков: {cost_fry}')
                    # 5) Получим результат выращивания. Будем оценивать по достижению продажи полного объемы рыбы
                    result_info: dict[str, float | dict[int, float]] | None = self.calculate_profit(
                        cwsd=cwsd,
                        days=0,
                        initial_capital=0,
                        cost_fry=cost_fry
                    )
                    # 6.1) Если произошло переполнение, то прекращаем расчет и тестируем новый вектор
                    if result_info is None:
                        new_vector_is_needed = True
                        break
                    # 6.2) Если выращивание прошло успешно, то зафиксируем минимальную прибыль из всех попыток
                    # для данного вектора
                    if result_info['profit'] < min_profit_one_test:
                        min_profit_one_test = result_info['profit']
                        new_vector_is_needed = False
                # 7) Если ни в одной попытке не было переполнения, то сохраняем результат
                if not new_vector_is_needed:
                    if min_profit_one_test > total_profit:
                        total_profit = min_profit_one_test
                        result_stocking = list(stocking)
                    if print_info:
                        print(f'Прибыль в худшем варианте: {min_profit_one_test}.\n'
                              f'На данный момент лучший вектор {result_stocking} с прибылью {total_profit}')
                    stocking.append(int(min_profit_one_test))
                    tested_vectors.append(stocking)

        return tested_vectors

    def calculate_profitable_first_stocking_with_long_term_cultivation(
            self, number_pools: int, square: float, max_density: float, commercial_fish_mass: float, package: int,
            min_limits: list[int] | int, max_limits: list[int] | int, number_vectors: int, step: int, attempts: int,
            days: int, print_info: bool = False
    ) -> list[list[int]]:
        """
        Метод для решения оптимизации первого зарыбления. Пока метод создает рандомные вектора
         (координаты - количества зарыбляемой рыбы) и рассчитывает прибыль данного зарыбления. Для каждого вектора будет
          проводиться несколько попыток, так как каждый раз будет зарыбляться рыба со случайным коэффициентом
           массонакопления. Из этих попыток будет браться наихудший сценарий (с наименьшей прибылью). Из всех векторов
            выбираться будет с наибольшей прибылью.
        :param number_pools: Количество бассейнов. Чем больше бассейнов, тем больше необходимо векторов, тем намного
         дольше будет производиться расчет.
        :param square: Площадь бассейна.
        :param max_density: Максимальная плотность посадки.
        :param commercial_fish_mass: Масса товарной рыбы.
        :param package: Минимальный размер пакета.
        :param max_limits: Границы количеств для каждой масс. Если передан список, то границы устанавливаются для каждой
         массы отдельно. Если передано int, то для всех устанавливается одинаковая граница.
        :param min_limits: Минимальные границы.
        :param number_vectors: Количество успешных векторов. Если передано число, большее чем 50% от количества
         возможных векторов, то будет вестись расчет для 20%.
        :param step: Шаг изменения координаты вектора.
        :param attempts: Количество попыток (тестов) для каждого вектора. Не стоит брать слишком много.
        :param days: Количество дней выращивания.
        :param print_info: Если True, то будет писаться подробная информация о процессе работы.
        :return: Список списков масс рыб и их количества.
        """
        # Результатом работы метода будет список количеств, они расположены в соответствии.
        stockings: set[tuple[int]] = set()
        result_stocking: list[int] = list()
        tested_vectors: list[list[int]] = list()
        total_profit: float = 0.0

        for vector_number in range(number_vectors):
            if print_info:
                print(f'\nПроисходит тестирование № {vector_number} из {number_vectors}\n')
            new_vector_is_needed: bool = True
            while new_vector_is_needed:
                # 1) Создадим случайный вектор
                stocking: list[int] = self._random_values(min_limits, max_limits, step)
                # 2) Если созданный вектор уже тестировался, то пропустим итерацию
                if tuple(stocking) in stockings:
                    continue
                else:
                    stockings.add(tuple(stocking))
                if print_info:
                    print(f'Тестируем вектор {stocking}')
                # 3) Проведем несколько попыток для точности
                min_profit_one_test: float = 999999999.9
                for attempt in range(attempts):
                    # 4) Создадим тестовое УЗВ и добавим в него рыбу в количествах в соответствии с созданным вектором
                    if print_info:
                        print(f'Происходит попытка {attempt} из {attempts}')
                    cwsd: CWSD = CWSD(number_pools, square, max_density, commercial_fish_mass, package)
                    for i in range(len(self.prices)):
                        cwsd.add_fish(create_list_fish(number_fish=stocking[i],
                                                       mass=self.prices[i][0]))
                    cost_fry: float = self.calculate_cost_fry(numbers_fish=stocking)
                    # 5) Получим результат выращивания. Будем оценивать по достижению продажи полного объемы рыбы
                    result_info: dict[str, float | dict[int, float]] | None = self.calculate_profit(
                        cwsd=cwsd,
                        days=days,
                        initial_capital=0,
                        cost_fry=cost_fry,
                        delta_mass=20.0,
                        step_number=50,
                        end_number=10000
                    )
                    # 6.1) Если произошло переполнение, то прекращаем расчет и тестируем новый вектор
                    if result_info is None:
                        new_vector_is_needed = True
                        break
                    # 6.2) Если выращивание прошло успешно, то зафиксируем минимальную прибыль из всех попыток
                    # для данного вектора
                    if result_info['profit'] < min_profit_one_test:
                        min_profit_one_test = result_info['profit']
                        new_vector_is_needed = False
                # 7) Если ни в одной попытке не было переполнения, то сохраняем результат
                if not new_vector_is_needed:
                    if min_profit_one_test > total_profit:
                        total_profit = min_profit_one_test
                        result_stocking = list(stocking)
                    if print_info:
                        print(f'Прибыль в худшем варианте: {min_profit_one_test}.\n'
                              f'На данный момент лучший вектор {result_stocking} с прибылью {total_profit}')
                    stocking.append(int(min_profit_one_test))
                    tested_vectors.append(stocking)

        return tested_vectors

    @staticmethod
    def save_best_random_vectors(set_vectors: list[list[int]], file_name: str | None = None):
        """
        Метод будет проводить тестирования на случайных векторах, после сохранять успешные векторы в файлы.
        :param set_vectors: Набор успешных векторов.
        :param file_name: Если str, то сохранит набор векторов в файл с указанным именем.
        :return: Ничего
        """
        file_path: str = 'E:/vovasProgram/cwsd_business_plan/set_of_vectors/'
        if file_name is None:
            file_number: int = 0
            file_path += f'{file_number}.txt'

            while os.path.isfile(file_path):
                file_number += 1
                file_path: str = f'E:/vovasProgram/cwsd_business_plan/set_of_vectors/{file_number}.txt'
        else:
            file_path += f'{file_name}.txt'

        new_file = open(file_path, 'w')
        for vector in set_vectors:
            str_vector: list[str] = [str(i) + ' ' for i in vector]
            new_file.writelines(str_vector)
            new_file.write('\n')
        new_file.close()

    @staticmethod
    def get_best_vectors(number_vectors_from_one_file: int) -> list[list[int]]:
        """
        Метод собирает со всех файлов из папки set_of_vectors по number_vectors_from_one_file лучших векторов, добавляет
         их в список и возвращает созданный список лучших векторов.
        :param number_vectors_from_one_file: Количество лучших векторов с каждого файла.
        :return: Список собранных лучших векторов.
        """
        file_number: int = 0
        file_path: str = f'E:/vovasProgram/cwsd_business_plan/set_of_vectors/{file_number}.txt'
        result_list_vectors: list[list[int]] = list()

        while os.path.isfile(file_path):
            new_file = open(file_path, 'r')
            for _ in range(number_vectors_from_one_file):
                line: str = new_file.readline()
                str_vector: list[str] = line.split(' ')
                vector: list[int] = list()
                for item in str_vector:
                    if item.isdigit():
                        vector.append(int(item))
                result_list_vectors.append(vector)
            new_file.close()
            file_number += 1
            file_path: str = f'E:/vovasProgram/cwsd_business_plan/set_of_vectors/{file_number}.txt'

        return result_list_vectors
