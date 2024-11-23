import csv

fp = open("C:/Users/82107/Documents/대학/2-2 디지털실생활/Seoul.csv", 'r')
data = csv.reader(fp, delimiter=',')

max_temp = float('-inf')

for row in data:
        
  try:
    temp = row[5]

    try:
      temp_float = float(temp)
      if max_temp < temp_float : 
        max_temp = temp_float
        max_date = row[9]
    except ValueError:
        continue

  except IndexError:
    continue

print("날짜 : ",max_date, "최고온도 : ", max_temp)

