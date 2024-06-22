from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication([])
window_widght = 650
window_height = 500
question_window = QWidget()
question_window.resize(window_widght, window_height)
question_window.move(300, 300)
question_window.setWindowTitle("Memory Card")




question_window.show()
app.exec_()





















































































