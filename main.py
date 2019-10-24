import os
import sys
import shutil
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QDialog, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTextEdit
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

def cpnt(text):
    print('[>] ' + text)

cpnt('Test Message. Will be used for pre-qt messages in the future.')
cpnt('Test Message 2.')

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
        metadata_btn.clicked.connect(self.metadata_editor)
        metadata_btn.resize(150,50)
        metadata_btn.move(25,87.5)

        export_btn = QPushButton('Export', self)
        export_btn.clicked.connect(self.icon_manager)
        export_btn.resize(150,50)
        export_btn.move(25,150)
        


    def icon_manager(self):
        self.icon_manager_win = IconManager()
        self.icon_manager_win.show()
    
    def metadata_editor(self):
        self.metadata_editor_win = MetaEditor()
        self.metadata_editor_win.show()

class IconManager(QDialog):
    def __init__(self):
        QMainWindow.__init__(self)
        if not os.path.isdir('IconBundles'):
            os.mkdir('IconBundles/')

        self.setMinimumSize(QSize(350, 300))  
        self.selectedItem = None  
        self.setWindowTitle("Icon Manager")

        self.icon_list = IconList(self)
        self.icon_list.resize(250,300)
        self.icon_list.itemClicked.connect(self.item_options)
        self.icon_list.item
        self.icon_list.move(25,25)

        ok_btn = QPushButton('Ok', self)
        ok_btn.resize(150,50)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton('Cancel', self)
        cancel_btn.resize(150,50)
        cancel_btn.clicked.connect(self.accept)

        add_btn = QPushButton('Add...', self)
        add_btn.resize(150,100)
        add_btn.clicked.connect(self.add_image)

        self.edit_btn = QPushButton('Edit', self)
        self.edit_btn.resize(150,100)
        self.edit_btn.setDisabled(True)

        self.remove_btn = QPushButton('Remove', self)
        self.remove_btn.resize(150,100)
        self.remove_btn.setDisabled(True)
        self.remove_btn.clicked.connect(self.remove_image)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.icon_list, 0, 0, 7, 4)
        grid.addWidget(ok_btn, 8, 0)
        grid.addWidget(cancel_btn, 8, 1)
        grid.addWidget(add_btn, 1, 4, 1, 1)
        grid.addWidget(self.edit_btn, 3, 4, 1, 1)
        grid.addWidget(self.remove_btn, 5, 4, 1, 1)

        self.setLayout(grid)

        oImage = QImage("background_2.png")
        sImage = oImage.scaled(QSize(500,300))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
    
    def item_options(self, item):
        print(item)
        self.selectedItem = item
        self.edit_btn.setDisabled(False)
        self.remove_btn.setDisabled(False)

    def add_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filepath, _ = QFileDialog.getOpenFileName(self,"Select Theme Icons", "","PNG Icons (*.png)", options=options)
        shutil.copyfile(filepath, 'IconBundles/' + filepath.split('/')[-1])
        thumb = QIcon()
        thumb.addPixmap(QPixmap('IconBundles/' + filepath.split('/')[-1]), QIcon.Normal)
        self.icon_list.addItem(QListWidgetItem(thumb,filepath.split('/')[-1]))
    
    def remove_image(self):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to permanently delete ' + self.selectedItem.text() + '?', QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            os.remove('IconBundles/' + self.selectedItem.text())
            self.icon_list.takeItem(self.icon_list.row(self.selectedItem))

class MetaEditor(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        self.setMinimumSize(QSize(300, 400))
        self.setWindowTitle("Metadata Editor")

        self.package = QLabel('Package', self)
        self.package_entry = QLineEdit()
        self.name = QLabel('Theme Name', self)
        self.name_entry = QLineEdit()
        self.version = QLabel('Version', self)
        self.version_entry = QLineEdit()
        self.author = QLabel('Author', self)
        self.author_entry = QLineEdit()
        self.description = QLabel('Description', self)
        self.description_entry = QLineEdit()
        self.ld = QLabel('Long Desc.', self)
        self.ld.setWordWrap(True)
        self.ld_entry = QTextEdit()

        ok_btn = QPushButton('Ok', self)
        ok_btn.resize(150,50)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton('Cancel', self)
        cancel_btn.resize(150,50)
        cancel_btn.clicked.connect(self.accept)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.package, 0, 0)
        grid.addWidget(self.package_entry, 0, 1, 1, 3)
        grid.addWidget(self.name, 1, 0)
        grid.addWidget(self.name_entry, 1, 1, 1, 3)
        grid.addWidget(self.version, 2, 0)
        grid.addWidget(self.version_entry, 2, 1, 1, 3)
        grid.addWidget(self.author, 3, 0)
        grid.addWidget(self.author_entry, 3, 1, 1, 3)
        grid.addWidget(self.description, 4, 0)
        grid.addWidget(self.description_entry, 4, 1, 1, 3)
        grid.addWidget(self.ld, 5, 0, 3, 3)
        grid.addWidget(self.ld_entry, 5, 1, 3, 3)
        grid.addWidget(ok_btn, 8, 2)
        grid.addWidget(cancel_btn, 8, 3)

        oImage = QImage("background_3.png")
        sImage = oImage.scaled(QSize(500,500))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.setLayout(grid)

        self.show()
        


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