from collections import Counter
from functools import reduce
from pydantic import BaseModel, Field, constr, PositiveInt, root_validator, PrivateAttr
from pydantic import validator
from pydantic import StrictStr
from pydantic.validators import str_validator
from typing import Optional
from typing import List
from re import compile

REGEX_STR_ROUTE = "^[A-Z]{2}\d{4}$|^[A-Z]{6}$|^[A-Z]{3}_[A-Z]{2}$|^#[A-Z]{5}"
REGEX_STR_PLACE_OF_LOAD = "^[A-Z]{3}"
REGEX_STR_PLACE_OF_UNLOAD = "^[A-Z]{2}\d{2}$|^[A-Z]{3}$"
REGEX_STR_DEPARTURE_DAYS = "^[0-1]{7}$"

class DuplicateError(Exception):
    ...
    

def empty_to_none(v: int|str|float|None) -> Optional[str]:
    if v in [0, 0.0, '', None]:
        return None
    else:
        return str(v)


class NoneInt(PositiveInt):
    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield empty_to_none


class Template(BaseModel):
    _api = PrivateAttr(default='TEMPLATE_V3')
    Route: constr(strip_whitespace=True, regex=REGEX_STR_ROUTE)
    DeliveryMethod: str
    PlaceOfLoad: constr(strip_whitespace=True, regex=REGEX_STR_PLACE_OF_LOAD)
    PlaceOfUnload: constr(strip_whitespace=True, regex=REGEX_STR_PLACE_OF_UNLOAD)
    RouteDeparture: Optional[int]
    DepartureDays: constr(strip_whitespace=True, regex=REGEX_STR_DEPARTURE_DAYS)
    ForwardingAgent: Optional[str]
    LeadTime: PositiveInt
    LeadTimeOffset: Optional[NoneInt]
    TransportationEquipment: Optional[str]
    DaysToDeadline: Optional[NoneInt]
    DeadlineHours: Optional[NoneInt]
    DeadlineMinutes: Optional[NoneInt]
    PickCutOffDays: Optional[NoneInt]
    PickCutOffTimeHours: Optional[NoneInt]
    PickCutOffTimeMinutes: Optional[NoneInt]
    StipulatedInternalLeadTimeHours: Optional[NoneInt]
    StipulatedInternalLeadTimeDays: Optional[NoneInt]
    StipulatedInternalLeadTimeMinutes: Optional[NoneInt]
    ForwardersArrivalLeadTimeDays: Optional[NoneInt]
    ForwardersArrivalLeadTimeHours: Optional[NoneInt]
    ForwardersArrivalLeadTimeMinutes: Optional[NoneInt]
    TimeOfDepartureHours: Optional[NoneInt]
    TimeOfDepartureMinutes: Optional[NoneInt]
    TimeOfArrivalHoursLocalTime: Optional[NoneInt]
    TimeOfArrivalMinutesLocalTime: Optional[NoneInt]
    RouteResponsible: str
    DepartureResponsible: str
    CustomsDeclaration: Optional[bool]
    AvoidConfirmedDeliveryOnWeekends: Optional[bool]
    CreateSmartSheets: Optional[bool]
    Comment: Optional[str]

    @validator('DepartureDays')
    def departure_days_validation(cls, v):
        if not all([c for c in list(str(v)) if c in ['0', '1']]) or len(str(v)) != 7:
            raise ValueError('Invalid departure days. All days of week should have 0 or 1 assigned')

        return str(v)

    @validator('DeliveryMethod')
    def delivery_method_validation(cls, v):
        if not all([c.isdigit() for c in list(str(v))]):
            raise ValueError('Invalid delivery method')

        return str(v)


class Route(BaseModel):
    _api: str = PrivateAttr(default='API_DRS005MI_AddRoute')
    ROUT: str
    RUTP: PositiveInt
    TX40: str
    TX15: str
    RESP: str
    SDES: str
    DLMC: PositiveInt
    DLAC: PositiveInt
    TSID: Optional[str]


