import xml.etree.ElementTree as et
def stuff():
    root = et.Element("orgchart")
    presNode = et.SubElement(root, "president", name = "bob", salary = "200")
    vp = et.SubElement(presNode, "vp", name = "susan")
    vp.text = "marketing"

    ourTree = et.ElementTree(root)
    ourTree.write("output.xml")

if __name__ == "__main__":
    stuff()