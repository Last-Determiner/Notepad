
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPainter







class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1226, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("QTextEdit {"
                                    "    background-color: rgba(0, 0, 0, 255); /* Semi-transparent white background */"
                                    "    color: #FFFFFF; /* Black text */"
                                    "    border-radius: 10px; /* Add border radius for rounded corners */"
                                    "    padding: 5px; /* Add padding */"
                                    "}"
                                    "")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1226, 21))
        self.menubar.setObjectName("menubar")
        #=================== Find ===============================
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFind = QtWidgets.QMenu(self.menubar)
        self.menuFind.setObjectName("menuFind")
        self.menuFind.aboutToShow.connect(self.Findeverything)
        #================== Looks ===============================
        self.menuSize = QtWidgets.QMenu(self.menubar)
        self.menuSize.setObjectName("menuSize")
        self.menuSize.aboutToShow.connect(self.size_up)
        self.menuSize_2 = QtWidgets.QMenu(self.menubar)
        self.menuSize_2.setObjectName("menuSize_2")
        self.menuSize_2.aboutToShow.connect(self.size_down)
        self.menuDay_Night = QtWidgets.QMenu(self.menubar)
        self.menuDay_Night.setObjectName("menuDay_Night")
        self.menuDay_Night.aboutToShow.connect(self.theme_bright)
        self.menuDay_Night.aboutToHide.connect(self.theme_dark)
        MainWindow.setMenuBar(self.menubar)
        #====================== Actions ========================
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.triggered.connect(self.SaveFile)
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.triggered.connect(self.SaveFileAs)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionLoad.triggered.connect(self.LoadFile)
        self.actionPrint = QtWidgets.QAction(MainWindow)
        self.actionPrint.setObjectName("actionPrint")
        self.actionPrint.triggered.connect(self.print_preview)

        #================ Main Menus =========================
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPrint)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuFind.menuAction())
        self.menubar.addAction(self.menuSize.menuAction())
        self.menubar.addAction(self.menuSize_2.menuAction())
        self.menubar.addAction(self.menuDay_Night.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def SaveFileAs(self):
        File, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save As", "", "*.txt")
        if File:
            text_content = self.textEdit.toPlainText()
            with open(File, "w") as file:
                file.write(text_content)
    def SaveFile(self):
        text_content = self.textEdit.toPlainText()
        if hasattr(self,"File"):
            with open(self.File,"w") as file:
                file.write(text_content)
        else:
            self.SaveFileAs()

    def print_preview(self):
        printer = QPrinter()
        print_dialog = QPrintDialog(printer)

        if print_dialog.exec_():
            text = self.textEdit.toPlainText()
            painter = QPainter(printer)  # Create a painter object for the printer
            painter.setFont(self.textEdit.font())  # Set font to match the QTextEdit
            painter.drawText(printer.pageRect(), QtCore.Qt.AlignLeft, text)  # Draw the text on the printer page
            painter.end()



    def handle_print_finished(self):
        # Handle successful or failed printing (optional)
        print("Printing finished")
    def size_down(self):
        font = self.textEdit.font()
        current_size = font.pointSize()
        new_size = max(current_size - 5, 5)
        font.setPointSize(new_size)
        self.textEdit.setFont(font)

    def size_up(self):
        font = self.textEdit.font()
        current_size = font.pointSize()
        new_size = min(current_size + 5, 72)
        font.setPointSize(new_size)
        self.textEdit.setFont(font)
    def theme_bright(self):
        self.textEdit.setStyleSheet("QTextEdit {"
                                    "    background-color: rgba(255, 255, 255, 255); /* Semi-transparent white background */"
                                    "    color: #000000; /* Black text */"
                                    "    border-radius: 10px; /* Add border radius for rounded corners */"
                                    "    padding: 5px; /* Add padding */"
                                    "}"
                                    "")
    def theme_dark(self):
        self.textEdit.setStyleSheet("QTextEdit {"
                                    "    background-color: rgba(0, 0, 0, 255); /* Semi-transparent white background */"
                                    "    color: #FFFFFF; /* Black text */"
                                    "    border-radius: 10px; /* Add border radius for rounded corners */"
                                    "    padding: 5px; /* Add padding */"
                                    "}"
                                    "")
    def Findeverything(self):
        text_to_find, ok = QtWidgets.QInputDialog.getText(None, "Find", "Enter text to find:")
        if ok:
            cursor = self.textEdit.document().find(text_to_find)
            if not cursor.isNull():
                cursor.select(QtGui.QTextCursor.WordUnderCursor)
                self.textEdit.setTextCursor(cursor)
                self.textEdit.setFocus()

                reply = QtWidgets.QMessageBox.question(None, "Find Next", "Find next occurrence?",
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                while reply == QtWidgets.QMessageBox.Yes:
                    cursor = self.textEdit.document().find(text_to_find, cursor)
                    if not cursor.isNull():
                        cursor.select(QtGui.QTextCursor.WordUnderCursor)
                        self.textEdit.setTextCursor(cursor)
                        self.textEdit.setFocus()

                        reply = QtWidgets.QMessageBox.question(None, "Find Next", "Find next occurrence?",
                                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    else:
                        reply = QtWidgets.QMessageBox.information(None, "Not Found", "No more occurrences found.")
            else:
                QtWidgets.QMessageBox.information(None, "Not Found", "Text not found.")

    def LoadFile(self):
        File, _ = QtWidgets.QFileDialog.getOpenFileName(None,"load it nooow","","*txt")
        if File:
            with open(File,"r") as file:
                text = file.read()
                self.textEdit.setText(text)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuFind.setTitle(_translate("MainWindow", "Find"))
        self.menuSize.setTitle(_translate("MainWindow", "Size +"))
        self.menuSize_2.setTitle(_translate("MainWindow", "Size -"))
        self.menuDay_Night.setTitle(_translate("MainWindow", "Day / Night"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionPrint.setText(_translate("MainWindow", "Print"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
