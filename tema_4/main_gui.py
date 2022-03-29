import tkinter as tk
import uuid
import main
import json
import prettymatrix
import numpy as np

# Default colors
INFO_COLOR = "green"
WARNING_COLOR = "purple"
ERROR_COLOR = "red"
DEBUG_COLOR = "blue"

# Global variable that stores the input
INPUT = {}

# Current selected system of equations
SYSTEM = None

def display_system(system : main.EqSystem, textbox: tk.Text):
    
    log_entry(textbox, " ")

    # First display the A matrix
    log_entry(textbox, "A matrix", "blue")
    x = 0
    for i in range(len(system.a)):
        for j in range(len(system.a[i])):
            # (LINE, COLUMN) : VALUE
            msg = f"({i}, {system.a[i][j][1]})"
            log_entry(textbox, msg, "blue", place_endline=False)

            msg = f" : {system.a[i][j][0]}"
            log_entry(textbox, msg, "red")
            textbox.update()
            x += 1
            if x >= 10:
                break
        if x == 10:
            break
    
    log_entry(textbox, "...", "blue")
    
    # Last elements
    x = 0
    for i in range(len(system.a) - 11, len(system.a) - 1, 1):
        for j in range(len(system.a[i])):
            # (LINE, COLUMN) : VALUE
            msg = f"({i}, {system.a[i][j][1]})"
            log_entry(textbox, msg, "blue", place_endline=False)

            msg = f" : {system.a[i][j][0]}"
            log_entry(textbox, msg, "red")
            textbox.update()
            x += 1
            if x >= 10:
                break
        if x == 10:
            break
    
    log_entry(textbox, " ")

    # Then display the X vector
    x = 0
    for i in range(len(system.x)):
        log_entry(textbox, f"\t[{system.x[i]}]", "red")
        x += 1
        if x == 10: 
            log_entry(textbox, "X   =", foreground_color="blue", place_endline=False)
            log_entry(textbox, f"\t[{system.x[i]}]", "red")
            break
    x = 0
    for i in range(len(system.x) - 1, 0, -1):
        log_entry(textbox, f"\t[{system.x[i]}]", "red")
        x += 1
        if x == 10: break

    log_entry(textbox, " ")

    # Then display the B vector
    x = 0
    for i in range(len(system.b)):
        log_entry(textbox, f"\t[{system.b[i]}]", "red")
        x += 1
        if x == 10:
            log_entry(textbox, "B   =", foreground_color="blue", place_endline=False)
            log_entry(textbox, f"\t[{system.b[i]}]", "red")
            break
    x = 0
    for i in range(len(system.b) - 1, 0, -1):
        log_entry(textbox, f"\t[{system.b[i]}]", "red")
        x += 1
        if x == 10: break
    
    log_entry(textbox, " ")

def read_input():
    '''
    Callback method for "Read input" button.
    
    JSON Example for Tema 4:
    {
        "a" : "a_1.txt",
        "b" : "b_1.txt",
        "p": 5
    }

    Also assigns global variable INPUT.

    @returns : nothing
    '''

    global INPUT, SYSTEM

    log_entry(information_text, "[INFO] Trying to parse './input.json'...", INFO_COLOR)
    try:
        with open("input.json", "r") as fin:
            _dict = json.load(fin)
    except:
        log_entry(information_text, "[ERROR] Could not parse './input.json'!", ERROR_COLOR)
        return
    
    log_entry(information_text, "[INFO] Successfully parsed './input.json'.", INFO_COLOR)

    INPUT = _dict

    # Get the system class
    log_entry(information_text, f"[INFO] Parsing from \"{INPUT['a']}\" and \"{INPUT['b']}\"", INFO_COLOR)
    information_text.update()

    SYSTEM = main.read_system(INPUT['a'], INPUT['b'])

def approximate_solution():
    '''
    Callback method for "Approximate solution" button.
    It calls for the backend implementation of the Jacobi algorithm.

    @returns : nothing
    '''

    global main_window, SYSTEM

    if INPUT == {}:
        log_entry(information_text, "[ERROR] The input must first be read!", ERROR_COLOR)
        return

    # Find the solution to the given system
    # iter_count = SYSTEM.find_sol()
    iter_count = SYSTEM.find_sol_gui(log_entry, information_text)

    # Display results
    log_entry(information_text, f"[INFO] Iteration count: {iter_count}", INFO_COLOR)

    display_system(SYSTEM, information_text)

def verify_solution():
    '''
    Callback method for "Verify solution" button.
    It calls the backend implementation of the verification algorithm, displaying useful messages if something goes wrong.

    @returns: nothing
    '''

    if INPUT == {}:
        log_entry(information_text, "[ERROR] The input must first be read!", ERROR_COLOR)
        return

    if SYSTEM == None or not SYSTEM.is_calculated:
        log_entry(information_text, "[ERROR] Solution needs to be calculated first!", ERROR_COLOR)
        return

    log_entry(information_text, "[INFO] Verifying solution...", INFO_COLOR)
    log_entry(information_text, f"Difference: ", foreground_color="blue", place_endline=False)
    information_text.update()
    log_entry(information_text, f"{SYSTEM.verify_sol()}", foreground_color="red")


def run_in_gui():
    '''
    Callback method for "Run in GUI" button.

    @returns: nothing
    '''

    if INPUT == {}:
        log_entry(information_text, "[ERROR] The input must first be read!", ERROR_COLOR)
        return

    log_entry(information_text, "[INFO] Running main program...", INFO_COLOR)
    information_text.update()

    read_input()
    approximate_solution()
    verify_solution()

    log_entry(information_text, "[INFO] Finished running main program.", INFO_COLOR)


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
    main_window.title("Tema 4")
    main_window.geometry("620x400")
    main_window.resizable(0, 0)

    # Top frame (used for control buttons)
    frame_top = tk.Frame(main_window)
    frame_top.pack(side=tk.TOP)

    # Read input button
    read_input_button = tk.Button(frame_top, text="Read input", command=read_input, padx=10)
    read_input_button.grid(row=0, column=0)

    # Aproximate solution button
    aproximate_solution_button = tk.Button(frame_top, text="Approximate solution", command=approximate_solution, padx=10)
    aproximate_solution_button.grid(row=0, column=1)

    # Verify solution button
    verify_solution_button = tk.Button(frame_top, text="Verify solution", command=verify_solution, padx=10)
    verify_solution_button.grid(row=0, column=2)

    # Run from GUI button
    run_from_gui_button = tk.Button(frame_top, text="Run in GUI", command=run_in_gui, padx=10)
    run_from_gui_button.grid(row=0, column=4)

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