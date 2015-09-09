'''
Created on 22 Jun 2015
FLOOD ZONE
@author: NoNotCar
'''
import Object


def flipdir(dire):
    return (-dire[0], -dire[1])


def rotclockdir(dire):
    dirconv = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    return dirconv[(dirconv.index(dire) + 1) % 4]


class Pipe(Object.OObject):
    ispipe = True

    def __init__(self, x, y, dire, owner):
        self.dir = dire
        self.x = x
        self.y = y
        self.owner = owner
        self.inputs = []

    def flow(self, length, world, visited):
        for dire in self.inputs:
            if (self.x + dire[0], self.y + dire[1]) not in visited:
                obj = world.get_obj(self.x + dire[0], self.y + dire[1])
                if obj and obj.ispipe:
                    visited.append((self.x, self.y))
                    return obj.flow(length + 1, world, visited)


class SPipe(Pipe):
    def __init__(self, x, y, dire, owner):
        self.dir = dire
        self.x = x
        self.y = y
        self.owner = owner
        self.inputs = [dire, flipdir(dire)]


class CPipe(Pipe):
    def __init__(self, x, y, dire, owner):
        self.dir = dire
        self.x = x
        self.y = y
        self.owner = owner
        self.inputs = [dire, rotclockdir(dire)]
