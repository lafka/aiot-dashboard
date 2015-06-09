import calendar

def to_epoch_mili(dt):
    """Converts Python `datetime` object to an UTC epoch in miliseconds (to be
    used with `flot`)
    """
    return calendar.timegm(dt.timetuple()) * 1000
