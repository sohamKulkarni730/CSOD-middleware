from typing import Dict, List, Any
from xml.etree import ElementTree
def data_parser(request_Body):
    application_type = request_Body.headers["Content-Type"]
    data = {}
    print("application Type ::::" + application_type)
    if("xml" in application_type ):
        data = XML_parser(request_Body)
    elif ("json" in application_type ):
        data =Json_parser(request_Body)

    return data

def XML_parser(request_Body):
    #getting root
    XML_Tree = ElementTree.fromstring(request_Body.content)

    i = 0
    j = 0
    family = {}
    child_Dict = {}
    for child in XML_Tree[4].getchildren():
        for childs in child.getchildren():
            child_Dict[i] = childs.text
            i = i + 1
        family[j] = child_Dict
        child_Dict = {}
        i = 0
        j = j + 1

    return family

def Json_parser(request_Body):
    return request_Body.json


