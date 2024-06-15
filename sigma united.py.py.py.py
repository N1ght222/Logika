class Widget():
    def __init__(self, title_text, x, y):
        self.x = x
        self.y = y
        self.title = title_text

    def print_info(self):
        print("Надпис:", self.title)
        print("Розташування:", self.x, self.y)

class Button(Widget):
    def __init__(self, title_text, x, y, is_clicked):
        super().__init__(title_text, x, y)
        self.is_clicked = is_clicked
    
    def click(self):
        self.is_clicked = True
        print("Ви зареєстровані!!!")
    
btn = Button("Брати участь", 100, 100, False)
btn.print_info()

answer = input("Хочете зареєструватися? (так/ні)")  
if answer == 'так':
    btn.click()
else:
    print("А шкода!!!")