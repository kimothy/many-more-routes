from pydantic import Field, NonNegativeInt, StrictStr, ConstrainedStr, constr
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
    if v in [0, 0.0, None]:
        return None
    else:
        return str(v)



class NoneInt(NonNegativeInt):
    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield empty_to_none


Message = Field('', name='Message')
ROUT = Field(..., name='Route')
EDEL = Field(..., name='Place of Load')
EDEU = Field(..., name='Place of Unload')
MODL = Field(..., name='Mode of Transport')
RODN = Field(..., name='Route Departure')
DDOW = Field(..., name='Departure Days')
FWNO = Field(None, name='ForwardingAgent')
ARDY = Field(..., name='Lead Time')
ARDX = Field(None, name='Lead Time Offset*')
TRCA = Field(None, name='Transportation Equipment', min_length=3, max_length=3)
LILD = Field(..., name='Days to Deadline')
LILH = Field(..., name='Deadline Hours')
LILM = Field(..., name='Deadline Minutes')
PCUD = Field(None, name='Pick Cutoff Days')
PCUH = Field(None, name='Pick Cutoff Hours')
PCUM = Field(None, name='Pick Cutoff Minutes')
SILD = Field(None, name='Stipulated Internal Lead Time Days')
SILH = Field(None, name='Stipulated Internal Lead Time Hours')
SILM = Field(None, name='Stipulated Internal Lead Time Minutes')
FWLD = Field(..., name='Forwarders Arrival Lead Time Days')
FWLH = Field(..., name='Forwarders Arrival Lead Time Hours')
FWLM = Field(..., name='Forwarders Arrival Lead Time Minutes')
DETH = Field(..., name='Time of Departure Hours')
DETM = Field(..., name='Time of Departure Minutes')
ARHH = Field(..., name='Time of Arrival Hours Local Time')
ARMM = Field(..., name='Time of Arrival Minutes Local Time')
RRSP = Field(..., name='Route Responsible')
DRSP = Field(..., name='Departure Responsible')
VFDT = Field(None, name='Valid From')
VTDT = Field(None, name='Valid To')
PREX = Field(..., name='Priority')
OBV1 = Field(..., name='Start Value 1')
OBV2 = Field(..., name='Start Value 2')
OBV3 = Field(..., name='Start Value 3')
OBV4 = Field(None, name='Start Value 4')
SEFB = Field(None, name='Selection method for departures')
SELP = Field(None, name='Try lower priority')
RFID = Field(None, name='Reference')
PAL1 = Field(None, name='Pallet registration number')
PRRO = Field(None, name='Preliminary route selection')
LOLD = Field(None, name='Local transportation lead time - days')
LOLH = Field(None, name='Local transportation lead time - hours')
LOLM = Field(None, name='Local transportation lead time - minutes')
CUSD = Field(False, name='CustomsDeclaration')
ADOW = Field(False, name='Avoid Confirmed Delivery on Weekends')
FILE = Field(..., name='Table')
PK01 = Field(..., name='Primary key 1')
PK02 = Field('', name='Primary key 2')
PK03 = Field('', name='Primary key 3')
N096 = Field(0, name='Numeric field')
N196 = Field(0, name='Numeric field')
N296 = Field(0, name='Numeric field')
TX40 = Field(..., name='Description')
TX15 = Field(..., name='Name')
RESP = Field(..., name='Responsible')
SDES = Field(..., name='Place')
DLMC = Field(..., name='Manual shipment scheduling allowed')
DLAC = Field(..., name='Ignore deadline when connecting dely no')
TSID = Field(..., name='Transportation service ID')
CHB1 = Field(False, name='Yes/No')
CMNT = Field(..., name='Comment') 





class StandardTemplate(BaseModel):
    _api: str = PrivateAttr(default='TEMPLATE_V3')
    Message: Optional[str] = ''
    ROUT: Optional[str] = ROUT
    EDEL: str = EDEL
    EDEU: str = EDEU
    MODL: str = MODL
    DDOW: str = DDOW
    FWNO: Optional[str] = FWNO
    ARDY: PositiveInt = ARDY
    LILD: Optional[NoneInt] = LILD
    LILH: Optional[NoneInt] = LILH
    LILM: Optional[NoneInt] = LILM
    PCUD: Optional[NoneInt] = PCUD
    PCUH: Optional[NoneInt] = PCUH
    PCUM: Optional[NoneInt] = PCUM
    DETH: Optional[NoneInt] = DETH
    DETM: Optional[NoneInt] = DETM
    ARHH: Optional[NoneInt] = ARHH
    ARMM: Optional[NoneInt] = ARMM
    RRSP: str = RRSP
    DRSP: str = DRSP
    CUSD: Optional[bool] = CUSD
    ADOW: Optional[bool] = ADOW
    CMNT: Optional[str] = CMNT

    class Config:
        anystr_strip_whitespace = True
 

