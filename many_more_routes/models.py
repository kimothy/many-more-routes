import sys
from pydantic import Field, NonNegativeInt, StrictStr, ConstrainedStr, constr
from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import PrivateAttr
from pydantic.validators import str_validator

from typing import Optional
from typing import Union
from typing import Any

from functools import partial

REGEX_STR_ROUTE = "^[A-Z]{2}\d{4}$|^[A-Z]{6}$|^[A-Z]{3}_[A-Z]{2}$|^#[A-Z]{5}"
REGEX_STR_PLACE_OF_LOAD = "^[A-Z]{3}"
REGEX_STR_PLACE_OF_UNLOAD = "^[A-Z]{2}\d$|^[A-Z]{2}\d{2}$|^[A-Z]{3}$"
REGEX_STR_DEPARTURE_DAYS = "^[0-1]{7}$"
REGEX_STR_MODE_OF_TRANSPORT = "^\d{2}|\d{3}$"


def empty_to_none(v: Union[int, str, float, None]) -> Optional[str]:
    if v in [0, 0.0, None, '']:
        return None
    else:
        return str(v)



class NoneInt(NonNegativeInt):
    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield empty_to_none


Message = partial(Field, name='Message', description='Feedback Message from the API')

ROUT = partial(Field, name='Route')
EDEL = partial(Field, name='Place of Load')
EDEU = partial(Field, name='Place of Unload')
MODL = partial(Field, name='Mode of Transport')
RODN = partial(Field, name='Route Departure')

DDOW = partial(Field, name='Departure Days')
FWNO = partial(Field, name='ForwardingAgent')
TRCA = partial(Field, name='Transportation Equipment')

ARDY = partial(Field, name='Lead Time')
ARDX = partial(Field, name='Lead Time Offset*')

LILD = partial(Field, name='Days to Deadline')
LILH = partial(Field, name='Deadline Hours')
LILM = partial(Field, name='Deadline Minutes')

PCUD = partial(Field, name='Pick Cutoff Days')
PCUH = partial(Field, name='Pick Cutoff Hours')
PCUM = partial(Field, name='Pick Cutoff Minutes')

SILD = partial(Field, name='Stipulated Internal Lead Time Days')
SILH = partial(Field, name='Stipulated Internal Lead Time Hours')
SILM = partial(Field, name='Stipulated Internal Lead Time Minutes')

FWLD = partial(Field, name='Forwarders Arrival Lead Time Days')
FWLH = partial(Field, name='Forwarders Arrival Lead Time Hours')
FWLM = partial(Field, name='Forwarders Arrival Lead Time Minutes')

DETH = partial(Field, name='Time of Departure Hours')
DETM = partial(Field, name='Time of Departure Minutes')

ARHH = partial(Field, name='Time of Arrival Hours Local Time')
ARMM = partial(Field, name='Time of Arrival Minutes Local Time')

RRSP = partial(Field, name='Route Responsible')
DRSP = partial(Field, name='Departure Responsible')

CHB1 = partial(Field, name='Yes/No')
VFDT = partial(Field, name='Valid From')
VTDT = partial(Field, name='Valid To')
CUSD = partial(Field, name='CustomsDeclaration')

FILE = partial(Field, name='File')
PK01 = partial(Field, name='Primary key 1')
N096 = partial(Field, name='Numeric field')
N196 = partial(Field, name='Numeric field')
N296 = partial(Field, name='Numeric field')

CMNT = partial(Field, name='Comment')
ADOW = partial(Field, name='Avoid Confirmed Delivery on Weekends')

OBV1 = partial(Field, name='Start Value 1')
OBV2 = partial(Field, name='Start Value 2')
OBV3 = partial(Field, name='Start Value 3')
OBV4 = partial(Field, name='Start Value 4')


