from xml.etree import ElementTree

from markdown.treeprocessors import Treeprocessor


class StandaloneFigureProcessor(Treeprocessor):
    def run(self, root: ElementTree.Element):
        number = 0

        for element in root.iter():
            if element.tag != "p":
                continue

            children = [child for child in element]
            if len(children) != 1:
                continue

            if children[0].tag != "img":
                continue

            number += 1
            element.tag = "figure"

            img: ElementTree.Element = children[0]
            alt = img.attrib.get("alt", "")
            if alt:
                caption = ElementTree.Element("figcaption")
                caption.text = f"Figure {number}: {alt}"
                element.attrib["id"] = f"format{number}"
                element.append(caption)
