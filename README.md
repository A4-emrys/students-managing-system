# Student Management System

A comprehensive system for managing student records with both CLI and GUI interfaces. The system allows for easy tracking of student information, attendance, and grades.

## Features

### Core Functionality
- Add, view, update, and delete student records
- Track student attendance and grades
- Search and filter capabilities
- Data validation for all inputs
- Automatic student ID generation

### Search and Filter Options
- Search by name, email, or course
- Filter students by course
- Filter by attendance (below 75%)
- Filter by grade (A/B/C/D/F)

### Dual Interface
- Command Line Interface (CLI) for quick operations
- Graphical User Interface (GUI) for user-friendly interaction
- Seamless switching between CLI and GUI

## Screenshots

[Coming soon]

<!-- Add your screenshots here using the following format:
![Description](path/to/screenshot.png)
-->

## Tech Stack

- **Python 3.x** - Core programming language
- **SQLite** - Database management
- **Tkinter** - GUI framework
- Additional Libraries:
  - `sqlite3` - Database operations
  - `logging` - Error and info logging
  - `re` - Input validation
  - `typing` - Type hints

## Installation

1. Clone the repository:
```bash
git clone https://github.com/A4-emrys/students-managing-system.git
cd Student-system
```

2. Make sure you have Python 3.x installed:
```bash
python --version
```

3. The system uses built-in Python libraries, so no additional installation is required.

## How to Run

### CLI Version
```bash
python main.py
```

### GUI Version
```bash
python gui.py
```

You can also launch the GUI from the CLI by selecting option 7 in the main menu.

## Features in Detail

### Student Information
- First Name and Last Name
- Course
- Email (with validation)
- Phone Number (with international format support)
- Attendance Percentage
- Grade (A/B/C/D/F)

### Data Validation
- Email format validation
- Phone number format validation
- Attendance range check (0-100%)
- Grade validation
- Input sanitization

### Database Features
- Automatic ID generation
- Unique email constraints
- Data persistence
- Error handling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

[Add your license here]

## Contact

[Add your contact information here] 