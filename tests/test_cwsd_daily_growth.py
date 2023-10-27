from cwsd import CWSD
from default_objects import create_cwsd


cwsd: CWSD = create_cwsd()
days: int = 365

for day in range(days):
    result: dict[str | float] | None = cwsd.daily_growth()
    if result is None:
        print(f'Переполнение на {day} день!!!!!!!!!')
        break
    else:
        print(f'День № {day}')
        print(f'Средние массы: {cwsd.get_mass_indexes()}\nПлотности посадки: {cwsd.get_densities()}')
