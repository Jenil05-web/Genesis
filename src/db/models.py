from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel , Field , JSON , Column

class Incident(SQLModel , table = True):
    id : Optional[int] = Field(default= None, primary_key=True)
    thread_id:str
    situation :str
    image_path : Optional[str] = None

    alert_info: dict = Field(default={}, sa_column=Column(JSON))
    image_findings: dict = Field(default={}, sa_column=Column(JSON))
    response_plan: dict = Field(default={}, sa_column=Column(JSON))
    quality_result: dict = Field(default={}, sa_column=Column(JSON))
    execution_result: dict = Field(default={}, sa_column=Column(JSON))

    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    approved: Optional[bool] = None
    retry_count: int = 0

    created_at: datetime = Field(default_factory=datetime.now)

    


    