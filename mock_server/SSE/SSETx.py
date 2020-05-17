import schedule

class SendEvent():

    def __init__(self):
        self.interval = 5 # seconds
        self.stopSend = False

    def start(self):
        schedule.every(self.interval).seconds.do(self.send)
        while not self.stopSend:
            schedule.run_pending()

    def stopSending(self):
        self.stopSend = True
        schedule.cancel_job()

    def send(self):
        print('Hello')