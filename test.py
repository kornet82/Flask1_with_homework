sql_data = [
    (1, 'Rick Cook', 'Программирование сегодня — это гонка разработчиков программ...'),
    (2, 'Waldi Ravens', 'Программирование на С похоже на быстрые танцы на только...'),
]

keys = ("id", "author", "text")

# quotes = {}

# Решение 1 - плохое
# quotes[keys[0]] = sql_data[0]
# quotes[keys[1]] = sql_data[1]
# quotes[keys[2]] = sql_data[2]

# Решение 2 - плохое - потому что через индексы

# for i in range(len(sql_data)):
#     quotes[keys[i]] = sql_data[i]

# Решение 3 - уже лучше
# for key,value in zip(keys, sql_data):
#     quotes[key] = value

# Решение 4 - самое элегантное
quotes = []
for el in sql_data:
    quote = dict(zip(keys,el))
    quotes.append(quote)
print(quotes)