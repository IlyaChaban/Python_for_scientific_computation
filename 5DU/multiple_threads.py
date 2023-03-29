import matplotlib.pyplot as plt
import numpy as np
import threading
import time
from threading import Timer


WRITE_UPDATE_TIME   = 0.9   #[s]
DRAW_UPDATE_TIME    = 0.6   #[s]
MATH_UPDATE_TIME    = 0.3   #[s]
TIME = 0
DATA_TO_ADD = []

FIGURE = plt.figure()
AX = FIGURE.add_subplot(111)
LINE1, = AX.plot(DATA_TO_ADD)


def math_function():
    global TIME
    TIME = TIME + 1
    DATA_TO_ADD.append([TIME, TIME ** 2])
    Timer(MATH_UPDATE_TIME, math_function).start()


def update_line():
    global LINE1, FIGURE
    print(LINE1.get_xdata())
    LINE1.set_xdata(np.append(LINE1.get_xdata(), np.array(DATA_TO_ADD[-2][0])))
    LINE1.set_xdata(np.append(LINE1.get_xdata(), np.array(DATA_TO_ADD[-1][0])))
    LINE1.set_ydata(np.append(LINE1.get_ydata(), np.array(DATA_TO_ADD[-2][1])))
    LINE1.set_ydata(np.append(LINE1.get_ydata(), np.array(DATA_TO_ADD[-1][1])))
    Timer(DRAW_UPDATE_TIME, update_line).start()

def update_graph():
    FIGURE.canvas.draw()
    time.sleep(DRAW_UPDATE_TIME)
    update_graph()


def add_to_csv():
    global DATA_TO_ADD
    with open("data.csv", mode='a') as file:
        for data in DATA_TO_ADD[-3:]:
            file.write(str(data))
    Timer(WRITE_UPDATE_TIME, add_to_csv).start()


if __name__ == "__main__":
    """
    Ilya's code starts here
    """

    math_function()
    time.sleep((WRITE_UPDATE_TIME-DRAW_UPDATE_TIME)*1.05)

    update_line()
    time.sleep((WRITE_UPDATE_TIME - DRAW_UPDATE_TIME)*1.05)
    plt.show()
    update_graph()

    add_to_csv()
    time.sleep((WRITE_UPDATE_TIME - DRAW_UPDATE_TIME)*1.05)

    time.sleep(10)

