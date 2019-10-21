import argparse
import operator
from pathlib import Path
import sys

import numpy as np
from PIL import Image

class Map:

    def __init__(self, data_file):
        self.data_file = data_file
        self.map_array = ''
        self.im = ''
        self.map_color_array = ''
        self.highest = ''
        self.lowest = ''
        self.diff_between_low_high = ''


    def set_map_array(self):
        with open(self.data_file) as file:
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

    def create_map_and_image(self):
        self.set_map_array()
        self.set_high_and_low()
        self.set_map_color_array()
        self.create_map_image()

class Pathfinder:

    def __init__(self, new_map, color_of_shortest_path=(51, 153, 255), downhill=False):
        self.color_of_shortest_path = color_of_shortest_path
        self.downhill = downhill
        self.map = new_map
        self.pixels = ''
        self.current_point = []
        self.path = []
        self.path_dict = {}

    def set_current_point(self, current_point):
        self.current_point = current_point

    def set_map_pixels(self):
        self.map.im = self.map.im.convert('RGB')
        self.pixels = self.map.im.load()

    def set_pixel_color(self, point, color=(204, 102, 0)):
        self.pixels[point[1], point[0]] = color

    # rememeber its y,x not x,y
    def find_all_paths(self):
        init_y = 0
        while init_y < len(self.map.map_array) - 1:
            y = init_y
            x = 0
            tot_delta = self.find_path(y, x)
            self.path_dict[init_y] = tot_delta
            init_y += 1
        shotest_path = min(self.path_dict.items(), key=operator.itemgetter(1))[0]
        self.find_path(shotest_path, 0, self.color_of_shortest_path)

    def find_path(self, y, x, color=(204, 102, 0)):
        tot_delta = 0
        while x < len(self.map.map_array) - 1:
            point = []
            NE = None
            E = None
            SE = None
            if y == 0:
                if self.downhill == False:
                    E = abs(self.map.map_array[y][x+1] - self.map.map_array[y][x])
                    SE = abs(self.map.map_array[y+1][x+1] - self.map.map_array[y][x])
                    lowest_point = min(E, SE)
                else:
                    E = self.map.map_array[y][x+1] - self.map.map_array[y][x]
                    SE = self.map.map_array[y+1][x+1] - self.map.map_array[y][x]
                    lowest_point = min(E, SE)
            elif y == len(self.map.map_array) - 1:
                if self.downhill == False:
                    NE = abs(self.map.map_array[y-1][x+1] - self.map.map_array[y][x])
                    E = abs(self.map.map_array[y][x+1] - self.map.map_array[y][x])
                    lowest_point = min(NE, E)
                else:
                    NE = self.map.map_array[y-1][x+1] - self.map.map_array[y][x]
                    E = self.map.map_array[y][x+1] - self.map.map_array[y][x]
                    lowest_point = min(NE, E)
            else:
                if self.downhill == False:
                    NE = abs(self.map.map_array[y-1][x+1] - self.map.map_array[y][x])
                    E = abs(self.map.map_array[y][x+1] - self.map.map_array[y][x])
                    SE = abs(self.map.map_array[y+1][x+1] - self.map.map_array[y][x])
                    lowest_point = min(NE, E, SE)
                else:
                    NE = self.map.map_array[y-1][x+1] - self.map.map_array[y][x]
                    E = self.map.map_array[y][x+1] - self.map.map_array[y][x]
                    SE = self.map.map_array[y+1][x+1] - self.map.map_array[y][x]
                    lowest_point = min(NE, E, SE)

            if lowest_point == NE and NE != None:
                point.append(y-1)
                point.append(x+1)
                tot_delta += NE
                self.set_pixel_color(point, color)
                y = y - 1
                x = x + 1
            elif lowest_point == E and E != None:
                point.append(y)
                point.append(x+1)
                tot_delta += E
                self.set_pixel_color(point, color)
                y = y
                x = x + 1
            elif lowest_point == SE and SE != None:
                point.append(y+1)
                point.append(x+1)
                tot_delta += SE
                self.set_pixel_color(point, color)
                y = y + 1
                x = x + 1
        return tot_delta

    def set_map_and_find_paths(self):
        self.set_map_pixels()
        self.find_all_paths()
        self.map.im.show()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Take a map of topographical data and plot the shortest path.'
    )
    parser.add_argument('file', help='file containing topographical data')
    parser.add_argument('--color', nargs=3, help='the color of the shortest path as three ints seperated by a space', type=int)
    parser.add_argument('--downhill', action='store_true', help='will create an image with paths that go downhill whenever possible')
    args = parser.parse_args()

    file_to_read = Path(args.file)
    if args.color:
        color_of_shortest_path = tuple(args.color)
    else:
        color_of_shortest_path = None

    if not file_to_read.is_file():
        print(f'{file_to_read} does not exist')
        sys.exit(1)
    else:
        n_map = Map(file_to_read)
        if args.downhill:
            if color_of_shortest_path == None:
                n_pathfinder = Pathfinder(n_map, downhill=True)
            else:
                n_pathfinder = Pathfinder(n_map, color_of_shortest_path, True)
        else:
            if color_of_shortest_path == None:
                n_pathfinder = Pathfinder(n_map)
            else:
                n_pathfinder = Pathfinder(n_map, color_of_shortest_path)
        n_map.create_map_and_image()
        n_pathfinder.set_map_and_find_paths()