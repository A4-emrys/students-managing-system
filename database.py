import sqlite3
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_name: str = "student_management.db"):
        self.db_name = db_name
        self.init_database()

    @contextmanager
    def get_db_cursor(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_name)
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()

    def init_database(self):
        """Initialize the database with the students table"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            student_id TEXT UNIQUE NOT NULL,
            course TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            attendance_percent REAL DEFAULT 0.0,
            grade TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with self.get_db_cursor() as cursor:
            cursor.execute(create_table_query)
            logger.info("Database initialized successfully")

    def add_student(self, student_data: Dict[str, Any]) -> int:
        """Add a new student to the database"""
        insert_query = """
        INSERT INTO students (full_name, student_id, course, email, phone, attendance_percent, grade)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        try:
            with self.get_db_cursor() as cursor:
                cursor.execute(insert_query, (
                    student_data['full_name'],
                    student_data['student_id'],
                    student_data['course'],
                    student_data['email'],
                    student_data['phone'],
                    student_data.get('attendance_percent', 0.0),
                    student_data.get('grade', 'N/A')
                ))
                logger.info(f"Added student: {student_data['full_name']}")
                return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            logger.error(f"Failed to add student - duplicate entry: {str(e)}")
            raise

    def update_student(self, student_id: str, update_data: Dict[str, Any]) -> bool:
        """Update student information"""
        update_query = """
        UPDATE students
        SET full_name = COALESCE(?, full_name),
            course = COALESCE(?, course),
            email = COALESCE(?, email),
            phone = COALESCE(?, phone),
            attendance_percent = COALESCE(?, attendance_percent),
            grade = COALESCE(?, grade)
        WHERE student_id = ?;
        """
        with self.get_db_cursor() as cursor:
            cursor.execute(update_query, (
                update_data.get('full_name'),
                update_data.get('course'),
                update_data.get('email'),
                update_data.get('phone'),
                update_data.get('attendance_percent'),
                update_data.get('grade'),
                student_id
            ))
            if cursor.rowcount > 0:
                logger.info(f"Updated student with ID: {student_id}")
                return True
            logger.warning(f"No student found with ID: {student_id}")
            return False

    def delete_student(self, student_id: str) -> bool:
        """Delete a student record"""
        delete_query = "DELETE FROM students WHERE student_id = ?;"
        with self.get_db_cursor() as cursor:
            cursor.execute(delete_query, (student_id,))
            if cursor.rowcount > 0:
                logger.info(f"Deleted student with ID: {student_id}")
                return True
            logger.warning(f"No student found with ID: {student_id}")
            return False

    def get_student(self, student_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single student by their student ID"""
        select_query = "SELECT * FROM students WHERE student_id = ?;"
        with self.get_db_cursor() as cursor:
            cursor.execute(select_query, (student_id,))
            result = cursor.fetchone()
            if result:
                return self._row_to_dict(cursor, result)
            return None

    def get_all_students(self) -> List[Dict[str, Any]]:
        """Fetch all students"""
        select_query = "SELECT * FROM students ORDER BY full_name;"
        with self.get_db_cursor() as cursor:
            cursor.execute(select_query)
            return [self._row_to_dict(cursor, row) for row in cursor.fetchall()]

    def search_students(self, search_term: str) -> List[Dict[str, Any]]:
        """Search students by name or email"""
        search_query = """
        SELECT * FROM students 
        WHERE full_name LIKE ? OR email LIKE ? OR course LIKE ?
        ORDER BY full_name;
        """
        search_term = f"%{search_term}%"
        with self.get_db_cursor() as cursor:
            cursor.execute(search_query, (search_term, search_term, search_term))
            return [self._row_to_dict(cursor, row) for row in cursor.fetchall()]

    def filter_by_course(self, course: str) -> List[Dict[str, Any]]:
        """Filter students by exact course name"""
        query = "SELECT * FROM students WHERE course = ? ORDER BY full_name;"
        with self.get_db_cursor() as cursor:
            cursor.execute(query, (course,))
            return [self._row_to_dict(cursor, row) for row in cursor.fetchall()]

    def filter_by_attendance(self, threshold: float) -> List[Dict[str, Any]]:
        """Filter students by attendance below threshold"""
        query = "SELECT * FROM students WHERE attendance_percent < ? ORDER BY attendance_percent;"
        with self.get_db_cursor() as cursor:
            cursor.execute(query, (threshold,))
            return [self._row_to_dict(cursor, row) for row in cursor.fetchall()]

    def filter_by_grade(self, grade: str) -> List[Dict[str, Any]]:
        """Filter students by exact grade"""
        query = "SELECT * FROM students WHERE grade = ? ORDER BY full_name;"
        with self.get_db_cursor() as cursor:
            cursor.execute(query, (grade.upper(),))
            return [self._row_to_dict(cursor, row) for row in cursor.fetchall()]

    def get_unique_courses(self) -> List[str]:
        """Get list of all unique courses"""
        query = "SELECT DISTINCT course FROM students ORDER BY course;"
        with self.get_db_cursor() as cursor:
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def _row_to_dict(cursor: sqlite3.Cursor, row: tuple) -> Dict[str, Any]:
        """Convert a database row to a dictionary"""
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))

# Example usage:
if __name__ == "__main__":
    # Initialize database manager
    db = DatabaseManager()
    
    # Example student data
    test_student = {
        "full_name": "John Doe",
        "student_id": "2024001",
        "course": "Computer Science",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "attendance_percent": 95.5,
        "grade": "A"
    }
    
    # Test database operations
    try:
        # Add student
        student_id = db.add_student(test_student)
        print(f"Added student with ID: {student_id}")
        
        # Get student
        student = db.get_student("2024001")
        print(f"Retrieved student: {student}")
        
        # Update student
        update_result = db.update_student("2024001", {"grade": "A+"})
        print(f"Update successful: {update_result}")
        
        # Get all students
        all_students = db.get_all_students()
        print(f"Total students: {len(all_students)}")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}") 