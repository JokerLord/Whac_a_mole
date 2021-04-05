import sys
import random
import sqlite3

from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout,
                             QPushButton, QLabel, QToolTip,
                             QMessageBox, QDesktopWidget,
                             QInputDialog, QLineEdit)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QBasicTimer, QSize, QCoreApplication

UNACTIVE = 'bo1.png'
BAD = 'bo2.png'
GOOD = 'bo3.png'
TIME = 30


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.now = 0

        self.timer = QBasicTimer()
        self.step = 0

        grid = QGridLayout()
        grid.setSpacing(10)

        self.holes = []
        k, n = 0, 0
        for i in range(9):
            self.holes.append(QPushButton("U", self))
            self.holes[i].setIcon(QIcon(UNACTIVE))
            self.holes[i].setIconSize(QSize(200, 200))
            self.holes[i].setFlat(True)
            self.holes[i].clicked.connect(self.smash)

            grid.addWidget(self.holes[i], k, n)
            if k < 2:
                k += 1
            else:
                n += 1
                k = 0

        QToolTip.setFont(QFont('SansSerif', 10))

        self.count = QLabel("0")
        self.count.setToolTip('This is your score')
        self.time = QLabel(str(TIME))
        self.time.setToolTip('This is time you have')
        self.runBt = QPushButton("Иди и бей")
        self.runBt.setToolTip('Click here to start')
        self.qbtn = QPushButton('Выход')
        self.name = QLineEdit()

        grid.addWidget(self.count, n, 0)
        grid.addWidget(self.time, n, 1)
        grid.addWidget(self.runBt, n, 2)
        grid.addWidget(self.qbtn, n + 1, 1)
        grid.addWidget(self.name, n + 1, 0)

        font = QFont('Serif', 15, QFont.Light)
        self.count.setFont(font)
        self.time.setFont(font)
        self.runBt.setFont(font)
        self.runBt.clicked.connect(self.startGame)
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)
        self.qbtn.setFont(font)
        self.name.setFont(font)

        self.builtTable()
        self.center()
        self.setLayout(grid)
        self.setWindowTitle("Это окошечко")
        self.setWindowIcon(QIcon('mole.png'))
        self.show()

    def timerEvent(self, e):
        self.clearHim()
        self.showHim()

        self.step += 1
        if self.step % 2:
            time = int(self.time.text()) - 1
            self.time.setText(str(time))

        if self.step >= TIME * 2:
            self.timer.stop()
            self.insert_result(self.name.text(), int(self.count.text()))
            self.runBt.setEnabled(True)
            self.time.setText(str(TIME))
            self.step = 0
            self.clearHim()

    def smash(self):
        sender = self.sender()
        if sender.text() == 'B':
            count = int(self.count.text()) + 1
            self.count.setText(str(count))
            self.clearHim()
        elif sender.text() == 'G':
            count = int(self.count.text()) - 1
            self.count.setText(str(count))
            self.clearHim()

    def showHim(self):
        number = random.randint(0, 8)
        kind = random.randint(0, 1)
        if kind:
            self.holes[number].setText("G")
            self.holes[number].setIcon(QIcon(GOOD))
        else:
            self.holes[number].setText("B")
            self.holes[number].setIcon(QIcon(BAD))
        self.now = number

    def clearHim(self):
        self.holes[self.now].setText("U")
        self.holes[self.now].setIcon(QIcon(UNACTIVE))

    def startGame(self):
        time = 500
        self.showDialog()
        self.timer.start(time, self)
        self.count.setText("0")
        self.runBt.setEnabled(False)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Сообщение',
                                     "Вы точно хотите выйти?",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            curs.close()
            conn.close()
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showDialog(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter your name:')
        if ok:
            self.name.setText(str(text))

    def builtTable(self):
        global conn
        global curs
        conn = sqlite3.connect("kipish.db")
        curs = conn.cursor()

        curs.execute("DROP TABLE list_of_players")

        curs.execute("""CREATE TABLE list_of_players (
        name VARCHAR(60) PRIMARY KEY,
        score INT
        )""")

    def insert_result(self, name, count):
        ins = "INSERT INTO list_of_players VALUES(?, ?)"
        data = name, count
        curs.execute(ins, data)
        conn.commit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
