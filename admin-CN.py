from xml.etree.ElementTree import ElementTree,Element
import xml.dom
import opencc
from xpinyin import Pinyin

converter = opencc.OpenCC('s2t')

def read_xml(in_path):
    tree = ElementTree()
    tree.parse(in_path)
    return tree

def write_xml(tree, out_path):
    tree.write(out_path, encoding="utf-8", xml_declaration=True)

def pinyin(han):
    p = Pinyin()
    py = p.get_pinyin(han, '')
    return py.capitalize()

if __name__ == "__main__":
    ################ Read XML File  ##########
    tree = read_xml("places.osm")

    root = tree.getroot()

    nodes = root.findall('node')
    for node in nodes:
        tags = node.findall('tag')
        name = 0
        en = 0
        zh = 0
        hant = 0
        if tags != []:
            for tag in tags:
                if tag.attrib["k"] == "name":
                    dft = tag.get("v")
                    name = 1
                    print(dft)
                if tag.attrib["k"] == "name:en":
                    en = 1
                if tag.attrib["k"] == "name:zh":
                    zh = 1
                if tag.attrib["k"] == "name:zh-Hant":
                    hant = 1
            if name == 1:
                if en == 0:
                    if dft.endswith("县") or dft.endswith("市") or dft.endswith("区") or dft.endswith("乡") or dft.endswith("镇") or dft.endswith("村"):
                        node.append(Element("tag", {"k": "name:en", "v": pinyin(dft[:-1])}))
                    elif dft.endswith("街道") or dft.endswith("社区"):
                        node.append(Element("tag", {"k": "name:en", "v": pinyin(dft[:-2])}))
                    #else:
                        #node.append(Element("tag", {"k": "name:en", "v": pinyin(dft)}))
                if zh == 0:
                    node.append(Element("tag", {"k": "name:zh", "v": dft}))
                if hant == 0:
                    node.append(Element("tag", {"k": "name:zh-Hant", "v": converter.convert(dft)}))

    relations = root.findall('relation')
    for relation in relations:
        tags = relation.findall('tag')
        name = 0
        en = 0
        zh = 0
        hant = 0
        if tags != []:
            for tag in tags:
                if tag.attrib["k"] == "name":
                    dft = tag.get("v")
                    name = 1
                    print(dft)
                if tag.attrib["k"] == "name:en":
                    en = 1
                if tag.attrib["k"] == "name:zh":
                    zh = 1
                if tag.attrib["k"] == "name:zh-Hant":
                    hant = 1
            if name == 1:
                if en == 0:
                    if dft.endswith("县"):
                        relation.append(Element("tag", {"k": "name:en", "v": pinyin(dft[:-1]) + " County"}))
                    elif dft.endswith("市"):
                        relation.append(Element("tag", {"k": "name:en", "v": pinyin(dft[:-1]) + " City"}))
                    elif dft.endswith("区"):
                        relation.append(Element("tag", {"k": "name:en", "v": pinyin(dft[:-1]) + " District"}))
                    elif dft.endswith("乡"):
                        relation.append(Element("tag", {"k": "name:en", "v": pinyin(dft[:-1]) + " Township"}))
                    elif dft.endswith("镇"):
                        relation.append(Element("tag", {"k": "name:en", "v": pinyin(dft[:-1]) + " Town"}))
                    elif dft.endswith("村"):
                        relation.append(Element("tag", {"k": "name:en", "v": pinyin(dft[:-1]) + " Village"}))
                    elif dft.endswith("街道"):
                        relation.append(Element("tag", {"k": "name:en", "v": pinyin(dft[:-2])} + " Sub-district"))
                    elif dft.endswith("社区"):
                        relation.append(Element("tag", {"k": "name:en", "v": pinyin(dft[:-2])} + " Community"))
                if zh == 0:
                    relation.append(Element("tag", {"k": "name:zh", "v": dft}))
                if hant == 0:
                    relation.append(Element("tag", {"k": "name:zh-Hant", "v": converter.convert(dft)}))

    ################    Output XML    ##########
    write_xml(tree, "./Multilingualized.osm")
