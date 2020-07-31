from __future__ import print_function
import datetime
import pickle
import os.path
import datefinder
import pprint as pp
import rfc3339
import tzlocal
import re

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def add_class_to_calendar(service, start_time_str, meeting_days, end_date, summary, duration=1,attendees=None, description=None, location=None):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + datetime.timedelta(hours=duration)
    else:
        return False

    local_timezone = tzlocal.get_localzone().zone

    start_time = rfc3339.rfc3339(start_time, utc=False, use_system_timezone=True)
    end_time = rfc3339.rfc3339(end_time, utc=False, use_system_timezone=True)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': local_timezone,
        },
        'end': {
            'dateTime': end_time,
            'timeZone': local_timezone,
        },
        'recurrence': [
            'RRULE:FREQ=WEEKLY;BYDAY=' + meeting_days + ';UNTIL='+end_date
        ],
        'attendees': [
            {'email': 'mboisver@ucsc.edu'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },

    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print("Event created: " + event.get('htmlLink'))
    return True

def get_meeting_days(ucsc_day_string):
    res_list = []
    res_list = re.findall('[A-Z][^A-Z]*', ucsc_day_string)
    meeting_days = ""
    for day in res_list:
        if(day == "M"):
            meeting_days += "MO,"
        elif(day == "T" or day == "Tu"):
            meeting_days += "TU,"
        elif(day == "W"):
            meeting_days += "WE,"
        elif(day == "Th"):
            meeting_days += "TH,"
        elif(day == "F"):
            meeting_days += "FR,"

    return meeting_days[:-1]




def main():
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #create_event(service, "30 Jul 12.00pm", "Test meeting", 0.5, "mboisver@ucsc.edu", "description here", "Santa Cruz, California");

    print(get_meeting_days("MWF"))

if __name__ == '__main__':
    main()

