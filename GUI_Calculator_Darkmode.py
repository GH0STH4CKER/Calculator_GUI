import sys
from PyQt5 import QtCore,QtGui
from decimal import Decimal, ROUND_HALF_UP
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QPalette, QColor 

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setLayout(QVBoxLayout())
        self.last_pressed = []
        
        # Create the input field
        self.input_field = QLineEdit()
        self.input_field.setReadOnly(True)
        self.input_field.setAlignment(QtCore.Qt.AlignRight)   # Set alignment to right
        self.input_field.setText('0')
        self.layout().addWidget(self.input_field)
        
        # Create the buttons
        buttons = [
            ['7', '8', '9', '÷'],
            ['4', '5', '6', '×'],
            ['1', '2', '3', '−'],
            ['0', '00', '.', '+'],
            ['C', '+/-', '=', '%']
        ]
        
        grid_layout = QGridLayout()
        
        for row, button_row in enumerate(buttons):
            for col, button_label in enumerate(button_row):
                button = QPushButton(button_label)
                button.clicked.connect(self.button_clicked)
                button.setObjectName("calculatorButton")
                # Add a separate selector for mathematical symbols buttons
                if button_label in ['÷', '×', '−', '+', '+/-', '=', '%','C']:
                    button.setObjectName("mathButton")
                grid_layout.addWidget(button, row, col)
        
        self.layout().addLayout(grid_layout)
        
        self.current_value = ''
        
        # Set the colors and styles
        self.setStyleSheet('''
            QPushButton#calculatorButton {
                background-color: #FFA500;
                color: white;
                font-size: 20px;
                padding: 10px;
                border-radius: 22px;
            }
            QWidget {
                background-color: #555555;
            }
            QLineEdit {
                background-color: #222222;
                color: white;
                font-size: 24px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton#mathButton {
                background-color: #dddddd;
                color: #FFA500;
                font-size: 20px;
                padding: 10px;
                border-radius: 22px;
            }
            QPushButton#mathButton:hover {
                background-color: #ffffff;
            }
            QPushButton#mathButton:pressed {
                background-color: #777777;
            }
            QPushButton#calculatorButton:hover {
                background-color: #ffb300;
            }

            QPushButton#calculatorButton:pressed {
                background-color: #735a1f;
            }
        ''')
    # Check if there is consecutive symbols
    def symbdup(self,text):
        if text in ['+', '-', '*', '/']:
                
            if len(self.current_value) > 0 and self.current_value[-1] in ['+', '-', '*', '/']:
                # Replace the last entered symbol with the new symbol
                self.current_value = self.current_value[:-1] + text
            else:
                self.current_value += text
        else:
            self.current_value += text

        self.input_field.setText(self.current_value)

    # Function for calculator button click event
    def button_clicked(self):
        button = self.sender()
        text = button.text()
        dis_text = self.input_field.text()
        symb = ['+', '-', '*', '/', '%']

        if text == '=':
            try:
                result = eval(self.current_value)
                # Limit displayed numbers to 13 digits
                result = round(result, 6)
                result = "{:.13g}".format(Decimal(str(result)))
                self.input_field.setText(result)
                self.current_value = str(result)
                self.last_pressed = '='  # Store the last pressed button as "="
            except (SyntaxError, ZeroDivisionError):
                self.input_field.setText('Error')
                self.current_value = ''
        elif text == 'C':
            self.input_field.clear()
            self.current_value = ''
            self.input_field.setText('0')
            self.last_pressed = []

        # Skip adding additional zeros at the beginning
        elif self.current_value == '0':
            if text != '0' and text != '.':
                self.current_value = text
                self.input_field.setText(text)
        elif self.current_value == '00':
            
            if text != '0':
                self.current_value = text
                self.input_field.setText(text)

        elif self.current_value == '0' or self.current_value == '00':
            self.current_value = text
            self.input_field.setText(text)
        # Add the following conditions to handle number input after getting a result
        elif self.last_pressed == '=' and text.isnumeric():
            self.input_field.setText(text)
            self.current_value = text
            self.last_pressed = text
        elif text == '÷':
            text = '/'
            self.symbdup(text)
        elif text == '−':
            text = '-'
            self.symbdup(text)
        elif text == '×':
            text = '*'
            self.symbdup(text)
        elif text == '+/-': # Change plus/minus 
           if self.current_value:
                if self.current_value.startswith('-'):
                    self.current_value = self.current_value[1:]
                else:
                    self.current_value = '-' + self.current_value
                self.input_field.setText(self.current_value)
        elif text == '%':
            text = '/100'
            self.symbdup(text)
        else:
            self.symbdup(text)

            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    
    # Set the window background color
    palette = calculator.palette()
    palette.setColor(QPalette.Window, QColor("#D3D3D3"))
    calculator.setPalette(palette)
    
    calculator.show()
    sys.exit(app.exec_())
