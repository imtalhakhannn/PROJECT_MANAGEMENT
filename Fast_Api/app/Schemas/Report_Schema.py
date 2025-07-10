# Importing BaseModel from Pydantic for data validation and parsing
from pydantic import BaseModel

# Importing date class to handle dates
from datetime import datetime
# Schema for creating a report
class ReportCreate(BaseModel):
    Report_id: int
    Task_id:int
    User_id:int
    Task_name:str
    Timestamp: datetime   
    Project_name:str
    Reported_by_name:str
    Overall_Quantity:int
    Reported_Quantity:int
    Rate:str
    Amount:float
    Status:str
    Pending_quantity:str 
    user_id: int              
    task_id: int             

# Schema for returning a report 
class ReportOut(BaseModel):
    Report_id: int
    Task_id:int
    User_id:int
    Task_name:str
    Timestamp: datetime   
    Project_name:str
    Reported_by_name:str
    Overall_Quantity:int
    Reported_Quantity:int
    Rate:str
    Amount:float
    Status:str
    Pending_quantity:str 
    user_id: int              
    task_id: int               

# Enables ORM mode to support SQLAlchemy models directly
    class Config:
        orm_mode = True
