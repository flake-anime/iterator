from engine.iterator import Iterator

base_url = "https://ww2.gogoanimes.org"
iterator = Iterator(base_url)

result = iterator.get_a_to_z_list(log=True)
print(result)