import datetime
import time
from re import match

def wait(dtarget, ttarget):
    date_pattern = r"(0[1-9]|[12][0-9]|3[01]).([1-9]|1[0-2]).(19|[2-4][0-9]|50)"
    time_pattern = r"(0[0-9]|1[0-9]|2[0-4]):(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])"
    try:
        if match(date_pattern, str(dtarget)):
            if isinstance(dtarget, str):
                day = int(dtarget.split(".")[0])
                month = int(dtarget.split(".")[1])
                year = int("20{}".format(dtarget.split(".")[2]))
                
                xday = datetime.date(year, month, day)
            elif isinstance(dtarget, datetime.date):
                xday = dtarget
            else:
                raise ValueError(
                    "Type Error: Invalid type for the "
                     + str(dtarget) + " date")

            today = datetime.date.today()
        else:
            raise ValueError(
                "Format Error: Invalid format for the "
                 + str(dtarget) + " date")

        if match(time_pattern, str(ttarget)):
            if isinstance(ttarget, datetime.time):
                xtime = ttarget
            elif isinstance(ttarget, str):
                hour = int(ttarget.split(":")[0])
                minute = int(ttarget.split(":")[1])

                xtime = datetime.time(hour, minute, second=0, microsecond=0)
            else:
                raise ValueError(
                    "Type Error: Invalid type for the "
                    + str(ttarget) + " time")
            
            now = datetime.datetime.now().time().replace(second=0, microsecond=0)
        else:
            raise ValueError(
                "Format Error: Invalid format for the "
                 + str(ttarget) + " time")
        
        ttw = datetime.datetime.combine(xday, xtime) - datetime.datetime.combine(today, now)
        #print(datetime.datetime.combine(xday, xtime))
        #print(datetime.datetime.combine(today, now))
        #print(ttw)
        return ttw
    except ValueError as err:
        print(err)
        return None
    except Exception as exc:
        print(exc)
        return None

if __name__ == "__main__":
    print("This module cannot be run directly")