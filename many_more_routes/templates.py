# -*- coding: utf-8 -*-
"""
template.py

Part of Route Configuration Program
Use in conjunction with template files .xlsx with sheet name TEMPLATE_V2

Based on the template SmartData tool excel sheets are created to be
uploaded into Infor M3 using the API's.

This files handles the loading of the template file, and the creation
for DRS005, DRS006 and DRS011 excel sheets for use with SmartData tool.

Author: Kim Timothy Engh
Maintainer: Kim Timothy Engh
Copyright: 2022, Kim Timothy Engh
Licence: GPL v3

Created for the More program template
"""

import pandas as pd
from . import sequence
from typing import Optional, List, Union
import datetime


class Template(pd.DataFrame):
    '''
    Template object that represents the template file
    '''
    self: pd.DataFrame

    COLUMNS = {
        'Route': object,
        'PlaceOfLoad': str,
        'PlaceOfUnload': str,
        'DeliveryMethod': str,
        'RouteDeparture': object,
        'DepartureDays': str,
        'LeadTime': 'int8',
        'LeadTimeOffset': 'int8',
        'ForwardingAgent': str,
        'TransportationEquipment': str,
        'DaysToDeadline': 'int8',
        'DeadlineHours': 'int8',
        'DeadlineMinutes': 'int8',
        'PickCutOffDays': 'int8',
        'PickCutOffTimeHours': 'int8',
        'PickCutOffTimeMinutes': 'int8',
        'StipulatedInternalLeadTimeHours': 'int8',
        'StipulatedInternalLeadTimeDays': 'int8',
        'StipulatedInternalLeadTimeMinutes': 'int8',
        'ForwardersArrivalLeadTimeDays': 'int8',
        'ForwardersArrivalLeadTimeHours': 'int8',
        'ForwardersArrivalLeadTimeMinutes': 'int8',
        'TimeOfDepartureHours': 'int8',
        'TimeOfDepartureMinutes': 'int8',
        'TimeOfArrivalHoursLocalTime': 'int8',
        'TimeOfArrivalMinutesLocalTime': 'int8',
        'RouteResponsible': str,
        'DepartureResponsible': str,
        'CustomsDeclaration': int,
        'AvoidConfirmedDeliveryOnWeekends': int,
        'CreateSmartSheets': int,
        'Comment': object
    }

Template                  = NewType('Template, pd.DateFrame')
InvalidTemplate           = NewType('InvalidTemplate, pd.DateFrame')
Routes                    = NewType('Routes', pd.DataFrame)
Departures                = NewType('Departures', pd.DataFrame)
Selection                 = NewType('Selection', pd.DataFrame)
CustomerExtension         = NewType('CustomerExtension', pd.DataFrame)
CustomerExtensionExtended = NewType('CustomerExtensionExtended', pd.DataFrame)


def load_template(template: Union[str, pd.DataFrame]) -> Template:
    '''
    Takes a path or a dataframe and returns a dataframe of type Template.
    '''

    if isinstance(template, str):
        template = Template(
            pd.read_excel(
                template,
                dtype=object,
                sheet_name='TEMPLATE_V3'
                )
            )
    elif isinstance(template, pd.DataFrame):
        template = Template(template)

        template.dropna(axis='index', subset=['PlaceOfLoad'], inplace=True)
        template.astype(template.COLUMNS, errors='ignore')

        for column, dtype in template.COLUMNS.items():
            template[column] = template[column].astype(dtype, errors='ignore')

        template['PlaceOfUnload'] = template.apply(
            lambda x: x['PlaceOfUnload'].split(','), axis=1
        )

        template = template.explode('PlaceOfUnload', ignore_index=True)
        template = template[template['CreateSmartSheets'] == True]

    else:
        raise TypeError("load_template requires a df with correct set-up or a path to a template file")


    return template


