from typing import List
from typing import Union
from typing import Optional

def calc_departures(departureDays: str, leadTime: int) -> List[str]:
    ''' Calculates the required departure days to avoid confirming
    delivery days on weekends.

    departureDays: str - A sting of length 7 containing only 0 and 1.
    leadTime: int - The lead time as a integer '''
    
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
    '''

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
    
    ValueError if there are no departure days in the departureDays argument.
    RuntimeError if no deparparture route departure is calculated.
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