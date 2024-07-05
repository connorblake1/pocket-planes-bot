import pyautogui
import time
from PIL import Image
import Levenshtein
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
sz = pyautogui.size()
center = np.array([sz[0]/2,sz[1]/2])

buttons = {
  "load": {
    "screen": "main",
    "pos": (173, 984)
  },
  "menu" : {
    "screen": "main",
    "pos" : (1669, 1039)
  },
  "next_plane": {
    "screen" : "main",
    "pos" : (1740,238)
  },
  "plane_list" : {
    "screen" : "main",
    "pos": (1387, 1025)
  },
  "close" : {
    "screen": "loading",
    "pos" : (1669, 1039)
  },
  "load_ppl" : {
     "screen" : "loading",
     "pos" : (321,961)
  },
  "load_cargo": {
     "screen" : "loading",
     "pos" : (507,974)
  },
  "plan_route" : {
    "screen" : "loading",
    "pos" : (852, 940)
  },
  "fly": {
    "screen" : "routing",
    "pos" : (795, 981)
  }
}
extractor_locs = {
  "profit_center": {
    "screen" : "routing",
    "pos" : (1454, 80)
  },
  "time_center": {
    "screen" : "routing",
    "pos" : (993, 80)
  },
  "payment_x": {
    "screen": "loading",
    "pos" : (1353,0)
  },
  "load_x" : {
    "screen" : "loading",
    "pos": (1675, 0)
  }
}

cities = {
  "OSAKA": {
    "index": 0,
    "class": 2,
    "mkr": "top right",
    "relatives": {
      "SENDAI": np.array([-344,  207]),
      "SAPPORO": np.array([-352,  470]),
      "TOKYO":  np.array([-275,  -23])
    }
  },
  "SENDAI": {
    "index": 1,
    "class": 1,
    "mkr": "top left",
    "relatives": {
      "OSAKA":  np.array( [ 344 ,-207] ),
      "SAPPORO":  np.array( [ -8 ,263] ),
      "TOKYO":  np.array( [  69 ,-230] ),
    }
  },
  "SAPPORO": {
    "index": 2,
    "class": 1,
    "mkr": "bottom right",
    "relatives": {
      "OSAKA":  np.array( [ 352, -470] ),
      "SENDAI":  np.array( [   8 ,-263] ),
      "TOKYO":  np.array( [  77, -493] ),
    }
  },
  "TOKYO": {
    "index": 3,
    "class": 3,
    "mkr": "top left",
    "relatives": {
      "OSAKA":  np.array( [275 , 23] ),
      "SENDAI":  np.array( [-69 ,230] ),
      "SAPPORO":  np.array( [-77 ,493] ),
    }
  }
}

def shifted_pos(region,location):
  locs = {
    "top left": (0,0),
    "top right": (1,0),
    "right": (1,.5),
    "bottom right": (1,1),
    "bottom left": (0,1), 
  }
  loc = locs[location]
  return np.array([region[0]+region[2]*loc[0],region[1]+region[3]*loc[1]])

def pp_do(cmd):
  pyautogui.moveTo(buttons[cmd]["pos"][0],buttons[cmd]["pos"][1])
  pyautogui.click()

def find_coords():
  for i in range(100000):
    time.sleep(.1)
    print(pyautogui.position())

def find_closest_word(input_str, word_dict):
    closest_word = None
    min_distance = float('inf')
    
    for word in word_dict:
        distance = Levenshtein.distance(input_str, word)
        if distance < min_distance:
            min_distance = distance
            closest_word = word
            
    return closest_word
def locate(needle,haystack,conf,grayscale=True):
  pos = 0
  try:
    pos = pyautogui.locateAll(needle,haystack,grayscale=grayscale,confidence=conf)
  except:
    pos = None
  return pos

def pull_destination(y):
  xmin = 130
  dest_item = pyautogui.screenshot(region=(xmin,y,985-xmin,100))
  extracted_string = pytesseract.image_to_string(dest_item)
  dest, name = extracted_string.split(" - ")
  return find_closest_word(dest,cities)

def fuzzy_in(item,l,tol):
  for li in l:
    if type(li) == tuple:
      li = li[1]
    if abs(li-item) < tol:
      return True
  return False

