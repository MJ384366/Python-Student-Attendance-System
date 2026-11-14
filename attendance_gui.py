import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import attendance_manager as app

# Load existing student records
app.load_data()

# Main window
root = tk.Tk()
root.title("Student Attendance Manager")
root.geometry("1000x650")
root.configure(bg="#F0F4F8")

# Heading
heading = tk.Label(
    root,
    text="STUDENT ATTENDANCE MANAGER",
    font=("Arial", 23, "bold"),
    bg="#173B67",
    fg="white",
    pady=20
)
heading.pack(fill="x")

# Subtitle
tk.Label(
    root,
    text="Manage student records and attendance easily",
    font=("Arial", 13),
    bg="#F0F4F8",
    fg="#173B67"
).pack(pady=12)

# Main frame
main_frame = tk.Frame(root, bg="#F0F4F8")
main_frame.pack(fill="both", expand=True, padx=25, pady=15)

# Buttons frame
button_frame = tk.Frame(main_frame, bg="#F0F4F8")
button_frame.pack(side="left", fill="y", padx=15)

# Student table
table_frame = tk.Frame(main_frame, bg="white")
table_frame.pack(side="right", fill="both", expand=True, padx=15)

tk.Label(
    table_frame,
    text="STUDENT RECORDS",
    font=("Arial", 16, "bold"),
    bg="white",
    fg="#173B67"
).pack(pady=12)

columns = ("roll", "name", "held", "attended", "percentage")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=15
)

tree.heading("roll", text="Roll Number")
tree.heading("name", text="Name")
tree.heading("held", text="Classes Held")
tree.heading("attended", text="Attended")
tree.heading("percentage", text="Percentage")

tree.column("roll", width=90, anchor="center")
tree.column("name", width=120, anchor="center")
tree.column("held", width=90, anchor="center")
tree.column("attended", width=90, anchor="center")
tree.column("percentage", width=100, anchor="center")

tree.pack(fill="both", expand=True, padx=10, pady=10)


# Refresh student table
def refresh_table():
    for item in tree.get_children():
        tree.delete(item)

    for student in app.students:
        held = student["held"]
        attended = student["attended"]

        percentage = (
            (attended / held) * 100 if held > 0 else 0
        )

        tree.insert(
            "",
            "end",
            values=(
                student["roll"],
                student["name"],
                held,
                attended,
                f"{percentage:.2f}%"
            )
        )


# Add student
def add_student_gui():
    roll = simpledialog.askstring(
        "Add Student", "Enter roll number:", parent=root
    )

    if roll is None:
        return

    roll = roll.strip()

    if not roll:
        messagebox.showerror("Error", "Roll number cannot be empty.")
        return

    if any(s["roll"] == roll for s in app.students):
        messagebox.showerror("Error", "Roll number already exists.")
        return

    name = simpledialog.askstring(
        "Add Student", "Enter student name:", parent=root
    )

    if name is None:
        return

    name = name.strip()

    if not name:
        messagebox.showerror("Error", "Student name cannot be empty.")
        return

    student = {
        "roll": roll,
        "name": name,
        "held": 0,
        "attended": 0
    }

    app.students.append(student)
    app.save_data()
    refresh_table()

    messagebox.showinfo(
        "Success", f"Student {name} added successfully!"
    )


# Mark attendance
def mark_attendance_gui():
    roll = simpledialog.askstring(
        "Mark Attendance", "Enter roll number:", parent=root
    )

    if roll is None:
        return

    roll = roll.strip()

    student = next(
        (s for s in app.students if s["roll"] == roll), None
    )

    if student is None:
        messagebox.showerror("Error", "Roll number not found.")
        return

    status = simpledialog.askstring(
        "Mark Attendance",
        "Enter status (P for Present / A for Absent):",
        parent=root
    )

    if status is None:
        return

    status = status.strip().upper()

    if status not in ["P", "A"]:
        messagebox.showerror(
            "Error", "Invalid status. Enter P or A."
        )
        return

    student["held"] += 1

    if status == "P":
        student["attended"] += 1

    app.save_data()
    refresh_table()

    messagebox.showinfo(
        "Success", "Attendance marked successfully!"
    )


# Show attendance percentage
def show_percentage_gui():
    roll = simpledialog.askstring(
        "Attendance Percentage",
        "Enter roll number:",
        parent=root
    )

    if roll is None:
        return

    roll = roll.strip()

    student = next(
        (s for s in app.students if s["roll"] == roll), None
    )

    if student is None:
        messagebox.showerror("Error", "Roll number not found.")
        return

    held = student["held"]

    if held == 0:
        result = "No classes held yet."
        percentage = 0
    else:
        percentage = (student["attended"] / held) * 100
        result = f"Attendance: {percentage:.2f}%"

    messagebox.showinfo(
        "Attendance Result",
        f"Name: {student['name']}\n"
        f"Roll: {student['roll']}\n"
        f"{result}"
    )


# Show attendance shortage
def show_shortage_gui():
    refresh_table()

    shortage = []

    for student in app.students:
        held = student["held"]

        if held == 0:
            continue

        percentage = (student["attended"] / held) * 100

        if percentage < 75:
            shortage.append(
                f"{student['name']} ({student['roll']}): "
                f"{percentage:.2f}%"
            )

    if shortage:
        messagebox.showinfo(
            "Attendance Shortage",
            "\n".join(shortage)
        )
    else:
        messagebox.showinfo(
            "Attendance Shortage",
            "No students have attendance below 75%."
        )


# Create buttons
def create_button(text, command):
    tk.Button(
        button_frame,
        text=text,
        command=command,
        font=("Arial", 12, "bold"),
        bg="#2463A6",
        fg="white",
        activebackground="#173B67",
        activeforeground="white",
        width=25,
        pady=12,
        cursor="hand2"
    ).pack(pady=10)


create_button("Add Student", add_student_gui)
create_button("Mark Attendance", mark_attendance_gui)
create_button("Show Attendance Percentage", show_percentage_gui)
create_button("Show Attendance Shortage", show_shortage_gui)
create_button("Refresh Records", refresh_table)
create_button("Exit", root.destroy)

# Display saved records
refresh_table()

# Start GUI
root.mainloop()