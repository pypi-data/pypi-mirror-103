import dominate

from collections import OrderedDict

from dominate.tags import *
from contextlib import suppress
from inflection import humanize, titleize

# Create your services here.

TEXT_GENERAL = 'General'


def json_arrays_destroy(sources):
    """
    Transform json arrays to dictionaries in object
    :param sources:
    :return:
    """
    for element, value in sources.copy().items():
        # If element is dict inspect each key value and clear useless keys
        if isinstance(sources[element], dict):
            json_arrays_destroy(sources[element])

        # If element is list inspect each key value and clear useless keys
        if isinstance(sources[element], list):
            sources.pop(element, None)

    return sources


def json_arrays_to_dictionary(sources):
    """
    Transform json arrays to dictionaries in object
    :param sources:
    :return:
    """
    for element, value in sources.copy().items():
        # If element is int convert to string
        if isinstance(sources[element], int):
            sources[element] = str(sources[element])

        # If element is None convert to string
        if sources[element] is None:
            sources[element] = ""

        # If element is dict inspect each key value and clear useless keys
        if isinstance(sources[element], dict):
            json_arrays_to_dictionary(sources[element])

        # If element is list inspect each key value and clear useless keys
        if isinstance(sources[element], list):
            # Clear of empty objects
            sources[element] = [elementor for elementor in sources[element] if elementor]

            # Loop through each item and create a dictionary
            for index, elements in enumerate(sources[element]):
                indexing = index
                keying = f'{element}_{indexing + 1}'
                sources[keying] = elements

                # Format if integer
                if isinstance(elements, int):
                    sources[element][index] = str(elements)

                # Ignored else for clear viewing
                if not isinstance(elements, int):
                    json_arrays_to_dictionary(elements)

    return sources


def builder(sources, document, etable=None, erows=None):
    """
    Build report html by adding tables for sources data
    :param sources: Main sources for tables
    :param document: Main HTML document
    :param etable: Reference table
    :param erows: Reference row
    :return:
    """
    for element, value in sources.copy().items():
        titles = titleize(humanize(element))

        if etable and not isinstance(sources[element], list) and not erows:
            with etable:
                trow = tr()
                if not isinstance(value, dict):
                    trow.add(th(titles))
                    trow.add(td(value))
        elif erows:
            with erows:
                if element == value:
                    # Heading
                    erows.add(th(titles))
                else:
                    erows.add(td(value))
        elif not erows and not etable and isinstance(value, str):
            with document:
                with table(id=f'table_{element}', _class="clearfix").add(tbody()) as etable:
                    etable.add(div(_class="pointer"))
                    etable.add(h3(TEXT_GENERAL))  # Heading
                    xrow = tr()
                    xrow.add(th(titles))
                    xrow.add(td(value))

        # If element is dict inspect each key value and clear useless keys
        if isinstance(sources[element], dict):
            with document:
                # div(_class="pointer")
                h3(titles)
                with table(id=f'table_{element}', _class="clearfix").add(tbody()) as tables:
                    builder(sources[element], document, tables)

        # If element is list inspect each key value and clear useless keys
        if isinstance(sources[element], list):
            # How many elements this list has
            size = len(sources[element])

            with document:
                # Make a table
                with table(id=f'table_{element}', _class="clearfix",
                           style="page-break-inside: avoid; margin-top: 2rem;").add(tbody()) as tables:

                    # Add headings
                    with tr(id=f'row_heading_{element}_heading'):
                        columns = 1
                        with suppress(Exception):
                            columns = len(next(iter(sources[element])).keys())

                        with td(colspan=columns) as heading:
                            heading.add(h3(f'{titles} - {size}', _class="clearfix"))

                    # Get each element value
                    for index, elements in enumerate(sources[element]):
                        if isinstance(elements, dict):
                            sources[element][index] = OrderedDict(elements)

                        if index == 0:
                            headings = {}

                            for part in elements.keys():
                                headings.update({part: part})

                            # Add headings
                            with tr(id=f'row_heading_{element}_{index}') as r:
                                builder(headings, document, tables, r)

                        # Add rows
                        with tr(id=f'row_{element}_{index}') as rows:
                            builder(elements, document, tables, rows)

    return sources


def normalize(sources):
    """
    Normalize keys values to strings
    :param sources:
    :return:
    """
    for element, value in sources.copy().items():

        # If element is int convert to string
        if isinstance(sources[element], int):
            sources[element] = str(sources[element])

        # If element is None convert to string
        if sources[element] is None:
            sources[element] = ""

        # If element is dict inspect each key value and clear useless keys
        if isinstance(sources[element], dict):
            normalize(sources[element])

        # If element is list inspect each key value and clear useless keys
        if isinstance(sources[element], list):
            evaluting = []

            for index, elements in enumerate(sources[element]):
                if isinstance(elements, int) or isinstance(elements, str):
                    sources[element][index] = str(elements)
                    evaluting.append(str(elements))

                # Ignored else for clear viewing
                if type(elements) not in [int, str]:
                    normalize(elements)

    return sources


def json_to_html(sources, titled='Report', size=7):
    """
    Convert json to html
    :param sources:
    :param titled:
    :param size:
    :return:
    """

    # Normalizes json fields values
    preparing = normalize(sources)

    # Create HTML Document
    document = dominate.document(title=titled)

    with document.head:
        style(
            'table { page-break-inside:auto } tr { page-break-inside:avoid; page-break-after:auto } thead { display:table-header-group } tfoot { display:table-footer-group } '
            '.pointer { display: block; clear: both; page-break-after: always; } '
            '.clearfix { overflow: auto; clear: both } '
            '.clearfix::after { content: ""; clear: both; display: table; } '
            'body { margin: 0 ' + f'{size}rem;' + ' } '
                                                  'table { width: 100%; font-size: 0.8rem; } '
                                                  'th,td { border: 0.11rem solid black; } '
                                                  'table, th,td { border-collapse: collapse; padding: 0.25rem 1rem; text-align: left; margin: 0; } '
                                                  'tr:nth-child(even) { background-color: #cccccc61; } ')

    builder(preparing, document)

    return preparing, str(document)
