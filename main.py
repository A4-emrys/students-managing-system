from database import DatabaseManager
from utils import (
    validate_email, validate_phone, validate_student_id,
    format_phone_number, sanitize_input, generate_student_id,
    format_name, log_error, log_info
)
import sys
import logging
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StudentManagementSystem:
    def __init__(self):
        self.db = DatabaseManager()

    def add_student(self):
        """Add a new student"""
        try:
            print("\n=== Add New Student ===")
            first_name = sanitize_input(input("Enter first name: "))
            last_name = sanitize_input(input("Enter last name: "))
            full_name = format_name(first_name, last_name)
            
            student_id = generate_student_id()
            course = sanitize_input(input("Enter course: "))
            
            while True:
                email = input("Enter email: ")
                if validate_email(email):
                    break
                print("Invalid email format. Please try again.")
            
            while True:
                phone = input("Enter phone number: ")
                if validate_phone(phone):
                    phone = format_phone_number(phone)
                    break
                print("Invalid phone format. Please try again.")
            
            while True:
                try:
                    attendance = float(input("Enter attendance percentage (0-100): "))
                    if 0 <= attendance <= 100:
                        break
                    print("Attendance must be between 0 and 100.")
                except ValueError:
                    print("Please enter a valid number.")
            
            grade = input("Enter grade (A/B/C/D/F): ").upper()
            if grade not in ['A', 'B', 'C', 'D', 'F']:
                grade = 'N/A'

            student_data = {
                "full_name": full_name,
                "student_id": student_id,
                "course": course,
                "email": email,
                "phone": phone,
                "attendance_percent": attendance,
                "grade": grade
            }

            self.db.add_student(student_data)
            print(f"\nStudent added successfully! Student ID: {student_id}")
            
        except Exception as e:
            log_error(f"Error adding student: {str(e)}")
            print("\nFailed to add student. Please try again.")

    def view_student(self):
        """View a student's details"""
        try:
            student_id = input("\nEnter student ID: ")
            if not validate_student_id(student_id):
                print("Invalid student ID format.")
                return

            student = self.db.get_student(student_id)
            if student:
                print("\n=== Student Details ===")
                print(f"Name: {student['full_name']}")
                print(f"Student ID: {student['student_id']}")
                print(f"Course: {student['course']}")
                print(f"Email: {student['email']}")
                print(f"Phone: {student['phone']}")
                print(f"Attendance: {student['attendance_percent']}%")
                print(f"Grade: {student['grade']}")
            else:
                print("\nStudent not found.")
                
        except Exception as e:
            log_error(f"Error viewing student: {str(e)}")
            print("\nFailed to retrieve student details.")

    def list_all_students(self):
        """List all students"""
        try:
            students = self.db.get_all_students()
            if not students:
                print("\nNo students found in the database.")
                return

            print("\n=== All Students ===")
            print(f"{'Name':<30} {'ID':<10} {'Course':<20} {'Grade':<5}")
            print("-" * 65)
            for student in students:
                print(
                    f"{student['full_name']:<30} "
                    f"{student['student_id']:<10} "
                    f"{student['course']:<20} "
                    f"{student['grade']:<5}"
                )
                
        except Exception as e:
            log_error(f"Error listing students: {str(e)}")
            print("\nFailed to retrieve student list.")

    def update_student(self):
        """Update student information"""
        try:
            student_id = input("\nEnter student ID to update: ")
            if not validate_student_id(student_id):
                print("Invalid student ID format.")
                return

            student = self.db.get_student(student_id)
            if not student:
                print("\nStudent not found.")
                return

            print("\n=== Update Student ===")
            print("Press Enter to keep current values")
            
            update_data = {}
            
            new_name = input(f"Current name: {student['full_name']}\nNew name (Enter to skip): ")
            if new_name:
                update_data['full_name'] = sanitize_input(new_name)

            new_course = input(f"Current course: {student['course']}\nNew course (Enter to skip): ")
            if new_course:
                update_data['course'] = sanitize_input(new_course)

            new_email = input(f"Current email: {student['email']}\nNew email (Enter to skip): ")
            if new_email and validate_email(new_email):
                update_data['email'] = new_email

            new_phone = input(f"Current phone: {student['phone']}\nNew phone (Enter to skip): ")
            if new_phone and validate_phone(new_phone):
                update_data['phone'] = format_phone_number(new_phone)

            new_grade = input(f"Current grade: {student['grade']}\nNew grade (Enter to skip): ").upper()
            if new_grade in ['A', 'B', 'C', 'D', 'F']:
                update_data['grade'] = new_grade

            if update_data:
                if self.db.update_student(student_id, update_data):
                    print("\nStudent information updated successfully!")
                else:
                    print("\nFailed to update student information.")
            else:
                print("\nNo changes made.")
                
        except Exception as e:
            log_error(f"Error updating student: {str(e)}")
            print("\nFailed to update student information.")

    def delete_student(self):
        """Delete a student"""
        try:
            student_id = input("\nEnter student ID to delete: ")
            if not validate_student_id(student_id):
                print("Invalid student ID format.")
                return

            confirm = input(f"Are you sure you want to delete student {student_id}? (y/n): ")
            if confirm.lower() == 'y':
                if self.db.delete_student(student_id):
                    print("\nStudent deleted successfully!")
                else:
                    print("\nStudent not found.")
            else:
                print("\nDeletion cancelled.")
                
        except Exception as e:
            log_error(f"Error deleting student: {str(e)}")
            print("\nFailed to delete student.")

    def search_students(self):
        """Search for students"""
        try:
            print("\n=== Search/Filter Students ===")
            print("1. Search by name/email/course")
            print("2. Filter by course")
            print("3. Filter by attendance < 75%")
            print("4. Filter by grade")
            print("5. Back to main menu")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '1':
                self._search_by_term()
            elif choice == '2':
                self._filter_by_course()
            elif choice == '3':
                self._filter_by_attendance()
            elif choice == '4':
                self._filter_by_grade()
            elif choice == '5':
                return
            else:
                print("\nInvalid choice. Please try again.")
                
        except Exception as e:
            log_error(f"Error in search/filter: {str(e)}")
            print("\nFailed to perform search/filter operation.")

    def _search_by_term(self):
        """Search students by name, email, or course"""
        search_term = input("\nEnter search term (name, email, or course): ")
        students = self.db.search_students(search_term)
        self._display_student_list(students, "Search Results")

    def _filter_by_course(self):
        """Filter students by course"""
        courses = self.db.get_unique_courses()
        if not courses:
            print("\nNo courses found in the database.")
            return

        print("\nAvailable courses:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course}")
        
        try:
            choice = int(input("\nSelect course number: "))
            if 1 <= choice <= len(courses):
                students = self.db.filter_by_course(courses[choice - 1])
                self._display_student_list(students, f"Students in {courses[choice - 1]}")
            else:
                print("\nInvalid course number.")
        except ValueError:
            print("\nPlease enter a valid number.")

    def _filter_by_attendance(self):
        """Filter students with attendance below 75%"""
        students = self.db.filter_by_attendance(75.0)
        self._display_student_list(students, "Students with Attendance < 75%")

    def _filter_by_grade(self):
        """Filter students by grade"""
        print("\nAvailable grades: A, B, C, D, F")
        grade = input("Enter grade to filter by: ").upper()
        if grade in ['A', 'B', 'C', 'D', 'F']:
            students = self.db.filter_by_grade(grade)
            self._display_student_list(students, f"Students with Grade {grade}")
        else:
            print("\nInvalid grade.")

    def _display_student_list(self, students: List[Dict[str, Any]], title: str):
        """Display a list of students with consistent formatting"""
        if not students:
            print(f"\nNo students found for: {title}")
            return

        print(f"\n=== {title} ===")
        print(f"{'Name':<30} {'ID':<10} {'Course':<20} {'Attendance':<10} {'Grade':<5}")
        print("-" * 75)
        for student in students:
            print(
                f"{student['full_name']:<30} "
                f"{student['student_id']:<10} "
                f"{student['course']:<20} "
                f"{student['attendance_percent']:<10.1f} "
                f"{student['grade']:<5}"
            )

    def display_menu(self):
        """Display the main menu"""
        print("\n=== Student Management System ===")
        print("1. Add Student")
        print("2. View Student")
        print("3. List All Students")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Search/Filter Students")
        print("7. Launch GUI Version")
        print("8. Exit")

    def run(self):
        """Run the main application loop"""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-8): ")
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.view_student()
            elif choice == '3':
                self.list_all_students()
            elif choice == '4':
                self.update_student()
            elif choice == '5':
                self.delete_student()
            elif choice == '6':
                self.search_students()
            elif choice == '7':
                print("\nLaunching GUI version...")
                try:
                    from gui import StudentManagementGUI
                    app = StudentManagementGUI()
                    app.run()
                    # After GUI closes, return to CLI
                    continue
                except Exception as e:
                    log_error(f"Failed to launch GUI: {str(e)}")
                    print("\nFailed to launch GUI. Make sure tkinter is installed.")
            elif choice == '8':
                print("\nThank you for using the Student Management System!")
                sys.exit(0)
            else:
                print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    try:
        sms = StudentManagementSystem()
        sms.run()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        log_error(f"Unexpected error: {str(e)}")
        print("\nAn unexpected error occurred. Please check the logs.")
        sys.exit(1) 