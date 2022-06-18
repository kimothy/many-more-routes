from .models import CustomerExtension, CustomerExtensionExtended, Template
from .models import Departure
from .models import Route
from .models import Selection
from typing import List
from datetime import datetime
from .methods import calc_departures, calc_route_departure, recalculate_lead_time


def MakeRoute(data: Template) -> Route:
    route = Route(
        ROUT=data.Route,
        RUTP=6,
        TX40=data.PlaceOfLoad\
            + '_' + data.PlaceOfUnload\
            + '_' + data.DeliveryMethod,
        TX15=data.PlaceOfLoad\
            + '_' + data.PlaceOfUnload\
            + '_' + data.DeliveryMethod,
        RESP=data.RouteResponsible,
        SDES=data.PlaceOfLoad,
        DLMC=1,
        DLAC=1,
        TSID=data.PlaceOfUnload
    )

    return route


def MakeDeparture(data: Template) -> List[Departure]:
    list_of_departure_days = [data.DepartureDays]\
        if not data.AvoidConfirmedDeliveryOnWeekends\
        else calc_departures(data.DepartureDays, data.LeadTime)
     
    departures = []
    for departureDays in list_of_departure_days:
        if not data.RouteDeparture:
            data.RouteDeparture = calc_route_departure(departureDays, data.LeadTime)

        if data.AvoidConfirmedDeliveryOnWeekends:
            data.LeadTime = recalculate_lead_time(departureDays, data.LeadTime)

        if data.LeadTimeOffset:
            data.LeadTime = int(data.LeadTimeOffset)

        departure =  Departure(
            WWROUT = data.Route,
            WWRODN = data.RouteDeparture,
            WRRESP = data.DepartureResponsible,
            WRFWNO = data.ForwardingAgent,
            WRTRCA = data.TransportationEquipment,
            WRMODL = data.DeliveryMethod,
            WRLILD = data.DaysToDeadline,
            WRSILD = data.StipulatedInternalLeadTimeDays,
            WRLILH = data.DeadlineHours,
            WRLILM = data.DeadlineMinutes,
            WRSILH = data.StipulatedInternalLeadTimeHours,
            WRSILM = data.StipulatedInternalLeadTimeMinutes,
            WEFWLD = data.ForwardersArrivalLeadTimeDays,
            WEFWLH = data.ForwardersArrivalLeadTimeHours,
            WEFWLM = data.ForwardersArrivalLeadTimeMinutes,
            WRDDOW = data.DepartureDays,
            WRDETH = data.TimeOfDepartureHours,
            WRDETM = data.TimeOfDepartureMinutes,
            WRVFDT = datetime.now().strftime('%y%m%d'),
            WRARDY = data.LeadTime,
            WRARHH = data.TimeOfArrivalHoursLocalTime,
            WRARMM = data.TimeOfArrivalMinutesLocalTime
        )
        departures.append(departure)

    return departures


def MakeSelection(data: Template) -> Selection:
    selection = Selection(
        EDES = data.PlaceOfLoad,
        PREX = ' 6',  # with preceeding space
        OBV1 = data.PlaceOfUnload,
        OBV2 = data.DeliveryMethod,
        OBV3 = '',
        OBV4 = '',
        ROUT = data.Route,
        RODN = data.RouteDeparture,
        SEFB = '4',
        DDOW = '1111100',
        LOLD = data.LeadTime\
            if data.LeadTimeOffset\
            else None
    )

    return selection


def MakeCustomerExtension(data: Template) -> List[CustomerExtension]:
    list_of_customer_extensions = []

    if data.PickCutOffDays or data.PickCutOffDays or data.PickCutOffTimeMinutes:
        list_of_customer_extensions.append(
            CustomerExtension(
                FILE='DROUDI',
                PK01=data.Route,
                N096=data.PickCutOffDays,
                N196=data.PickCutOffTimeHours,
                N296=data.PickCutOffTimeMinutes
            )
        )

    if data.CustomsDeclaration:
        list_of_customer_extensions.append(
            CustomerExtension(
                FILE='DROUTE',
                PK01=data.Route
            )
        )

    return list_of_customer_extensions
    

def MakeCustomerExtensionExtended(data: Template) -> List[CustomerExtensionExtended]:
    customer_extensions_extended_list = []

    if data.CustomsDeclaration:
        customer_extensions_extended_list.append(
            CustomerExtensionExtended(
                FILE='DROUTE',
                PK01=data.Route
            )
        )

    return customer_extensions_extended_list