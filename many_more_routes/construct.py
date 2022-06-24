from .models import CustomerExtension, CustomerExtensionExtended, Template
from .models import Departure
from .models import Route
from .models import Selection
from typing import List
from datetime import datetime
from .methods import calc_departures, calc_route_departure, recalculate_lead_time


def MakeRoute(data: Template) -> Route:
    route = Route(
        ROUT=data.ROUT,
        RUTP=6,
        TX40=data.EDEL\
            + '_' + data.EDEU\
            + '_' + data.MODL,
        TX15=data.EDEL\
            + '_' + data.EDEU\
            + '_' + data.MODL,
        RESP=data.RRSP,
        SDES=data.EDEL,
        DLMC=1,
        DLAC=1,
        TSID=data.EDEU
    )

    return route


def MakeDeparture(data: Template) -> List[Departure]:
    list_of_departure_days = [data.DDOW]\
        if not data.ADOW\
        else calc_departures(data.DDOW, data.ARDY)
     
    departures = []
    for departureDays in list_of_departure_days:
        if not data.RODN:
            data.RODN = calc_route_departure(departureDays, data.ARDY)

        if data.ADOW:
            data.ARDY = recalculate_lead_time(departureDays, data.ARDY)

        if data.ARDX:
            data.ARDY = int(data.ARDX)

        departure =  Departure(
            WWROUT = data.ROUT,
            WWRODN = data.RODN,
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
            WRDDOW = data.DDOW,
            WRDETH = data.DETH,
            WRDETM = data.DETM,
            WRVFDT = datetime.now().strftime('%y%m%d'),
            WRARDY = data.ARDY,
            WRARHH = data.ARHH,
            WRARMM = data.ARMM
        )
        departures.append(departure)

    return departures


def MakeSelection(data: Template) -> Selection:
    selection = Selection(
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

    return selection


def MakeCustomerExtension(data: Template) -> List[CustomerExtension]:
    list_of_customer_extensions = []

    if data.PCUD or data.PCUH or data.PCUM:
        list_of_customer_extensions.append(
            CustomerExtension(
                FILE='DROUDI',
                PK01=data.ROUT,
                N096=data.PCUD,
                N196=data.PCUH,
                N296=data.PCUM
            )
        )

    if data.CUSD:
        list_of_customer_extensions.append(
            CustomerExtension(
                FILE='DROUTE',
                PK01=data.ROUT
            )
        )

    return list_of_customer_extensions
    

def MakeCustomerExtensionExtended(data: Template) -> List[CustomerExtensionExtended]:
    customer_extensions_extended_list = []

    if data.CUSD:
        customer_extensions_extended_list.append(
            CustomerExtensionExtended(
                FILE='DROUTE',
                PK01=data.ROUT,
                CHB1=data.CUSD
            )
        )

    return customer_extensions_extended_list