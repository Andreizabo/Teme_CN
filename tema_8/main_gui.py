import tkinter as tk
from termcolor import colored
import uuid
import main

# Default colors
INFO_COLOR = "green"
WARNING_COLOR = "yellow"
ERROR_COLOR = "red"
DEBUG_COLOR = "blue"

def select_f1():
    main.selected_function = main.f1
    log_entry(information_text, 'Selected function = "(x ** 3) / 3 - 2 * (x ** 2) + 2 * x + 3"', 'blue')
def select_f2():
    main.selected_function = main.f2
    log_entry(information_text, 'Selected function = "x ** 2 + sin(x)"', 'blue')
def select_f3():
    main.selected_function = main.f3
    log_entry(information_text, 'Selected function = "x ** 4 - 6 * (x ** 3) + 13 * (x ** 2) - 12 * x + 4', 'blue')


def compare_results():
    r = main.selected_function.compare_results().splitlines()
    log_entry(information_text, r[0], 'green')
    log_entry(information_text, r[1], 'green')

def log_entry(text_object: tk.Text, message: str, foreground_color: str = "black", background_color: str = "white", place_endline=True):
    '''
    Adds a new entry to the logging window.

    @param text_object: Tk Text object which will get colored.
    @param message: string to be appended to the existing information in the logging window.
    @param foreground_color: the color of the word, as a string.
    @param background_color: the background color of the word, as a string (defaults to white).
    @param place_endline: whether or not to place a endline after the message. Defaults to True.
    '''

    end = '\n' if place_endline else ''
    text_object.insert(tk.END, message + end)

    _index = "1.0"

    # A new tag is needed for every color added
    random_tag_name = str(uuid.uuid4())

    while True:
        pos_str = text_object.search(message, index=_index, stopindex="end")

        # Stop when no more occurences are present
        if pos_str == "":
            break
        
        # Hackish
        line = pos_str.split(".")[0]
        column = pos_str.split(".")[1]
        
        pos = int(column)

        _index = str(line) + "." + str(pos + len(message))

        text_object.tag_add(random_tag_name, pos_str, _index)
        text_object.tag_config(random_tag_name, foreground=foreground_color, background=background_color)

    # Move the scrollbar to the newly added line
    information_text.see(tk.END)

if __name__ == "__main__":

    # Main window configuration
    main_window = tk.Tk()
    main_window.title("Tema 8")
    main_window.geometry("700x400")
    main_window.resizable(0, 0)

    # Top frame (used for control buttons)
    frame_top = tk.Frame(main_window)
    frame_top.pack(side=tk.TOP)

    # F1 button
    f1_button = tk.Button(frame_top, text="Function 1", command=select_f1, padx=10)
    f1_button.grid(row=0, column=0)

    # F2 button
    f2_button = tk.Button(frame_top, text="Function 2", command=select_f2, padx=10)
    f2_button.grid(row=0, column=1)

    # F3 button
    f3_button = tk.Button(frame_top, text="Function 3", command=select_f3, padx=10)
    f3_button.grid(row=0, column=2)

    compare_button = tk.Button(frame_top, text="Compare results", command=compare_results, padx=10)
    compare_button.grid(row=1, column=1)

    # Bottom frame (used as an alternative for command line prints)
    frame_bottom = tk.Frame(main_window)
    frame_bottom.pack(side=tk.BOTTOM)

    # Information text, used for displaying relevant information
    information_scrollbar = tk.Scrollbar(frame_bottom)
    information_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    information_text = tk.Text(frame_bottom)
    information_text.pack(side=tk.LEFT, fill=tk.Y)

    information_scrollbar.config(command=information_text.yview)
    information_text.config(yscrollcommand=information_scrollbar.set)

    log_entry(information_text, 'Default function is function 1', 'green')
    select_f1()

    # Start the window
    main_window.mainloop()