import numpy as np
from PIL import Image

class Map:

    def __init__(self):
        self.map_array = ''
        self.im = ''
        self.map_color_array = ''
        self.highest = ''
        self.lowest = ''
        self.diff_between_low_high = ''

    def set_map_array(self):
        with open('elevation_small.txt') as file:
            self.map_array = np.loadtxt(file, dtype=int)

    def set_map_color_array(self):
        self.map_color_array = self.map_array
        self.diff_between_low_high = self.highest - self.lowest
        self.map_color_array = np.subtract(self.map_color_array, self.lowest)
        self.map_color_array = np.divide(self.map_color_array, self.diff_between_low_high)
        self.map_color_array = np.multiply(self.map_color_array, 255)

    def create_map_image(self):
        im = Image.fromarray(np.uint8(self.map_color_array))
        self.im = im

    def set_high_and_low(self):
        self.highest = np.amax(self.map_array)
        self.lowest = np.amin(self.map_array)

    def get_map_array(self):
        return self.map_array

class Pathfinder:

    def __init__(self, new_map):
        self.map = new_map
        self.pixels = ''
        self.current_point = []
        self.path = []

    def set_current_point(self, current_point):
        self.current_point = current_point

    def set_map_pixels(self):
        self.map.im = self.map.im.convert('RGB')
        self.pixels = self.map.im.load()

    def set_pixel_color(self, point):
        self.pixels[point[1], point[0]] = (204, 102, 0)

    # rememeber its y,x not x,y
    def find_path(self):
        starting_point = [300, 0]
        y = starting_point[0]
        x = starting_point[1]
        while x < 599:
            point = []
            NE = abs(self.map.map_array[y-1][x+1] - self.map.map_array[y][x])
            E = abs(self.map.map_array[y][x+1] - self.map.map_array[y][x])
            SE = abs(self.map.map_array[y+1][x+1] - self.map.map_array[y][x])
            lowest_point = min(NE, E, SE)
            if lowest_point == NE:
                point.append(y-1)
                point.append(x+1)
                self.set_pixel_color(point)
                y = y - 1
                x = x + 1
            elif lowest_point == E:
                point.append(y)
                point.append(x+1)
                self.set_pixel_color(point)
                y = y
                x = x + 1
            else:
                point.append(y+1)
                point.append(x+1)
                self.set_pixel_color(point)
                y = y + 1
                x = x + 1
            print(point)



n_map = Map()
n_pathfinder = Pathfinder(n_map)
n_map.set_map_array()
n_map.set_high_and_low()
n_map.set_map_color_array()
n_map.create_map_image()
n_pathfinder.set_map_pixels()
n_pathfinder.find_path()
n_pathfinder.map.im.show()