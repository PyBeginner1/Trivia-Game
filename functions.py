import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from urllib.request import urlopen
import json
import pandas as pd
import random

#https://opentdb.com/api.php?amount=50&category=18&difficulty=easy&type=multiple

with urlopen("https://opentdb.com/api.php?amount=50&category=18&difficulty=medium&type=multiple") as webpage:
    data = json.loads(webpage.read().decode())
    df = pd.DataFrame(data["results"])
    print(df.columns)

def preload_data(idx):
    question=df['question'][idx]
    correct=df["correct_answer"][idx]
    wrong=df["incorrect_answers"][idx]

    formatting = [
        ("#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("&lt;", "<"),
        ("&gt;", ">")
    ]

    for tuple in formatting:
        question = question.replace(tuple[0], tuple[1])
        correct = correct.replace(tuple[0], tuple[1])

    for tuple in formatting:
        wrong = [char.replace(tuple[0], tuple[1]) for char in wrong]

    all_answers = wrong + [correct]
    #since from above the correct ans will always appear at end(option d), we use random
    random.shuffle(all_answers)

# appending values into empty list from df
    parameters["question"].append(question)
    parameters["correct"].append(correct)
    parameters["answer1"].append(all_answers[0])
    parameters["answer2"].append(all_answers[1])
    parameters["answer3"].append(all_answers[2])
    parameters["answer4"].append(all_answers[3])


#global list of parameters
parameters={
    "question" : [],
    "answer1" : [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "correct": [],
    "score": [0],
    "index":[random.randint(0,49)]
}



#global list of widgets
widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "message": [],
    "score": []
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


def clear_parameters():
    for parm in parameters:
        if parameters[parm] != []:
            for i in range(0, len(parameters[parm])):
                parameters[parm].pop()

    parameters["index"].append(random.randint(0,49))
    parameters["score"].append(0)

def start_game():
    clear_widgets()
    clear_parameters()
    preload_data(parameters["index"][-1])
    frame2()

def show_frame1():
    clear_widgets()
    frame1()

#answer buttons
def create_buttons(answer, l_margin, r_margin):             #left & right margin added to create space between them & edge of window
    button = QPushButton(answer)                            #answer is text of button
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

    #create a click event
    button.clicked.connect(lambda:  is_correct(button))
    #lambda functions are used when we need a nameless function for a short period of time.
    #In python, we use it as an argument for higher order function(a fn that takes other fn as args)
    return button

def is_correct(btn):
    #print(answer)                                  #prints the options u click
    if btn.text() == parameters["correct"][-1]:
        print(btn.text() + " is correct")

        temp_score = parameters["score"][-1]
        parameters["score"].pop()
        parameters["score"].append(temp_score + 10)

        parameters["index"].pop()
        parameters["index"].append(random.randint(0,49))

        preload_data(parameters["index"][-1])

        #to display
        widgets["score"][-1].setText(str(parameters["score"][-1]))
        widgets["question"][0].setText(parameters["question"][-1])
        widgets["answer1"][0].setText(parameters["answer1"][-1])
        widgets["answer2"][0].setText(parameters["answer2"][-1])
        widgets["answer3"][0].setText(parameters["answer3"][-1])
        widgets["answer4"][0].setText(parameters["answer4"][-1])

        if parameters["score"][-1] == 100:                      #win
            clear_widgets()
            frame3()



    else:
        clear_widgets()
        frame4()


def frame1():
    clear_widgets()
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
    score= QLabel(str(parameters["score"][-1]))
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

    question = QLabel(parameters["question"][-1])
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
    button1 = create_buttons(parameters["answer1"][-1], 85, 5)
    button2 = create_buttons(parameters["answer2"][-1], 5, 85)
    button3 = create_buttons(parameters["answer3"][-1], 85, 5)
    button4 = create_buttons(parameters["answer4"][-1], 5, 85)

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

def frame3():
    #congradulations widget
    message = QLabel("Congradulations! You\nare a true programmer!\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 25px; color: 'white'; margin: 100px 0px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel("100")
    score.setStyleSheet("font-size: 100px; color: #8FC740; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #go back to work widget
    message2 = QLabel("OK. Now go back to WORK.")
    message2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'Shanti'; font-size: 30px; color: 'white'; margin-top:0px; margin-bottom:75px;"
        )
    widgets["message2"].append(message2)

    #button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        "*{background:'#BC006C'; padding:25px 0px; border: 1px solid '#BC006C'; color: 'white'; font-family: 'Arial'; font-size: 25px; border-radius: 40px; margin: 10px 300px;} *:hover{background:'#ff1b9e';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px; margin-bottom: 20px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 2, 2)


def frame4():
    #sorry widget
    messages = QLabel("Sorry, this answer \nwas wrong\n your score is:")
    messages.setAlignment(QtCore.Qt.AlignRight)
    messages.setStyleSheet(
        "font-family: 'Shanti'; font-size: 35px; color: 'white'; margin: 75px 5px; padding:20px;"
        )
    widgets["message"].append(messages)

    #score widget
    score = QLabel(str(parameters["score"] [-1]))
    score.setStyleSheet("font-size: 100px; color: white; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        '''*{
            padding: 25px 0px;
            background: '#BC006C';
            color: 'white';
            font-family: 'Arial';
            font-size: 35px;
            border-radius: 40px;
            margin: 10px 200px;
        }
        *:hover{
            background: '#ff1b9e';
        }'''
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)

#answer buttons

frame1()


#display
window.show()
#exit
sys.exit(app.exec())
