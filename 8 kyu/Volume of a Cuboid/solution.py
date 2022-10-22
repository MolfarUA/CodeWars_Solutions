58261acb22be6e2ed800003a


def get_volume_of_cuboid(length, width, height):
    return length * width * height


# PEP8: kata function name should use snake_case not mixedCase
getVolumeOfCubiod = get_volume_of_cuboid
_____________________________
from functools import reduce


def get_volume_of_cuboid(length, width, height):
    return reduce(lambda x,y: x * y, (length, width, height))
_____________________________
def get_volume_of_cuboid(length, width, height):
    lst=[length,width,height]
    lst=length*width*height
    return lst
_____________________________
def get_volume_of_cuboid(length, width, height):
    return height * width * length
    pass
_____________________________
def get_volume_of_cuboid(length, width, height):
    sum = length * width * height
    return(sum)
_____________________________
def get_volume_of_cuboid(length, width, height):
    return (width*length) * height
_____________________________
def get_volume_of_cuboid(length, width, height):
    volume_cuboid = round(length * width * height)
    return volume_cuboid
_____________________________
def get_volume_of_cuboid(length, width, height):
    volume = length * width * height
    return volume
a = get_volume_of_cuboid(5, 2, 7)
print(a)
_____________________________
def get_volume_of_cuboid(i, j, l):
    return i*j*l
