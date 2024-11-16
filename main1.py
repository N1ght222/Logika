import os
from PyQt5.QtWidgets import QApplication
app = QApplication([])  # Ініціалізація додатку (Qt Application)
from PyQt5.QtWidgets import (
   QWidget, QFileDialog, QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageFilter import SHARPEN, BLUR

# Створення головного вікна додатку
win = QWidget()       
win.resize(700, 500)  # Задаємо розмір вікна
win.setWindowTitle('Easy Editor')  # Встановлюємо заголовок вікна

# Створення віджетів
lb_image = QLabel("Картинка")  # Місце для відображення зображення
btn_dir = QPushButton("Папка")  # Кнопка для вибору папки
lw_files = QListWidget()  # Список файлів

# Кнопки для редагування зображень
btn_left = QPushButton("Вліво")
btn_right = QPushButton("Вправо")
btn_flip = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")

# Створення макетів для розміщення віджетів
row = QHBoxLayout()  # Основний горизонтальний макет
col1 = QVBoxLayout()  # Ліва колонка
col2 = QVBoxLayout()  # Права колонка

# Додаємо віджети у ліву колонку
col1.addWidget(btn_dir)
col1.addWidget(lw_files)

# Додаємо віджети у праву колонку
col2.addWidget(lb_image, 95)  # Місце для зображення займає 95% висоти

# Рядок інструментів для кнопок редагування
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)

# Додаємо рядок інструментів у праву колонку
col2.addLayout(row_tools)

# Додаємо обидві колонки в основний макет
row.addLayout(col1, 20)  # Ліва колонка займає 20% ширини
row.addLayout(col2, 80)  # Права колонка займає 80% ширини

# Встановлюємо основний макет для вікна
win.setLayout(row)
win.show()  # Показуємо вікно користувачеві

workdir = ''  # Глобальна змінна для зберігання обраної робочої директорії

# Функція для фільтрації файлів за розширенням
def filter(filenames, extensions):
    result = []
    for filename in filenames:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

# Функція для вибору робочої директорії
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

# Функція для відображення списку файлів у обраній папці
def showFilenamesList():
    extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.avif']  # Допустимі розширення
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)  # Фільтрація файлів
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)  # Додаємо файли до списку

btn_dir.clicked.connect(showFilenamesList)  # Підключення кнопки для вибору папки

# Клас для обробки зображень
class ImageProcessor():
    def __init__(self):
        self.image = None  # Змінна для зображення
        self.dir = None  # Директорія з файлом
        self.filename = None  # Ім'я файлу
        self.save_dir = "Modified/"  # Папка для збереження оброблених зображень
        
    # Завантаження зображення
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
        
    # Збереження зображення у папку Modified
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
        
    # Фільтр для переведення у чорно-білий формат
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        
    # Дзеркальне відображення
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        
    # Поворот на 90 градусів вліво
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        
    # Поворот на 90 градусів вправо
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        
    # Застосування фільтру різкості
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    # Відображення зображення у QLabel
    def showImage(self, path):
        lb_image.hide()  # Ховаємо попереднє зображення
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()  # Показуємо нове зображення
    
workimage = ImageProcessor()  # Створення об'єкта класу для обробки зображень

# Функція для відображення вибраного файлу
def showChoisenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

# Підключення кнопок до відповідних методів
lw_files.currentRowChanged.connect(showChoisenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_flip.clicked.connect(workimage.do_flip)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)

app.exec()  # Запуск головного циклу програми
