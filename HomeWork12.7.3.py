per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}
money = float(input("Введите сумму:"))
value = list(map(float, per_cent.values()))
deposit = value [0] * (money/100), value [1] * (money/100), value [2] * (money/100), value [3] * (money/100)
deposit_i = max(deposit)
print(deposit_i)











