from datetime import datetime, timedelta


def date_handler(date_string, date_format='%Y-%m-%d'):
    """
    Takes a date string or phrase and returns the valid date in
    the specified format.
    :date_string: A phrase like "3_days_ago", "yesterday" or "today"
                     or a date string such as "2021-01-01".
    :date_format: The returned formatting of the date.
    """
    try:
        if date_string == 'today':
            return datetime.now().strftime(date_format)
        if date_string == 'yesterday':
            return (datetime.now() - timedelta(days=1)).strftime(date_format)
        if '_days_ago' in date_string:
            return phrase_to_date(phrase=date_string, date_format=date_format)
        return date_string
    except ValueError as err:
        raise ValueError('StartDate requires a valid input '
                         'such as "today", "yesterday" or "<int>_days_ago".') from err


def phrase_to_date(phrase, date_format='%Y-%m-%d'):
    """
    Takes a typical phrase such as "3_days_ago" and returns a
    date based on that phrase.
    :phrase: str. Something like 3_days_ago or 25_days_ago etc.
    :return: '%Y-%m-%d'
    """
    try:
        date_delta = int(phrase.split('_')[0])
        return (datetime.now() - timedelta(days=date_delta)).strftime(date_format)
    except ValueError as err:
        raise ValueError(f'Phrasing for date: {phrase} is not valid, '
                         f'try something like: 3_days_ago') from err