class Departure(BaseModel):
    _api: str = PrivateAttr(default='MPD_DRS006_Create_CL')
    WWROUT: str
    WWRODN: PositiveInt
    WRRESP: Optional[str]
    WRFWNO: Optional[str]
    WRTRCA: Optional[str]
    WRMODL: Optional[str]
    WRLILD: Optional[str]
    WRSILD: Optional[str]
    WRLILH: Optional[int]
    WRLILM: Optional[int]
    WRSILH: Optional[int]
    WRSILM: Optional[int]
    WEFWLD: Optional[int]
    WEFWLH: Optional[int]
    WEFWLM: Optional[int]
    WRDDOW: Optional[str]
    WRDETH: Optional[int]
    WRDETM: Optional[int]
    WRVFDT: Optional[str]
    WRVTDT: Optional[int]
    WRARDY: Optional[int]
    WRARHH: Optional[int]
    WRARMM: Optional[int]

    @validator('WWRODN')
    def validate_rodn(cls, v):
        if v == 0:
            ValueError('Route Departure (RODN) must be greater then 0')
        
        return v


class Selection(BaseModel):
    _api: str = PrivateAttr(default='MPD_DRS011_Create_CL')
    EDES: str
    PREX: str
    OBV1: Optional[str]
    OBV2: Optional[str]
    OBV3: Optional[str]
    OBV4: Optional[str]
    ROUT: Optional[str]
    RODN: PositiveInt
    SEFB: Optional[int]
    SELP: Optional[int]
    DDOW: Optional[str]
    FWNO: Optional[str]
    TRCA: Optional[str]
    RFID: Optional[str]
    PAL1: Optional[str]
    PRRO: Optional[int]
    LOLD: Optional[int]
    LOLH: Optional[int]
    LOLM: Optional[int]


class CustomerExtension(BaseModel):
    _api: str = PrivateAttr(default='API_CUSEXTMI_AddFieldValue')
    FILE: str
    PK01: Optional[str]
    PK02: Optional[str]
    PK03: Optional[str]
    PK04: Optional[str]
    PK05: Optional[str]
    PK06: Optional[str]
    PK07: Optional[str]
    PK08: Optional[str]
    A030: Optional[str]
    A130: Optional[str]
    A230: Optional[str]
    A330: Optional[str]
    A430: Optional[str]
    A530: Optional[str]
    A630: Optional[str]
    A730: Optional[str]
    A830: Optional[str]
    A930: Optional[str]
    N096: Optional[str]
    N196: Optional[str]
    N296: Optional[str]
    N396: Optional[str]
    N496: Optional[str]
    N596: Optional[str]
    N696: Optional[str]
    N796: Optional[str]
    N896: Optional[str]
    N996: Optional[str]
    MIGR: Optional[str]


class CustomerExtensionExtended(BaseModel):
    _api: str = PrivateAttr(default='API_CUSEXTMI_ChgFieldValueEx')
    FILE: Optional[str]
    PK01: Optional[str]
    PK02: Optional[str]
    PK03: Optional[str]
    PK04: Optional[str]
    PK05: Optional[str]
    PK06: Optional[str]
    PK07: Optional[str]
    PK08: Optional[str]
    CHB1: Optional[bool]
    CHB2: Optional[bool]
    CHB3: Optional[bool]
    CHB4: Optional[bool]
    CHB5: Optional[bool]
    CHB6: Optional[bool]
    CHB7: Optional[bool]
    CHB8: Optional[bool]
    CHB9: Optional[bool]
    DAT1: Optional[str]
    DAT2: Optional[str]
    DAT3: Optional[str]
    DAT4: Optional[str]
    DAT5: Optional[str]
    DAT6: Optional[str]
    DAT7: Optional[str]
    DAT8: Optional[str]
    DAT9: Optional[str]
    A122: Optional[str]
    A256: Optional[str]