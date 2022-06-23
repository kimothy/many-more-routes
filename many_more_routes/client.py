import typer

from typing import Optional
from typing import List

from pathlib import Path

from . construct import MakeRoute
from . construct import MakeDeparture
from . construct import MakeSelection
from . construct import MakeCustomerExtension
from . construct import MakeCustomerExtensionExtended

from . ducks import OutputRecord
from . models import Template

from . io import load_excel
from . io import save_excel
from . io import save_template

from . sequence import generator

app = typer.Typer()


@app.command()
def template(file_path: Path):
    save_template(Template, file_path) #ignore mypy error here

@app.command()
def generate(in_file: Path, out_file: Path, seed: Optional[str] = None):
    if seed:
        routegen = generator(seed)

    records = map(lambda x: Template(**x), load_excel(in_file))

    results: List[OutputRecord] = []
    for index, record in enumerate(records, 2):
        if seed and not record.ROUT:
            record.ROUT = next(routegen)

        results.append(record)
        results.append(MakeRoute(record))
        
        for departure in MakeDeparture(record):
            results.append(departure)

        results.append(MakeSelection(record))

        for cusex in MakeCustomerExtension(record):
            results.append(cusex)

        for cusexex in MakeCustomerExtensionExtended(record):
            results.append(cusexex)

    save_excel(results, out_file)


if __name__ == '__main__':
    app()
