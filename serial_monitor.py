import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import ttk
from multiprocessing import Process, Lock

global port_lock 
port_lock = Lock()

global active_port
active_port = None

lines = []

def check_serial_output():
    while True:
        port_lock.acquire()
        try:
            global active_port
            print("BACK: " + str(active_port))
            if active_port != None and active_port.isOpen():
                if active_port.in_waiting > 0:
                    line = active_port.readline().decode("utf-8").strip()
                    print(line)
                    lines.append(line)
                    # output_console.insert(END, line)
        finally:
            port_lock.release()

def main():
    def attempt_port_selection(*_):
        if option_select.get() in port_names:
            try:
                print("Attempting connection...")
                port = serial.Serial(option_select.get())
                print("Connection completed!")
                warning_label.grid_forget()
                missing_label.grid_forget()
                connected_label.grid(column=0, columnspan=2, row=1)
                return port    
            except:
                connected_label.grid_forget()
                missing_label.grid_forget()
                warning_label.grid(column=0, columnspan=2, row=1)
                return None
        else:
            connected_label.grid_forget()
            missing_label.grid_forget()
            warning_label.grid(column=0, columnspan=2, row=1)
            return None 

    # fetching all active ports
    port_names = list(map(lambda port: port.name, serial.tools.list_ports.comports()))

    # creating a window to display the port selection
    root = Tk()
    root.title("Serial Monitor")
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    label = ttk.Label(frm, text="Please select a port:")
    label.grid(column=0, row=0)

    # used to save the port from attempt_port_selection before callback is completed
    def save_port(*_):
        port_lock.acquire()
        try:
            global active_port
            active_port = attempt_port_selection(*_)
            print("GUI: " + str(active_port))
            return active_port
        finally:
            port_lock.release()

    # creating a listener to see when the contents of the combobox change
    selected = StringVar()
    selected.trace_add('write', save_port)

    option_select = ttk.Combobox(frm, textvar=selected, values=port_names)
    option_select.grid(column=1, row=0)

    missing_label = ttk.Label(frm, text="No port selected.", foreground='#f00')
    warning_label = ttk.Label(frm, text="Port could not be found!", foreground='#f00')
    connected_label = ttk.Label(frm, text="Connected to port.")
    missing_label.grid(column=0, columnspan=2, row=1)

    output_console = Text(frm, height=20, state=DISABLED, xscrollcommand=True, yscrollcommand=True, padx=10, pady=10)
    output_console.grid(column=0, columnspan=2, row=2)

    scanning_proc = Process(target=check_serial_output, name="scanning_proc")
    scanning_proc.start()
    # tkinter has to run on main thread
    root.mainloop()

if __name__ == "__main__":
    main()