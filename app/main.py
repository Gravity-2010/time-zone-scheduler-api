from fastapi import FastAPI, HTTPException
from app.schemas import ScheduleInput, ScheduleOutput
from datetime import datetime, timedelta
import pytz
from app import models

app = FastAPI()

@app.get("/")
def home():
    return{"message": "Time-zone Aware Scheduler API"}

@app.post("/schedule", response_model=ScheduleOutput)
def create_schedule(schedule: ScheduleInput):
    # Validate timezone
    try:
        local_tz = pytz.timezone(schedule.timezone)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid timezone")
    
    # Parse and localize start time
    try:
        local_start = local_tz.localize(datetime.fromisoformat(schedule.start_time))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid start time format")
    
    utc_start = local_start.astimezone(pytz.utc)
    end_local = local_start + timedelta(minutes=schedule.duration_mins)

    data = {
        "title": schedule.title,
        "start_time_utc": utc_start.isoformat(),
        "start_time_local": local_start.isoformat(),
        "end_time_local": end_local.isoformat(),
        "timezone": schedule.timezone
    }

    models.schedules.append(data)
    return data

@app.get("/schedule", response_model=list[ScheduleOutput])
def get_schedule():
    return models.schedules