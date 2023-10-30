from management import Optimization
from cwsd import CWSD
from default_objects import create_cwsd


cwsd: CWSD = create_cwsd()
opt: Optimization = Optimization()
mass: float = 200.0

print(f'Средние массы до: {cwsd.get_mass_indexes()}')
print(f'Плотности посадки до: {cwsd.get_densities()}')
while not cwsd.has_empty_pool():
    cwsd.daily_growth()
print(f'Средние массы после: {cwsd.get_mass_indexes()}')
print(f'Плотности посадки после: {cwsd.get_densities()}')

result_number: int = opt.calculate_optimal_number_new_fish_in_empty_pool(
    cwsd=cwsd,
    mass=mass,
    start_number=0,
    step_number=50,
    end_number=10000,
    print_info=True,
    attempts=10
)
print(f'Оптимальное количество рыбы весом {mass}г равно {result_number}')
