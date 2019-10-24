import os
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication, QVBoxLayout, QListWidget, QListWidgetItem, QDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QIcon
from PyQt5.QtCore import QSize

def console_text():
    text = """
   ___       _ _ _                    _     
  |_  |     (_) | |                  | |    
    | | __ _ _| | |__  _ __ _   _ ___| |__  
    | |/ _` | | | '_ \| '__| | | / __| '_ \ 
/\__/ / (_| | | | |_) | |  | |_| \__ \ | | |
\____/ \__,_|_|_|_.__/|_|   \__,_|___/_| |_|

    """.strip('\n')
    print(text)


console_text()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(200, 225))    
        self.setWindowTitle("Jailbrush 🖌") 

        oImage = QImage("background.png")
        sImage = oImage.scaled(QSize(300,200))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        icon_manager_btn = QPushButton('Icon Manager', self)
        icon_manager_btn.clicked.connect(self.icon_manager)
        icon_manager_btn.resize(150,50)
        icon_manager_btn.move(25, 25)

        metadata_btn = QPushButton('Info Editor', self)
        metadata_btn.clicked.connect(self.icon_manager)
        metadata_btn.resize(150,50)
        metadata_btn.move(25,87.5)

        export_btn = QPushButton('Export', self)
        export_btn.clicked.connect(self.icon_manager)
        export_btn.resize(150,50)
        export_btn.move(25,150)
        


    def icon_manager(self):
        self.icon_manager_win = IconManager()
        self.icon_manager_win.show()

class IconManager(QDialog):
    def __init__(self):
        QMainWindow.__init__(self)
        if not os.path.isdir('IconBundles'):
            os.mkdir('IconBundles/')

        self.setMinimumSize(QSize(450, 400))    
        self.setWindowTitle("Icon Manager")

        icon_list = IconList(self)
        icon_list.resize(250,300)
        icon_list.move(25,25)

        ok_btn = QPushButton('Ok', self)
        ok_btn.resize(150,50)
        ok_btn.move(50,350)

        cancel_btn = QPushButton('Cancel', self)
        cancel_btn.resize(150,50)
        cancel_btn.move(225,350)
    
    def item_options(self, item):
        print(item)

class IconList(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        self.parent = parent
        icons = [icon for icon in os.listdir('IconBundles') if icon.endswith('.png')]
        for icon in icons:
            thumb = QIcon()
            thumb.addPixmap(QPixmap('IconBundles/' + icon), QIcon.Normal)
            self.addItem(QListWidgetItem(thumb, icon))
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())