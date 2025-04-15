import re
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def validate_email(email: str) -> bool:
    """
    Validate email format.
    Rules:
    - Must contain exactly one @
    - Local part must be 1-64 characters
    - Domain part must be 1-255 characters
    - Only allowed characters: letters, numbers, and .!#$%&'*+/=?^_`{|}~-
    - Periods must not be first, last, or consecutive
    """
    if not email or len(email) > 320:  # 64 + @ + 255
        return False
    
    try:
        local, domain = email.split('@')
    except ValueError:
        return False
    
    if not local or not domain:
        return False
    
    if len(local) > 64 or len(domain) > 255:
        return False
    
    local_pattern = r'^[a-zA-Z0-9!#$%&\'*+\-/=?^_`{|}~]+([\.]?[a-zA-Z0-9!#$%&\'*+\-/=?^_`{|}~]+)*$'
    domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$'
    
    return bool(re.match(local_pattern, local) and re.match(domain_pattern, domain))

def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.
    Rules:
    - Must contain only digits after removing any formatting
    - Must be between 10 and 15 digits
    - Can start with + followed by country code (e.g., +233 for Ghana)
    
    Examples:
    - +233545678910 (Ghana)
    - +233-54-567-8910
    - 0545678910 (Local Ghana format)
    """
    # Remove all non-digit characters except leading +
    digits = re.sub(r'[^\d+]', '', phone)
    
    # Handle Ghanaian local format (convert 0... to +233...)
    if digits.startswith('0') and len(digits) == 10:
        digits = '+233' + digits[1:]
    
    if digits.startswith('+'):
        digits = digits[1:]  # Remove + for length check
    
    # Check if remaining string contains only digits and has correct length
    return bool(digits.isdigit() and 10 <= len(digits) <= 15)

def validate_student_id(student_id: str) -> bool:
    """Validate student ID format (e.g., 2024001)"""
    pattern = r'^\d{7}$'
    return bool(re.match(pattern, student_id))

def format_phone_number(phone: str) -> str:
    """
    Format phone number to consistent international format.
    
    Examples:
    - +233545678910 -> +233-54-567-8910
    - 0545678910 -> +233-54-567-8910
    """
    # Remove all non-digit characters except leading +
    digits = re.sub(r'[^\d+]', '', phone)
    
    # Convert local Ghana format to international
    if digits.startswith('0') and len(digits) == 10:
        digits = '+233' + digits[1:]
    elif not digits.startswith('+') and len(digits) == 9:
        digits = '+233' + digits
    
    # If it's a Ghana number (+233 format)
    if digits.startswith('+233') and len(digits) == 13:
        return f"{digits[:4]}-{digits[4:6]}-{digits[6:9]}-{digits[9:]}"
    
    # For other formats, keep as is with just the + if present
    return digits

def calculate_grade(score: float) -> str:
    """Convert numerical score to letter grade"""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def sanitize_input(text: str) -> str:
    """
    Clean and sanitize user input.
    Rules:
    - Convert to string if not already
    - Strip whitespace
    - Remove potentially harmful characters
    - Normalize whitespace
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Strip whitespace and normalize spaces
    text = ' '.join(text.split())
    
    # Remove potentially harmful characters
    text = re.sub(r'[<>&;\'"]', '', text)
    
    return text.strip()

def generate_student_id(year: Optional[int] = None) -> str:
    """Generate a unique student ID based on year and sequence"""
    from datetime import datetime
    import random
    
    if year is None:
        year = datetime.now().year
    
    # Generate a random 3-digit sequence number
    sequence = random.randint(1, 999)
    return f"{str(year)}{sequence:03d}"

def format_name(first_name: str, last_name: str) -> str:
    """Format full name consistently"""
    return f"{first_name.strip().title()} {last_name.strip().title()}"

def validate_attendance(attendance: float) -> bool:
    """
    Validate attendance percentage.
    Rules:
    - Must be a number between 0 and 100 (inclusive)
    - Can be a float or integer
    """
    try:
        attendance_float = float(attendance)
        return 0 <= attendance_float <= 100
    except (ValueError, TypeError):
        return False

def log_error(error_msg: str) -> None:
    """Log error messages"""
    logger.error(error_msg)

def log_info(info_msg: str) -> None:
    """Log information messages"""
    logger.info(info_msg) 