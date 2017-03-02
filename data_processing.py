import numpy as np


def pad_area(area, location=(0, 0), shape=(4, 4)):
    mat = np.zeros(shape)
    h, w = area.shape
    x, y = location
    # print 'mat', location, shape
    # print area
    mat[y:y + h, x:x + w] = area
    return mat


def get_padding(cut_start):
    return abs(min(0, cut_start))


def get_areas(base, cut=(2, 2), padding=False):
    bh, bw = base.shape
    ah, aw = cut
    areas = []
    if padding:
        reach_x, reach_y = bw + aw, bh + ah
        ax0, ax1 = -aw + 1, 1
        ay0o, ay1o = -ah + 1, 1
    else:
        reach_x, reach_y = bw - (aw / 2), bh - (ah / 2)
        ax0, ax1 = 0, aw
        ay0o, ay1o = 0, aw
    for ix in range(1, reach_x):
        ay0, ay1 = ay0o, ay1o
        for iy in range(1, reach_y):
            # Padding Offset
            if padding:
                npx, npy = get_padding(ax0), get_padding(ay0)
            else:
                npx, npy = 0, 0
            # Cutting
            start_x, start_y = max(0, ax0), max(0, ay0)
            end_x, end_y = min(bw + 1, ax1), min(bh + 1, ay1)
            base_area = base[start_y:end_y, start_x:end_x]
            # Padding
            pad = pad_area(base_area, location=(npx, npy), shape=(ah, aw))
            areas.append(pad)

            ay0 += 1
            ay1 += 1
        ax0 += 1
        ax1 += 1
    return areas
