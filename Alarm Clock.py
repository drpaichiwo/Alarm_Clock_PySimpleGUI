# Alarm Clock
import PySimpleGUI as sg
import time
import winsound


def create_window():
    sg.theme("black")

    clock_layout = [
        [sg.VPush()],
        [sg.Text("", font="Any 90", key="-TIME-")],
        [sg.VPush()]
    ]

    alarm_layout = [
        [sg.Text("HOUR", size=(9, 1)), sg.Text("MINUTE", size=(10, 1))],
        [sg.Input(key="-HR-", size=(10, 1)), sg.Input(key="-MIN-", size=(10, 1))],
        [sg.Text("", size=(40, 5), key="-LST-")],
        [sg.Button("Confirm", button_color=("white", "black"), border_width=0),
         sg.Button("Stop", disabled=True, button_color=("white", "black"),border_width=0)]
    ]

    layout = [
        [sg.Push(), sg.Image('CloseWindow.png',
                             pad=0,
                             enable_events=True,
                             key="-CLOSE-")],
        [sg.TabGroup([[sg.Tab("Clock", clock_layout, element_justification="center"),
                       sg.Tab("Alarm", alarm_layout)]])]]

    return sg.Window(
        "", layout, size=(520, 240), finalize=True, no_titlebar=True)


# Window setup
window = create_window()


list_of_alarms = []


def get_time():
    # Updates the time, checks if alarm should go off

    global list_of_alarms
    now = time.strftime("%H:%M:%S")
    window["-TIME-"].update(now)

    if list_of_alarms:
        for index, alarm in enumerate(list_of_alarms):
            if now == alarm:
                winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)
                window["Stop"].update(disabled=False)
                list_of_alarms = list_of_alarms[index:]
                update()


def confirm_alarm():
    # Obtains the alarm time, adds it to the list

    hour_val = values["-HR-"]
    minute_val = values["-MIN-"]

    if hour_val and minute_val:
        list_of_alarms.append(f"{hour_val}:{minute_val}:00")
    update()


def stop_alarm():
    # Stops the alarm currently going off

    window["Stop"].update(disabled=True)
    list_of_alarms.pop(0)
    update()


def update():
    # Updates the list of alarms

    window["-LST-"].update("")
    for alarm in list_of_alarms:
        window["-LST-"].update(window["-LST-"].get() + alarm + '\t')


# Main loop
while True:
    event, values = window.read(timeout=10)
    if event in (sg.WIN_CLOSED, "-CLOSE-"):
        break

    if event == "Confirm":
        confirm_alarm()
    if event == "Stop":
        stop_alarm()

    get_time()

window.close()