TX40 = partial(Field, name='Description')
TX15 = partial(Field, name='Name')
RESP = partial(Field, name='Responsible')
SDES = partial(Field, name='Place')
DLMC = partial(Field, name='Manual shipment scheduling allowed')
DLAC = partial(Field, name='Ignore deadline when connecting dely no')


SEFB = partial(Field, name='Selection method for departures')
SELP = partial(Field, name='Try lower priority')
RFID = partial(Field, name='Reference')
PAL1 = partial(Field, name='Pallet registration number')
PRRO = partial(Field, name='Preliminary route selection')
LOLD = partial(Field, name='Local transportation lead time - days')
LOLH = partial(Field, name='Local transportation lead time - hours')
LOLM = partial(Field, name='Local transportation lead time - minutes')

TSID = partial(Field, name='Transportation service ID')
PREX = partial(Field, name='Priority')
RUTP = partial(Field, name='Route p.')

class UnvalidatedTemplate(BaseModel):
    _api: str = PrivateAttr(default='TEMPLATE_V3')
    ROUT: Optional[Any] = ROUT(None)
    EDEL: Optional[Any] = EDEL(None)
    EDEU: Optional[Any] = EDEU(None)
    MODL: Optional[Any] = MODL(None)
    RODN: Optional[Any] = RODN(None)
    DDOW: Optional[Any] = DDOW(None)
    FWNO: Optional[Any] = FWNO(None)
    ARDY: Optional[Any] = ARDY(None)
    ARDX: Optional[Any] = ARDX(None)
    TRCA: Optional[Any] = TRCA(None)
    LILD: Optional[Any] = LILD(None)
    LILH: Optional[Any] = LILH(None)
    LILM: Optional[Any] = LILM(None)
    SILD: Optional[Any] = SILD(None)
    SILH: Optional[Any] = SILH(None)
    SILM: Optional[Any] = SILM(None)
    FWLD: Optional[Any] = FWLD(None)
    FWLH: Optional[Any] = FWLH(None)
    FWLM: Optional[Any] = FWLM(None)
    PCUD: Optional[Any] = PCUD(None)
    PCUH: Optional[Any] = PCUH(None)
    PCUM: Optional[Any] = PCUM(None)
    DETH: Optional[Any] = DETH(None)
    DETM: Optional[Any] = DETM(None)
    ARHH: Optional[Any] = ARHH(None)
    ARMM: Optional[Any] = ARMM(None)
    RRSP: Optional[Any] = RRSP(None)
    DRSP: Optional[Any] = DRSP(None)
    CUSD: Optional[Any] = CUSD(None)
    ADOW: Optional[Any] = ADOW(None)
    CMNT: Optional[Any] = CMNT(None)

    class Config:
        anystr_strip_whitespace = True


class ValidatedTemplate(UnvalidatedTemplate):
    _api: str = PrivateAttr(default='TEMPLATE_V3')
    ROUT: str = ROUT(..., min_length=6, max_length=6, regex=REGEX_STR_ROUTE)
    EDEL: str = EDEL(..., min_length=3, max_length=4, regex=REGEX_STR_PLACE_OF_LOAD)
    EDEU: str = EDEU(..., min_length=3, max_length=4, regex=REGEX_STR_PLACE_OF_UNLOAD)
    RODN: Optional[PositiveInt] = RODN(...)
    MODL: str = MODL(..., min_length=2, max_length=3, regex=REGEX_STR_MODE_OF_TRANSPORT)
    DDOW: str = DDOW(..., min_length=7, max_length=7, regex=REGEX_STR_DEPARTURE_DAYS)
    FWNO: str = FWNO(..., min_length=7, max_length=7)
    ARDY: PositiveInt = ARDY(...)
    RRSP: str = RRSP('M3GENUSR')
    DRSP: str = DRSP('M3GENUSR')
    CUSD: Optional[bool] = CUSD(None)
    ADOW: Optional[bool] = ADOW(None)


