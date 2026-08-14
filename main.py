import psutil
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class PerformanceMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title('Performans Monitörü')
        self.root.geometry('950x800')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.data_length = 50
        self.cpu_data = np.zeros(self.data_length)
        self.ram_data = np.zeros(self.data_length)
        self.time_data = np.arange(1, self.data_length + 1)

        self.previous_ram_usage = {}

        self.graph_frame = Frame(self.root)
        self.graph_frame.pack(side=TOP, fill=BOTH, expand=True)

        self.cpu_frame = Frame(self.graph_frame)
        self.cpu_frame.pack(side=TOP, fill=X)

        self.fig, self.ax1 = plt.subplots(figsize=(5, 3))
        self.fig.tight_layout(pad=4)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.cpu_frame)
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=True)

        self.cpu_icon = Image.open('cpu_icon.png')
        self.cpu_icon = self.cpu_icon.resize((80, 80))
        self.cpu_icon = ImageTk.PhotoImage(self.cpu_icon)
        self.cpu_icon_label = Label(self.cpu_frame, image=self.cpu_icon, bd=0, highlightthickness=0, bg='white')
        self.cpu_icon_label.place(relx=0.012, rely=0.5, anchor=W)

        self.ram_frame = Frame(self.graph_frame)
        self.ram_frame.pack(side=TOP, fill=X)

        self.fig2, self.ax2 = plt.subplots(figsize=(5, 3))
        self.fig2.tight_layout(pad=4)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.ram_frame)
        self.canvas2.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)

        self.ram_icon = Image.open('ram_icon.png')
        self.ram_icon = self.ram_icon.resize((80, 80))
        self.ram_icon = ImageTk.PhotoImage(self.ram_icon)
        self.ram_icon_label = Label(self.ram_frame, image=self.ram_icon, bd=0, highlightthickness=0, bg='white')
        self.ram_icon_label.place(relx=0.012, rely=0.5, anchor=W)

        self.table_frame = Frame(self.root)
        self.table_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.columns = ('Ad', 'PID', 'CPU Kullanımı (%)', 'Bellek Kullanımı (MB)')
        self.process_table = ttk.Treeview(self.table_frame, columns=self.columns, show='headings', height=20)

        for col in self.columns:
            self.process_table.heading(col, text=col, anchor=CENTER)
            self.process_table.column(col, anchor=CENTER)

        self.process_table.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.table_frame, orient=VERTICAL, command=self.process_table.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.process_table.configure(yscrollcommand=self.scrollbar.set)

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview",
                             background="white",
                             foreground="black",
                             rowheight=25,
                             font=("Arial", 12))
        self.style.configure("Treeview.Heading",
                             font=("Arial", 14, "bold"),
                             background="gray",
                             foreground="white",
                             borderwidth=1)
        self.style.map("Treeview", background=[('selected', 'blue')])

        self.process_table.tag_configure('oddrow', background='lightgray')
        self.process_table.tag_configure('evenrow', background='white')
        self.process_table.tag_configure('highlight', background='lightgreen')

        self.update_data()

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=0.1)

    def get_ram_usage(self):
        return psutil.virtual_memory().percent

    def get_process_list(self):
        process_list = []
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
                process_list.append((proc.info['name'], proc.info['pid'], proc.info['cpu_percent'], memory_mb))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return process_list

    def update_data(self):
        self.cpu_data = np.roll(self.cpu_data, -1)
        self.ram_data = np.roll(self.ram_data, -1)
        self.cpu_data[-1] = self.get_cpu_usage()
        self.ram_data[-1] = self.get_ram_usage()

        self.update_graph()
        self.update_process_table()

        self.root.after(500, self.update_data)

    def update_graph(self):
        self.ax1.clear()
        self.ax1.plot(self.time_data, self.cpu_data, label='CPU Kullanımı (%)', color='blue', linewidth=2)
        self.ax1.fill_between(self.time_data, self.cpu_data, color='lightblue', alpha=0.5)
        self.ax1.set_xlabel('Zaman (s)')
        self.ax1.set_ylabel('CPU Kullanımı (%)')

        avg_cpu = np.mean(self.cpu_data)
        max_cpu = np.max(self.cpu_data)
        min_cpu = np.min(self.cpu_data)
        self.ax1.axhline(avg_cpu, color='green', linestyle='--', label=f'Ortalama CPU: {avg_cpu:.2f}%')
        self.ax1.axhline(max_cpu, color='red', linestyle='--', label=f'Maksimum CPU: {max_cpu:.2f}%')
        self.ax1.axhline(min_cpu, color='orange', linestyle='--', label=f'Minimum CPU: {min_cpu:.2f}%')

        self.ax1.legend(loc='upper left')
        self.ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

        self.ax2.clear()
        self.ax2.plot(self.time_data, self.ram_data, label='RAM Kullanımı (%)', color='red', linewidth=2)
        self.ax2.fill_between(self.time_data, self.ram_data, color='lightcoral', alpha=0.5)
        self.ax2.set_xlabel('Zaman (s)')
        self.ax2.set_ylabel('RAM Kullanımı (%)')

        avg_ram = np.mean(self.ram_data)
        max_ram = np.max(self.ram_data)
        min_ram = np.min(self.ram_data)
        self.ax2.axhline(avg_ram, color='green', linestyle='--', label=f'Ortalama RAM: {avg_ram:.2f}%')
        self.ax2.axhline(max_ram, color='red', linestyle='--', label=f'Maksimum RAM: {max_ram:.2f}%')
        self.ax2.axhline(min_ram, color='orange', linestyle='--', label=f'Minimum RAM: {min_ram:.2f}%')

        self.ax2.legend(loc='upper left')
        self.ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

        self.canvas.draw_idle()
        self.canvas2.draw_idle()

    def update_process_table(self):
        for row in self.process_table.get_children():
            self.process_table.delete(row)

        process_list = self.get_process_list()
        for i, process in enumerate(process_list):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            memory = f"{process[3]:.2f} MB"

            if process[1] in self.previous_ram_usage and self.previous_ram_usage[process[1]] != process[3]:
                tag = 'highlight'
                self.previous_ram_usage[process[1]] = process[3]
            else:
                self.previous_ram_usage[process[1]] = process[3]

            self.process_table.insert("", END, values=(process[0], process[1], f"{process[2]:.2f}%", memory), tags=(tag,))

    def on_close(self):
        self.root.destroy()
        self.root.quit()

if __name__ == "__main__":
    root = Tk()
    app = PerformanceMonitor(root)
    root.mainloop()
