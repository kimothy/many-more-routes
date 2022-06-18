from many_more_routes.construct import MakeCustomerExtension, MakeCustomerExtensionExtended, MakeRoute
from many_more_routes.construct import MakeSelection
from many_more_routes.construct import MakeDeparture
from many_more_routes.models import Template

from many_more_routes.io import load_excel
import pandas as pd


xl = load_excel('/Users/nnckten/Desktop/TEST_TEMPLATE.xlsx')

records = [Template(**record) for record in xl]
many_records = [record for record in records for _ in range(1000)]


route_df = pd.DataFrame([MakeRoute(record).dict() for record in many_records])
departure_df = pd.DataFrame([departure.dict() for record in many_records for departure in MakeDeparture(record)])
selection_df = pd.DataFrame([MakeSelection(record).dict() for record in many_records])
cugex_df = pd.DataFrame([cugex.dict() for record in many_records for cugex in MakeCustomerExtension(record)])
cugex_ex_df = pd.DataFrame([cugexex.dict() for record in many_records for cugexex in MakeCustomerExtensionExtended(record)])