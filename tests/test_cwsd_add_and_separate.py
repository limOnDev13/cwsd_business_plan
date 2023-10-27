from fish import ListFish, create_list_fish
from cwsd import CWSD


masses_and_numbers: list[list[float | int]] = [[50.0, 2000], [100.0, 1500], [150.0, 1000], [200.0, 1300]]
# Создаем cwsd
cwsd: CWSD = CWSD(
    number_pools=len(masses_and_numbers),
    square=6.0,
    max_density=40.0,
    commercial_fish_mass=400.0,
    package=100
)

# Добавляем в него новую рыбу
print(f'total biomass in CWSD: {cwsd.get_biomass()}')
for i in range(len(masses_and_numbers)):
    print(cwsd.add_fish(create_list_fish(number_fish=masses_and_numbers[i][1],
                                         mass=masses_and_numbers[i][0])))

print(f'total biomass in CWSD: {cwsd.get_biomass()}')
# Попробуем добавить рыбу в НЕ пустой бассейн
print(cwsd.add_fish(create_list_fish(number_fish=masses_and_numbers[0][1],
                                     mass=masses_and_numbers[0][0])))
print(f'total biomass in CWSD: {cwsd.get_biomass()}')

# Разделим рыбу из переполненного правого бассейна
print(cwsd.get_densities())
cwsd.separate_fish(cwsd.pools[-1])
print(cwsd.get_densities())
print()

# Разделим рыбу из переполненного левого бассейна
masses_and_numbers2: list[list[float | int]] = [[50.0, 5000], [100.0, 1500], [150.0, 1000], [200.0, 1300]]
cwsd2: CWSD = CWSD(
    number_pools=len(masses_and_numbers2),
    square=6.0,
    max_density=40.0,
    commercial_fish_mass=400.0,
    package=100
)
print(cwsd2.get_densities())
for i in range(len(masses_and_numbers2) - 1):
    print(cwsd2.add_fish(create_list_fish(number_fish=masses_and_numbers2[i][1],
                                          mass=masses_and_numbers2[i][0])))
print(cwsd2.get_densities())
print(cwsd2.get_mass_indexes())
print(f'cwsd2.pool[0].mass_index: {cwsd2.pools[0].mass_index},'
      f' cwsd2.pool[0].average_mass: {cwsd2.pools[0].get_average_mass()}')
cwsd2.separate_fish(cwsd2.pools[0])
print(cwsd2.get_densities())
print(cwsd2.get_mass_indexes())
print()

# Разделим переполненный бассен в середине
masses_and_numbers3: list[list[float | int]] = [[50.0, 5000], [100.0, 1500], [150.0, 1000], [200.0, 1300]]
cwsd3: CWSD = CWSD(
    number_pools=len(masses_and_numbers2),
    square=6.0,
    max_density=40.0,
    commercial_fish_mass=400.0,
    package=100
)
print(cwsd3.get_densities())
for i in range(len(masses_and_numbers3)):
    print(cwsd3.add_fish(create_list_fish(number_fish=masses_and_numbers3[i][1],
                                          mass=masses_and_numbers3[i][0])))
print(cwsd3.get_densities())
print(cwsd3.get_mass_indexes())
print(f'cwsd2.pool[0].mass_index: {cwsd3.pools[1].mass_index},'
      f' cwsd2.pool[0].average_mass: {cwsd3.pools[1].get_average_mass()}')
cwsd3.separate_fish(cwsd3.pools[1])
print(cwsd3.get_densities())
print(cwsd3.get_mass_indexes())
