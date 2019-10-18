import numpy as np
from PIL import Image

class Map:

    def __init__(self):
        self.map_array = ''
        self.map_color_array = ''
        self.highest = ''
        self.lowest = ''

    def set_map_array(self):
        with open('elevation_small.txt') as file:
            self.map_array = np.loadtxt(file, dtype=int)

    def set_map_color_array(self):
        self.map_color_array = self.map_array
        diff_between_low_high = self.highest - self.lowest
        self.map_color_array = np.subtract(self.map_color_array, self.lowest)
        self.map_color_array = np.divide(self.map_color_array, diff_between_low_high)
        self.map_color_array = np.multiply(self.map_color_array, 255)

    def create_map_image(self):
        im = Image.fromarray(np.uint8(self.map_color_array))
        return im

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
        im = self.map.create_map_image()
        im = im.convert('RGB')
        self.pixels = im.load()
        print(self.pixels[1,1])

    def set_pixel_color(self, point):
        self.pixels[point[0], point[1]] = (204, 102, 0)

    def find_path(self):
        starting_point = [0, 300]
        while starting_point[0] < 601:
            



n_map = Map()
n_pathfinder = Pathfinder(n_map)
n_map.set_map_array()
n_map.set_high_and_low()
n_map.set_map_color_array()
image = n_map.create_map_image()
n_pathfinder.set_map_pixels()