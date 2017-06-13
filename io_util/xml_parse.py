import xml.etree.ElementTree as et
import logging

logger = logging.getLogger(__name__)

def parse_val(value,type):

    if value is not None:
        out = None
        if type in ["int", "i"]:
            out = int(value)
        elif type in ["float", "f"]:
            out = float(value)
        elif type in ["bool", "b"]:
            if value in ["False","F","FALSE"]:
                out=False
            else:
                out = bool(value)

        elif type in ["str", "s"]:
            out = str(value)
        elif type in ["tuple_int", "ti"]:
            out = tuple([int(x) for x in value.split(",")])
        elif type in ["list_int", "li"]:
            out = [int(x) for x in value.split(",")]
        else:
            out = str(value)
    else:
        out = None

    return out


def xml_to_dict(xml):

    def internal_iter(xml, accum):

        if xml is None:
            return accum

        if xml.getchildren():
            accum[xml.tag] = {}
            for child in xml.getchildren():
                result = internal_iter(child, {})
                if child.tag in accum[xml.tag]:
                    if not isinstance(accum[xml.tag][child.tag], list):
                        accum[xml.tag][child.tag] = [
                            accum[xml.tag][child.tag]
                        ]
                    accum[xml.tag][child.tag].append(result[child.tag])
                else:
                    accum[xml.tag].update(result)
        else:

            if "data_type" in xml.attrib:
                accum[xml.tag] = parse_val(xml.text,xml.attrib["data_type"])
            else:
                accum[xml.tag] = xml.text

        return accum

    return internal_iter(xml, {})

