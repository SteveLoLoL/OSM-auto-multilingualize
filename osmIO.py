import xml.etree.ElementTree as ET
import pyperclip
import re
import xml.dom.minidom


def level0_to_xml(data):
    root = ET.Element("osm")
    elements = data.split('\r\n\r\n')
    for item in elements:
        if item.startswith("node"):
            title, *tags = item.split('\r\n')
            _, node_id, lat, lon, *notes = title.split()
            notes = ' '.join(notes)
            node_id = node_id.strip(":")
            lat = lat.replace(",", "")
            lat, lon = map(float, [lat, lon])
            node = ET.SubElement(root, "node", id=node_id, lat=str(lat), lon=str(lon), notes=notes)
            for tag in tags:
                if tag == '':
                    break
                else:
                    k, v = tag.split("=", 1)
                    ET.SubElement(node, "tag", k=k.strip(), v=v.strip())

        elif item.startswith("way"):
            title, *rest = item.split('\r\n')
            _, way_id, *notes = title.split()
            notes = ' '.join(notes)
            way_id = way_id.strip()
            way = ET.SubElement(root, "way", id=way_id, notes=notes)
            for part in rest:
                if part.startswith("  nd"):
                    nd_ref = part.split()[1].strip()
                    ET.SubElement(way, "nd", ref=nd_ref)
                elif part == '':
                    break
                else:
                    k, v = part.split("=", 1)
                    ET.SubElement(way, "tag", k=k.strip(), v=v.strip())

        elif item.startswith("relation"):
            title, *rest = item.split('\r\n')
            _, relation_id, *notes = title.split()
            notes = ' '.join(notes)
            relation_id = relation_id.strip()
            relation = ET.SubElement(root, "relation", id=relation_id, notes=notes)
            for part in rest:
                if part.startswith("  nd") or part.startswith("  wy") or part.startswith("  rel"):
                    part = re.sub(r'  #', ' # #', part)
                    element, ref, role, *notes = part.split()
                    if role == "#":
                        role = ""
                    notes = ' '.join(notes)
                    ET.SubElement(relation, "member", type=element, ref=ref, role=role, notes=notes)
                elif part == '':
                    break
                else:
                    k, v = part.split("=", 1)
                    ET.SubElement(relation, "tag", k=k.strip(), v=v.strip())

    return root


def xml_to_level0(root):
    data = []

    for elem in root:
        if elem.tag == "node":
            node_id = elem.get("id")
            lat = elem.get("lat")
            lon = elem.get("lon")
            data.append(f"node {node_id}: {lat}, {lon} {elem.get('notes')}")
            for tag in elem.findall("tag"):
                data.append(f"  {tag.get('k')} = {tag.get('v')}")

        elif elem.tag == "way":
            way_id = elem.get("id")
            data.append(f"way {way_id} {elem.get('notes')}")
            for tag in elem.findall("tag"):
                data.append(f"  {tag.get('k')} = {tag.get('v')}")
            for nd in elem.findall("nd"):
                data.append(f"  nd {nd.get('ref')}")

        elif elem.tag == "relation":
            relation_id = elem.get("id")
            data.append(f"relation {relation_id} {elem.get('notes')}")
            for tag in elem.findall("tag"):
                data.append(f"  {tag.get('k')} = {tag.get('v')}")
            for member in elem.findall("member"):
                role = member.get("role")
                ref = member.get("ref")
                type_ = member.get("type")
                data.append(f"  {type_} {ref} {role} {member.get('notes')}")
        data.append("")

    return data


if __name__ == "__main__":
    # Example of converting from clipboard level0 to XML and back to level0
    clipboard_text = pyperclip.paste()

    xml_data = level0_to_xml(clipboard_text)

    temp = xml.dom.minidom.parseString(ET.tostring(xml_data, encoding='unicode'))
    print("XML:")
    print(temp.toprettyxml())

    level0 = xml_to_level0(xml_data)

    pyperclip.copy("\r\n".join(level0))
    print("level0:")
    for line in level0:
        print(line)
