from management import BusinessPlan
from typing import Any


bp: BusinessPlan = BusinessPlan(
    prices=[[50.0, 80], [100.0, 160], [200.0, 300], [300.0, 420]],
    fish_price=1000.0,
    feed_price=240.0,
    price_per_kg=False
)
number_tests: int = 10
number_pools: int = 4
step: int = 50

best_vectors: list[list[int]] = bp.get_best_vectors(number_vectors_from_one_file=1)
print(best_vectors)
min_limits: list[int] = [9999 for _ in range(number_pools)]
max_limits: list[int] = [0 for _ in range(number_pools)]
for vector in best_vectors:
    for i in range(len(vector) - 1):
        if min_limits[i] > vector[i]:
            min_limits[i] = vector[i]
        if max_limits[i] < vector[i]:
            max_limits[i] = vector[i]
print(min_limits)
print(max_limits)
# min_limits: [19, 12, 2, 5]
# max_limits: [36, 23, 28, 23]
# delta:      [17, 11, 26, 18]

for _ in range(number_tests):
    result_info: list[list[int]] = bp.calculate_profitable_first_stocking(
        number_pools=number_pools,
        square=6.0,
        max_density=40.0,
        commercial_fish_mass=400.0,
        package=100,
        min_limits=[19, 12, 2, 5],
        max_limits=[36, 23, 28, 23],
        step=step,
        attempts=5,
        print_info=True,
        number_vectors=1000
    )
    result_info.sort(key=lambda x: x[-1], reverse=True)
    bp.save_best_random_vectors(result_info)
