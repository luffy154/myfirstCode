from cron_lite import cron_task, start_all,stop_all
import time


@cron_task("* * * * * 0/2")
def event1():
    print("event1", time.strftime("%Y-%m_%d %H:%M:%S", time.localtime(time.time())))
    time.sleep(3)
    print("event1 done", time.strftime("%Y-%m_%d %H:%M:%S", time.localtime(time.time())))


@cron_task("* * * * * 0/15")
def event2():
    print("event2", time.strftime("%Y-%m_%d %H:%M:%S", time.localtime(time.time())))
    time.sleep(10)
    print("event2 done", time.strftime("%Y-%m_%d %H:%M:%S", time.localtime(time.time())))

# th = start_all(spawn=True)  # use bare `start_all()` to run forever as a service
# print("start")
# time.sleep(60)
# print("stop")
# stop_all(th)
# print("done")
start_all()

time.sleep(60)
