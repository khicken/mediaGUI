import matplotlib.pyplot as plt
import csv

x1, y1 = [], [] 
with open('./test/v1.csv','r') as csvfile: 
    lines = csv.reader(csvfile, delimiter = ',') 
    next(lines) # skip first row
    for row in lines:
        x1.append(row[0])
        y1.append(float(row[4]))
plt.plot(x1, y1, color = 'r', linestyle = 'solid', 
         marker = 'o',label = "v1 data")

x2, y2 = [], []
with open('./test/v2.csv','r') as csvfile: 
    lines = csv.reader(csvfile, delimiter = ',') 
    next(lines)
    for row in lines:
        x2.append(row[0]) 
        y2.append(float(row[4]))
plt.plot(x2, y2, color='g', linestyle='solid', 
         marker='x', label="v2 data") 

diffs = [''] * len(y1)
for i in range(len(diffs)):
    d = (y1[i] - y2[i]) / y1[i] * 100
    diffs[i] = f'{d:.2f}%'
print(f'Differences: {diffs}')

plt.xlabel('Frames per video') 
plt.ylabel('Time') 
plt.title('v1/v2: Frames per video v. Time') 
plt.legend() 
plt.show() 