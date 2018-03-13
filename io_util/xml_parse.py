import xml.etree.ElementTree as et

import logging
from xmljson import cobra
import json as json

logger = logging.getLogger(__name__)


def print_xml(xml):
    return print(et.dump(xml))

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

def parse_val_to_xml(value,type):

    if value is not None:

        out = None
        out_type = None

        if type == int:
            out = str(value)
            out_type = "int"
        elif type in ["float", "f"]:
            out = float(value)
        elif type == bool:
            if value in ["False","F","FALSE"]:
                out="False"
            else:
                out = "True"
            out_type = "bool"

        elif type == str:
            out = value
            out_type = "str"
        else:
            out = "None"
            out_type = None
    else:
        out = "None"
        out_type = None

    return out, out_type

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

def dict_to_xml(dict_data, root_name = "root"):


    new_root = et.Element(root_name)
    new_tree = et.ElementTree(new_root)

    def internal_iter(dict_data,parent):
        print(dict_data)
        for key, item in dict_data.items():

            if isinstance(item,dict):
                new_node = et.Element(key)
                parent.append(new_node)
                internal_iter(item, new_node)
            elif isinstance(item,list):
                for child in item:
                    new_node = et.Element(key)
                    parent.append(new_node)
                    internal_iter(child, new_node)
            else:
                new_node = et.Element(key)
                new_node.text, data_type = parse_val_to_xml(dict_data[key],type(dict_data[key]))
                if data_type:
                    new_node.set("data_type",data_type)

                parent.append(new_node)

        return parent

    internal_iter(dict_data, new_root)

    return new_tree

def xml_to_json(xml):

    json_data = cobra.data(xml)

    json_data = json.dumps(json_data)

    print(json_data)
    return json_data

def dict_to_json(dict, child_levels = None):

    if child_levels:
        set_child_nodes(dict, child_levels)

  #  json_new = json.dumps(dict)
    json_new = dict

        #TODO

    return json_new

def json_to_xml(json_data):

    xml = cobra.etree(json_data)


    return xml

def set_child_nodes(dict_data,level_keys,level=0):

    if not isinstance(dict_data, list):
        dict_data = [dict_data]


    for item in dict_data:
        logging.debug("Item: " + str(item))
        for key in item.keys():
            logger.debug("Key: " + str(key))
            if key in level_keys:
                set_child_nodes(item[key], level_keys, level=level + 1)
                item["children"] = item[key]
                del item[key]

    return dict_data

def rename_child_nodes(dict_data,level_keys,level=0):

    if not isinstance(dict_data, list):
        dict_data = [dict_data]


    for item in dict_data:
        logging.debug("Item: " + str(item))
        for key in item.keys():

            logger.debug("Key: " + str(key))
            if key in ["children","child"]:
                rename_child_nodes(item[key], level_keys, level=level + 1)
                item[level_keys[level]] = item[key]
                del item["children"]

    return dict_data




