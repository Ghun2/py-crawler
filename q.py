import datetime
import os
import thatactor_f as th

def check_time():
    utcnow = datetime.datetime.utcnow()
    time_gap = datetime.timedelta(hours=9)
    now = utcnow + time_gap
    nowday = now.strftime('%Y-%m-%d')
    nowtime = now.strftime('%H:%M:%S')
    return [str(nowday),str(nowtime)]


def logging(txt):
    f = open("qlog.txt",'a')   #로그 file open
    curr_time = check_time()
    f.write(curr_time[0] + ' ' + curr_time[1] + ' ' + txt + '\n')
    f.close()

logging(os.getcwd())
