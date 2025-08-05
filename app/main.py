from fastapi import FastAPI, HTTPException
from app.schemas import ScheduleInput, ScheduleOutput, TimeConvertInput, TimeConvertOutput
from datetime import datetime, timedelta
import pytz
from app import models
from app.models import generate_id

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
        "id": generate_id(),
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

@app.put("/schedule/{schedule_id}", response_model=ScheduleOutput)
def update_schedule(schedule_id: str, schedule: ScheduleInput):
    for index, s in enumerate(models.schedules):
        if s["id"] == schedule_id:
            try:
                local_tz = pytz.timezone(schedule.timezone)
                local_start = local_tz.localize(datetime.fromisoformat(schedule.start_time))
                utc_start = local_start.astimezone(pytz.utc)
                end_local = local_start + timedelta(minutes=schedule.duration_mins)
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
            
            updated = {
                "id": s["id"],
                "title": schedule.title,
                "start_time_utc": utc_start.isoformat(),
                "start_time_local": local_start.isoformat(),
                "end_time_local": end_local.isoformat(),
                "timezone": schedule.timezone
            }

            models.schedules[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Schedule not found")

@app.delete("/schedule/{schedule_id}")
def delete_schedule(schedule_id: str):
    for index, s in enumerate(models.schedules):
        if s["id"] == schedule_id:
            del models.schedules[index]
            return{"message": "Schedule deleted"}
        
    raise HTTPException(status_code=404, detail="Schedule not found")

@app.get("/convert", response_model=TimeConvertOutput)
def convert_time(time: str, from_tz: str, to_tz: str):
    try:
        from_zone = pytz.timezone(from_tz)
        to_zone = pytz.timezone(to_tz)
        original = from_zone.localize(datetime.fromisoformat(time))
        converted = original.astimezone(to_zone)

        return {
            "original_time": original.isoformat(),
            "converted_time": converted.isoformat(),
            "from_tz": from_tz,
            "to_tz": to_tz
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))