from pydantic import BaseModel
from pydantic import validator
from pydantic import StrictStr
from pydantic.validators import str_validator
from typing import Optional


def empty_to_none(v: int|str|float) -> Optional[str]:
    if v in [0, 0.0, '']:
        return None
    else:
        return int(v)


class NoneInt(str):
    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield empty_to_none


class Template(BaseModel):
    Route: Optional[str]
    DeliveryMethod: str
    PlaceOfLoad: str
    PlaceOfUnload: str
    RouteDeparture: Optional[str]
    DepartureDays: str
    ForwardingAgent: Optional[str]
    LeadTime: int
    LeadTimeOffset: Optional[NoneInt]
    TransportationEquipment: Optional[str]
    DaysToDeadline: Optional[NoneInt]
    DeadLineHours: Optional[NoneInt]
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


    @validator('DeliveryMethod')
    def delivery_method_validation(cls, v):
        if not all([c.isdigit() for c in list(str(v))]):
            raise ValueError('Invalid delivery method')

        return str(v)

    @validator('DepartureDays')
    def departure_days_validation(cls, v):
        if not all([c for c in v if list(str(c)) in ['0','1']]):
            raise ValueError(f'Only "0" and "1" allowed')

        if not len(list(str(v))) == 7:
            raise ValueError(f'All 7 days must be defined')

        return str(v)