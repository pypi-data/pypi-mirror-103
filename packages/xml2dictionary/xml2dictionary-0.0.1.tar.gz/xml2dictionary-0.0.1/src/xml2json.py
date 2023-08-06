from xmltodict import parse as parser
from contextlib import suppress
from dicttoxml import dicttoxml


# Create your functions here.

def parse(xml):
    """
    Parse xml string to json
    :param xml: XML sources string
    :return:
    """
    with suppress(Exception):
        parsing = parser(xml)
        return parsing

    return {}


def clear_signs(sources, sign='@', shift='#text', scape='item'):
    """
    Clear sources from sign keys
    Shift key with value
    Scape key with main elements
    :param sources:
    :param sign:
    :param shift:
    :param scape:
    :return:
    """
    for element, value in sources.copy().items():
        if element.startswith(sign):
            sources.pop(element)
            continue

        # If element is dict inspect each key value and clear useless keys
        if isinstance(sources[element], dict):
            clear_signs(sources[element], sign)

        # If element is list inspect each key value and clear useless keys
        if isinstance(sources[element], list):
            for elements in sources[element]:
                clear_signs(elements, sign)

        # If element value is a object with shift key use it as value
        with suppress(AttributeError):
            if sources[element] and shift in sources[element]:
                sources[element] = value.get(shift, '')

        # If element value is a empty object make it empty string or remove <<<
        if not sources[element]:
            sources.pop(element)
            continue

        # Skip if scape does not exists in element
        if scape not in sources[element] and element in sources:
            continue

        # If scape exists set as main element value , as array
        if scoped := sources[element][scape]:
            if isinstance(scoped, list):
                sources[element] = scoped

            if isinstance(scoped, dict):
                sources[element] = [scoped]

    return sources


def json_to_xml(sources):
    """
    Parse json to xml
    :param sources: Json sources
    :return:
    """
    parsing = dicttoxml(sources)
    return parsing


def xml2json(xml='', sign='@', shift='#text', scape='item'):
    """
    Parse xml to json
    :param xml: XML Source
    :param sign:
    :param shift:
    :param scape:
    :return:
    """
    parsed = parse(xml)

    with suppress(Exception):
        return clear_signs(parsed, sign, shift, scape)

    return parsed
