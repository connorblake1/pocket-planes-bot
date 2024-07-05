import numpy as np
from pp_utils import *
# OSAKA SENDAI SAPPORO TOKYO
dists = np.array([[0,56.0,93],[0,0,45.0],[0,0,0]])
dists = dists + dists.T
multiplier = 1.25
planes = {
  "PL003": {
    "type": "navigator",
    "speed": 165,
    "weight": 2,
    "cargo": [0,2],
    "class": 1,
  },
  "PL007": {
    "type": "navigator",
    "speed": 165,
    "weight": 2,
    "cargo": [1,1],
    "class": 1,
  },
  "PL008": {
    "type": "airvan",
    "speed": 163,
    "weight": 3,
    "cargo": [2,1],
    "class": 1
  },
  "PL009": {
    "type": "airvan",
    "speed": 163,
    "weight": 3,
    "cargo": [3,0],
    "class": 1
  },
  "PL010": {
    "type": "airvan",
    "speed": 163,
    "weight": 3,
    "cargo": [2,1],
    "class": 1
  }
}

def distance(route):
  return dists[cities[route[0]]["index"],cities[route[1]]["index"]]

def route_cost(route,plane):
  return plane["speed"]*plane["weight"]*distance(route)/400

def route_time(route,plane):
  return distance(route)*10/plane["speed"]

# routes are list(str, str, ...)
# route is tuple(str,str)
# options are list(int, bool, str, int)
# choices are list(int, bool, str, int)
def calculate_route_cost(legs,plane):
  total_cost = 0
  for i in range(len(legs)-1):
    total_cost += route_cost((legs[i],legs[i+1]),plane)
  return -int(total_cost)

def calculate_route_time(legs,plane):
  total_time = 0
  for i in range(len(legs)-1):
    total_time += route_time((legs[i],legs[i+1]),plane)
  return total_time


def calculate_profit(choice,choice_route,plane):
  cityA = choice[0][2]
  revenue = sum([item[3] for item in choice])
  if all([cityA == pc[2] for pc in choice]) and len(choice) == sum(plane["cargo"]):
    revenue *= multiplier
  return int(revenue) + calculate_route_cost(choice_route,plane)

def is_valid_choice(choice,choice_route,plane):
  cities_to_visit = set([item[2] for item in choice])
  all_visited = all([city in legs for city in cities_to_visit])
  passengers = len([item for item in choice if item[1]])
  cargos = len([item for item in choice if not item[1]])
  all_seats = (passengers <= plane["cargo"][0]) and (cargos <= plane["cargo"][1])
  all_classes = all([plane["class"] <= cities[city]["class"] for city in choice_route])
  return all_visited and all_classes and all_seats

def choose_payload(city,options,plane,method="bruteforce"):
  best_dpm = 0
  outlist = []
  passengers = [option for option in options if option[1]]
  cargos = [option for option in options if not option[1]]
  print("P",passengers)
  print("C",cargos)
  if method=="bruteforce":
    
  else:
    print("IMPLEMENT IT")
  return outlist 
 
city = "OSAKA"
# y coord, is_person, city, price
# options = [(759, True,"OSAKA", 106), (588, True, "SENDAI", 206),(244, False, "OSAKA", 106) ]
options = [(759, True,"SAPPORO", 143), (588, True, "SENDAI", 106),(244, True, "SENDAI", 106) ]
plane = planes["PL010"]
out = choose_payload(city,options,plane)
print(out)

plane = planes["PL007"]
city = "SAPPORO"
options = [(244,False,"OSAKA",143),(416,False,"SENDAI",95),(588,True,"SENDAI",95),(759,False,"SENDAI",95)]
# best is sendai any cargo and person
output = choose_payload(city,options,plane)

run_tests = False
if run_tests:
  plane = planes["PL008"]
  legs = ("SAPPORO","SENDAI")
  options = [(0,True,"SENDAI",95),(0,True,"SENDAI",95),(0,False,"SENDAI",95)]
  print(calculate_profit(options,legs,plane)) # 302
  print(calculate_route_time(legs,plane)) # 3
  print(is_valid_choice(options,legs,plane)) # true

  plane = planes["PL008"]
  legs = ("SAPPORO","SENDAI")
  options = [(0,True,"SENDAI",95),(0,True,"SENDAI",95)]
  print(calculate_profit(options,legs,plane)) # 135
  print(calculate_route_time(legs,plane)) # 3
  print(is_valid_choice(options,legs,plane)) # true

  plane = planes["PL010"]
  legs = ("SAPPORO","OSAKA")
  options = [(0,True,"OSAKA",143),(0,False,"OSAKA",143),(0,True,"OSAKA",143)]
  print(calculate_profit(options,legs,plane)) # 424
  print(calculate_route_time(legs,plane)) # 6
  print(is_valid_choice(options,legs,plane)) # true

  plane = planes["PL003"]
  legs = ("SENDAI","OSAKA")
  options = [(0,False,"OSAKA",106),(0,False,"OSAKA",106)]
  print(calculate_profit(options,legs,plane)) # 220
  print(calculate_route_time(legs,plane)) # 3
  print(is_valid_choice(options,legs,plane)) # true

  plane = planes["PL003"]
  legs = ("SENDAI","SAPPORO","OSAKA")
  options = [(0,False,"OSAKA",106),(0,False,"SAPPORO",95)]
  print(calculate_profit(options,legs,plane)) # 88
  print(calculate_route_time(legs,plane)) # 9
  print(is_valid_choice(options,legs,plane)) # true

  plane = planes["PL003"]
  legs = ("SENDAI","OSAKA")
  options = [(0,False,"OSAKA",106),(0,False,"SAPPORO",95)]
  print(calculate_profit(options,legs,plane)) # idk
  print(calculate_route_time(legs,plane)) # idk
  print(is_valid_choice(options,legs,plane)) # false

