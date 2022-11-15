import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import ttk
from threading import Thread

def main():
    def check_serial_output(port):
        while not type(port) and port != None and port.isOpen():
            if port.in_waiting > 0:
                line = port.readline().decode("utf-8").strip()
                output_console.insert(END, line)

    def attempt_port_selection(index, value, op):
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

    global active_port
    active_port = None
    def save_port(index, value, op):
        global active_port
        active_port = attempt_port_selection(index, value, op)
        return active_port

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

    output_thread = Thread(target=check_serial_output(active_port))
    output_thread.start()
    output_thread.join()

    root.mainloop()

if __name__ == "__main__":
    main()