def assign_routes(routes: pd.array, seed: Optional[str] = None, overwrite: bool = True) -> pd.array:
    '''
    Assigns route ids. Depending on parameters the sequence will differ:
    routes: An array of routes. Even if routes are not assigned this should be given.
    seed: If not given, the function will use the highest number in the route array to
    determine the seed, and then assign new routes to the ones that are blanc.
    overwrite: As if no routes id's are assigned. Based on seed new routes are assigned.
    '''
    if overwrite:
        return pd.array(list(sequence.generator(seed, len(routes))))

    if not seed: seed = max(routes[routes.notna()]) if len(routes[routes.notna()]) > 0 else None

    missingRoutes = routes[routes.isna()]
    rangeGenerator = sequence.generator(seed, len(missingRoutes))
    missingRoutes = missingRoutes.apply(lambda x: next(rangeGenerator))

    routes.update(missingRoutes)
    return routes



def make_route_table(template: Template) -> Routes:
    '''
    Creates a route dataframe based on a Template object
    '''

    routes = Routes()
    routes['ROUT'] = template['Route']
    routes['RUTP'] = 6
    routes['TX40'] = template['PlaceOfLoad'].astype('str')\
        + '_' + template['PlaceOfUnload'].astype('str')\
        + '_' + template['DeliveryMethod'].astype('str')
    routes['TX15'] = routes['TX40']
    routes['RESP'] = template['RouteResponsible']
    routes['SDES'] = template['PlaceOfLoad']
    routes['EDES'] = ''
    routes['SILD'] = ''
    routes['SILH'] = ''
    routes['SILM'] = ''
    routes['DLMC'] = 1
    routes['DLAC'] = 1
    routes['ACNC'] = ''
    routes['MARE'] = ''
    routes['MALP'] = ''
    routes['MACA'] = ''
    routes['FWNO'] = ''
    routes['TRCA'] = ''
    routes['MODL'] = ''
    routes['TSID'] = template['PlaceOfUnload']
    routes['DIST'] = ''
    routes['LOBL'] = ''
    routes['LODO'] = ''

    return routes



def calc_departures(departureDays: str, leadTime: int) -> List[str]:
    '''
    Takes the template and creates a set of route departures that avoids arrival on weekends
    '''

    departureArray = [
        ['0'] * 7,  # index 0, lead time bias of 0 days
        ['0'] * 7,  # index 1, lead time bias of 1 day
        ['0'] * 7,  # index 2, lead time bias of 2 days
        ['0'] * 7   # index 3, lead time bias of 0 days (overflow)
    ]

    departures = []

    for n, departureDay in enumerate(departureDays):
        arrivalDay = (n + leadTime) % 7

        if departureDays[n] == '1':
            if arrivalDay <= 4 and (n + leadTime % 7) < 6:
                departureArray[3][n] = '1'
            
            elif arrivalDay <= 4:
                departureArray[0][n] = '1'

            elif arrivalDay == 5:
                departureArray[2][n] = '1'

            elif arrivalDay == 6:
                departureArray[1][n] = '1'

    for n, departureList in enumerate(departureArray):
        if '1' in departureList:
            departures.append(''.join(departureList))

    return sorted(departures, reverse=True)

      
def recalculate_lead_time(departureDays: str, leadTime: int) -> int:
    '''
    Takes the departure days and lead time, selects the first
    departure days and caluclates the arrival day, if on a weekday
    leadTime is returned, if on a Sunday, leadTime + 1, if on a
    Saturday leadTime + 2. ValueError if no departure days.
    '''

    arrivalDay = (departureDays.index('1') + leadTime) % 7

    if arrivalDay <= 4:
        return leadTime

    elif arrivalDay == 5:
        return leadTime + 2

    elif arrivalDay == 6:
        return leadTime + 1


