import numpy as np

with open('elevation_small.txt') as file:
    map_array = np.loadtxt(file, dtype=int)

highest = 5648
lowest = 3139
map_color_array = map_array
diff_between_low_high = highest - lowest
map_color_array = np.subtract(map_color_array, lowest)
map_color_array = np.divide(map_color_array, diff_between_low_high)
map_color_array = np.multiply(map_color_array, 255)
print(map_color_array)