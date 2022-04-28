from . templates import Template
from . templates import load_template
from . templates import assign_routes
from . templates import make_route_table
from . templates import make_departure_table
from . templates import make_selection_table
from . templates import make_customer_extension
from . templates import make_customer_extension_extended
from . outputs import to_smart_format
from . outputs import export_many

from typing import Optional


def export_template_file_to_smartheet(file_name: str) -> None:
    template = load_template(file_name)
    export_template_dataframe_to_smartsheet(template)


def export_template_dataframe_to_smartsheet(template: Template, route_seed: Optional[str] = None) -> None:
    template['Route'] = assign_routes(template['Route'], overwrite=False, seed=None)

    route_table = make_route_table(template)
    departure_table = make_departure_table(template)
    selection_table = make_selection_table(template)
    customer_extension_table = make_customer_extension(template)
    customer_extension_extended_table = make_customer_extension_extended(template)

    export_many(
        [   template.fillna(''),
            to_smart_format(route_table.fillna('')),
            to_smart_format(departure_table.fillna('')),
            to_smart_format(selection_table.fillna('')),
            to_smart_format(customer_extension_table.fillna('')),
            to_smart_format(customer_extension_extended_table.fillna(''))
        ],
        [
            'TEMPLATE_V3',
            'API_DRS005MI_AddRoute',
            'MPD_DRS006_Create_CL',
            'MPD_DRS011_Create_CL',
            'API_CUSEXTMI_AddFieldValue',
            'API_CUSEXTMI_ChgFieldValueEx'
        ]
    )