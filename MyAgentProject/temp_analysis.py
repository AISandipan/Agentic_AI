import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Thermo Analytics Dashboard")
        self.geometry("1100x650")

        self.df = None

        # Try auto-load CSV
        try:
            self.df = pd.read_csv("temp.csv")
            print("temp.csv loaded automatically")
        except:
            print("temp.csv not found")

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(self.sidebar, text="Controls", font=("Arial", 18)).pack(pady=10)

        ctk.CTkButton(self.sidebar, text="Load CSV", command=self.load_data).pack(pady=5)

        # Dropdowns for axis selection
        self.x_var = ctk.StringVar(value="Time")
        self.y_var = ctk.StringVar(value="Temp_out_C")

        self.x_menu = ctk.CTkOptionMenu(self.sidebar, variable=self.x_var, values=[])
        self.x_menu.pack(pady=5)

        self.y_menu = ctk.CTkOptionMenu(self.sidebar, variable=self.y_var, values=[])
        self.y_menu.pack(pady=5)

        # Graph buttons
        ctk.CTkButton(self.sidebar, text="Line Graph", command=self.plot_line).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Bar Graph", command=self.plot_bar).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Scatter Plot", command=self.plot_scatter).pack(pady=5)

        ctk.CTkLabel(self.sidebar, text="--- Equation Input ---").pack(pady=10)

        self.temp_in = ctk.CTkEntry(self.sidebar, placeholder_text="Temp In")
        self.temp_in.pack(pady=2)

        self.temp_out = ctk.CTkEntry(self.sidebar, placeholder_text="Temp Out")
        self.temp_out.pack(pady=2)

        self.flow = ctk.CTkEntry(self.sidebar, placeholder_text="Flow rate")
        self.flow.pack(pady=2)

        self.eff = ctk.CTkEntry(self.sidebar, placeholder_text="Efficiency %")
        self.eff.pack(pady=2)

        ctk.CTkButton(self.sidebar, text="Calculate", command=self.calculate).pack(pady=10)

        self.result_label = ctk.CTkLabel(self.sidebar, text="")
        self.result_label.pack(pady=5)

        # Graph area
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Populate dropdowns if data loaded
        if self.df is not None:
            self.update_dropdowns()

    # Load CSV manually
    def load_data(self):
        file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file:
            self.df = pd.read_csv(file)
            self.update_dropdowns()
            self.result_label.configure(text="Data Loaded!")

    # Update dropdown values
    def update_dropdowns(self):
        cols = list(self.df.columns)
        self.x_menu.configure(values=cols)
        self.y_menu.configure(values=cols)

    # Plot functions
    def plot_line(self):
        if self.df is None:
            return

        x = self.x_var.get()
        y = self.y_var.get()

        fig, ax = plt.subplots()
        ax.plot(self.df[x], self.df[y], marker='o')
        ax.set_title(f"{x} vs {y}")
        self.show_plot(fig)

    def plot_bar(self):
        if self.df is None:
            return

        x = self.x_var.get()
        y = self.y_var.get()

        fig, ax = plt.subplots()
        ax.bar(self.df[x], self.df[y])
        ax.set_title(f"{x} vs {y}")
        self.show_plot(fig)

    def plot_scatter(self):
        if self.df is None:
            return

        x = self.x_var.get()
        y = self.y_var.get()

        fig, ax = plt.subplots()
        ax.scatter(self.df[x], self.df[y])
        ax.set_title(f"{x} vs {y}")
        self.show_plot(fig)

    # Display plot
    def show_plot(self, fig):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # Equation calculation
    def calculate(self):
        try:
            Tin = float(self.temp_in.get())
            Tout = float(self.temp_out.get())
            m = float(self.flow.get())
            eff = float(self.eff.get())

            Cp = 4.18  # kJ/kg°C

            Q = m * Cp * (Tout - Tin)
            useful = (eff / 100) * Q

            result = f"Heat Transfer: {Q:.2f} kW\nUseful Energy: {useful:.2f} kW"
            self.result_label.configure(text=result)

        except:
            self.result_label.configure(text="Invalid Input")


# Run app
if __name__ == "__main__":
    app = App()
    app.mainloop()
