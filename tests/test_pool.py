from fish import Fish, ListFish, create_list_fish
from pool import Pool


# Создадим бассейн и список рыбы
pool: Pool = Pool(
    square=6.0
)

list_fish1: ListFish = create_list_fish(number_fish=1000, mass=150.0)
list_fish2: ListFish = create_list_fish(number_fish=2000, mass=350.0)

# Добавим рыбу в бассейн
print(pool.get_biomass())
pool.add_fish(new_fish=list_fish1)
print(pool.get_biomass())
pool.add_fish(list_fish2)
print(pool.get_biomass())

# Удалим самую большую рыбу из бассейна
removed_fish1: ListFish = pool.remove_fish(number_fish=2000, biggest_fish=True)
print(pool.get_biomass())
# Добавим удаленную рыбу и удалим самую маленькую
pool.add_fish(removed_fish1)
print(pool.get_biomass())
removed_fish2: ListFish = pool.remove_fish(number_fish=1000, biggest_fish=False)
print(pool.get_biomass())
print()
# Удалим всю рыбу и узнаем, пустой ли бассейн
removed_fish3: ListFish = pool.remove_fish(number_fish=5000)
print(pool.get_biomass())
print(f'pool is empty: {pool.is_empty()}')
# Вернем удаленную рыбу и узнаем пуст ли бассейн
print()
pool.add_fish(removed_fish3)
print(f'pool is empty: {pool.is_empty()}')
print(f'number fish in pool: {pool.get_number_fish()}')
print(f'density: {pool.get_density()}')
print()
# Проведем выращивание рыбы в течение 10 дней.
for _ in range(10):
    pool.daily_growth()

print(f'biomass: {pool.get_biomass()}')
print(f'number fish in pool: {pool.get_number_fish()}')
print(f'density: {pool.get_density()}')
print(f'pool is empty: {pool.is_empty()}')
