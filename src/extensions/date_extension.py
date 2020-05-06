import datetime

class date_extension(object):
    
    @staticmethod
    def diff_dates_seconds(date1, date2):
        print(date2)
        print(date1)
        return abs(date2-date1).seconds
