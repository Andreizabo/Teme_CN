import tkinter as tk
from termcolor import colored

def read_input():
    '''
    Callback method for "Read input" button.

    @returns : a dictionary of values
    '''
    path = "./input.json"

    print(colored(f"read_input at {path}", "red"))

def run():
    '''
    Callback method for "Run" button.

    @returns: nothing
    '''
    print(colored(f"run program", "blue"))

if __name__ == "__main__":

    # Main window configuration
    main_window = tk.Tk()
    main_window.title("Template GUI")
    main_window.geometry("300x300")

    # Top frame (used for control buttons)
    frame_top = tk.Frame(main_window)
    frame_top.pack(side=tk.TOP)

    # Read input button
    read_input_button = tk.Button(frame_top, text="Read input", command=read_input, padx=10)
    read_input_button.grid(row=0, column=0)

    # Run button
    run_button = tk.Button(frame_top, text="Run", command=run, padx=10)
    run_button.grid(row=0, column=1)

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

    default_msg = '''
    There are 4 types of messages:
    [INFO] Information messages, which reveal aspects about the program state, in which process it is or whether or not it waits for input (GREEN)
    [DEBUG] Relevant only to the developers, should not be visible in the final stage (BLUE)
    [ERROR] Why the program crashed (RED)
    [WARNING] warning, but not really cases for exceptions or program ending (YELLOW)

    Also, we could
    add
    besides the info provided
    something related to the current time stamp.

    This is only the default message. It 
    should 
    also
    be
    colored.
    
    Hello world!
    '''

    information_text.insert(tk.END, default_msg)

    # Start the window
    main_window.mainloop()