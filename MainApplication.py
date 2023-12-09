import sys
import random
import string
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QPainter, QLinearGradient, QColor, QFont, QGuiApplication
from PyQt6.QtWidgets import QPushButton, QLabel, QLineEdit, QWidget, QApplication, QSlider, QCheckBox

class MainApplication(QWidget):
    # Constructor
    def __init__(self):
        super(MainApplication, self).__init__()

        self.defaultButtonStyle = """
            .QPushButton {  
                border: 1px solid transparent;
                border: none;
                border-radius: 15px;
                color: rgb(44, 62, 80);
                background-color: rgb(46, 134, 193);
            }

            .QPushButton:hover {
                color:white;
                background-color: rgb(52, 152, 219);
            }

            .QPushButton:pressed {
                color:white;
                background-color: rgb(93, 173, 226);
            }
        """

        self.buttonStyleCopy = """
        .QPushButton {
            border: 1px solid  transparent;
            border: none;
            border-radius: 15px;
            color: rgb(248, 249, 249);
            background-color: rgb(88, 214, 141);
        }
        """

        # Load template
        uic.loadUi('Templates/MainForm.ui',self)

        # Search and set properties
        self.QLineEditFont = QFont()
        self.QLineEditFont.setPointSize(14)
        self.QLineEditFont.setBold(True)
        self.QLineEditFont.setFamily("Century Gothic")

        self.QPusButtonFont = QFont()
        self.QPusButtonFont.setPointSize(11)
        self.QPusButtonFont.setBold(True)
        self.QPusButtonFont.setFamily("Century Gothic")

        self.QCheckFont = QFont()
        self.QCheckFont.setPointSize(10)
        self.QCheckFont.setFamily("Century Gothic")

        self.LblTwo = self.findChild(QLabel, 'LblTwo')
        self.LblTwo.setFont(self.QLineEditFont)

        self.LblLenght = self.findChild(QLabel, 'LblLenght')
        self.LblLenght.setFont(self.QLineEditFont)

        self.SlidePassword = self.findChild(QSlider, 'SlidePassword')
        self.SlidePassword.valueChanged.connect(self.Display)
        self.SlidePassword.setSingleStep(2)
        self.SlidePassword.setValue(2)

        self.textPassword = self.findChild(QLineEdit, 'textPassword')
        self.textPassword.setFont(self.QLineEditFont)

        self.BtnGeneratePassword = self.findChild(QPushButton, 'BtnGeneratePassword')
        self.BtnGeneratePassword.clicked.connect(self.SetPassWord)
        
        self.BtnGeneratePassword.setFont(self.QPusButtonFont)

        self.BtnCopyPassword = self.findChild(QPushButton, 'BtnCopyPassword')
        self.BtnCopyPassword.clicked.connect(self.CopyPassword)
        self.BtnCopyPassword.setFont(self.QPusButtonFont)

        # Load QCheck Boxes
        self.CheckUppercase = self.findChild(QCheckBox, 'CheckUppercase')
        self.CheckUppercase.setChecked(True)
        self.CheckUppercase.setFont(self.QCheckFont)
        
        self.CheckLowercase = self.findChild(QCheckBox, 'CheckLowercase')
        self.CheckLowercase.setChecked(True)
        self.CheckLowercase.setFont(self.QCheckFont)
        
        self.CheckNumers = self.findChild(QCheckBox, 'CheckNumers')
        self.CheckNumers.setChecked(True)
        self.CheckNumers.setFont(self.QCheckFont)

        self.CheckSimbols = self.findChild(QCheckBox, 'CheckSimbols')
        self.CheckSimbols.setChecked(True)
        self.CheckSimbols.setFont(self.QCheckFont)

        self.SetPassWord()


    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0 , 0 , 0, self.height())
        gradient.setColorAt(0, QColor(170, 75, 107))
        gradient.setColorAt(0.5, QColor(107, 107, 131))
        gradient.setColorAt(1, QColor(59, 141, 153))
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

    def SetPassWord(self):
        defaultPasswordLength = self.SlidePassword.value()

        if(self.SlidePassword.value() != defaultPasswordLength):
            # Get custom length from slide
            customPasswordLength = self.SlidePassword.value()
            # Generate password
            passwordResult = self.GeneratePassword(customPasswordLength)
            # Set password
            self.textPassword.setText(passwordResult)

        # Generate password
        passwordResult = self.GeneratePassword(defaultPasswordLength)
        # Set password
        self.textPassword.setText(passwordResult)

    def GeneratePassword(self, length):
        upperletters = string.ascii_uppercase
        lowerletters = string.ascii_lowercase
        specialCharacters = ['!', '@', '#', '$', '%', '&', '*','?', '/', ':']
        numberList = ['0','1','2','3','4','5','6','7','8','9']
        checkBoxKeystChecked = []
        passWordResult = ''

         # Get QCheckBox list
        for child in self.findChildren(QCheckBox):
            if(child.isChecked()):
                checkBoxKeystChecked.append(child.objectName())

        passWordOptions = {
            self.CheckLowercase.objectName() : ''.join(random.choice(lowerletters) for _ in range(length)),
            self.CheckUppercase.objectName() : ''.join(random.choice(upperletters) for _ in range(length)),
            self.CheckNumers.objectName() : ''.join(random.choice(numberList) for _ in range(length)),
            self.CheckSimbols.objectName() : ''.join(random.choice(specialCharacters) for _ in range(length))
        }

        for key, value in passWordOptions.items():
            if(key) in checkBoxKeystChecked:
                passWordResult += value

        return passWordResult
        
    def CopyPassword(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.textPassword.text())

        self.SetCopiedStyle()
        QtCore.QTimer.singleShot(1000,self.ResetButtonStyle)

    def SetCopiedStyle(self):
        self.BtnCopyPassword.setText('Copied!')
        self.BtnCopyPassword.setStyleSheet(self.buttonStyleCopy)
    
    def ResetButtonStyle(self):
        self.BtnCopyPassword.setStyleSheet(self.defaultButtonStyle)
        self.BtnCopyPassword.setText('Copy')

    def Display(self):
        self.LblLenght.setText(str(self.sender().value()) + ' by Option')

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainApplication()

    window.show()

    app.exec()