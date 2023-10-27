from cwsd import CWSD
from fish import create_list_fish


masses_and_numbers: list[list[float | int]] = [[50.0, 1000], [100.0, 750], [150.0, 500], [200.0, 250]]


# Создаем cwsd
def create_cwsd() -> CWSD:
    cwsd: CWSD = CWSD(
        number_pools=len(masses_and_numbers),
        square=6.0,
        max_density=40.0,
        commercial_fish_mass=400.0,
        package=100
    )
    for i in range(len(masses_and_numbers)):
        print(cwsd.add_fish(create_list_fish(number_fish=masses_and_numbers[i][1],
                                             mass=masses_and_numbers[i][0])))

    return cwsd
