import cv2 as cv
from tkinter import ttk, Tk
from PIL import ImageTk, Image

path = "images/zzz.jpg"


class Solution:
    def __init__(self):
        self.image = cv.imread(path, cv.IMREAD_GRAYSCALE)

    def run(self):
        self.create_interface()

        image_original = self.make_image(self.image)
        image_global_one = self.global_one(self.image)
        image_global_two = self.global_two(self.image)
        image_adaptive = self.adaptive(self.image)
        image_aliasing = self.aliasing(self.image)

        self.place_image(image_original, 50, 30, 350, 350)
        self.place_image(image_global_one, 430, 30, 350, 350)
        self.place_image(image_global_two, 50, 430, 350, 350)
        self.place_image(image_adaptive, 430, 430, 350, 350)
        self.place_image(image_aliasing, 830, 300, 350, 350)

    def place_image(self, image, x, y, w, h):
        label = ttk.Label(image=image)
        label.image = image
        label.place(x=x, y=y, width=w, height=h)

    def create_interface(self):
        label_original = ttk.Label(text="Исходное изображение")
        label_global_one = ttk.Label(text="Глобальная пороговая обработка(Binary)")
        label_global_two = ttk.Label(text="Глобальная пороговая обработка(Trunc)")
        label_adaptive_two = ttk.Label(text="Адаптивная пороговая обработка")
        label_aliasing = ttk.Label(text="Сглаживающий фильтр")

        label_original.place(x=100, y=5)
        label_global_one.place(x=470, y=5)
        label_global_two.place(x=80, y=400)
        label_adaptive_two.place(x=470, y=400)
        label_aliasing.place(x=900, y=280)

    def make_image(self, image):
        return ImageTk.PhotoImage(Image.fromarray(image).resize((350, 350)))

    def global_one(self, image):
        ret, th = cv.threshold(image, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        return self.make_image(th)

    def global_two(self, image):
        ret, th = cv.threshold(image, 0, 255, cv.THRESH_TRUNC + cv.THRESH_OTSU)
        return self.make_image(th)

    def adaptive(self, image):
        th = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 9, 3)
        return self.make_image(th)

    def aliasing(self, image):
        th = cv.blur(image, (8, 8), )
        return self.make_image(th)


if __name__ == "__main__":
    root = Tk()
    ms = Solution()
    root.geometry("1300x800")
    ms.run()
    root.mainloop()
