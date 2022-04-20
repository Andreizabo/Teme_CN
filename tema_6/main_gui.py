import tkinter as tk
from termcolor import colored
import uuid
import json
import main

# Default colors
INFO_COLOR = "green"
WARNING_COLOR = "yellow"
ERROR_COLOR = "red"
DEBUG_COLOR = "blue"


def read_input():
    '''
    Callback method for "Read input" button.
    
    JSON Example for Tema 6:
    {
        "a" : "a.txt",
        "b" : "b.txt",
        "verify_sum" : "a_plus_b.txt",
        "verify_prod" : "a_ori_a.txt"
    }

    Also assigns global variable INPUT.

    @returns : nothing
    '''

    global INPUT

    log_entry(information_text, "[INFO] Trying to parse './input.json'...")
    try:
        with open("input.json", "r") as fin:
            _dict = json.load(fin)
    except:
        log_entry(information_text, "[ERROR] Could not parse './input.json'!", ERROR_COLOR)
        return False
    
    log_entry(information_text, "[INFO] Successfully parsed './input.json'.", INFO_COLOR)

    INPUT = _dict
    main.fxa.read_input = True
    return True


def verify_aitken_newton():
    '''
    Callback for Verify Aitken-Newton button.
    '''

    if not main.fxa.read_input:
        log_entry(information_text, "[INFO] Input not parsed, trying to parse now...")
        if not read_input():
            return
        main.fxa.read_input = True
    
    log_entry(information_text, "[INFO] Running verification with Aitken-Newton approach.", INFO_COLOR)
    log_entry(information_text, "■" * 72, INFO_COLOR)

    aux1, aux2 = main.fxa.gui_aitken_newton()
    log_entry(information_text, "Lₙ(x̄) = " + str(aux1), "blue")
    log_entry(information_text, "|Lₙ(x̄) - f(x̄)| = " + str(aux2), "blue")

    log_entry(information_text, "■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■", INFO_COLOR)
    log_entry(information_text, "[INFO] Finished verification with Aitken-Newton approach.", INFO_COLOR)

def verify_least_squares():
    '''
    Callback for Verify least squares button.
    '''
    


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
    main_window.title("Tema 6")
    main_window.geometry("600x300")
    main_window.resizable(0, 0)

    # Top frame (used for control buttons)
    frame_top = tk.Frame(main_window)
    frame_top.pack(side=tk.TOP)

    # Read input button
    read_input_button = tk.Button(frame_top, text="Read input", command=read_input, padx=10)
    read_input_button.grid(row=0, column=0)

    # Aitken-Newton button
    ak_button = tk.Button(frame_top, text="Verify Aitken-Newton", command=verify_aitken_newton, padx=10)
    ak_button.grid(row=0, column=1)

    # Least squares button
    least_squares_button = tk.Button(frame_top, text="Verify least squares", command=verify_least_squares, padx=10)
    least_squares_button.grid(row=0, column=2)

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

    # Start the window
    main_window.mainloop()
