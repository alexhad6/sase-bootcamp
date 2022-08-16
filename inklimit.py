import sys
from PIL import Image
import numpy as np

def scale_method(arr, limit):
    arr_percent = arr / 255
    arr_sum = arr_percent.sum(axis=2)

    arr_scale_factor = limit / arr_sum
    arr_scale_factor[arr_scale_factor > 1] = 1

    arr_scale_factor = np.repeat(arr_scale_factor[:, :, np.newaxis], 4, axis=2)
    arr_output = arr * arr_scale_factor
    return arr_output.astype(np.uint8)

def replace_method(arr, limit):
    arr_percent = arr / 255
    arr_sum = arr_percent.sum(axis=2)

    arr_x = (arr_sum - limit) / 2
    arr_x[arr_x < 0] = 0

    arr_percent[:, :, 0] -= arr_x
    arr_percent[:, :, 1] -= arr_x
    arr_percent[:, :, 2] -= arr_x
    arr_percent[:, :, 3] += arr_x

    arr_output = arr_percent * 255
    arr_output[arr_output > 255] = 255
    arr_output[arr_output < 0] = 0
    return arr_output.astype(np.uint8)

def main():
    # path ends with ".tiff"
    img = Image.open(sys.argv[1], 'r')
    arr = np.asarray(img)
    limit = float(sys.argv[3]) / 100

    if limit < 1:
        print("Ink Limit too low")
        return

    if len(sys.argv) < 5:
        print("No method")
        return

    method = sys.argv[4]
    if method == "scale":
        arr_output = scale_method(arr, limit)
    elif method == "replace":
        arr_output = replace_method(arr, limit)
    else:
        print(f"Method {method} is invalid")
        return

    img = Image.fromarray(arr_output, mode='CMYK')
    # path ends with ".tiff"
    img.save(sys.argv[2], compression='tiff_deflate')

if __name__ == '__main__':
    main()
