from pydantic import BaseModel

class ScheduleInput(BaseModel):
    title: str
    start_time: str #ISO string
    duration_mins: int
    timezone: str

class ScheduleOutput(BaseModel):
    id: str
    title: str
    start_time_utc: str
    start_time_local: str
    end_time_local: str
    timezone: str

class TimeConvertInput(BaseModel):
    time_str: str
    from_tz: str
    to_tz: str

class TimeConvertOutput(BaseModel):
    original_time: str
    converted_time: str
    from_tz: str
    to_tz: str