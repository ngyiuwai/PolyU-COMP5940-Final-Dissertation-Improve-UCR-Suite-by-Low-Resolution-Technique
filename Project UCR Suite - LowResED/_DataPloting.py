import os
import json
import matplotlib.pyplot as plt
import time

print('Start reading at ', time.ctime())

script_dir = os.path.dirname(__file__)
read_path = os.path.join(script_dir, 'rawData/data.json')
textfile = open(read_path, "r")
data = json.loads(textfile.read())


print('End reading at ', time.ctime())

plt.plot(data)
plt.show()