class Route(BaseModel):
    _api: str = PrivateAttr(default='API_DRS005MI_AddRoute')
    Message: Optional[str] =  Message(None)
    ROUT: str = ROUT(..., min_length=6, max_length=6, regex=REGEX_STR_ROUTE)
    RUTP: PositiveInt = RUTP(...)
    TX40: str = TX40(..., max_length=40)
    TX15: str = TX15(..., max_length=15)
    RESP: str = RESP(..., max_length=8)
    SDES: str = SDES(..., max_length=4)
    DLMC: NonNegativeInt = DLMC(...)
    DLAC: NonNegativeInt = DLAC(...)
    TSID: Optional[str] = TSID(None, max_length=4)


class Departure(BaseModel):
    _api: str = PrivateAttr(default='MPD_DRS006_Create_CL')
    Message: Optional[str] = Message(None)
    WWROUT: str = ROUT(...)
    WWRODN: PositiveInt = RODN(...)
    WRRESP: Optional[str] = RRSP(None)
    WRFWNO: Optional[str] = FWNO(None)
    WRTRCA: Optional[str] = TRCA(None)
    WRMODL: Optional[str] = MODL(None)
    WRLILD: Optional[str] = LILD(None)
    WRSILD: Optional[str] = SILD(None)
    WRLILH: Optional[int] = LILH(None)
    WRLILM: Optional[int] = LILM(None)
    WRSILH: Optional[int] = SILH(None)
    WRSILM: Optional[int] = SILM(None)
    WEFWLD: Optional[int] = FWLD(None)
    WEFWLH: Optional[int] = FWLH(None)
    WEFWLM: Optional[int] = FWLM(None)
    WRDDOW: Optional[str] = DDOW(None)
    WRDETH: Optional[int] = DETH(None)
    WRDETM: Optional[int] = DETM(None)
    WRVFDT: Optional[str] = VFDT(None)
    WRVTDT: Optional[int] = VTDT(None)
    WRARDY: Optional[int] = ARDY(None)
    WRARHH: Optional[int] = ARHH(None)
    WRARMM: Optional[int] = ARMM(None)


class Selection(BaseModel):
    _api: str = PrivateAttr(default='API_DRS011_Add')
    Message: Optional[str] = Message(None)
    EDES: str = EDEL(...)
    PREX: str = PREX(...)
    OBV1: Optional[str] = OBV1(None)
    OBV2: Optional[str] = OBV2(None)
    OBV3: Optional[str] = OBV3(None)
    OBV4: Optional[str] = OBV4(None)
    ROUT: Optional[str] = ROUT(None)
    RODN: Optional[PositiveInt] = RODN(None)
    SEFB: Optional[int] = SEFB(None)
    SELP: Optional[int] = SELP(None)
    DDOW: Optional[str] = DDOW(None)
    FWNO: Optional[str] = FWNO(None)
    TRCA: Optional[str] = TRCA(None)
    RFID: Optional[str] = RFID(None)
    PAL1: Optional[str] = PAL1(None)
    PRRO: Optional[int] = PRRO(None)
    LOLD: Optional[int] = LOLD(None)
    LOLH: Optional[int] = LOLH(None)
    LOLM: Optional[int] = LOLM(None)


class CustomerExtension(BaseModel):
    _api: str = PrivateAttr(default='API_CUSEXTMI_AddFieldValue')
    Message: Optional[str] = Message(None)
    FILE: str = FILE(...)
    PK01: str = PK01(...)
    N096: Optional[NonNegativeInt] = N096(None)
    N196: Optional[NonNegativeInt] = N196(None)
    N296: Optional[NonNegativeInt] = N296(None)


class CustomerExtensionExtended(BaseModel):
    _api: str = PrivateAttr(default='API_CUSEXTMI_ChgFieldValueEx')
    Message: Optional[str] = Message()
    FILE: str = FILE(...)
    PK01: str = PK01(...)
    CHB1: Optional[int] = CHB1(...)



