from datetime import timedelta, datetime
from threading import Timer

run_at = datetime(2017, 7, 2, 3, 25)

#now + timedelta(hours=3)
delay = (run_at - datetime.now()).total_seconds()


def hello():
    print "hello, world"
    t = Timer(5, hello)
    t.start()

t = Timer(5, hello)
t.start()  # after 30 seconds, "hello, world" will be printed

