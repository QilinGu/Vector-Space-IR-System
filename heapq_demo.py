import heapq
from collections import Counter
import math
import json
import operator

#open and read a json file into "data"
# with open('2015_movies.json') as data_file:
#     data = json.load(data_file)
#
# print data['1']['title']
#
# myDict = {"B":1, "C":2, "D":6, "A":9}
# for obj in myDict.items():
#    print obj
#
# nums = [1]*4
# print nums
#
# print math.pow(2,3)
#
# s = ["apple", "hello", "apple"]
# counts = Counter(s)
# print counts["apple"]

x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
print sorted(x.items(), reverse=True)
sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
print sorted_x
print sorted_x[0][1]

h = []
heapq.heappush(h, {'5':100})
heapq.heappush(h, {'7':222})
heapq.heappush(h, {'1':333})
heapq.heappush(h, {'3':444})
heapq.heappush(h, {'4':555})
print heapq.count
print heapq.heappop(h).get(1)
list = heapq.nlargest(4, h)#list
for item in list:
   for key, value in item.iteritems():
      print key, value

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums))  # Prints [42, 37, 23]
print(heapq.nsmallest(3, nums)) # Prints [-4, 1, 2]

portfolio = [
   {'name': 'IBM', 'shares': 100, 'price': 91.1},
   {'name': 'AAPL', 'shares': 50, 'price': 543.22},
   {'name': 'FB', 'shares': 200, 'price': 21.09},
   {'name': 'HPQ', 'shares': 35, 'price': 31.75},
   {'name': 'YHOO', 'shares': 45, 'price': 16.35},
   {'name': 'ACME', 'shares': 75, 'price': 115.65}
]

cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
print cheap
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
print expensive