import random
def generate_coordinates(min_num,max_num):
 while True:
  for coords in range(1):
    x = random.randint(min_num,max_num)
    y = random.randint(min_num,max_num)
    z = random.randint(min_num,max_num)
    return x,y,z
    


