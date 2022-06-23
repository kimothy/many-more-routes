from pydantic import Field
from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import PrivateAttr
from pydantic.validators import str_validator

from typing import Optional
from typing import Protocol
from typing import Dict
from typing import Union
from typing import runtime_checkable

REGEX_STR_ROUTE = "^[A-Z]{2}\d{4}$|^[A-Z]{6}$|^[A-Z]{3}_[A-Z]{2}$|^#[A-Z]{5}"
REGEX_STR_PLACE_OF_LOAD = "^[A-Z]{3}"
REGEX_STR_PLACE_OF_UNLOAD = "^[A-Z]{2}\d{2}$|^[A-Z]{3}$"
REGEX_STR_DEPARTURE_DAYS = "^[0-1]{7}$"
REGEX_STR_DELIVERY_METHOD = "^\d{2}|\d{3}$"


def empty_to_none(v: Union[int, str, float, None]) -> Optional[str]:
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
    _api: str = PrivateAttr(default='TEMPLATE_V3')
    ROUT: Optional[str] = Field(..., name='Route', strip_whitespace=True, regex=REGEX_STR_ROUTE)
    EDEL: str = Field(..., name='Place of Load', strip_whitespace=True, regex=REGEX_STR_PLACE_OF_LOAD)
    EDEU: str = Field(..., name='Place of Unload', strip_whitespace=True, regex=REGEX_STR_PLACE_OF_UNLOAD)
    MODL: str = Field(..., name='Mode of Transport', strip_whitespace=True, regex=REGEX_STR_DELIVERY_METHOD)
    RODN: Optional[PositiveInt] = Field(..., name='Route Departure')
    DDOW: str = Field(..., name='Departure Days', strip_whitespace=True, regex=REGEX_STR_DEPARTURE_DAYS)
    FWNO: Optional[str] = Field(..., name='ForwardingAgent', strip_whitespace=True)
    ARDY: PositiveInt = Field(..., name='Lead Time')
    ARDX: Optional[NoneInt] = Field(..., name='Lead Time Offset*')
    TRCA: Optional[str] = Field(..., name='Transportation Equipment', min_length=3, max_length=3)
    LILD: Optional[NoneInt] = Field(..., name='Days to Deadline')
    LILH: Optional[NoneInt] = Field(..., name='Deadline Hours')
    LILM: Optional[NoneInt] = Field(..., name='Deadline Minutes')
    PCUD: Optional[NoneInt] = Field(..., name='Pick Cutoff Days')
    PCUH: Optional[NoneInt] = Field(..., name='Pick Cutoff Hours')
    PCUM: Optional[NoneInt] = Field(..., name='Pick Cutoff Minutes')
    SILD: Optional[NoneInt] = Field(..., name='Stipulated Internal Lead Time Days')
    SILH: Optional[NoneInt] = Field(..., name='Stipulated Internal Lead Time Hours')
    SILM: Optional[NoneInt] = Field(..., name='Stipulated Internal Lead Time Minutes')
    FWLD: Optional[NoneInt] = Field(..., name='Forwarders Arrival Lead Time Days')
    FWLH: Optional[NoneInt] = Field(..., name='Forwarders Arrival Lead Time Hours')
    FWLM: Optional[NoneInt] = Field(..., name='Forwarders Arrival Lead Time Minutes')
    DETH: Optional[NoneInt] = Field(..., name='Time of Departure Hours')
    DETM: Optional[NoneInt] = Field(..., name='Time of Departure Minutes')
    ARHH: Optional[NoneInt] = Field(..., name='Time of Arrival Hours Local Time')
    ARMM: Optional[NoneInt] = Field(..., name='Time of Arrival Minutes Local Time')
    RRSP: str = Field(..., name='Route Responsible')
    DRSP: str = Field(..., name='Departure Responsible')
    CUSD: Optional[bool] = Field(..., name='CustomsDeclaration')
    ADOW: Optional[bool] = Field(..., name='Avoid Confirmed Delivery on Weekends')
    CMNT: Optional[str] = Field(..., name='Comment') 


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


class Selection(BaseModel):
    _api: str = PrivateAttr(default='API_DRS011_Add')
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
    FILE: str
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