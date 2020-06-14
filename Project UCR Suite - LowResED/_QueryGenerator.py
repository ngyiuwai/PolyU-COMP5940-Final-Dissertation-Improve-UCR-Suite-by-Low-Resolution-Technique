import os
import json
import random
import matplotlib.pyplot as plt
import time

# Modify 'interval' to determine the length of query.
# We are simulating the case that user is search for:
#   match at day [T],
#   match at day [T, T-1],
#   match at day [T, T-1, T-2],
#   match at day [T, T-1, T-2, T-3],
#   match at day [T, T-1, T-2, T-3, T-4],
# And 'interval' is number of data point in one day.
# The longest query will have a length of interval * 5

interval = 400
optimalLen = 0

if not os.path.exists('rawData'):
    os.mkdir('rawData')

print('Start generating at ', time.ctime())

data = [random.uniform(-1, 1)]

for n in range(0,5):
    for i in range(0, interval):
        data.append(data[len(data)-1] + random.uniform(-1, 1))
    if (n == 0):
        data.pop(0)
    
    print('DONE query', n)
    
    output_path = 'rawData/query' + str(n) + '.json'
    script_dir = os.path.dirname(__file__)
    save_path = os.path.join(script_dir, output_path)
    textfile = open(save_path, "w")
    textfile.write(json.dumps(data))
    textfile.close()

    optimalLen = optimalLen + (n+1)*interval ** 0.5
    
print('End generating at ', time.ctime())
print('File saved at ', time.ctime())


optimalLen = optimalLen / 5
print('Optimal lenth of Low Resolution Block =', optimalLen)

plt.plot(data)
plt.show()
