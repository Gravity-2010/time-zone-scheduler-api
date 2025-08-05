from pydantic import BaseModel

class ScheduleInput(BaseModel):
    title: str
    start_time: str #ISO string
    duration_mins: int
    timezone: str

class ScheduleOutput(BaseModel):
    title: str
    start_time_utc: str
    start_time_local: str
    end_time_local: str
    timezone: str