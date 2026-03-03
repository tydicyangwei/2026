from enum import Enum
Months = Enum('Months', 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec')
print(Months.Jan)
print(Months['Jan'])
for name, member in Months.__members__.items():
    print(name, '=>', member, ',', member.value)

