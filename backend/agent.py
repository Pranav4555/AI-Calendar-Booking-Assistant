from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from backend.config import GROQ_API_KEY
from backend.calendar_utils import check_availability, create_event, find_next_available_slots, delete_event
from datetime import datetime, timedelta, timezone
import re

llm = ChatGroq(
    temperature=0,
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192"
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

TEMP_BOOKING_SLOT = {}
LAST_BOOKED_EVENT_ID = {"id": None}

def suggest_time_slots(_: str) -> str:
    try:
        slots = find_next_available_slots()
        now = datetime.now(timezone.utc)
        future_slots = [slot for slot in slots if slot > now]

        if not future_slots:
            return "No available future slots found today."

        TEMP_BOOKING_SLOT.clear()  # Clear previous context

        slot_strings = [slot.astimezone().strftime("%I:%M %p") for slot in future_slots[:3]]
        return (
            "You're free at: "
            + ", ".join(slot_strings)
            + " today. Which time would you like to book?"
        )
    except Exception as e:
        print(f"[SuggestSlots Error] {e}")
        return "Couldn't retrieve slots. Please try again later."

def confirm_booking(query: str) -> str:
    try:
        match = re.search(r'\b(\d{1,2})(?::(\d{2}))?\s?(AM|PM)\b', query, re.IGNORECASE)
        if not match:
            return "Please specify a time like '6 PM' or '4:30 PM' to book."

        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        am_pm = match.group(3).upper()

        if am_pm == "PM" and hour != 12:
            hour += 12
        if am_pm == "AM" and hour == 12:
            hour = 0

        now = datetime.now().astimezone()
        start = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if start < now:
            return "That time has already passed today. Please pick a future slot."

        end = start + timedelta(minutes=30)
        TEMP_BOOKING_SLOT['start'] = start
        TEMP_BOOKING_SLOT['end'] = end

        return f"You want to book {start.strftime('%I:%M %p')} today for 30 minutes, correct? Reply 'Yes' to confirm."
    except Exception as e:
        print(f"[ConfirmBooking Error] {e}")
        return "Couldn't process the booking time."

def final_book_slot(_: str) -> str:
    try:
        start = TEMP_BOOKING_SLOT.get('start')
        end = TEMP_BOOKING_SLOT.get('end')
        if not start or not end:
            return "No time confirmed. Please specify a time first."

        event_id, link = create_event("Appointment", start.isoformat(), end.isoformat(), return_event_id=True)
        LAST_BOOKED_EVENT_ID['id'] = event_id
        TEMP_BOOKING_SLOT.clear()
        return f" Event booked successfully: {link}"
    except Exception as e:
        print(f"[FinalBook Error] {e}")
        return "Couldn't book the event. Please try again."

def delete_last_event(_: str) -> str:
    try:
        event_id = LAST_BOOKED_EVENT_ID.get('id')
        if not event_id:
            return "No event to delete. You haven't booked anything yet."

        delete_event(event_id)
        LAST_BOOKED_EVENT_ID['id'] = None
        return " Last booked event has been deleted successfully."
    except Exception as e:
        print(f"[DeleteEvent Error] {e}")
        return "Couldn't delete the event. Maybe it was already removed?"

# Tools for agent
tools = [
    Tool(name="SuggestTimeSlots", func=suggest_time_slots, description="Suggests available free slots."),
    Tool(name="ConfirmBookingSlot", func=confirm_booking, description="Confirms a specific time like '6 PM'."),
    Tool(name="BookFinalSlot", func=final_book_slot, description="Books a confirmed time slot."),
    Tool(name="DeleteLastEvent", func=delete_last_event, description="Deletes the last booked calendar event.")
]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

def run_agent(user_input: str):
    try:
        print(f"Query received: {user_input}")
        cleaned_input = user_input.strip().lower()

        if cleaned_input in ["yes", "yes please", "confirm", "book it"]:
            return final_book_slot("")

        if re.search(r'\b(\d{1,2})(?::(\d{2}))?\s?(AM|PM)\b', user_input, re.IGNORECASE):
            return confirm_booking(user_input)

        if cleaned_input in ["delete", "cancel", "remove", "cancel last", "delete event"]:
            return delete_last_event("")

        return agent_executor.invoke({"input": user_input})["output"]
    except Exception as e:
        print(f"[Agent Error] {e}")
        return "Sorry, something went wrong. Please try again later."
