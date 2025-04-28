import tkinter as tk
from tkinter import messagebox
import json
import os

FILENAME = "tasks_gui_colorful.json"

def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks):
    with open(FILENAME, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task():
    task = task_entry.get()
    priority = priority_var.get()

    if task:
        tasks.append({"task": task, "priority": priority, "done": False})
        save_tasks(tasks)
        update_listbox()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task!")

def delete_task():
    try:
        selected_index = listbox.curselection()[0]
        tasks.pop(selected_index)
        save_tasks(tasks)
        update_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete!")

def mark_done():
    try:
        selected_index = listbox.curselection()[0]
        tasks[selected_index]['done'] = True
        save_tasks(tasks)
        update_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark as done!")

def clear_done_tasks():
    global tasks
    tasks = [task for task in tasks if not task.get('done')]
    save_tasks(tasks)
    update_listbox()
    messagebox.showinfo("Cleared", "All completed tasks have been removed!")

def update_listbox():
    listbox.delete(0, tk.END)
    for t in tasks:
        display_text = t['task']
        if t.get('done'):
            display_text += " ✅"
        else:
            display_text += f" [{t['priority']}]"
        
        color = get_priority_color(t['priority']) if not t.get('done') else "gray"
        listbox.insert(tk.END, display_text)
        listbox.itemconfig(tk.END, {'fg': color})

def get_priority_color(priority):
    if priority == "High":
        return "red"
    elif priority == "Medium":
        return "orange"
    else:
        return "green"

# GUI setup
root = tk.Tk()
root.title("📝 Colorful To-Do List GUI (Done ✅ + Clear Feature)")

# Load tasks
tasks = load_tasks()

# Task entry
task_entry = tk.Entry(root, width=40)
task_entry.grid(row=0, column=0, padx=10, pady=10)

# Priority menu
priority_var = tk.StringVar(root)
priority_var.set("Medium")
priority_menu = tk.OptionMenu(root, priority_var, "High", "Medium", "Low")
priority_menu.grid(row=0, column=1, padx=10)

# Add button
add_button = tk.Button(root, text="Add Task", width=15, command=add_task)
add_button.grid(row=0, column=2, padx=10)

# Listbox
listbox = tk.Listbox(root, width=60)
listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Buttons
delete_button = tk.Button(root, text="Delete Selected Task", width=20, command=delete_task)
delete_button.grid(row=2, column=0, pady=10)

done_button = tk.Button(root, text="Mark as Done ✅", width=20, command=mark_done)
done_button.grid(row=2, column=1, pady=10)

clear_button = tk.Button(root, text="Clear Done Tasks 🗑️", width=20, command=clear_done_tasks)
clear_button.grid(row=2, column=2, pady=10)

# Populate listbox
update_listbox()

# Start the GUI loop
root.mainloop()
