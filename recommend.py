import random
import time 
import timeit

def main():

  objecttime = time.clock()
  objects = create_objects()
  print 'create objects: ', (time.clock() - objecttime) * 1000, 'ms'

  visitortime = time.clock()
  visitors = create_visitors(objects)
  print 'create visitors: ', (time.clock() - visitortime) * 1000, 'ms'
  
  maptime = time.clock()
  objects_visitors = map_visitors_to_objects(visitors, objects)
  print 'create index: ', (time.clock() - maptime) * 1000, 'ms'
  
  findtime = time.clock()
  similar = find_similar(create_single_visitor(objects), objects_visitors)
  print 'find similar users: ', (time.clock() - findtime) * 1000, 'ms'

  objectpooltime = time.clock()
  object_pool = create_object_pool(similar, visitors)
  print 'create object recommendation pool: ', (time.clock() - objectpooltime) * 1000, 'ms'

  print 'top 5 recommendations:', sorted(object_pool.items(), key = lambda x: x[1], reverse = True)[:5]


def create_object_pool(similar, visitors):
  object_pool = {}
  for similar_user in similar.items():
    for sobj in visitors[similar_user[0]]:
      if sobj in object_pool:
        object_pool[sobj] += 1 * similar_user[1]
      else:
        object_pool[sobj] = 1 * similar_user[1]

  return object_pool

def create_objects():
  objects = []
  for i in range(0, 90000):
    objects.append(i)
  return objects


def map_visitors_to_objects(visitors,objects):
  objects_visitors = {}
  for visitor_id in range(0, len(visitors)):
    for sobj in visitors[visitor_id]:
      if sobj in objects_visitors:
        objects_visitors[sobj].append(visitor_id)
      else:
        objects_visitors[sobj] = [visitor_id]
  
  return objects_visitors

def find_similar(visitor, objects_visitors):
  similar = {}
  for visited in visitor:
    if visited in objects_visitors:
      for user in objects_visitors[visited]:
        if user in similar:
          similar[user] += 1
        else:
          similar[user] = 1
  
  return similar

def create_single_visitor(objects):
  visited = []
  for x in range(0,random.randint(3,9)):
    visited.append(objects[int(random.gauss(45000,5000))])
    #visited.append(objects[random.randint(0, len(objects) - 1)])
  return visited

def create_visitors(objects):
  visitors = []
  for i in range(0, 400000):
    visitors.append(create_single_visitor(objects))

  return visitors


if __name__ == '__main__':
  main()
