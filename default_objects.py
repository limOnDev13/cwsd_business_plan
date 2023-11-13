from cwsd import CWSD
from fish import create_list_fish
from management import BusinessPlan


masses_and_numbers: list[list[float | int]] = [[50.0, 1000], [100.0, 750], [150.0, 500], [200.0, 250]]


# Создаем cwsd
def create_cwsd(needed_add_fish: bool = True) -> CWSD:
    cwsd: CWSD = CWSD(
        number_pools=len(masses_and_numbers),
        square=6.0,
        max_density=40.0,
        commercial_fish_mass=400.0,
        package=100
    )
    if needed_add_fish:
        for i in range(len(masses_and_numbers)):
            print(cwsd.add_fish(create_list_fish(number_fish=masses_and_numbers[i][1],
                                                 mass=masses_and_numbers[i][0])))

    return cwsd


def create_business_plan() -> BusinessPlan:
    return BusinessPlan(
        prices=[[50.0, 80], [100.0, 160], [200.0, 300], [300.0, 420]],
        fish_price=1000.0,
        feed_price=240.0,
        price_per_kg=False
    )
