
__all__ = [ 'Date', 'Time', 'Timestamp', 'DateFromTicks', 'TimeFromTicks',
			'TimestampFromTicks', 'Binary', 'STRING', 'BINARY', 'NUMBER',
			'DATETIME', 'ROWID', 'TypeObjectFromNuodb' ]

from exception import *
import datetime, decimal, time
<<<<<<< Updated upstream
=======
from exception import DataError

>>>>>>> Stashed changes

class Date(object):
	
	def __init__(self, year, month, day):
		self.year 	= year
		self.month 	= month
		self.day 	= day
		
	def __str__(self):
		return "%s" % datetime.date(self.year, self.month, self.day).isoformat()

class Time(object):
	
	def __init__(self, hour, minute, second):
		self.hour 	= hour
		self.minute = minute
		self.second = second

	def __str__(self):
		return "%s" % datetime.time(self.hour, self.minute, self.second).isoformat()

class Timestamp(object):
	
	def __init__(self, year, month, day, hour, minute, second):
		self.year 	= year
		self.month 	= month
		self.day 	= day
		self.hour 	= hour
		self.minute = minute
		self.second = second
		
	def __str__(self):
		return "%s" % datetime.datetime(self.year, self.month, self.day, self.hour, self.minute, self.second).isoformat()
		
class Binary(object):
	
	def __init__(self, string):
		self.string = string
		
	def __str__(self):
		return "%s" % [ bin(ord(ch))[2:].zfill(8) for ch in self.string ]
		
def DateFromTicks(ticks):
	return Date(*time.localtime(ticks)[:3])

def TimeFromTicks(ticks):
	return Time(*time.localtime(ticks)[3:6])

def TimestampFromTicks(ticks):
	return Timestamp(*time.localtime(ticks)[:6])

class TypeObject(object):
	def __init__(self, *values):
		self.values = values
	def __cmp__(self, other):
		if other in self.values:
			return 0
		if other < self.values:
			return 1
		return -1

STRING 		= TypeObject(str)
BINARY 		= TypeObject(str)
NUMBER 		= TypeObject(int, decimal.Decimal)
DATETIME 	= TypeObject(datetime.datetime, datetime.date, datetime.time)
ROWID 		= TypeObject()

def TypeObjectFromNuodb(nuodb_type_name):
    ''' returns one of STRING, BINARY, NUMBER, DATETIME, ROWID based on the 
    supplied NuoDB column type name
    '''
    
    if nuodb_type_name == "<null>":
        return None
        
    elif nuodb_type_name == "string":
        return STRING
        
    elif nuodb_type_name == "char":
        return STRING
        
    elif nuodb_type_name == "varchar":
        return STRING
        
    elif nuodb_type_name == "smallint":
        return NUMBER
        
    elif nuodb_type_name == "integer":
        return NUMBER
        
    elif nuodb_type_name == "bigint":
        return NUMBER
        
    elif nuodb_type_name == "float":
        return NUMBER
        
    elif nuodb_type_name == "double":
        return NUMBER
        
    elif nuodb_type_name == "date":
        return DATETIME
        
    elif nuodb_type_name == "timestamp":
        return DATETIME
        
    elif nuodb_type_name == "time":
        return DATETIME
        
    elif nuodb_type_name == "clob":
        return BINARY
        
    elif nuodb_type_name == "blob":
        return BINARY
        
    elif nuodb_type_name == "numeric":
        return NUMBER
        
    elif nuodb_type_name == "number":
        return NUMBER
        
    elif nuodb_type_name == "bytes":
        return BINARY
        
    elif nuodb_type_name == "binarystring":
        return BINARY
        
    elif nuodb_type_name == "binaryvaryingstring":
        return BINARY
        
    elif nuodb_type_name == "boolean":
        #TODO: Not sure about this?
        return NUMBER

    else:
        raise DataError('received unknown column type from the database')

