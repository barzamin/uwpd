from .extract import eventlog, clery

# stuff = eventlog.extract('eventlog-2021-9-29.pdf')
# stuff.to_csv('eventlog-2021-9-29.csv')

stuff = clery.extract('clery-2021-9-29.pdf')
stuff.to_csv('clery-2021-9-29.csv')