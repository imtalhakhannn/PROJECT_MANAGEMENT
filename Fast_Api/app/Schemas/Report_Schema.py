# Importing BaseModel from Pydantic for data validation and parsing
from pydantic import BaseModel

# Importing date class to handle dates
from datetime import datetime
# Schema for creating a report
class ReportCreate(BaseModel):
    content: str               
    timestamp: datetime    
    user_id: int              
    task_id: int             

# Schema for returning a report 
class ReportOut(BaseModel):
    id: int                   
    content: str              
    timestamp:datetime    
    user_id: int             
    task_id: int               

    # Enables ORM mode to support SQLAlchemy models directly
    class Config:
        orm_mode = True
