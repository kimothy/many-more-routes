from .models import CustomerExtension, CustomerExtensionExtended, Template
from .models import Departure
from .models import Route
from .models import Selection
from typing import Iterator, List, Optional
from datetime import datetime
from .methods import calc_departures, calc_route_departure, recalculate_lead_time

def tostr(string: Optional[str]) -> str:
    if not string:
        return ''
    else:
        return string

def MakeRoute(data: Template) -> Iterator[Route]:
    data = data.copy()

    tostr = lambda x: str(x) if x != None else ''

    yield Route.construct(
        ROUT=data.ROUT,
        RUTP=6,
        TX40=tostr(data.EDEL)\
            + '_' + tostr(data.EDEU)\
            + '_' + tostr(data.MODL),
        TX15=tostr(data.EDEL)\
            + '_' + tostr(data.EDEU)\
            + '_' + tostr(data.MODL),
        RESP=data.RRSP,
        SDES=data.EDEL,
        DLMC=1,
        DLAC=1,
        TSID=data.EDEU
    )


def MakeDeparture(data: Template) -> Iterator[Departure]:
    data = data.copy()

    list_of_departure_days = [data.DDOW]\
        if not data.ADOW\
        else calc_departures(data.DDOW, data.ARDY)
     
    for DDOW in list_of_departure_days:
        RODN = calc_route_departure(DDOW, data.ARDY) if not data.RODN else data.RODN
        ARDY = recalculate_lead_time(DDOW, data.ARDY) if data.ADOW else data.ARDY
        ARDY = int(data.ARDX) if data.ARDX else ARDY
    
        yield Departure.construct(
            WWROUT = data.ROUT,
            WWRODN = RODN,
            WRRESP = data.DRSP,
            WRFWNO = data.FWNO,
            WRTRCA = data.TRCA,
            WRMODL = data.MODL,
            WRLILD = data.LILD,
            WRSILD = data.SILD,
            WRLILH = data.LILH,
            WRLILM = data.LILM,
            WRSILH = data.SILH,
            WRSILM = data.SILM,
            WEFWLD = data.FWLD,
            WEFWLH = data.FWLH,
            WEFWLM = data.FWLM,
            WRDDOW = DDOW,
            WRDETH = data.DETH,
            WRDETM = data.DETM,
            WRVFDT = datetime.now().strftime('%y%m%d'),
            WRARDY = ARDY,
            WRARHH = data.ARHH,
            WRARMM = data.ARMM
        )


def MakeSelection(data: Template) -> Iterator[Selection]:
    data = data.copy()
    yield Selection.construct(
        EDES = data.EDEL,
        PREX = ' 6',  # with preceeding space
        OBV1 = data.EDEU,
        OBV2 = data.MODL,
        OBV3 = '',
        OBV4 = '',
        ROUT = data.ROUT,
        RODN = data.RODN,
        SEFB = '4',
        DDOW = '1111100',
        LOLD = data.ARDY\
            if data.ARDX\
            else None
    )



def MakeCustomerExtension(data: Template) -> Iterator[CustomerExtension]:
    data = data.copy()

    if data.PCUD or data.PCUH or data.PCUM:
        yield CustomerExtension.construct(
            FILE='DROUDI',
            PK01=data.ROUT,
            N096=data.PCUD if data.PCUD else None,
            N196=data.PCUH if data.PCUH else None,
            N296=data.PCUM if data.PCUM else None
        )

    if data.CUSD:
        yield CustomerExtension.construct(
                FILE='DROUTE',
                PK01=data.ROUT
            )


def MakeCustomerExtensionExtended(data: Template) -> Iterator[CustomerExtensionExtended]:
    data = data.copy()

    if data.CUSD:
        yield CustomerExtensionExtended.construct(
                FILE='DROUTE',
                PK01=data.ROUT,
                CHB1=data.CUSD
            )