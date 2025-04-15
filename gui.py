import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager
from utils import validate_email, validate_phone, validate_attendance, sanitize_input, generate_student_id
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StudentManagementGUI:
    def __init__(self):
        self.db = DatabaseManager()
        self.root = tk.Tk()
        self.root.title("Student Management System")
        self.root.geometry("1200x700")
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        
        self.setup_gui()
        self.load_students()

    def setup_gui(self):
        """Set up the main GUI layout"""
        # Create main frames
        self.form_frame = ttk.LabelFrame(self.root, text="Student Information", padding="10")
        self.form_frame.pack(fill="x", padx=10, pady=5)
        
        self.table_frame = ttk.LabelFrame(self.root, text="Student List", padding="10")
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.setup_form()
        self.setup_table()

    def setup_form(self):
        """Set up the input form"""
        # Create form fields
        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Course:", "course"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Attendance (%):", "attendance"),
            ("Grade:", "grade")
        ]
        
        self.entries = {}
        for i, (label, field) in enumerate(fields):
            row = i // 3
            col = i % 3
            
            ttk.Label(self.form_frame, text=label).grid(row=row*2, column=col*2, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(self.form_frame, width=30)
            entry.grid(row=row*2+1, column=col*2, padx=5, pady=5, sticky="w")
            self.entries[field] = entry
        
        # Add buttons
        btn_frame = ttk.Frame(self.form_frame)
        btn_frame.grid(row=4, column=0, columnspan=6, pady=10)
        
        ttk.Button(btn_frame, text="Add Student", command=self.add_student).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=5)

    def setup_table(self):
        """Set up the student table"""
        # Create Treeview
        columns = ("ID", "Name", "Course", "Email", "Phone", "Attendance", "Grade")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            width = 150 if col in ("Name", "Course", "Email") else 100
            self.tree.column(col, width=width, anchor="w")
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Pack everything
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)
        
        # Add buttons frame
        btn_frame = ttk.Frame(self.table_frame)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame, text="Edit Selected", command=self.edit_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.load_students).pack(side="left", padx=5)

    def add_student(self):
        """Add a new student from form data"""
        try:
            # Gather and validate form data
            first_name = sanitize_input(self.entries["first_name"].get())
            last_name = sanitize_input(self.entries["last_name"].get())
            full_name = f"{first_name} {last_name}"
            email = self.entries["email"].get().strip()
            phone = self.entries["phone"].get().strip()
            course = sanitize_input(self.entries["course"].get())
            attendance = self.entries["attendance"].get().strip()
            grade = self.entries["grade"].get().upper().strip()
            
            # Validate inputs
            if not all([first_name, last_name, email, course]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
                
            if not validate_email(email):
                messagebox.showerror("Error", "Invalid email format")
                return
                
            if phone and not validate_phone(phone):
                messagebox.showerror("Error", "Invalid phone format")
                return
                
            try:
                attendance = float(attendance)
                if not validate_attendance(attendance):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Attendance must be a number between 0 and 100")
                return
                
            if grade and grade not in ['A', 'B', 'C', 'D', 'F']:
                messagebox.showerror("Error", "Invalid grade")
                return
            
            # Create student data
            student_data = {
                "full_name": full_name,
                "student_id": generate_student_id(),
                "course": course,
                "email": email,
                "phone": phone,
                "attendance_percent": attendance,
                "grade": grade or 'N/A'
            }
            
            # Add to database
            self.db.add_student(student_data)
            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_form()
            self.load_students()
            
        except Exception as e:
            logger.error(f"Error adding student: {str(e)}")
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")

    def edit_selected(self):
        """Edit selected student"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to edit")
            return
            
        # Get student data
        student_id = self.tree.item(selected[0])["values"][0]
        student = self.db.get_student(student_id)
        
        if student:
            # Create edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Student")
            edit_window.geometry("400x500")
            
            # Create form fields
            entries = {}
            fields = [
                ("Name:", "full_name", student["full_name"]),
                ("Course:", "course", student["course"]),
                ("Email:", "email", student["email"]),
                ("Phone:", "phone", student["phone"]),
                ("Attendance (%):", "attendance_percent", str(student["attendance_percent"])),
                ("Grade:", "grade", student["grade"])
            ]
            
            for i, (label, field, value) in enumerate(fields):
                ttk.Label(edit_window, text=label).pack(padx=5, pady=2)
                entry = ttk.Entry(edit_window, width=40)
                entry.insert(0, value)
                entry.pack(padx=5, pady=2)
                entries[field] = entry
            
            def save_changes():
                try:
                    # Gather and validate data
                    update_data = {
                        "full_name": sanitize_input(entries["full_name"].get()),
                        "course": sanitize_input(entries["course"].get()),
                        "email": entries["email"].get().strip(),
                        "phone": entries["phone"].get().strip(),
                        "attendance_percent": float(entries["attendance_percent"].get()),
                        "grade": entries["grade"].get().upper().strip()
                    }
                    
                    # Validate inputs
                    if not validate_email(update_data["email"]):
                        messagebox.showerror("Error", "Invalid email format")
                        return
                        
                    if update_data["phone"] and not validate_phone(update_data["phone"]):
                        messagebox.showerror("Error", "Invalid phone format")
                        return
                        
                    if not validate_attendance(update_data["attendance_percent"]):
                        messagebox.showerror("Error", "Attendance must be between 0 and 100")
                        return
                        
                    if update_data["grade"] not in ['A', 'B', 'C', 'D', 'F', 'N/A']:
                        messagebox.showerror("Error", "Invalid grade")
                        return
                    
                    # Update database
                    if self.db.update_student(student_id, update_data):
                        messagebox.showinfo("Success", "Student updated successfully!")
                        edit_window.destroy()
                        self.load_students()
                    else:
                        messagebox.showerror("Error", "Failed to update student")
                        
                except Exception as e:
                    logger.error(f"Error updating student: {str(e)}")
                    messagebox.showerror("Error", f"Failed to update student: {str(e)}")
            
            # Add save button
            ttk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)

    def delete_selected(self):
        """Delete selected student"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            student_id = self.tree.item(selected[0])["values"][0]
            if self.db.delete_student(student_id):
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.load_students()
            else:
                messagebox.showerror("Error", "Failed to delete student")

    def load_students(self):
        """Load all students into the table"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load students
        students = self.db.get_all_students()
        for student in students:
            self.tree.insert("", "end", values=(
                student["student_id"],
                student["full_name"],
                student["course"],
                student["email"],
                student["phone"],
                f"{student['attendance_percent']}%",
                student["grade"]
            ))

    def clear_form(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def sort_treeview(self, col):
        """Sort treeview by column"""
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children("")]
        items.sort()
        
        for index, (_, item) in enumerate(items):
            self.tree.move(item, "", index)

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = StudentManagementGUI()
    app.run() 