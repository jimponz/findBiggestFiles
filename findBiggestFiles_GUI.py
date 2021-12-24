import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTimer,Qt

from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtWidgets import QApplication, QWidget,QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QFileDialog
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QListWidget


qtcreator_file  = "findBiggestFiles.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class File:
    path = ""
    size = 0

    def format_bytes(self,size):
        # 2**10 = 1024
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return str(round(size,2)) + " " + power_labels[n]+'B'
    
    def __init__(self,path):
        if os.path.isfile(path):
            self.path = path
            self.size = os.stat(path).st_size
        
    def __str__(self):
        return "\nPath: " + self.path + "\nSize: " + self.format_bytes(self.size)



class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    input_dir = os.getcwd()
    selected = ""
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.listWidget.itemClicked.connect(self.onClicked)

        self.buttonFolder.clicked.connect(self.onClickFolder)
        self.buttonDelete.clicked.connect(self.onClickDelete)
        
        self.buttonDirChooser.clicked.connect(self.choose_dir)
        self.buttonRefresh.clicked.connect(self.inspect_dir)
        
        self.labelPath.setText(self.input_dir)
        self.labelStatus.setText("Status: Pronto!")

        self.inspect_dir(self.input_dir)


    def onClicked(self,item):
        #QMessageBox.information(self, "Info", item.text())
        self.selected = item.text()
        self.labelSelected.setText(self.selected)

    def onClickDelete(self):
        try:
            filepath = self.selected.split("\t")[1]
            ret = QMessageBox.question(self, 'Stai per cancellare dei file!', "Stai per cancellare " + filepath + " , vuoi procedere?", QMessageBox.Yes | QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                print('Button QMessageBox.Yes clicked.')
                os.remove(filepath)
                self.labelStatus.setText(filepath + " eliminato!")
               
        except Exception as ex:
            print("\nSi è verificata un'eccezione", ex)

    def onClickFolder(self):
        try:
            filepath = self.selected.split("\t")[1]
            head, tail = os.path.split(filepath)
            os.startfile(head)
        except Exception as ex:
            print("\nSi è verificata un'eccezione", ex)

            
    listOfFiles = []    
    def inspect_dir(self, input_dir):
        contFile = 0
        dirSize = 0
        
        # carica nomi file da cartella
        if os.path.isdir(input_dir):
            self.listWidget.clear()
            
            message = "Status: Analizzando la cartella " + input_dir
            print(message)
            self.labelStatus.setText(message)
            
            for root,d_names,f_names in os.walk(input_dir):
                for fi in f_names:
                    try:
                        filename = os.path.join(root, fi)
                        
                        file = File(filename)
                        dirSize += file.size
                        self.listOfFiles.append(file)
                        
                        contFile += 1
                    except Exception as err:
                        message = "Errore analizzando il file: " + filename + "Si è verificata un'eccezione: " + str(err)
                        print(message)
                        self.labelStatus.setText(message)

            self.listOfFiles.sort(key=lambda x: x.size, reverse=True)
            for f in self.listOfFiles:
                self.listWidget.addItem(str(f.format_bytes(f.size)) + "\t" + f.path)

                    
            self.labelStatus.setText("Status: Pronto!")
            message = "Nella cartella attuale (" + File.format_bytes(self,dirSize) + ") sono presenti i seguenti " + str(contFile) + " file:"
            self.labelList.setText(message)
            if contFile == 0:
                self.listWidget.clear()
                self.listWidget.addItem("Non è stato trovato nessun file! Controlla il percorso di lavoro!")
                self.labelStatus.setText("Status: Non è stato trovato nessun file!")


    def choose_dir(self):
        try:
            self.input_dir = QFileDialog.getExistingDirectory(self, "Scegli la cartella che vuoi decriptare", self.input_dir)
            self.labelPath.setText(self.input_dir)

            self.inspect_dir(self.input_dir)
            
        except Exception as ex:
            message = "Errore analizzando il file: " + filename + str("Si è verificata un'eccezione:", err)
            print(message)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())