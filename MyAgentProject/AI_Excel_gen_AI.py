'''Key Takeaways-WHAT OUR DATA MEANS

EmpID + Code + EmpName = unique context for a row

TypeFlag (-1/1) = status

Param1/Param2 = task metrics

Start/End dates = duration for pivot charts

Some rows are incomplete—maybe templates or defaults '''


"""

1609441 test.test1.test3    1/15.34 -1  100 622 669
160441  test.test1.test3    2/11.101    -1  100 140216  177363
16041   test2.test8.test6   2/15.34 -1  100 2791    2346
160441  test.test7.test5    2/15.34 1   100 Bin Any 5   1794    2346 10/31/2024 11/10/2024 Alex
160441  test.test7.test5    2/15.34 1   100 Bin Any 5   1794    2346 10/31/2024 11/10/2025 John
1609441 test4.test4.test4   2/15.34 1   100 E   Any 5   997 0
1642    test4.test3.test1   28.0.101    -1  100 5409155 10357332
16421    test4.test3.test1   28.0.101    -1  100 5409155 10357332
160441  test.test1.test3    2/11.101    -1  100 140216  177363
16041   test2.test8.test6   2/15.34 -1  100 2791    2346 10/31/2024
160441  test.test7.test5    2/15.34 1   100 Bin Any 5   1794    2346 10/31/2024 11/10/2024 Alex
160441  test.test7.test5    2/15.34 1   100 Bin Any 5   1794    2346 10/31/2024 11/10/2025 John
1609441 test4.test4.test4   2/15.34 1   100 E   Any 5   997 0
1642    test4.test3.test1   28.0.101    -1  100 5409155 10357332
16421    test4.test3.test1   28.0.101    -1  100 5409155 10357332
16420    test4.test3.test1   28.0.101    -1  100 5409155 10357332
164223    test4.test3.test1   28.0.101    -1  100 5409155 10357332

160441  test.test9.test9    3/12.50 1 100 2000 2500 01/15/2025 02/14/2025 Emma
160442  test.test8.test7    4/14.20 -1 100 3000 3500 02/01/2025 03/01/2025 Liam
160443  test.test2.test3    2/10.10 1 100 4000 4500 03/10/2025 04/12/2025 Olivia
160444  test.test5.test1    5/11.50 -1 100 1500 1700 04/05/2025 04/25/2025 Noah
160445  test.test6.test4    1/13.75 1 100 5000 5200 05/08/2025 06/08/2025 Sophia


"""







import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import re



def convert():
    try:
        raw_text = e1.get("1.0", END).strip()
        if not raw_text:
            message.set("Please enter raw data!")
            return

        rows = []
        date_pattern = re.compile(r"\d{1,2}/\d{1,2}/\d{4}")

        for line in raw_text.splitlines():
            if not line.strip():
                continue

            parts = line.split()

            empname = None
            start = None
            end = None

            # Employee name (last token if alphabetic)
            if parts[-1].isalpha():
                empname = parts.pop()

            # End date
            if parts and date_pattern.match(parts[-1]):
                end = parts.pop()

            # Start date
            if parts and date_pattern.match(parts[-1]):
                start = parts.pop()

            # Pad remaining columns
            parts += [None] * (13 - len(parts))
            parts = parts[:13]

            rows.append(parts + [start, end, empname])

        columns = [
            'Empid','Pcode','Wparam','Hr_time','Type',
            'Type2','Paramval1','Paramval2','Paramval3',
            'Paramval4','Paramval5','Paramval6','Paramval7',
            'Start','End','EmpName'
        ]

        df = pd.DataFrame(rows, columns=columns)

        # Convert date columns
        df['Start'] = pd.to_datetime(df['Start'], errors='coerce')
        df['End'] = pd.to_datetime(df['End'], errors='coerce')

        # Numeric columns
        param_cols = [c for c in df.columns if c.startswith("Paramval")]
        for col in param_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Duration calculation
        df['Duration'] = (df['End'] - df['Start']).dt.days.fillna(0)

        df.to_csv("test.csv", index=False)
        df.to_excel("testnew.xlsx", sheet_name="RawData", index=False)

        message.set("Excel report generated successfully")

    except Exception as e:
        message.set(f"Error: {e}")



