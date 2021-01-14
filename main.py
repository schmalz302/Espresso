import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite.db")
        self.pushButton.clicked.connect(self.select_data)
        # По умолчанию будем выводить все данные из таблицы films
        self.textEdit.setPlainText("SELECT * FROM coffee")
        self.select_data()

    def select_data(self):
        # Получим результат запроса,
        # который ввели в текстовое поле
        query = self.textEdit.toPlainText()
        res = self.connection.cursor().execute(query).fetchall()
        # Заполним размеры таблицы
        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setRowCount(len(res))
        # Заполняем таблицу элементами
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())