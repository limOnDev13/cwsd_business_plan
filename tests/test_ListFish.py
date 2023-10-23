from fish import Fish, ListFish, create_list_fish


list_fish1: ListFish = create_list_fish(100, 100.0)
list_fish2: ListFish = create_list_fish(200, 200.0)

print(list_fish1)
print(list_fish1.list_fish)
print(list_fish1.get_number_fish())
print(list_fish1.get_biomass())
print(list_fish1.get_mass(min=True))
print(list_fish1.get_mass(max=True))
print(list_fish1.get_mass(average=True))

list_fish1.sort()
one_fish: Fish = list_fish1.pop()
print(one_fish)
list_fish1.sort(reverse=True)
print((list_fish1 + list_fish2).list_fish)
print((list_fish1 + one_fish).list_fish)

print(list_fish2.get_number_fish())
fish2: Fish = list_fish2.pop()
print(list_fish2.get_number_fish())
list_fish2 += fish2
print(list_fish2.get_number_fish())
list_fish2 += list_fish1
print(list_fish2.get_number_fish())
