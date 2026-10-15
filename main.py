import numpy as np
from PIL import Image
from math import floor
from pathlib import Path

project_dir = Path(__file__).resolve().parent
file = open(project_dir / "models" / "cat.obj")
def line(img_mat, x0, y0, x1, y1):
    x, y = x0, y0
    dmax = max(abs(floor(x0) - floor(x1)), abs(floor(y0) - floor(y1)))
    L = dmax + 1
    if (L == 1):
        img_mat[floor(y), floor(x)] = [50, 150, 150]
        return
    else:
        dx = (x1 - x0) / (L - 1)
        dy = (y1 - y0) / (L - 1)
        for _ in range(L):
            img_mat[floor(y), floor(x)] = [50, 150, 150]
            x += dx
            y += dy
        return

def line1(img_mat, x0, y0, x1, y1):
    x, y = x0, y0
    dmax = max(abs(floor(x0) - floor(x1)), abs(floor(y0) - floor(y1)))
    L = dmax + 1
    if (L == 1):
        img_mat[floor(y), floor(x)] = [255, 0, 0]
        return
    else:
        dx = (x1 - x0) / (L - 1)
        dy = (y1 - y0) / (L - 1)
        for _ in range(L):
            img_mat[floor(y), floor(x)] = [255, 0, 0]
            x += dx
            y += dy
        return

img_mat = np.zeros((20000, 20000, 3), dtype=np.uint8)


v = []
f = []
for s in file:
    sp = s.split()
    if sp[0] == 'v':
        v.append([float(sp[1]), float(sp[2]), float(sp[3])])
    elif sp[0] == 'f':
        f.append([int(sp[1].split('/')[0]), int(sp[2].split('/')[0]), int(sp[3].split('/')[0])])
print (v[-1], f[-1])
matchab = 55
smechenie = 10000
for i in f:
    x0 = (v[i[0]-1][0]) * matchab + smechenie
    y0 = -(v[i[0]-1][1]) * matchab + smechenie
    x1 = (v[i[1]-1][0]) * matchab + smechenie
    y1 = -(v[i[1]-1][1]) * matchab + smechenie
    x2 = (v[i[2]-1][0]) * matchab + smechenie
    y2 = -(v[i[2]-1][1]) * matchab + smechenie
    # yy0 = (v[i[0] - 1][1]) * matchab + smechenie
    # yy1 = (v[i[1] - 1][1]) * matchab + smechenie
    # yy2 = (v[i[2] - 1][1]) * matchab + smechenie
    line(img_mat, x0, y0, x1, y1)
    line(img_mat, x0, y0, x2, y2)
    line(img_mat, x1, y1, x2, y2)

    # line1(img_mat, x0, yy0, x1, yy1)
    # line1(img_mat, x0, yy0, x2, yy2)
    # line1(img_mat, x1, yy1, x2, yy2)


for s in file:
    sp = s.split()




#for i in v:    img_mat[floor(-i[1] * 5000 + 500), floor(-i[0] * 5000 + 500)] = [50, 150, 150]


x0, y0, x1, y1 = 50.3, 30.2, 987.65, 800.45
#line(img_mat, x0, y0, x1, y1)

img = Image.fromarray(img_mat)
img.save(project_dir / "images" / "result.png")