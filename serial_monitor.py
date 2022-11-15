import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import ttk
from multiprocessing import Process, Queue

lines = Queue()
selected_port_names = Queue()

def send_line_event():
    root.event_generate("<<FoundNewLine>>")

def show_connection_failed():
    status_label.config(text="Port could not be found!")
    status_label.config(foreground='#f00')

def check_serial_output():
    print("Starting output.")
    while True:
        # print("Queue size: " + str(selected_port_names.qsize()))
        while selected_port_names.qsize() > 0:
            active_port_name = port_names.get()
            print("Taken from queue.")
            try:
                print("Attempting connection...")
                port = serial.Serial(active_port_name)
                print("Connection completed!")
                while selected_port_names.qsize() == 0:
                    if port.isOpen():
                        if port.in_waiting > 0:
                            line = port.readline().decode("utf-8").strip()
                            lines.put(line)
                            print(line)
                            send_line_event()
            except:
                show_connection_failed()
                print("Connection failure!")
            print("Disconnected from port.")

def attempt_port_selection(*_):
    if option_select.get() in port_names:
        status_label.config(text="Connected to port.")
        status_label.config(foreground='#000')
        return option_select.get()
    else:
        status_label.config(text="Port could not be found!")
        status_label.config(foreground='#f00')
        return None

if __name__ == "__main__":
    # fetching all active ports
    port_names = list(map(lambda port: port.name, serial.tools.list_ports.comports()))

    # creating a window to display the port selection
    global tk_root
    root = Tk()
    tk_root = root
    root.title("Serial Monitor")
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    label = ttk.Label(frm, text="Please select a port:")
    label.grid(column=0, row=0)

    # used to save the port from attempt_port_selection before callback is completed
    def save_port(*_):
        new_port_name = attempt_port_selection(*_)
        selected_port_names.put(new_port_name)
        print("GUI: " + str(new_port_name))
        print("Queue size: " + str(selected_port_names.qsize()))
        return new_port_name

    # creating a listener to see when the contents of the combobox change
    selected = StringVar()
    selected.trace_add('write', save_port)

    option_select = ttk.Combobox(frm, textvar=selected, values=port_names)
    option_select.grid(column=1, row=0)

    status_label = ttk.Label(frm, text="No port selected.", foreground='#f00')
    status_label.grid(column=0, columnspan=2, row=1)

    def add_line():
        output_console.config(state=NORMAL)
        output_console.insert(END, lines.get())
        output_console.config(state=DISABLED)

    output_console = Text(frm, height=20, state=DISABLED, xscrollcommand=True, yscrollcommand=True, padx=10, pady=10)
    output_console.grid(column=0, columnspan=2, row=2)
    output_console.bind("<<FoundNewLine>>", add_line)

    scanning_proc = Process(target=check_serial_output)
    scanning_proc.start()
    # tkinter has to run on main thread
    root.mainloop()