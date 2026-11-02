import numpy as np
from PIL import Image, ImageTk
from random import randint
import tkinter as tk
from math import floor
from math import cos

def render_model(img_mat, f, v, z_bufer, matchab, smechenie_x, smechenie_y):
    for i in f:
        x0 = (v[i[0]][0])
        y0 = (v[i[0]][1])
        z0 = (v[i[0]][2])
        x1 = (v[i[1]][0])
        y1 = (v[i[1]][1])
        z1 = (v[i[1]][2])
        x2 = (v[i[2]][0])
        y2 = (v[i[2]][1])
        z2 = (v[i[2]][2])
        px0 = x0 * matchab + smechenie_x
        py0 = - y0 * matchab + smechenie_y
        px1 = x1 * matchab + smechenie_x
        py1 =  - y1 * matchab + smechenie_y
        px2 = x2 * matchab + smechenie_x
        py2 = - y2 * matchab + smechenie_y
        pramougolnic(px0, px1, px2, py0, py1, py2, z0, z1, z2, z_bufer, img_mat)

class Scena:
    def __init__(self, file_name = 'cat.obj'):
        file = open(file_name)
        self.v = []
        self.f = []
        for s in file:
            sp = s.split()
            if sp[0] == 'v':
                self.v.append([float(sp[1]), float(sp[2]), float(sp[3])])
            elif sp[0] == 'f':
                self.f.append([int(sp[1].split('/')[0]) - 1, int(sp[2].split('/')[0]) - 1, int(sp[3].split('/')[0]) - 1])
        #print(self.f)

class Renderer:
    def __init__(self, matchab, dlina, shirina):
        self.matchab = matchab
        self.dlina = dlina
        self.shirina = shirina
        self.smechenie_x = dlina/2
        self.smechenie_y = shirina/2
        self.img_mat = np.zeros((dlina, shirina, 3), dtype=np.uint8)
        self.z_bufer = np.full((dlina, shirina), np.inf, dtype=np.float32)
    def render(self, scena):
        self.img_mat.fill(0)
        self.z_bufer.fill(np.inf)
        render_model(self.img_mat, scena.f, scena.v, self.z_bufer, self.matchab, self.smechenie_x, self.smechenie_y)

class App:
    def __init__(self, scene, renderer, win_w = 900, win_h = 900):
        self.scene = scene
        self.renderer = renderer

        # Оставляем как есть
        # Окно верхнего уровня
        self.root = tk.Tk()
        # Размеры окна
        self.root.geometry(f"{win_w}x{win_h}")
        # Область для рисования внутри окна
        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.focus_set()
        # Обновление изображения при изменении размеров окна
        self.canvas.bind('<Configure>', lambda e: self._refit())
        # Привязка обработчика клавиш
        self.root.bind('<Key>', self.on_key)

        # Изображение внутри окна
        self.photo = None
        self.full_image = None

        self.render()

    def on_key(self, event):
        k = event.keysym

        if k == 'plus':
            self.renderer.matchab *= 1.1
        elif k == 'minus':
            self.renderer.matchab /= 1.1
        elif k == 'space':
            Image.fromarray(render_cot.img_mat).save('test.png')
            return 'break'
        else:
            return

        self.render()
        # Не обрабатываем дальше – return 'brake'
        return 'break'

    def render(self):
        self.renderer.render(self.scene)
        self.full_image = Image.fromarray(self.renderer.img_mat)
        self._refit()

    # скопировать как есть
    def _refit(self):
        # Если ещё не отрендерилось, пропускаем
        if self.full_image is None: return
        # Ширина и высота области для рисования
        ww = self.canvas.winfo_width()
        wh = self.canvas.winfo_height()
        # Если вдруг сделали область слишком маленькой
        if ww < 10 or wh < 10: return
        # Вписать с сохранением пропорций
        s = min(ww / self.renderer.dlina, wh / self.renderer.shirina)
        dw = max(1, int(self.renderer.dlina * s))
        dh = max(1, int(self.renderer.shirina * s))
        disp = self.full_image.resize((dw, dh), Image.BILINEAR)
        # Очень важно сохранить ImageTk.PhotoImage(disp) в поле класса
        # Если оно будет локальным, то удалится после выхода сборщиком мусора
        self.photo = ImageTk.PhotoImage(disp)
        self.canvas.delete('all')
        self.canvas.create_image(ww // 2, wh // 2, image=self.photo)

    # скопировать как есть
    def run(self):
        self.root.mainloop()

def baritsentricheskie_koord(x, y, x0, y0, x1, y1, x2, y2):
    lambda_nol = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda_odin = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lamda_dva = 1.0 - lambda_nol - lambda_odin
    return lambda_nol, lambda_odin, lamda_dva

def pramougolnic(px0 ,px1, px2, py0, py1, py2, z0, z1, z2, z_bufer, img_mat):
    xmin, ymin = int(min(px0, px1, px2)), int(min(py0, py1, py2))
    xmax, ymax = int(max(px0, px1, px2)), int(max(py0, py1, py2))
    h, w = img_mat.shape[0:2]
    if (xmin < 0): xmin = 0
    if (ymin < 0): ymin = 0
    if (xmax > w-1): xmax = w-1
    if (ymax > h-1): ymax = h-1
    cosinus = ne_normalno(px0, px1, px2, py0, py1, py2, z0, z1, z2)
    cvet = [randint(100, 255) * -cosinus, randint(100, 255) * -cosinus, randint(100, 255) * -cosinus]
    if cosinus < 0:
        for i in range(xmin, xmax + 1):
            for j in range(ymin, ymax + 1):
                lambda_nol, lambda_odin, lamda_dva = baritsentricheskie_koord(i + 0.5, j + 0.5, px0, py0, px1, py1, px2, py2)
                if min(lambda_nol, lambda_odin, lamda_dva) >= 0:
                    z_koordinata = lambda_nol * z0 + lambda_odin * z1 + lamda_dva * z2
                    if z_koordinata < z_bufer[i][j]:
                        z_bufer[i][j] = z_koordinata
                        img_mat[j, i] = cvet

def ne_normalno(x0, x1, x2, y0, y1, y2, z0, z1, z2):
    n_normalno = - np.cross([x1 - x2, y1 - y2, z1 - z2], [x1 - x0, y1 - y0, z1 - z0])
    cosinus = np.dot(n_normalno, [0, 0, 1]) / np.linalg.norm(n_normalno)
    return cosinus

if __name__ == '__main__':
    scena = Scena()
    render_cot = Renderer(5.0, 2000, 2000)
    render_cot.render(scena)
    Image.fromarray(render_cot.img_mat).save('spheres.png')
    App(scena, render_cot, 500, 500).run()

