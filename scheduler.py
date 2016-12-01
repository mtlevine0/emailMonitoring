import properties
from apscheduler.schedulers.background import BackgroundScheduler
from lib import mailGun
import database as db
import logging
import uuid

sched = BackgroundScheduler()

print("Scheduler Running..." + str(sched))

@sched.scheduled_job('interval', seconds=int(properties.d['sendDelay']))
def timed_job():
    uuidMessage = uuid.uuid4()
    mailGun.sendMessage(uuidMessage)
    print('Sending Mail!')

@sched.scheduled_job('interval', seconds=int(properties.d["SLAInterval"]))
def timeoutDetection():
    print("SLA Check!")
    try:
        rq = db.pw.RawQuery( db.outgoingMessage,'select outgoingmessage.messageKey, TIMESTAMPDIFF(SECOND, outgoingmessage.outgoingTime, NOW()) as diff from outgoingmessage left join incomingmessage on outgoingmessage.messageKey=incomingmessage.messageKey where incomingmessage.messageKey is null and outgoingmessage.SLABreached is false;')
        for row in rq.execute():
            print(row.diff, row.messageKey, row.SLABreached)
            if row.diff > int(properties.d["emailTimeout"]) and row.SLABreached == False:
                print("Email Slowdown Detected!")
                for stat in db.outgoingMessage.select().where(db.outgoingMessage.messageKey == row.messageKey):
                    stat.SLABreached = True
                    stat.save()
                    
            print("\n")
    except:
        print("SLA Check Failed!")

try:
    sched.start()
except:
    print("Failed to Start Scheduler!")
