from .extract import eventlog

stuff = eventlog.extract('eventlog-2021-9-29.pdf')
stuff.to_csv('eventlog-2021-9-29.csv')