def calc_route_departure(departureDays: str, leadTime: int) -> int:
    '''
    Takes the departure days and lead time, selects the first
    departure days and caluclates the arrival day, if on a weekday
    leadTime is returned, if on a Sunday, leadTime + 1, if on a
    Saturday leadTime + 2. ValueError if no departure days.
    '''

    departureDay = departureDays.index('1')
    arrivalDay = (departureDays.index('1') + leadTime) % 7

    if arrivalDay <= 4 and (departureDay + leadTime % 7) < 6:
        return '1'
    
    elif arrivalDay <= 4:
        return '4'

    elif arrivalDay == 5:
        return '2'

    elif arrivalDay == 6:
        return '3'
    

def make_departure_table(template: Template) -> Departures:
    '''
    Assigns route depatures to avoid weekends
    if skip_empty is true then only departues with at least one departure day will
    be returned. If false, three route departures will be returned even if there
    are no departure days for the route departure. One for lead time bias 0, 1 & 2.
    '''

    template = template.copy()

    template['DepartureDays'] = template.apply(
        lambda x: calc_departures(x['DepartureDays'], x['LeadTime'])\
            if x['AvoidConfirmedDeliveryOnWeekends']\
            else x['DepartureDays'],
        axis=1
    )


    template = template.explode(
        'DepartureDays',
        ignore_index=True
    )

    template['RouteDeparture'] = template.apply(
        lambda x: calc_route_departure(x['DepartureDays'], x['LeadTime'])\
        if pd.isna(x['RouteDeparture'])\
        else x['RouteDeparture'],
        axis=1
    )
    
    template['LeadTime'] = template.apply(
        lambda x: recalculate_lead_time(x['DepartureDays'], x['LeadTime'])\
        if x['AvoidConfirmedDeliveryOnWeekends']\
        else x['LeadTime'],
        axis=1
    )

    template['LeadTime'] = template.apply(
        lambda x: x['LeadTime']\
        if pd.isna(x['LeadTimeOffset'])\
        else x['LeadTimeOffset'],
        axis=1
    )

    
    departures = Departures()
    departures['WWROUT'] = template['Route']
    departures['WWRODN'] = template['RouteDeparture']
    departures['WRRESP'] = template['DepartureResponsible']
    departures['WRFWNO'] = template['ForwardingAgent']
    departures['WRTRCA'] = template['TransportationEquipment']
    departures['WRMODL'] = template['DeliveryMethod']
    departures['WETSID'] = ''
    departures['WRLILD'] = template['DaysToDeadline']
    departures['WRSILD'] = template['StipulatedInternalLeadTimeDays']
    departures['WRLILH'] = template['DeadlineHours']
    departures['WRLILM'] = template['DeadlineMinutes']
    departures['WRSILH'] = template['StipulatedInternalLeadTimeHours']
    departures['WRSILM'] = template['StipulatedInternalLeadTimeMinutes']
    departures['WEFWLD'] = template['ForwardersArrivalLeadTimeDays']
    departures['WEFWLH'] = template['ForwardersArrivalLeadTimeHours']
    departures['WEFWLM'] = template['ForwardersArrivalLeadTimeMinutes']
    departures['WRDDOW'] = template['DepartureDays']
    departures['WRDETH'] = template['TimeOfDepartureHours']
    departures['WRDETM'] = template['TimeOfDepartureMinutes']
    departures['WRVFDT'] = datetime.datetime.now().strftime('%y%m%d')
    departures['WRVTDT'] = ''
    departures['WRARDY'] = template['LeadTime']
    departures['WRARHH'] = template['TimeOfArrivalHoursLocalTime']
    departures['WRARMM'] = template['TimeOfArrivalMinutesLocalTime']

    return departures