class Template(BaseModel):
    _api: str = PrivateAttr(default='TEMPLATE_V3')
    ROUT: Optional[str] = ROUT
    EDEL: str = EDEL
    EDEU: str = EDEU
    MODL: str = MODL
    RODN: Optional[PositiveInt] = RODN
    DDOW: str = DDOW
    FWNO: Optional[str] = FWNO
    ARDY: PositiveInt = ARDY
    ARDX: Optional[NoneInt] = ARDX
    TRCA: Optional[str] = TRCA
    LILD: Optional[NoneInt] = LILD
    LILH: Optional[NoneInt] = LILH
    LILM: Optional[NoneInt] = LILM
    PCUD: Optional[NoneInt] = PCUD
    PCUH: Optional[NoneInt] = PCUH
    PCUM: Optional[NoneInt] = PCUM
    SILD: Optional[NoneInt] = SILD
    SILH: Optional[NoneInt] = SILH
    SILM: Optional[NoneInt] = SILM
    FWLD: Optional[NoneInt] = FWLD
    FWLH: Optional[NoneInt] = FWLH
    FWLM: Optional[NoneInt] = FWLM
    DETH: Optional[NoneInt] = DETH
    DETM: Optional[NoneInt] = DETM
    ARHH: Optional[NoneInt] = ARHH
    ARMM: Optional[NoneInt] = ARMM
    RRSP: str = RRSP
    DRSP: str = DRSP
    CUSD: Optional[bool] = CUSD
    ADOW: Optional[bool] = ADOW
    CMNT: Optional[str] = CMNT

    class Config:
        anystr_strip_whitespace = True


class Route(BaseModel):
    _api: str = PrivateAttr(default='API_DRS005MI_AddRoute')
    Message: Optional[str] =  Message
    ROUT: str = ROUT
    RUTP: PositiveInt = Field(..., name='Route type')
    TX40: str = TX40
    TX15: str = TX15
    RESP: str = RESP
    SDES: str = SDES
    DLMC: NonNegativeInt = DLMC
    DLAC: NonNegativeInt = DLAC
    TSID: Optional[str] = TSID


class Departure(BaseModel):
    _api: str = PrivateAttr(default='MPD_DRS006_Create_CL')
    Message: Optional[str] = Message
    WWROUT: str = ROUT
    WWRODN: PositiveInt = RODN
    WRRESP: Optional[str] = RRSP
    WRFWNO: Optional[str] = FWNO
    WRTRCA: Optional[str] = TRCA
    WRMODL: Optional[str] = MODL
    WRLILD: Optional[str] = LILD
    WRSILD: Optional[str] = SILD
    WRLILH: Optional[int] = LILH
    WRLILM: Optional[int] = LILM
    WRSILH: Optional[int] = SILH
    WRSILM: Optional[int] = SILM
    WEFWLD: Optional[int] = FWLD
    WEFWLH: Optional[int] = FWLH
    WEFWLM: Optional[int] = FWLM
    WRDDOW: Optional[str] = DDOW
    WRDETH: Optional[int] = DETH
    WRDETM: Optional[int] = DETM
    WRVFDT: Optional[str] = VFDT
    WRVTDT: Optional[int] = VTDT
    WRARDY: Optional[int] = ARDY
    WRARHH: Optional[int] = ARHH
    WRARMM: Optional[int] = ARMM


class Selection(BaseModel):
    _api: str = PrivateAttr(default='API_DRS011_Add')
    Message: Optional[str] = Message
    EDES: str = EDEL
    PREX: str = PREX
    OBV1: Optional[str] = OBV1
    OBV2: Optional[str] = OBV2
    OBV3: Optional[str] = OBV3
    OBV4: Optional[str] = OBV4
    ROUT: Optional[str] = ROUT
    RODN: PositiveInt = RODN
    SEFB: Optional[int] = SEFB
    SELP: Optional[int] = SELP
    DDOW: Optional[str] = DDOW
    FWNO: Optional[str] = FWNO
    TRCA: Optional[str] = TRCA
    RFID: Optional[str] = RFID
    PAL1: Optional[str] = PAL1
    PRRO: Optional[int] = PRRO
    LOLD: Optional[int] = LOLD
    LOLH: Optional[int] = LOLH
    LOLM: Optional[int] = LOLM


class CustomerExtension(BaseModel):
    _api: str = PrivateAttr(default='API_CUSEXTMI_AddFieldValue')
    Message: Optional[str] = Message
    FILE: str
    PK01: Optional[str] = PK01
    N096: Optional[str] = N096
    N196: Optional[str] = N196
    N296: Optional[str] = N296



class CustomerExtensionExtended(BaseModel):
    _api: str = PrivateAttr(default='API_CUSEXTMI_ChgFieldValueEx')
    Message: Optional[str] = Message
    FILE: str = FILE
    PK01: Optional[str] = PK01
    CHB1: Optional[bool] = CHB1