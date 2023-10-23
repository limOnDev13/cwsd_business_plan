from fish import Fish, ListFish


class Pool:
    def __init__(self, square: float, max_density: float):
        self.square: float = square
        self.max_density: float = max_density

        self.fishes: ListFish | None = None

    def add_fish(self, new_fish: Fish | ListFish):
        self.fishes += new_fish

    def remove_fish(self, number_fish: int, biggest_fish: bool = True) -> ListFish:
        self.fishes.sort(reverse=not biggest_fish)

        removed_fish: list[Fish] = list()
        amount: int
        length: int = self.fishes.get_number_fish()
        if number_fish > self.fishes.get_number_fish():
            amount = length
        else:
            amount = number_fish

        for _ in range(amount):
            removed_fish.append(self.fishes.pop())

        return ListFish(removed_fish)
