class Title():
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.appearance = True
    def hide(self):
        self.appearance = False
        print(self.text, "- Прихований")
    
    def show(self):
        self.appearance = True
        print(self.text, "- Відкритий")
    
    def print_info(self):
        print("Надпис:", self.text)
        print("Розташування:(", self.x, self.y,")")
        print("Видимість:", self.appearance)

text1 = Title("Дізнатися переможця прямо зараз!", 150, 50)
text2 = Title("Переможець може бути тільки один", 150, -100)
text1.print_info()
text2.print_info()

text2.hide()