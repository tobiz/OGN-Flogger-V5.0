import datetime 


def inc_flt_cnt(settings, flt_time):
    #
    # Find number of flights with duration greater than 5 mins
    #
    if flt_time >= settings.FLOGGER_MIN_FLIGHT_TIME:
        flight_count = flight_count + 1
        self.set_flight_count.emit(str(flight_count))
    
    
    cursor.execute('''SELECT max(id) FROM flight_log_final WHERE duration<=?''', \
        (datetime.datetime.strptime("0:5:0", "%H:%M:%S"))) 
    row = cursor.fetchone()
    print("Number of flights in flight_log_final is: ", row[0])
    return row[0]
    #flight_count = row[0]
    #self.set_flight_count.emit(str(flight_count))  