from typing import Optional, Generator

def increment(sequenceNumber: Optional[str] = None) -> str:
    '''Taked a route sequence number and incriments by one.
    >>> increment(None)
    'AA0001'
    >>> increment('AA0001')
    'AA0002'
    >>> increment('AA9999')
    'AB0001'
    >>> increment('ZZ9999')
    'AA0001'
    '''
    if sequenceNumber:
        _validate_seed(sequenceNumber)

    return _next(sequenceNumber)


def generator(sequenceNumber: Optional[str] = None, n: Optional[int] = None) -> Generator:
    '''Returns a sequence generator. If n is not given it will loop infinitely'''
    if sequenceNumber:
        _validate_seed(sequenceNumber)

    return _generator(sequenceNumber, n)


def _validate_seed(sequenceNumber: str) -> None:
    '''Validate the input of a seed'''
    if len(sequenceNumber) != 6:
        raise ValueError('The sequence number has to be exatly 6 chars long')
    elif not sequenceNumber[:2].isalpha():
        raise ValueError('The first to chars of the sequence number has to be alpha numeric')
    elif not sequenceNumber[2:].isdigit():
        raise ValueError('The last four chars of the sequence number has to be numeric')


def is_sequenceNumber_valid(sequenceNumber: str):
    ''' Returns True if seed is valid, else False. Can be used in a functional way
    to determine if a sequence number is valid or not, or to filter out route names that follows
    an different route name scheme in combination with the standard python filter function '''
    try:
        _validate_seed(sequenceNumber=sequenceNumber)
        return True

    except ValueError:
        return False


def _generator(sequenceNumber: Optional[str] = None, n: Optional[int] = None) -> Generator:
    '''Returns a sequence generator. If n is not given it will loop infinitely'''
    if sequenceNumber:
        yield sequenceNumber

    if n:
        for _ in range(n - 1):
            sequenceNumber = _next(sequenceNumber)
            yield sequenceNumber

    else:
        while True:
            sequenceNumber = _next(sequenceNumber)
            yield sequenceNumber
        

def _next(sequenceNumber: Optional[str] = None) -> str:
    '''Taked a route sequence number and incriments by one.'''
    if sequenceNumber:
        alpha = sequenceNumber[:2]
        digit = sequenceNumber[2:]

        newDigit = _incrementDigit(digit)
        newAlpha = _incrementAlpha(alpha) if newDigit == increment()[2:] else alpha

        return newAlpha + newDigit

    else:
        return 'AA0001'

        
def _incrementAlpha(alpha: str) -> str:
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


def _incrementDigit(alpha: str) -> str:
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