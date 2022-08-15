import sys
from PIL import Image
import numpy as np

# path ends with ".tiff"
img = Image.open(sys.argv[1], 'r')
arr = np.asarray(img)
limit = float(sys.argv[3]) / 100

arr_percent = arr / 255
arr_sum = arr_percent.sum(axis=2)
arr_over_limit = arr_sum > limit

arr_scale_factor = limit / arr_sum
arr_scale_factor[arr_scale_factor > 1] = 1
arr_output = arr * arr_scale_factor
print(arr_output)

img = Image.fromarray(arr, mode='CMYK')
# path ends with ".tiff"
img.save(sys.argv[2], compression='tiff_deflate')