def pull_price(y):
  price_shot = pyautogui.screenshot(region=(1275,y,200,100))
  price_img = price_shot.save("price.png")
  nums = [0,1,3,4,5,6,7,9]
  xtol = 20
  locs = []
  for num in nums:
    pos =locate(f"img/pp{num}.png","price.png",.9)
    if pos is not None:
      for p in pos:
        locs.append((num,p.left))
  uniques = []
  for item in locs:
    if not fuzzy_in(item[1],uniques,xtol):
      uniques.append(item)
  sorted_list = sorted(uniques, key=lambda x: x[1])
  if len(sorted_list) == 0:
    return None
  val = int(''.join(str(t[0]) for t in sorted_list))
  return val

def pull_all_page():
  im1 = pyautogui.screenshot()
  loads = locate("img/load_item.png",im1,.9)
  locs = []
  ytol = 20
  if loads is not None:
    for load in loads:
      if not fuzzy_in(load.top,locs,ytol):
        locs.append(int(load.top))
  extracted = []
  print(locs)
  for loc in locs:
    extracted.append((loc,pull_destination(loc-20),pull_price(loc-20)))
  # TODO scrolling
  return extracted

def load_item(y):
  pyautogui.moveTo(1669,y)
  pyautogui.click()


def execute_route(loading_list):
  for item in loading_list:
    load_item(item[0])
    time.sleep(.5)
  waypoints = []
  for item in loading_list:
    if item[1] not in waypoints:
      waypoints.append(item[1])
  # TODO routing algo
  print(waypoints)
  pp_do("plan_route")
  city_locations = []
  time.sleep(.5)
  for waypoint in waypoints:
    click_city(waypoint)
    time.sleep(1)
  pp_do("fly")

# [244, 416, 588, 759, 931]
# city = "SENDAI"
# llist = [(759, city, 106), (588, city, 206),(244, "OSAKA", 106) ]
# llist = [(244, "OSAKA", 0),(416, "OSAKA", 0)]
# execute_route(llist)


def get_visible_cities():
  im1 = pyautogui.screenshot()
  im1.save("scrn.png")
  thresh = .75
  click_positions = {}
  for city in cities:
    clocs = list(locate(f"img/{city}.png",im1,thresh,grayscale=False))
    if len(clocs) == 0:
      continue
    loc = np.zeros((len(clocs),2))
    for i,cloc in enumerate(clocs):
      loc[i,:] = np.array([cloc.left,cloc.top])
      w = cloc.width
      h = cloc.height
    mean_loc = np.mean(loc,axis=0)
    # print(city,mean_loc)
    target_region = (int(mean_loc[0]),int(mean_loc[1]),w,h)
    click_pos = shifted_pos(target_region,cities[city]["mkr"])
    click_positions[city] = click_pos
  return click_positions


def pos_clickable(pos):
  return (100 <= pos[0]) and (pos[0] <= (sz[0]-100)) and (200 <= pos[1] <= (sz[1]-300))

def compute_city_pos(city,visibles):
  if city in visibles:
    return visibles[city]
  for relative in cities[city]['relatives']:
    if relative in visibles:
      return cities[city]['relatives'][relative] + visibles[relative]
  return None

def sign(x):
  return -1 + 2*(x > 0)

def drag_to_pos(pos):
  max_y_drag = (sz[1]-700)/2
  max_x_drag = (sz[0]-400)/2
  total_drag = pos - center
  print("total drag",total_drag)
  sx = sign(total_drag[0])
  sy = sign(total_drag[1])
  dvx = divmod(abs(total_drag[0]),max_x_drag)
  dvy = divmod(abs(total_drag[1]),max_y_drag)
  n_drags = int(max(dvx[0]+1,dvy[0]+1))
  drags = []
  for i in range(n_drags):
    if i < int(dvx[0]):
      dx = max_x_drag*sx
    elif i == int(dvx[0]):
      dx = sx*dvx[1]
    else:
      dx = 0
    if i < int(dvy[0]):
      dy = max_y_drag*sy
    elif i == int(dvy[0]):
      dy = dvy[1]*sy
    else:
      dy = 0
    drags.append((dx,dy))
  print(drags)
  for drag in drags:
    pyautogui.moveTo(center[0],center[1])
    pyautogui.drag(-drag[0],-drag[1],1,button='left')

def click_city(city):
  while True:
    print("Clicking:",city)
    visibles = get_visible_cities()
    print(visibles)
    pos = compute_city_pos(city,visibles)
    print("computed",pos)
    if pos_clickable(pos):
      pyautogui.moveTo(pos[0],pos[1])
      pyautogui.click()
      return
    drag_to_pos(pos)
    time.sleep(1)