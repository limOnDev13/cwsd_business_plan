from cwsd import CWSD
from copy import deepcopy
from fish import create_list_fish


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


class BusinessPlan:
    pass
