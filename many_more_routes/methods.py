from typing import List


def calc_departures(departureDays: str, leadTime: int) -> List[str]:
    ''' Calculates the required departure days to avoid confirming
    delivery days on weekends.

    departureDays: str - A sting of length 7 containing only 0 and 1.
    leadTime: int - The lead time as a integer
    
    >>> calc_departures('1111100', 2)
    ['1110000', '0001000', '0000100']
    
    >>> calc_departures('0111100', 3)
    ['0100000', '0010000', '0001000', '0000100']
    '''

    match departureDays:
        case list():
            departureDays = ''.join([str(n) for n in departureDays])
        case int():
            departureDays = ''.join([str(n) for n in str(departureDays)])
    
    departureDays = ''.join([str(n) for n in departureDays])
    leadTime = int(leadTime)

    departureArray = [
        ['0'] * 7,  # index 0, lead time bias of 0 days
        ['0'] * 7,  # index 1, lead time bias of 1 day
        ['0'] * 7,  # index 2, lead time bias of 2 days
        ['0'] * 7   # index 3, lead time bias of 0 days (overflow)
    ]

    departures = []

    for n in range(len(departureDays)):
        arrivalDay = (n + leadTime) % 7

        if departureDays[n] == '1':
            if arrivalDay <= 4 and (n + leadTime % 7) < 6:
                departureArray[3][n] = '1'
            
            elif arrivalDay <= 4:
                departureArray[0][n] = '1'

            elif arrivalDay == 5:
                departureArray[2][n] = '1'

            elif arrivalDay == 6:
                departureArray[1][n] = '1'

    for n, departureList in enumerate(departureArray):
        if '1' in departureList:
            departures.append(''.join(departureList))

    return sorted(departures, reverse=True)


def recalculate_lead_time(departureDays: str, leadTime: int) -> int:
    '''
    Takes the departure days and lead time, selects the first
    departure days and caluclates the arrival day, if on a weekday
    leadTime is returned, if on a Sunday, leadTime + 1, if on a
    Saturday leadTime + 2. ValueError if no departure days.
    >>> recalculate_lead_time('0100000', 3)
    3
    >>> recalculate_lead_time('0010000', 3)
    5
    >>> recalculate_lead_time('0001000', 3)
    4
    >>> recalculate_lead_time('0000100', 3)
    3
    '''
    departureDays = ''.join([str(n) for n in departureDays])
    leadTime = int(leadTime)

    arrivalDay = (departureDays.index('1') + leadTime) % 7

    if arrivalDay <= 4:
        return leadTime

    elif arrivalDay == 5:
        return leadTime + 2

    elif arrivalDay == 6:
        return leadTime + 1

    else:
        raise RuntimeError('Unable to recalculate lead time')


def calc_route_departure(departureDays: str, leadTime: int) -> int:
    '''
    Takes the departure days and lead time, selects the first
    departure days and caluclates the arrival day, if on a weekday
    leadTime is returned, if on a Sunday, leadTime + 1, if on a
    Saturday leadTime + 2.
    
    >>> calc_route_departure('0100000', 3)
    1
    >>> calc_route_departure('0010000', 3)
    2
    >>> calc_route_departure('0001000', 3)
    3
    >>> calc_route_departure('0000100', 3)
    4
    '''

    departureDay = departureDays.index('1')
    arrivalDay = (departureDays.index('1') + leadTime) % 7

    if arrivalDay <= 4 and (departureDay + leadTime % 7) < 6:
        return 1
    
    elif arrivalDay <= 4:
        return 4

    elif arrivalDay == 5:
        return 2

    elif arrivalDay == 6:
        return 3

    else:
        raise RuntimeError('Unable to calculate route departure')


if __name__ == '__main__':
    import doctest
    doctest.testmod()