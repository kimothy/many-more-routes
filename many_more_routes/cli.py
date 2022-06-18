from argparse import ArgumentParser

from typing import List

from . construct import MakeRoute
from . construct import MakeDeparture
from . construct import MakeSelection
from . construct import MakeCustomerExtension
from . construct import MakeCustomerExtensionExtended

from . models import OutputRecord
from . models import Template

from . io import load_excel
from . io import write_excel

from . sequence import generator


def main(infile: str, outfile: str, seed: str):
    ''' Main program routine '''
    routegen = generator(seed)

    records = map(lambda x: Template(**x), load_excel(infile))

    results: List[OutputRecord] = []
    for record in records:
        if not record.Route:
            record.Route = next(routegen)

        results.append(record)
        results.append(MakeRoute(record))
        
        for departure in MakeDeparture(record):
            results.append(departure)

        results.append(MakeSelection(record))

        for cusex in MakeCustomerExtension(record):
            results.append(cusex)

        for cusexex in MakeCustomerExtensionExtended(record):
            results.append(cusexex)

    write_excel(results, outfile)


def cli():
    ''' The main command line client program, collects
    arguments and starts the main routines ''' 
    parser = ArgumentParser(
        prog='many-more-routes-cli',
        description='Route Generation Program',
        epilog='The epilog, update me!'
    )

    parser.add_argument(
        'infile',
        type=str,
        help='The input file'
    )

    parser.add_argument(
        'outfile',
        type=str,
        help='The output file'
    )

    parser.add_argument(
        '-s', '--seed',
        type=str,
        help='The routes seed for assigning routes where not set.'
    )

    args = parser.parse_args()
    main(args.infile, args.outfile, args.seed)


if __name__ == '__main__':
    cli()