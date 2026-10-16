import numpy as np
from PIL import Image
from random import randint
from math import floor
from math import cos
file = open('model.obj')

def baritsentricheskie_koord(x, y, x0, y0, x1, y1, x2, y2):
    lambda_nol = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda_odin = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lamda_dva = 1.0 - lambda_nol - lambda_odin
    return lambda_nol, lambda_odin, lamda_dva

def pramougolnic(x0 ,x1, x2, y0, y1, y2, z0, z1, z2, z_bufer):
    xmin, ymin = int(min(x0, x1, x2)), int(min(y0, y1, y2))
    xmax, ymax = int(max(x0, x1, x2)), int(max(y0, y1, y2))
    if (xmin < 0): xmin = 0
    if (ymin < 0): ymin = 0
    cosinus = ne_normalno(x0, x1, x2, y0, y1, y2, z0, z1, z2)
    cvet = [randint(100, 255) * -cosinus, randint(100, 255) * -cosinus, randint(100, 255) * -cosinus]
    if cosinus < 0:
        for i in range(xmin, xmax + 1):
            for j in range(ymin, ymax + 1):
                lambda_nol, lambda_odin, lamda_dva = baritsentricheskie_koord(i + 0.5, j + 0.5, x0, y0, x1, y1, x2, y2)
                if min(lambda_nol, lambda_odin, lamda_dva) >= 0:
                    z_koordinata = lambda_nol * z0 + lambda_odin * z1 + lamda_dva * z2
                    if z_koordinata < z_bufer[i][j]:
                        z_bufer[i][j] = z_koordinata
                        img_mat[j, i] = cvet

def ne_normalno(x0, x1, x2, y0, y1, y2, z0, z1, z2):
    n_normalno = - np.cross([x1 - x2, y1 - y2, z1 - z2], [x1 - x0, y1 - y0, z1 - z0])
    cosinus = np.dot(n_normalno, [0, 0, 1]) / np.linalg.norm(n_normalno)
    return cosinus


matchab = 200
razmer = 45
smechenie = razmer / 2
img_mat = np.zeros((razmer, razmer, 3), dtype=np.uint8)

z_bufer = [[np.inf for j in range(razmer)] for i in range(razmer)]
#
# def line(img_mat, x0, y0, x1, y1):
#     x, y = x0, y0
#     dmax = max(abs(floor(x0) - floor(x1)), abs(floor(y0) - floor(y1)))
#     L = dmax + 1
#     if (L == 1):
#         img_mat[floor(y), floor(x)] = [50, 150, 150]
#         return
#     else:
#         dx = (x1 - x0) / (L - 1)
#         dy = (y1 - y0) / (L - 1)
#         for _ in range(L):
#             img_mat[floor(y), floor(x)] = [50, 150, 150]
#             x += dx
#             y += dy
#         return
#
# def line1(img_mat, x0, y0, x1, y1):
#     x, y = x0, y0
#     dmax = max(abs(floor(x0) - floor(x1)), abs(floor(y0) - floor(y1)))
#     L = dmax + 1
#     if (L == 1):
#         img_mat[floor(y), floor(x)] = [255, 0, 0]
#         return
#     else:
#         dx = (x1 - x0) / (L - 1)
#         dy = (y1 - y0) / (L - 1)
#         for _ in range(L):
#             img_mat[floor(y), floor(x)] = [255, 0, 0]
#             x += dx
#             y += dy
#         return
#

#
v = []
f = []
for s in file:
    sp = s.split()
    if sp[0] == 'v':
        v.append([float(sp[1]), float(sp[2]), float(sp[3])])
    elif sp[0] == 'f':
        f.append([int(sp[1].split('/')[0]), int(sp[2].split('/')[0]), int(sp[3].split('/')[0])])
print (v[-1], f[-1])

for i in f:
    x0 = - (v[i[0] - 1][0]) * matchab + smechenie
    y0 = - (v[i[0] - 1][1]) * matchab + smechenie
    z0 = - (v[i[0] - 1][2]) * matchab + smechenie
    x1 = - (v[i[1] - 1][0]) * matchab + smechenie
    y1 = - (v[i[1] - 1][1]) * matchab + smechenie
    z1 = - (v[i[1] - 1][2]) * matchab + smechenie
    x2 = - (v[i[2] - 1][0]) * matchab + smechenie
    y2 = - (v[i[2] - 1][1]) * matchab + smechenie
    z2 = - (v[i[2] - 1][2]) * matchab + smechenie
    pramougolnic(x0, x1, x2, y0, y1, y2, z0, z1, z2, z_bufer)

#
#
# for s in file:
#     sp = s.split()
#
#
#
#
# #for i in v:    img_mat[floor(-i[1] * 5000 + 500), floor(-i[0] * 5000 + 500)] = [50, 150, 150]
#
#
# x0, y0, x1, y1 = 50.3, 30.2, 987.65, 800.45
# #line(img_mat, x0, y0, x1, y1)

img = Image.fromarray(img_mat)
img.save("img.png")