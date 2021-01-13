import sqlite3
import sys
from release.addEditCoffeeForm import Ui_MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("release/data/coffee.sqlite.db")
        self.pushButton.clicked.connect(self.save_results)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.update_result)
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        query = self.textEdit.toPlainText()
        result = cur.execute(query).fetchall()
        # Заполнили размеры таблицы
        if not result:
            self.label.setText('Ничего не нашлось')
            return
        else:
            self.label.setText('')
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        if self.tableWidget.item(0, item.row()):
            a = self.tableWidget.item(0, item.row()).text()
            self.modified[self.titles[item.column()]] = item.text(), a

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            for key in self.modified.keys():
                a = "{}='{}'\n".format(key, self.modified[key][0])
                cur.execute(f'{que} {a} WHERE ID = {self.modified[key][1]}')
            self.con.commit()
            self.modified.clear()

    def closeEvent(self, event):
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())