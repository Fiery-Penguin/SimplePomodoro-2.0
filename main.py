import os  # For use in locating paths
from playsound import playsound  # For playing the alarm sounds
import time  # For sleeping
import subprocess
import configparser

# Retrieve the path to the script
path = os.path.dirname(__file__)  # Get the path to the project root

# ======================== C O N F I G U R A T I O N ======================== #

# Set up the progress bar characters
barChar = "⣿"
progressChar = "█"

configPath = path + "/config.ini"

# Initialise the config parser
config = configparser.ConfigParser()

# Read the config file
config.read(configPath)

# Set the work and rest times in minutes
prepTime = int(config.get('General', 'prepTime'))  # minutes
workTime = int(config.get('General', 'workTime'))  # minutes
restTime = int(config.get('General', 'restTime'))  # minutes

# =========================================================================== #

# Convert the minutes for work and rest into seconds
second = 60  # minutes
prepTimeS = prepTime * second
workTimeS = workTime * second
restTimeS = restTime * second
marginOffset = 6

# Initiate the session counter (not used)
session = 1

# Define the path to the alarm sound
bells = path + "/Pomodoro Alarm Bells.mp3"

# The rendering function
def renderProgressBar(message, currentTime, fullTime, colour):
    try:
        # Clear the screen before writing anything new to the screen
        os.system("clear")
        progress = 1 - currentTime / fullTime  # Calculate the progress percentage
        barfill = []

        # Format the progress percentage as a percentage
        progressString = format(progress, ".0%") + " │"

        # Calculate the individual minutes of the timer
        minutes = str(int(currentTime / 60)).zfill(2)
        # Calculate the individual seconds of the timer
        seconds = str(currentTime % 60).zfill(2)

        # join the minutes and seconds variable together to get the countdown
        timer = " %s:%s " % (minutes, seconds)

        # === Calculate the width of the current window ===
        (
            windowWidth,
            windowHeight,
        ) = os.get_terminal_size()
        barWidth = windowWidth - marginOffset  # Set the width of the bar
        progressWidth = int(barWidth * progress)
        timerStart = int(marginOffset / 2) + int(barWidth / 2 - (len(timer) / 2))
        messageStart = int(marginOffset / 2) + int(barWidth / 2 - (len(message) / 2))

        # ====== Draw the progress bar ======
        # build the initial single row bar
        bar = barChar * barWidth
        # Add the progress to the bar
        bar = "  │" + progressChar * progressWidth + bar[progressWidth:] + "│"

        for i in range(windowHeight - 4):
            barfill.append(bar)

        # Add the timer in the middle of the progress bar
        barfill[int(len(barfill) / 2) + 1] = (
            bar[:timerStart] + timer + bar[timerStart + len(timer) :]
        )

        barfill[int(len(barfill) / 2) - 1] = (
            bar[:messageStart] + message + bar[messageStart + len(message) :]
        )

        # Create the surrounding lines to make the app prettier, but also have
        # more colour so it's easier to see the colour at a glance

        top = "  ╭" + "─" * (windowWidth - marginOffset) + "╮  "
        bottom = "  ╰" + "─" * (windowWidth - marginOffset) + "╯  "

        # Print the UI
        print()
        print(colour + top)
        for i in range(len(barfill)):
            print(barfill[i])
        print(bottom + "\033[1;00m")
    except:
            print("Terminal too low")


# Get ready timer
currentTime = prepTimeS
for i in range(prepTimeS):
    # Call the render progress bar function
    renderProgressBar(" P R E P A R I N G ", currentTime, prepTimeS, "\033[1;32m")

    # Sleep for one second and count decrement the current time by one
    time.sleep(1)
    currentTime -= 1

# Play the alarm sound to indicate that the timer has run out
subprocess.run(
    [
        "notify-send",
        "Pomodoro",
        "Preparation over, time to work",
        "-t",
        "15000",
        "--urgency",
        "critical",
    ]
)
playsound(bells, False)


while True:  # Loop indefinitely
    currentTime = workTimeS  # Set the current time to the work time seconds

    # Count down for the work time
    for i in range(workTimeS):  # loop though all the seconds of work
        # Call the render progress bar function
        renderProgressBar(" W O R K I N G ", currentTime, workTimeS, "\033[1;34m")

        # Sleep for one second and count decrement the current time by one
        time.sleep(1)
        currentTime -= 1

    # Play the alarm sound to indicate that the timer has run out
    renderProgressBar(" W O R K I N G ", currentTime, workTimeS, "\033[1;34m")
    subprocess.run(
        [
            "notify-send",
            "Pomodoro",
            "Take a break! You diserve it",
            "-t",
            "15000",
            "--urgency",
            "critical",
        ]
    )
    playsound(bells, False)

    currentTime = restTimeS

    for i in range(restTimeS):
        # Call the render progress bar function
        renderProgressBar(" R E S T I N G ", currentTime, restTimeS, "\033[1;31m")

        # Sleep for one second and count decrement the current time by one
        time.sleep(1)
        currentTime -= 1

    # Play the alarm sound to indicate that the timer has run out
    renderProgressBar(" R E S T I N G ", currentTime, restTimeS, "\033[1;31m")
    subprocess.run(
        [
            "notify-send",
            "Pomodoro",
            "Time to get back to work!",
            "-t",
            "15000",
            "--urgency",
            "critical",
        ]
    )
    playsound(bells, False)
