import datetime

import peewee as pw
from playhouse.pool import PooledMySQLDatabase

import properties

myDB = PooledMySQLDatabase(properties.d["database"], max_connections=32, stale_timeout=300, user=properties.d["dbUser"], password=properties.d["dbPass"])

class incomingMessage(pw.Model):
    messageKey = pw.CharField(max_length=512)
    incomingTime = pw.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = myDB
        
class outgoingMessage(pw.Model):
    messageKey = pw.CharField(max_length=512)
    outgoingTime = pw.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = myDB

# when you're ready to start querying, remember to connect
myDB.connect()
myDB.create_tables([incomingMessage, outgoingMessage], safe=True)