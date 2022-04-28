from typing import Optional

def generator(sequenceNumber: Optional[str] = None, n: Optional[int] = None):
    '''Returns a sequence generator. If n is not given it will loop infinitely'''
    if n:
        for _ in range(n):
            sequenceNumber = next(sequenceNumber)
            yield sequenceNumber

    else:
        while True:
            sequenceNumber = next(sequenceNumber)
            yield sequenceNumber
        


def next(sequenceNumber: Optional[str] = None):
    '''Taked a route sequence number and incriments by one.

    >>> next(None)
    'AA0001'
    >>> next('AA0001')
    'AA0002'
    >>> next('AA9999')
    'AB0001'
    >>> next('ZZ9999')
    'AA0001'
    '''
    if sequenceNumber:
        alpha = sequenceNumber[:2]
        digit = sequenceNumber[2:]

        newDigit = incrementDigit(digit)
        newAlpha = incrementAlpha(alpha) if newDigit == next()[2:] else alpha

        return newAlpha + newDigit

    else:
        return 'AA0001'

        
def incrementAlpha(alpha: str) -> str:
    '''Takes a upper char string and increments as it's a number sequence.
    
    >>> incrementAlpha('AA')
    'AB'
    >>> incrementAlpha('ZZ')
    'AA'
    
    '''
    assert any(map(lambda x: x.isalpha(), alpha))

    alphaArray = list(reversed(alpha))

    for n, char in enumerate(alphaArray):
        alphaArray[n] = chr((ord(char.upper())+1 - 65) % 26 + 65)

        if not char == 'Z':
            break

    return ''.join(reversed(alphaArray))



def incrementDigit(alpha: str) -> str:
    ''' Takes a digit as string type and returns as equal length number as string.
        Number is reset to 1 when max number is reached.    
     '''
    assert any(map(lambda x: x.isdigit(), alpha))

    if all(map(lambda x: x  == '9', alpha)):
        return f'1'.zfill(len(alpha))

    else:
        return f'{int(alpha) + 1}'.zfill(len(alpha))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
