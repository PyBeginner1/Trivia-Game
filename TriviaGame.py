import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

#global
widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": []
}

#initialize application
app = QApplication(sys.argv)
#create window widget
window = QWidget()
window.setWindowTitle("Do you want to be a Programmer?")
window.setFixedWidth(1000)      #in pixels
window.setStyleSheet("background:black;")

#grid
grid = QGridLayout()                                        #set grid layout
window.setLayout(grid)                                      #apply grid on window

#switch between frame1 & frame2
def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:                           #check if is empty
            widgets[widget][-1].hide()                      #if its not empty remove existing widget
            for i in range(0, len(widgets[widget])):
                widgets[widget].pop()

def start_game():
    clear_widgets()
    frame2()

def show_frame1():
    clear_widgets()
    frame1()

#answer buttons
def create_buttons(answer, l_margin, r_margin):             #left & right margin added to create space between them & edge of window
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(450)
    button.setStyleSheet(
        "*{border:4px solid '#BC006C';" +
        "margin-left:" + str(l_margin) + "px;" +
        "margin-right:" + str(r_margin) + "px;" +
        "border-radius:25px;" +
        "font-family:'shanti';" +
        "font-size:16px;" +
        "color:'white';" +
        "padding:15px 0;" +
        "margin-top:20px;}" +
        "*:hover{background:'#BC006C';}" )

    return button

def frame1():
    #logo
    image = QPixmap("logo (1).png")                             #pixmap selects image & loads
    logo = QLabel()                                             #create label widget
    logo.setPixmap(image)                                       #place image
    logo.setAlignment(QtCore.Qt.AlignCenter)                    #aligns image center
    logo.setStyleSheet("margin-top:100px;")
    widgets["logo"].append(logo)                                #widgets[logo] is key & logo is value to it

    #button
    button = QPushButton("PLAY")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        "*{border:4px solid 'grey';" +
        "border-radius:40px;" +
        "font-size:35px;" +
        "color:'white';" +
        "padding:25px;" +
        "margin:100px 200px;}" +
        "*:hover{background:'grey';}"                           #hover is used to change colour of button when u move cursor on it
    )
    button.clicked.connect(start_game)
    widgets["button"].append(button)

    grid.addWidget(widgets["logo"] [-1], 0, 0)                                    #load image in grid(row, col) & -1 is last item
    grid.addWidget(widgets["button"] [-1], 1, 0)                                #load button(row,col) & -1 indicates last item

def frame2():
    score= QLabel("80")
    score.setAlignment(QtCore.Qt.AlignRight)
    score.setStyleSheet("border:1px solid 'grey'; " +
                        "border-radius:20px;" +
                        "font-size:35px;" +
                        "color:'white';"
                        + "padding:20px 20px 10px 20px;"
                        + "margin:20px 200px;" +
                        "background:'#64A314';"
                        )

    widgets["score"].append(score)

    question = QLabel("Text")
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet("font-size:35px;" +
                           "font-family:'shanti';"
                           + "color:'white';"
                        + "padding:75px;" )
    widgets["question"].append(question)

    image = QPixmap("logo_bottom.png")              # pixmap selects image & loads
    logo = QLabel()                                 # create label widget
    logo.setPixmap(image)                           # place image
    logo.setAlignment(QtCore.Qt.AlignCenter)        # aligns image center
    logo.setStyleSheet("margin-top:75px; margin-bottom:30px")
    widgets["logo"].append(logo)



    #answer buttons
    button1 = create_buttons("answer1", 85, 5)
    button2 = create_buttons("answer2", 5, 85)
    button3 = create_buttons("answer3", 85, 5)
    button4 = create_buttons("answer4", 5, 85)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)

    grid.addWidget(widgets["score"][-1], 0, 1)                  # load image in grid(row, col) & -1 is last item
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)         #including rowspan & col span since its wide
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)
    grid.addWidget(widgets["logo"][-1], 4, 0, 1, 2)


#answer buttons

frame1()


#display
window.show()
#exit
sys.exit(app.exec())
