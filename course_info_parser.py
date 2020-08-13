import re
import json
import datetime
import datefinder
from pydal import DAL, Field
import course_finder
from textwrap import wrap

def main():
    controller = course_finder.DatabaseController()
    parser = CourseInfoParser()
    print(parser.get_meeting_days(controller.find_course(class_id=21915)))


class CourseInfoParser:
    def get_meeting_days(self, db_row):
        ucsc_day_string = db_row.date_time.split()[0]
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

    def get_quarter(self):
        with open("relevant_term.json") as term_file:
            data = json.load(term_file)
            term = data["relevant_term"]
            quarter = term.split()[1]
            return quarter

    def get_quarter_start(self):
        with open("relevant_term.json") as term_file:
            data = json.load(term_file)
            start = data["start"]
            start_date = list(datefinder.find_dates(start))[0]
            return start_date

    def get_quarter_end(self, class_start):
        quarter = self.get_quarter()
        if(quarter == "Fall"):
            # Accounting for the quarter starting on a Thursday (week before classes)
            end_date = class_start + datetime.timedelta(days=1, weeks=10)
        elif(quarter == "Winter"):
            # Accounting for the quarter starting on a Monday
            end_date = class_start + datetime.timedelta(days=4, weeks=9)
        elif(quarter == "Spring"):
            # Accounting for the quarter starting on a Monday
            end_date = class_start + datetime.timedelta(days=4, weeks=9)
        return end_date

    def get_first_day_info(self, db_row):
        quarter_start = self.get_quarter_start()
        date_time = db_row.date_time
        start_time = get_time(date_time.split()[1].split("-")[0])
        end_time = get_time(date_time.split()[1].split("-")[1])
        first_day_times = {}
        class_weekdays = date_time.split()[0]
        weekday_info = []
        day_offset = 100
        for weekday in re.findall('[A-Z][^A-Z]*', class_weekdays):
            dist = (parse_weekday(weekday)-quarter_start.weekday() + 7) % 7
            if(dist < day_offset):
                day_offset = dist
        num_days_to_shift = 0
        
        first_day_times["start"] = quarter_start + datetime.timedelta(days = day_offset, hours = int(start_time["hours"]), minutes=int(start_time["minutes"]))
        first_day_times["end"] = quarter_start + datetime.timedelta(days = day_offset, hours = int(end_time["hours"]), minutes=int(end_time["minutes"]))
        return first_day_times


def get_time(time_string):
    data = time_string.split(":")
    hours = int(data[0])
    minutes = wrap(data[1], 2)[0]
    period = wrap(data[1], 2)[1]
    if(period == "PM" and hours != 12):
        hours += 12
    time = {}
    time["hours"] = hours
    time["minutes"] = minutes
    return time

def parse_weekday(weekday_char):
    if (weekday_char == "M"):
        return 0
    elif (weekday_char == "T" or weekday_char == "Tu"):
        return 1
    elif (weekday_char == "W"):
        return 2
    elif (weekday_char == "Th"):
        return 3
    elif (weekday_char == "F"):
        return 4
    else:
        return None

if __name__ == '__main__':
    main()




