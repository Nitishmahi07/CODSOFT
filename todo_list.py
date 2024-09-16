import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import sqlite3

conn = sqlite3.connect('todo_list.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task TEXT,
            status TEXT
            )''')
conn.commit()

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("380x500")
        self.root.config(bg="#FBD786")
        self.create_widgets()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        title = tk.Label(self.root, text="My To-Do List", font=("Times New Roman", 20), bg="#FBD786")
        title.pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        self.task_listbox = tk.Listbox(frame, height=10, width=40, font=("Arial", 14), selectmode=tk.SINGLE)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        self.load_tasks()

        button_frame = tk.Frame(self.root, bg="#FBD786")
        button_frame.pack(pady=20)

        add_button = tk.Button(button_frame, text="Add Task", command=self.add_task, font=("Arial", 12), width=10)
        add_button.grid(row=0, column=0, padx=10)

        delete_button = tk.Button(button_frame, text="Delete Task", command=self.delete_task, font=("Arial", 12), width=10)
        delete_button.grid(row=0, column=1, padx=10)

        edit_button = tk.Button(button_frame, text="Edit Task", command=self.edit_task, font=("Arial", 12), width=10)
        edit_button.grid(row=0, column=2, padx=10)

        mark_done_button = tk.Button(button_frame, text="Mark as Done", command=self.mark_done, font=("Arial", 12), width=10)
        mark_done_button.grid(row=1, column=1, padx=10)

        export_button = tk.Button(self.root, text="Save To File", command=self.save_to_file, font=("Arial", 12), width=16)
        export_button.pack(pady=10)

    def add_task(self):
        task = simpledialog.askstring("Input", "Enter the task:", parent=self.root)
        if task:
            try:
                c.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, 'pending'))
                conn.commit()
                self.load_tasks()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

    def delete_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            task_id = self.task_listbox.get(selected_task).split(":")[0]
            try:
                c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
                conn.commit()
                self.load_tasks()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def edit_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            task_id, task_text = self.task_listbox.get(selected_task).split(": ", 1)
            new_task = simpledialog.askstring("Input", "Edit the task:", initialvalue=task_text, parent=self.root)
            if new_task:
                try:
                    c.execute("UPDATE tasks SET task=? WHERE id=?", (new_task, task_id))
                    conn.commit()
                    self.load_tasks()
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")

    def mark_done(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            task_id = self.task_listbox.get(selected_task).split(":")[0]
            try:
                c.execute("UPDATE tasks SET status=? WHERE id=?", ('done', task_id))
                conn.commit()
                self.load_tasks()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

    def save_to_file(self):
        tasks = self.task_listbox.get(0, tk.END)
        if tasks:
            file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt")])
            if file:
                try:
                    with open(file, 'w') as f:
                        for task in tasks:
                            f.write(task + "\n")
                    messagebox.showinfo("Success", "Tasks saved successfully!")
                except IOError as e:
                    messagebox.showerror("File Error", str(e))

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        try:
            c.execute("SELECT id, task, status FROM tasks")
            rows = c.fetchall()
            for row in rows:
                task = f"{row[0]}: {row[1]}"
                if row[2] == "done":
                    task += " (Done)"
                self.task_listbox.insert(tk.END, task)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def on_closing(self):
        conn.close()
        self.root.destroy()

root = tk.Tk()
app = ToDoApp(root)
root.mainloop()
