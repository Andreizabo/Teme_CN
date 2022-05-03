import tkinter as tk
from termcolor import colored
import uuid
import main

# Default colors
INFO_COLOR = "green"
WARNING_COLOR = "yellow"
ERROR_COLOR = "red"
DEBUG_COLOR = "blue"


def p1_select():
    main.selected_polynome = 1
    log_entry(information_text, 'Selected polynome (x - 1)(x - 2)(x - 3)', 'blue')
    p1_try_button['state'] = p1_try_until_button['state'] = 'normal'
    p2_try_button['state'] = p2_try_until_button['state'] = 'disabled'
    p3_try_button['state'] = p3_try_until_button['state'] = 'disabled'
    p4_try_button['state'] = p4_try_until_button['state'] = 'disabled'
def p2_select():
    main.selected_polynome = 2
    log_entry(information_text, 'Selected polynome (x - 2/3)(x - 1/7)(x + 1)(x - 3/2)', 'blue')
    p1_try_button['state'] = p1_try_until_button['state'] = 'disabled'
    p2_try_button['state'] = p2_try_until_button['state'] = 'normal'
    p3_try_button['state'] = p3_try_until_button['state'] = 'disabled'
    p4_try_button['state'] = p4_try_until_button['state'] = 'disabled'
def p3_select():
    main.selected_polynome = 3
    log_entry(information_text, 'Selected polynome (x - 1)(x - 1/2)(x - 3)(x - 1/4)', 'blue')
    p1_try_button['state'] = p1_try_until_button['state'] = 'disabled'
    p2_try_button['state'] = p2_try_until_button['state'] = 'disabled'
    p3_try_button['state'] = p3_try_until_button['state'] = 'normal'
    p4_try_button['state'] = p4_try_until_button['state'] = 'disabled'
def p4_select():
    main.selected_polynome = 4
    log_entry(information_text, 'Selected polynome (x - 1)(x - 1)(x - 2)(x - 2)', 'blue')
    p1_try_button['state'] = p1_try_until_button['state'] = 'disabled'
    p2_try_button['state'] = p2_try_until_button['state'] = 'disabled'
    p3_try_button['state'] = p3_try_until_button['state'] = 'disabled'
    p4_try_button['state'] = p4_try_until_button['state'] = 'normal'


def p1_try():
    result, output_str = main.ps1.solve()
    if result == None:
        log_entry(information_text, output_str, 'red')
    else:
        log_entry(information_text, output_str, 'green')

def p1_try_until():
    result = None
    while result == None:
        result, output_str = main.ps1.solve()
        if result == None:
            log_entry(information_text, output_str, 'red')
            information_text.update()
    
    log_entry(information_text, output_str, 'green')


def p2_try():
    result, output_str = main.ps2.solve()
    if result == None:
        log_entry(information_text, output_str, 'red')
    else:
        log_entry(information_text, output_str, 'green')

def p2_try_until():
    result = None
    while result == None:
        result, output_str = main.ps2.solve()
        if result == None:
            log_entry(information_text, output_str, 'red')
            information_text.update()
    
    log_entry(information_text, output_str, 'green')

def p3_try():
    result, output_str = main.ps3.solve()
    if result == None:
        log_entry(information_text, output_str, 'red')
    else:
        log_entry(information_text, output_str, 'green')

def p3_try_until():
    result = None
    while result == None:
        result, output_str = main.ps3.solve()
        if result == None:
            log_entry(information_text, output_str, 'red')
            information_text.update()
    
    log_entry(information_text, output_str, 'green')

def p4_try():
    result, output_str = main.ps4.solve()
    if result == None:
        log_entry(information_text, output_str, 'red')
    else:
        log_entry(information_text, output_str, 'green')

def p4_try_until():
    result = None
    while result == None:
        result, output_str = main.ps4.solve()
        if result == None:
            log_entry(information_text, output_str, 'red')
            information_text.update()
    
    log_entry(information_text, output_str, 'green')


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
    main_window.title("Tema 7")
    main_window.geometry("600x400")
    main_window.resizable(0, 0)

    # Top frame (used for control buttons)
    frame_top = tk.Frame(main_window)
    frame_top.pack(side=tk.TOP)

    # Polynome 1 button
    p1_button = tk.Button(frame_top, text="Polynome 1", command=p1_select, padx=10)
    p1_button.grid(row=0, column=0)

    p1_try_button = tk.Button(frame_top, text="Try", command=p1_try, padx=10)
    p1_try_button.grid(row=0, column=1)

    p1_try_until_button = tk.Button(frame_top, text="Try until solution", command=p1_try_until, padx=10)
    p1_try_until_button.grid(row=0, column=2)

    # Polynome 2 button
    p2_button = tk.Button(frame_top, text="Polynome 2", command=p2_select, padx=10)
    p2_button.grid(row=1, column=0)

    p2_try_button = tk.Button(frame_top, text="Try", command=p2_try, padx=10)
    p2_try_button.grid(row=1, column=1)

    p2_try_until_button = tk.Button(frame_top, text="Try until solution", command=p2_try_until, padx=10)
    p2_try_until_button.grid(row=1, column=2)

    # Polynome 3 button
    p3_button = tk.Button(frame_top, text="Polynome 3", command=p3_select, padx=10)
    p3_button.grid(row=2, column=0)

    p3_try_button = tk.Button(frame_top, text="Try", command=p3_try, padx=10)
    p3_try_button.grid(row=2, column=1)

    p3_try_until_button = tk.Button(frame_top, text="Try until solution", command=p3_try_until, padx=10)
    p3_try_until_button.grid(row=2, column=2)

    # Polynome 4 button
    p4_button = tk.Button(frame_top, text="Polynome 4", command=p4_select, padx=10)
    p4_button.grid(row=3, column=0)

    p4_try_button = tk.Button(frame_top, text="Try", command=p4_try, padx=10)
    p4_try_button.grid(row=3, column=1)

    p4_try_until_button = tk.Button(frame_top, text="Try until solution", command=p4_try_until, padx=10)
    p4_try_until_button.grid(row=3, column=2)


    

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
    
    # First, disable all buttons until a polynome is selected
    p1_try_button['state'] = 'disabled'
    p2_try_button['state'] = 'disabled'
    p3_try_button['state'] = 'disabled'
    p4_try_button['state'] = 'disabled'
    
    p1_try_until_button['state'] = 'disabled'
    p2_try_until_button['state'] = 'disabled'
    p3_try_until_button['state'] = 'disabled'
    p4_try_until_button['state'] = 'disabled'

    log_entry(information_text, 'Select which polynome you want to evaluate.', 'green')

    # Start the window
    main_window.mainloop()

