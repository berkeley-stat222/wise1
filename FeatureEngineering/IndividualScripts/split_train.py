def split_train_test(date):
    if isinstance(date, float):
        return 'NaN'
    try:
        date = parse(date)
        day = date.day
        month = date.month
        year = date.year
    except Exception, e:
        print date, type(date)
        raise e
    if year >= 2012:
        return 'Train1'
    if year >= 2008:
        return 'Train2'
    if year >= 2006:
        return 'Train3'