from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

class Student(BaseModel):
    id: Optional[int] = None
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    date_of_birth: date
    email: str = Field(..., max_length=100)
    phone: str = Field(..., max_length=15)
    address: str = Field(..., max_length=200)
    grade: float = Field(..., ge=0.0, le=100.0)
    
    class Config:
        from_attributes = True

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self) -> str:
        return (f"Student(id={self.id}, name='{self.full_name()}', "
                f"grade={self.grade}, email='{self.email}')") 