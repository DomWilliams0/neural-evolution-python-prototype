from world import *
from entity import *
import time

def main():

    world = World((10, 10))
    entity = Entity(world)

    while True:
        entity.tick()
        time.sleep(0.5)


if __name__ == "__main__":
    main()