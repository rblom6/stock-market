import xml.etree.ElementTree as et
import pkg_resources

class TickerTree():

    def __init__(self, filename):
        self.filename = filename
        self.tree = {}

    def read_tree(self):
        """This function will read in the S&P 500 tickers xml file into a dictionary.
        The keys to the dictionary will be the sectors found in the xml file and the value of each key will be another dictionary.
        This dictionary's keys will be the industries that make up that particular sector.
        The value of each key will be a list of the xml elements in the original tree for the stocks
        that make up that industry.
        """
        fin = open(pkg_resources.resource_filename("stockSamples26", self.filename))
        text = fin.read().replace("&", "&amp;")
        fin.close()
        self.parse(text)

    def parse(self, text):
        #Parse input text and construct the dictionary
        root = et.fromstring(text)
        for child in root:
            attributes = child.attrib
            sector = attributes["sector"]
            industry = attributes["industry"]

            #sector not in finalDict
            if self.tree.get(sector, None) == None:
                self.tree[sector] = {industry: [child]}
            #sector in finalDict
            else:
                #industry not in sector dictionary
                if self.tree[sector].get(industry, None) == None:
                    self.tree[sector].update({industry: [child]})
                #industry in sector dictionary
                else:
                    self.tree[sector][industry].append(child)

    
    def export_tree(self, filename="output.xml"):
        """Writes that tree to a file called "output.xml"

        Parameters:
        filename: string - the filename of the output file

        Return: None
        """
        root = et.Element("SP500")

        for sector, industries in self.xml_dict.items():
            sectorNode = et.SubElement(root, "Sector", name = sector)
            for industry, elements in self.xml_dict[sector].items():
                industryNode = et.SubElement(sectorNode, "Industry", name = industry)
                for element in elements:
                    elementNode = et.SubElement(industryNode, "Stock", ticker = element.attrib["ticker"])
                    elementNode.text = element.attrib["name"]

        ourTree = et.ElementTree(root)
        ourTree.write(filename)


    def get_industry_tickers(self, sector, industry):
        """Returns a list of tickers of the stocks that belong
        to a sector and industry.

        Parameters:
        sector: sector that the industry belongs to
        industry: industry name

        Return: list of tickers that belong to the industry
        """

        tickers = self.tree[sector][industry]
        result = []
        for ticker in tickers:
            result.append(ticker.attrib["ticker"])
        return result