def generate_pivot_excel():
    try:
        df = pd.read_excel("testnew.xlsx", sheet_name="RawData")

        param_cols = [
            "Paramval1","Paramval2","Paramval3",
            "Paramval4","Paramval5","Paramval6",
            "Paramval7","Duration"
        ]

        for col in param_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        pivot = pd.pivot_table(
            df,
            index="EmpName",
            values=param_cols,
            aggfunc="sum",
            fill_value=0
        )

        with pd.ExcelWriter("Pivot_Report_Full.xlsx", engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="RawData", index=False)
            pivot.to_excel(writer, sheet_name="PivotSummary")

        message.set("Pivot + Raw data saved to Pivot_Report_Full.xlsx")

    except Exception as e:
        message.set(f"Error: {e}")


def show_pivot_chart():
    try:
        pivot = pd.read_excel(
            "Pivot_Report_Full.xlsx",
            sheet_name="PivotSummary",
            index_col=0
        )

        pivot.plot(kind='bar', figsize=(10, 6))
        plt.title("Employee Pivot Summary")
        plt.xlabel("Employee")
        plt.ylabel("Values")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        message.set(f"Error: {e}")

def show_duration_chart():
    try:
        pivot = pd.read_excel(
            "Pivot_Report_Full.xlsx",
            sheet_name="PivotSummary",
            index_col=0
        )

        if 'Duration' in pivot.columns:
            pivot['Duration'].plot(
                kind='bar',
                figsize=(10, 6),
                color='skyblue'
            )

            plt.title("Employee vs Total Duration (Days)")
            plt.xlabel("Employee")
            plt.ylabel("Total Duration")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            message.set("Duration column not found")

    except Exception as e:
        message.set(f"Error: {e}")



root = tk.Tk()
root.title("Excel Report Generator")
root.geometry("900x650")
root.config(bg="black")

message = StringVar()

header_frame = Frame(root, bg="lightblue")
header_frame.pack(fill=X)

try:
    logo_img = Image.open('logo.png')
    logo_img = logo_img.resize((200, 100))
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = Label(header_frame, image=logo, bg="lightblue")
    logo_label.image = logo
    logo_label.pack(pady=5)
except:
    pass

Label(
    header_frame,
    text="APtech",
    bg="lightblue",
    fg="black",
    font=("Times New Roman", 16, "bold")
).pack()

Label(
    root,
    text="~GEN-AI Devlopment ~",
    bg="lightblue",
    fg="black"
).pack(fill=X)

frame = Frame(root, bg="black")
frame.pack(pady=20)

Label(
    frame,
    text="Enter Raw Data Below:",
    fg="white",
    bg="black"
).grid(row=0, column=0, sticky=W)

e1 = Text(frame, width=110, height=14)
e1.grid(row=1, column=0, padx=10, pady=10)

Button(
    frame,
    text="Generate Excel",
    bg="red",
    fg="white",
    width=50,
    command=convert
).grid(row=2, column=0, pady=5)

Button(
    frame,
    text="Generate (Excel + Pivot)",
    bg="orange",
    fg="white",
    width=50,
    command=generate_pivot_excel
).grid(row=3, column=0, pady=5)

Button(
    frame,
    text="Generate Pivot Chart",
    bg="yellow",
    fg="black",
    width=50,
    command=show_pivot_chart
).grid(row=4, column=0, pady=5)

Button(
    frame,
    text="Show Duration Chart",
    bg="green",
    fg="white",
    width=50,
    command=show_duration_chart
).grid(row=5, column=0, pady=5)

Button(
    frame,
    text="Quit",
    bg="darkblue",
    fg="white",
    width=50,
    command=root.quit
).grid(row=6, column=0, pady=5)

Label(frame, textvariable=message, fg="cyan", bg="black").grid(row=7, column=0)

root.mainloop()

