import PySimpleGUI as sg
from Common_actors import imdb_search
from collections import Counter

sg.theme("DarkBlue")  # window theme
col_Text = []  # init column
col_Input = []  # init column
col_Result_Id = []  # init column
col_Result_Cast = []
col_Common_Results = (
    [sg.Text("", key="-COMMONACTORS-", size=(900, 1), visible=False)],
)
Nbr_Movies_Previous = 0
Common_results = []
dupnames = []

for i in range(9):  # populate columns with 10 occurences, not visible.
    col_Text += (
        [
            sg.Text(
                f"Enter movie number {i+1}:", key="-MOVIE" + str(i) + "-", visible=False
            )
        ],
    )
    col_Input += ([sg.InputText("", key="-MOVIEINPUT" + str(i) + "-", visible=False)],)
    col_Result_Id += (
        [
            sg.Text(
                "",
                key="-MOVIERESULTID" + str(i) + "-",
                visible=False,
                size=(9, 1),
            )
        ],
    )
    col_Result_Cast += (
        [
            sg.Text(
                "", key="-MOVIERESULTCAST" + str(i) + "-", visible=False, size=(48, 1)
            )
        ],
    )

# general layout
layout = [
    [
        sg.Text(
            "This tool will give you the common actors from a selection of given movies."
        )
    ],
    [
        sg.Text("How many movies would you like to enter? (Max 9)"),
        sg.InputText(key="-NUM-", size=(3, 1), enable_events=True),
    ],
    [
        sg.Column(col_Text, size=(150, 250)),
        sg.Column(
            col_Input,
            size=(300, 250),
        ),
        sg.Column(col_Result_Id, size=(90, 250)),
        sg.Column(col_Result_Cast, size=(460, 250)),
    ],
    [sg.Column(col_Common_Results, size=(1000, 50))],
    [sg.Button("Submit", key="-SUBMIT-"), sg.Button("Exit")],
]

# load window
window = sg.Window("Welcome to common-actors!", layout, size=(1000, 400))

# handle events
while True:  # Event Loop
    event, values = window.read()
    # print(event, values)
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "-NUM-":  # number of movies to compare
        for i in range(int(Nbr_Movies_Previous)):  # delete all previous movies input
            window["-MOVIE" + str(i) + "-"].update(visible=False)
            window["-MOVIEINPUT" + str(i) + "-"].update("", visible=False)
            window["-MOVIERESULTID" + str(i) + "-"].update("", visible=False)
            window["-MOVIERESULTCAST" + str(i) + "-"].update("", visible=False)
        window["-COMMONACTORS-"].update("")
        Nbr_Movies = values["-NUM-"]
        if Nbr_Movies:  # if field not empty
            for i in range(
                int(Nbr_Movies)
            ):  # create input fields according to nbr of movies
                window["-MOVIE" + str(i) + "-"].update(visible=True)
                window["-MOVIEINPUT" + str(i) + "-"].update(visible=True)
                window["-MOVIERESULTID" + str(i) + "-"].update(visible=True)
                window["-MOVIERESULTCAST" + str(i) + "-"].update(visible=True)
            Nbr_Movies_Previous = (
                Nbr_Movies  # save the nbr of movies for delete and submit
            )
    if event == "-SUBMIT-":
        Common_results.clear()
        counts = ()
        dupnames.clear()
        window["-COMMONACTORS-"].update("")
        col_Result_Id.clear()  # in case number of movies was changed many times
        for i in range(int(Nbr_Movies_Previous)):
            query = imdb_search(values["-MOVIEINPUT" + str(i) + "-"])
            window["-MOVIERESULTID" + str(i) + "-"].update(value=query[0])
            window["-MOVIERESULTCAST" + str(i) + "-"].update(value=query[1])
            Common_results += query[2]
        counts = Counter(Common_results)
        for key, value in counts.items():
            if int(Nbr_Movies) == value:
                dupnames += [key]
        window["-COMMONACTORS-"].update(value=dupnames, visible=True)

window.close()