def make_selection_table(template: Template) -> Selection:
    '''
    Makes the DRS011 selection table based on the template
    '''
    selection = Selection()

    LOLD = template.apply(
        lambda x: x['LeadTime']\
        if x['LeadTimeOffset'] > 0\
        else '',
        axis=1
    )

    selection['WWEDES'] = template['PlaceOfLoad']
    selection['WWPREX'] = ' 6'  # with preceeding space
    selection['WWOBV1'] = template['PlaceOfUnload']
    selection['WWOBV2'] = template['DeliveryMethod']
    selection['WWOBV3'] = ''
    selection['WWOBV4'] = ''
    selection['WEROUT'] = template['Route']
    selection['WERODN'] = template['RouteDeparture']
    selection['WESEFB'] = '4'
    selection['WESELP'] = ''
    selection['WEDDOW'] = '1111100'
    selection['WEFWNO'] = ''
    selection['WETRCA'] = ''
    selection['WERFID'] = ''
    selection['WEPAL1'] = ''
    selection['WEPRRO'] = ''
    selection['WFLOLD'] = LOLD
    selection['WFLOLH'] = ''
    selection['WFLOLM'] = ''

    return selection


def make_customer_extension(template: Template) -> CustomerExtension:

    customer_extension = CustomerExtension(
        columns=[
            'FILE',
            'PK01',
            'PK02',
            'PK03',
            'PK04',
            'PK05',
            'PK06',
            'PK07',
            'PK08',
            'A030',
            'A130',
            'A230',
            'A330',
            'A430',
            'A530',
            'A630',
            'A730',
            'A830',
            'A930',
            'N096',
            'N196',
            'N296',
            'N396',
            'N496',
            'N596',
            'N696',
            'N796',
            'N896',
            'N996',
            'MIGR',
            'A121',
        ]
    )

    droudi = template.query('(PickCutOffDays or PickCutOffDays or PickCutOffTimeMinutes)')[['Route', 'PickCutOffDays', 'PickCutOffTimeHours', 'PickCutOffTimeMinutes']]
    customer_extension_droudi = customer_extension.copy()
    customer_extension_droudi['PK01'] = droudi['Route']
    customer_extension_droudi['N096'] = droudi['PickCutOffDays']
    customer_extension_droudi['N196'] = droudi['PickCutOffTimeHours']
    customer_extension_droudi['N296'] = droudi['PickCutOffTimeMinutes']
    customer_extension_droudi['FILE'] = 'DROUDI'

    droute = template.query('CustomsDeclaration == 1')[['Route']]
    customer_extension_droute = customer_extension.copy()
    customer_extension_droute['PK01'] = droute['Route']
    customer_extension_droute['FILE'] = 'DROUTE'

    customer_extension = pd.concat([customer_extension, customer_extension_droudi, customer_extension_droute])

    return customer_extension.reset_index().drop(columns=['index'])
    

def make_customer_extension_extended(template: Template) -> CustomerExtensionExtended:

    customer_extension_extended = CustomerExtensionExtended(
        columns=[
            'FILE',
            'PK01',
            'PK02',
            'PK03',
            'PK04',
            'PK05',
            'PK06',
            'PK07',
            'PK08',
            'CHB1',
            'CHB2',
            'CHB3',
            'CHB4',
            'CHB5',
            'CHB6',
            'CHB7',
            'CHB8',
            'CHB9',
            'DAT1',
            'DAT2',
            'DAT3',
            'DAT4',
            'DAT5',
            'DAT6',
            'DAT7',
            'DAT8',
            'DAT9',
            'A122',
            'A256'
        ]
    )

    droute = template.query('CustomsDeclaration == 1')[['Route', 'CustomsDeclaration']]
    customer_extension_extended_droute = customer_extension_extended.copy()
    customer_extension_extended_droute['PK01'] = droute['Route']
    customer_extension_extended_droute['CHB1'] = droute['CustomsDeclaration']
    customer_extension_extended_droute['FILE'] = 'DROUTE'

    customer_extension_extended = pd.concat([customer_extension_extended, customer_extension_extended_droute])

    return customer_extension_extended.reset_index().drop(columns=['index'])