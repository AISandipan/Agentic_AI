













import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score



try:
    df = pd.read_csv('Sample_Superstore.csv')
    required_columns = {'Sales', 'Profit', 'Quantity', 'Order Date'}
    if not required_columns.issubset(df.columns):
        raise ValueError("Missing required columns in dataset")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
except Exception as e:
    messagebox.showerror("Error", f"Failed to load dataset: {e}")
    exit()


y_ols = df['Quantity']
x_ols = df[['Sales', 'Profit']]
x_ols = sm.add_constant(x_ols)
ols_model = sm.OLS(y_ols, x_ols).fit()
summary_str = ols_model.summary().as_text()


root = tk.Tk()
root.title("Superstore Regression & Forecast App")
root.geometry("1100x900")

data_frame = ttk.Frame(root)
data_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

columns = ["Sales", "Profit", "Quantity"]
tree = ttk.Treeview(data_frame, columns=columns, show='headings', height=8)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(side=tk.LEFT, fill=tk.BOTH)
scroll = ttk.Scrollbar(data_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

def load_data(rows=10):
    tree.delete(*tree.get_children())
    subset = df[['Sales', 'Profit', 'Quantity']].head(rows)
    for _, row in subset.iterrows():
        tree.insert("", "end", values=(row["Sales"], row["Profit"], row["Quantity"]))

load_data()


def manual_regression():
    x = df['Sales'].values
    y = df['Profit'].values

    x_mean = np.mean(x)
    y_mean = np.mean(y)

    Sxy = np.sum((x - x_mean) * (y - y_mean))
    Sxx = np.sum((x - x_mean) ** 2)

    b1 = Sxy / Sxx
    b0 = y_mean - b1 * x_mean

    y_pred = b0 + b1 * x

    plt.figure(figsize=(8,5))
    plt.scatter(x, y)
    plt.plot(x, y_pred, color='red')
    plt.title("Manual Regression: Sales vs Profit")
    plt.xlabel("Sales")
    plt.ylabel("Profit")
    plt.show()

    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, y_pred)

    messagebox.showinfo("Manual Regression Results",
                        f"Slope: {b1:.4f}\nIntercept: {b0:.4f}\nRMSE: {rmse:.4f}\nR²: {r2:.4f}")


def sklearn_regression():
    x = df['Sales'].values.reshape(-1, 1)
    y = df['Profit'].values

    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)

    plt.figure(figsize=(8,5))
    plt.scatter(x, y)
    plt.plot(x, y_pred, color='green')
    plt.title("Sklearn Regression")
    plt.xlabel("Sales")
    plt.ylabel("Profit")
    plt.show()

    messagebox.showinfo("Sklearn Results",
                        f"Intercept: {model.intercept_:.4f}\n"
                        f"Coefficient: {model.coef_[0]:.4f}\n"
                        f"R²: {model.score(x, y):.4f}")


def monthly_plot():
    df_monthly = df.resample('ME', on='Order Date').agg({'Sales': 'sum', 'Profit': 'sum'})

    plt.figure(figsize=(10, 5))
    plt.bar(df_monthly.index, df_monthly['Sales'], alpha=0.6)
    plt.plot(df_monthly.index, df_monthly['Profit'], color='red')
    plt.title("Monthly Sales vs Profit")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def show_ols_summary():
    summary_window = tk.Toplevel(root)
    summary_window.title("OLS Regression Summary")

    text = tk.Text(summary_window, wrap='none', width=120)
    text.insert(tk.END, summary_str)
    text.pack()


btn_frame = ttk.Frame(root)
btn_frame.pack(pady=15)

ttk.Button(btn_frame, text="Manual Regression", command=manual_regression).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="Sklearn Regression", command=sklearn_regression).grid(row=0, column=1, padx=10)
ttk.Button(btn_frame, text="Monthly Plot", command=monthly_plot).grid(row=0, column=2, padx=10)
ttk.Button(btn_frame, text="OLS Summary", command=show_ols_summary).grid(row=0, column=5, padx=10)

root.mainloop()