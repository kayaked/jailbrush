import os
import sys
import requests
import time
import paramiko
import threading
import traceback
import shutil
import subprocess
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QDialog, QFileDialog, QMessageBox, QProgressBar
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTextEdit, QTabWidget
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QIcon
from PyQt5.QtCore import QSize
from textwrap import wrap

def console_text():
    text = """
   ___       _ _ _                    _           _--|
  |_  |     (_) | |                  | |         |   |
    | | __ _ _| | |__  _ __ _   _ ___| |__       |_--
    | |/ _` | | | '_ \| '__| | | / __| '_ \     / /
/\__/ / (_| | | | |_) | |  | |_| \__ \ | | |   / /
\____/ \__,_|_|_|_.__/|_|   \__,_|___/_| |_|  |_/

    """.strip('\n')
    print(text)

INFO_PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>IB-MaskIcons</key>
	<true/>
</dict>
</plist>"""

console_text()

def cpnt(text):
    print('[>] ' + text)

current_project_name = 'New Theme 1'

project_list = [folder for folder in os.listdir() if folder.endswith('.theme')]
if project_list:
    current_project_name = project_list[0].split('.')[0]

cpnt('Checking directory for Debian Structure.')
if not os.path.isdir(f'{current_project_name}.theme'):
    cpnt(f'Creating directory :/{current_project_name}.theme/')
    os.mkdir(f'{current_project_name}.theme')

if not os.path.isdir(f'{current_project_name}.theme/Library'):
    cpnt(f'Creating directory :/{current_project_name}.theme/Library/')
    os.mkdir(f'{current_project_name}.theme/Library')

if not os.path.isdir(f'{current_project_name}.theme/DEBIAN'):
    cpnt(f'Creating directory :/{current_project_name}.theme/DEBIAN/')
    os.mkdir(f'{current_project_name}.theme/DEBIAN')

if not os.path.isdir(f'{current_project_name}.theme/Library/Themes/'):
    cpnt(f'Creating directory :/{current_project_name}.theme/Library/Themes/')
    os.mkdir(f'{current_project_name}.theme/Library/Themes')

if not os.listdir(f'{current_project_name}.theme/Library/Themes/'):
    os.mkdir(f'{current_project_name}.theme/Library/Themes/{current_project_name}.theme')
else:
    current_project_name =  os.listdir(f'{current_project_name}.theme/Library/Themes')[0].split('.')[0]

cpnt('Found theme directory.')
cpnt('Current theme name is "' + current_project_name.upper() + '".')

def project_path():
    return f'{current_project_name}.theme/Library/Themes/' + current_project_name + '.theme/'

if not os.path.isfile(project_path() + 'Info.plist'):
    with open(project_path() + 'Info.plist', 'w+') as fp:
        fp.write(INFO_PLIST)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setFixedSize(QSize(200, 287.5))
        self.setWindowTitle("Jailbrush 🖌")

        oImage = QImage("background/background.png")
        sImage = oImage.scaled(QSize(300,262.5))
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
        export_btn.clicked.connect(self.export_editor)
        export_btn.resize(150,50)
        export_btn.move(25,150)

        export_btn = QPushButton('Install', self)
        export_btn.clicked.connect(self.sftp_installer)
        export_btn.resize(150,50)
        export_btn.move(25,212.5)

    def sftp_installer(self):
        self.sftp_installer = SSHInstall()

    def icon_manager(self):
        self.icon_manager_win = IconManageMain()
        self.icon_manager_win.show()

    def metadata_editor(self):
        self.metadata_editor_win = MetaEditor()
        self.metadata_editor_win.show()

    def export_editor(self):
        self.export_editor_win = ExportLoader()

class IconManageMain(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # one option here to set size constraints between these two
        self.setMinimumSize(QSize(300, 300))
        self.setMaximumSize(QSize(500,300))
        # or you could just lock in the size and they cant resize at all
        #self.setFizedSize(QSize(300,500))
        if not os.path.isdir(project_path() + 'IconBundles'):
            os.mkdir(project_path() + 'IconBundles/')
        self.setWindowTitle("Icon Manager")

        oImage = QImage("background/background_2.png")
        sImage = oImage.scaled(QSize(500,300))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        self.tabs = QTabWidget()
        self.tab1 = IconManager(self)
        self.tab2 = ClockManager(self)
        self.tabs.addTab(self.tab1,"General")
        self.tabs.addTab(self.tab2,"Clock")
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.tabs, 0, 0)
        self.setLayout(grid)

class ClockManager(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

class IconManager(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.selectedItem = None

        self.icon_list = IconList(self)
        self.icon_list.resize(250,300)
        self.icon_list.itemClicked.connect(self.item_options)
        self.icon_list.item
        self.icon_list.move(25,25)

        ok_btn = QPushButton('OK', self)
        ok_btn.resize(150,50)
        ok_btn.clicked.connect(parent.accept)

        add_btn = QPushButton('Add...', self)
        add_btn.resize(150,100)
        add_btn.clicked.connect(self.add_image)

        self.edit_btn = QPushButton('Edit...', self)
        self.edit_btn.resize(150,100)
        self.edit_btn.setDisabled(True)
        self.edit_btn.clicked.connect(self.edit_image)

        self.remove_btn = QPushButton('Remove', self)
        self.remove_btn.resize(150,100)
        self.remove_btn.setDisabled(True)
        self.remove_btn.clicked.connect(self.remove_image)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.icon_list, 0, 0, 7, 4)
        grid.addWidget(ok_btn, 8, 0, 1, 6)
        grid.addWidget(add_btn, 1, 4, 1, 1)
        grid.addWidget(self.edit_btn, 3, 4, 1, 1)
        grid.addWidget(self.remove_btn, 5, 4, 1, 1)

        self.setLayout(grid)

    def item_options(self, item):
        self.selectedItem = item
        self.edit_btn.setDisabled(False)
        self.remove_btn.setDisabled(False)

    def add_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filepath, _ = QFileDialog.getOpenFileName(self,"Select Theme Icons", "","PNG Icons (*.png)", options=options)
        shutil.copyfile(filepath, project_path() + 'IconBundles/' + filepath.split('/')[-1])
        thumb = QIcon()
        thumb.addPixmap(QPixmap(project_path() + 'IconBundles/' + filepath.split('/')[-1]), QIcon.Normal)
        self.icon_list.addItem(QListWidgetItem(thumb,filepath.split('/')[-1]))

    def remove_image(self):
        reply = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to permanently delete ' + self.selectedItem.text() + '?', QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            os.remove(project_path() + 'IconBundles/' + self.selectedItem.text())
            self.icon_list.takeItem(self.icon_list.row(self.selectedItem))

    def edit_image(self):
        self.iconsubeditor = IconSubEditor(self.selectedItem)
        self.iconsubeditor.show()

class SSHInstall(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        self.setFixedSize(500, 100)
        self.setWindowTitle("SSH Installer")

        self.ip = QLineEdit()
        self.ip.setPlaceholderText('IP Address')
        self.pw = QLineEdit()
        self.pw.setEchoMode(QLineEdit.Password)
        self.pw.setPlaceholderText('Password (default is alpine)')
        self.install = QPushButton('Install')
        self.install.clicked.connect(self.connect_and_install)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.ip, 0, 0)
        grid.addWidget(self.pw, 0, 1)
        grid.addWidget(self.install, 1, 0, 1, 2)
        self.setLayout(grid)

        self.show()

    def connect_and_install(self):
        self.exporter = ExportLoader(install=True, credentials={'hostname': self.ip.text(), 'port': 22, 'username': 'root', 'password': self.pw.text()})


class MetaEditor(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        self.setFixedSize(QSize(500, 500))
        self.setWindowTitle("Metadata Editor")

        self.package = QLabel('Package ID', self)
        self.package_entry = QLineEdit()
        self.package_entry.setPlaceholderText('com.example.theme (auto-generates!)')
        self.name = QLabel('Theme Name', self)
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText('Stacks')
        self.version = QLabel('Version', self)
        self.version_entry = QLineEdit()
        self.version_entry.setPlaceholderText('1.1')
        self.author = QLabel('Author', self)
        self.author_entry = QLineEdit()
        self.author_entry.setPlaceholderText('Luminant Design')
        self.description = QLabel('Description', self)
        self.description_entry = QLineEdit()
        self.description_entry.setPlaceholderText('A new outlook on your icons.')
        self.ld = QLabel('Long Desc.', self)
        self.ld.setWordWrap(True)
        self.ld_entry = QTextEdit()
        self.ld_entry.setPlaceholderText('Stacks brings a new outlook to your device, handcrafted by the Aceruos team to feature a stacked effect for your icons.')

        if os.path.isfile(f'{current_project_name}.theme/DEBIAN/control'):
            with open(f'{current_project_name}.theme/DEBIAN/control', 'r') as fp:
                controllines = [line.strip() for line in fp.readlines()]
                for line in controllines:
                    if line.startswith('Package: '): self.package_entry.setText(line.split(': ', 1)[-1])
                    if line.startswith('Name: '): self.name_entry.setText(line.split(': ', 1)[-1])
                    if line.startswith('Version: '): self.version_entry.setText(line.split(': ', 1)[-1])
                    if line.startswith('Author: '): self.author_entry.setText(line.split(': ', 1)[-1])
                    if line.startswith('Description: '): self.description_entry.setText(line.split(': ', 1)[-1])

        ok_btn = QPushButton('OK', self)
        ok_btn.resize(150,50)
        ok_btn.clicked.connect(self.controlfile)

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

        oImage = QImage("background/background_3.png")
        sImage = oImage.scaled(QSize(500,500))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.setLayout(grid)

        self.show()

    def autopackageid(self):
        pass

    def controlfile(self):
        global current_project_name
        name = self.name_entry.text()
        os.rename(current_project_name + '.theme', name + '.theme')
        current_project_name = name
        os.rename(f'{name}.theme/Library/Themes/' + os.listdir(f'{name}.theme/Library/Themes/')[0], f'{name}.theme/Library/Themes/{name}.theme')

        control = open(f"{current_project_name}.theme/DEBIAN/control", 'w+')
        control.write(f'Package: {self.package_entry.text()}\n')
        control.write(f'Name: {self.name_entry.text()}\n')
        control.write(f'Version: {self.version_entry.text()}\n')
        control.write(f'Architecture: iphoneos-arm\n')
        long_desc = ''.join([" " + line + "\n" for line in wrap(self.ld_entry.toPlainText(), 30)])
        control.write(f'Description: {self.description_entry.text()}\n{long_desc}')
        control.write(f'Maintainer: {self.author_entry.text()}\n')
        control.write(f'Author: {self.author_entry.text()}\n')
        control.write('Section: Themes\n')
        control.write('Depends: com.anemonetheming.anemone\n')
        control.close()
        self.accept()

class IconSubEditor(QDialog):
    def __init__(self, item):
        QDialog.__init__(self)

        self.setMinimumSize(QSize(450, 400))
        self.icon = item
        self.setWindowTitle(f"Icon Editor - {item.text()}")
        self.rate_lim = time.time()
        self.selectedItem = None

        oImage = QImage("background/background_4.png")
        sImage = oImage.scaled(QSize(500,400))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        grid = QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)
        self.idlist = QListWidget(self)
        self.idlist.itemClicked.connect(self.item_options)
        self.appname = QLineEdit(self)
        self.appname.setPlaceholderText('App Name (e.g. Fruit Ninja)')
        grid.addWidget(self.appname, 0, 0, 1, 3)
        grid.addWidget(self.idlist, 1, 0, 2, 4)

        self.search = QPushButton('Search', self)
        self.search.resize(150,50)
        self.search.clicked.connect(self.request)
        grid.addWidget(self.search, 0, 3)

        self.bundleid = QLineEdit(self)
        self.bundleid.setPlaceholderText('Bundle ID (auto-fills!)')
        grid.addWidget(self.bundleid, 3, 0, 1, 4)

        self.ok_btn = QPushButton('OK', self)
        self.ok_btn.resize(150,50)
        self.ok_btn.clicked.connect(self.savename)
        self.ok_btn.setDisabled(True)
        grid.addWidget(self.ok_btn, 4, 2, 1, 1)

        cancel_btn = QPushButton('Cancel', self)
        cancel_btn.resize(150,50)
        cancel_btn.clicked.connect(self.accept)
        grid.addWidget(cancel_btn, 4, 3, 1, 1)
        self.show()

    def request(self):
        text = self.appname.text()
        self.idlist.clear()
        cpnt(text)
        rl = time.time()
        if rl-self.rate_lim <0.5:
            return
        self.rate_lim = time.time()
        response = requests.get("https://itunes.apple.com/search?term=" + text + "&entity=software&limit=25")
        if response.status_code != 200:
            cpnt(f'Error occurred in request. Temporary non-qt error message, we apologize for the inconvenience. (e.c. {response.status_code})')
        response = response.json()['results']
        for item in response:
            self.idlist.addItem(QListWidgetItem(item['trackCensoredName'][:25] + ' | ' + item['bundleId']))

    def savename(self):
        new = self.bundleid.text()
        os.rename(project_path() + 'IconBundles/' + self.icon.text(), project_path() + 'IconBundles/' + new + '.png')
        self.accept()

    def item_options(self, item):
        self.bundleid.setText(item.text().split(' | ')[-1])
        self.selectedItem = item
        self.ok_btn.setDisabled(False)

class ExportLoader(QDialog):
    def __init__(self, **kwargs):
        QDialog.__init__(self)

        self.install = bool(kwargs.get('install'))

        self.setFixedSize(QSize(400, 150))
        self.setWindowTitle(f"Exporting {current_project_name}.deb")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

        grid = QGridLayout()
        grid.setSpacing(10)

        self.setLayout(grid)

        self.progress = QProgressBar(self)
        self.status = QLabel("Jailbrush Exporter 0.1.1 by github.com/kayaked")
        self.status.setAlignment(QtCore.Qt.AlignCenter)

        grid.addWidget(self.progress, 1, 0, 2, 1)
        grid.addWidget(self.status, 0, 0, 1, 1)

        oImage = QImage("background/background_5.png")
        sImage = oImage.scaled(QSize(400,150))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.show()

        self.gui_prog('Checking for directory ./')
        if not os.path.isdir(current_project_name + '.theme/'):
            QMessageBox.critical(self, 'Exporting Error', 'Project directory not found!', QMessageBox.Ok)
            self.accept()

        self.gui_prog('Checking for directory ./DEBIAN/')
        if not os.path.isdir(current_project_name + '.theme/DEBIAN/'):
            QMessageBox.critical(self, 'Exporting Error', 'DEBIAN directory not found (try using the info editor)!', QMessageBox.Ok)
            self.accept()

        self.gui_prog('Checking for directory ./Library/')
        if not os.path.isdir(current_project_name + '.theme/Library/'):
            QMessageBox.critical(self, 'Exporting Error', 'Library directory not found!', QMessageBox.Ok)
            self.accept()

        self.gui_prog('Checking operating system')
        if os.name == 'nt':
            QMessageBox.critical(self, 'Exporting Error', 'Windows is currently not support by Jailbrush. Please wait for future updates or official releases on our GitHub.', QMessageBox.Ok)
            self.accept()

        self.gui_prog('Packaging and saving')
        test = subprocess.Popen(["dpkg-deb", "-bZlzma", "./{}.theme".format(current_project_name), "./"], stdout=subprocess.PIPE)
        output = str(test.communicate()[0])
        cpnt(output)
        debname = output.split("'")[:-1][-1]

        if self.install == True:
            self.gui_prog('Creating client')
            try:
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.WarningPolicy)
                self.gui_prog('Connecting to host')
                client.connect(**kwargs.get('credentials'))
                self.gui_prog('Opening SFTP session')
                sftp = client.open_sftp()
                self.gui_prog('Copying DEB')
                sftp.put(debname, '/var/mobile/Documents/' + debname)
                self.gui_prog('Installing')
                stdin, stdout, stderr = client.exec_command('dpkg -i /var/mobile/Documents/' + debname)
                for line in stdout.read().decode().split('\n'):
                    cpnt(line)
                cpnt('Successfully installed! Respringing...')
                client.exec_command('killall -9 SpringBoard')
            except Exception as e:
                traceback.print_exc()
                cpnt('Uncaught error. Please wait for a future update to Jailbrush for more information.')
            finally:
                client.close()
                del sftp


        QMessageBox.information(self, 'Exporter', 'Successfully exported to the package "{}".'.format(debname))
        self.accept()

    def gui_prog(self, text):
        self.status.setText(text)
        offset = 20
        if self.install:
            offset = 10
        self.progress.setValue(self.progress.value() + offset)

class IconList(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        self.parent = parent
        icons = [icon for icon in os.listdir(project_path() + 'IconBundles') if icon.endswith('.png')]
        for icon in icons:
            thumb = QIcon()
            thumb.addPixmap(QPixmap(project_path() + 'IconBundles/' + icon), QIcon.Normal)
            self.addItem(QListWidgetItem(thumb, icon))
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
