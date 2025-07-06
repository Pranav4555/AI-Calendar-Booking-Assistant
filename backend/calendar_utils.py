from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
from backend.config import GOOGLE_CALENDAR_ID, GOOGLE_CREDENTIALS_PATH

def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH,
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    return build("calendar", "v3", credentials=credentials)

def check_availability(start_time: str, end_time: str) -> bool:
    service = get_calendar_service()
    events = service.events().list(
        calendarId=GOOGLE_CALENDAR_ID,
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy='startTime'
    ).execute().get('items', [])
    return len(events) == 0

def find_next_available_slots(duration_minutes=30, hours_ahead=3):
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    slots = []
    service = get_calendar_service()

    for i in range(hours_ahead * 2):  # 30-min intervals
        start = now + timedelta(minutes=i * 30)
        end = start + timedelta(minutes=duration_minutes)

        if check_availability(start.isoformat(), end.isoformat()):
            slots.append(start)
        if len(slots) >= 3:
            break
    return slots

def create_event(summary: str, start_time: str, end_time: str, return_event_id=False):
    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }
    created_event = service.events().insert(calendarId=GOOGLE_CALENDAR_ID, body=event).execute()
    if return_event_id:
        return created_event.get('id'), created_event.get('htmlLink')
    return created_event.get('htmlLink')

def delete_event(event_id: str):
    service = get_calendar_service()
    service.events().delete(calendarId=GOOGLE_CALENDAR_ID, eventId=event_id).execute()
