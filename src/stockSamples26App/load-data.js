const sectorsAndIndustriesData = {
    Industrials: [
      "Industrial Conglomerates",
      "Diversified Commercial Services",
      "Electrical Components and Equipment",
      "Electrical Components & Equipment",
      "Aerospace & Defense",
      "Air Freight & Logistics",
      "Construction & Farm Machinery & Heavy Trucks",
      "Construction & Engineering",
      "Railroads",
      "Industrial Machinery",
      "Airlines",
      "Data Processing Services",
      "Building Products",
      "Heavy Electrical Equipment",
      "Industrial Materials",
      "Research & Consulting Services",
      "Environmental Services"
    ],
    "Health Care": [
      "Health Care Equipment & Services",
      "Pharmaceuticals",
      "Managed Health Care",
      "Biotechnology",
      "Health Care Distribution & Services",
      "Health Care Distributors & Services",
      "Health Care Facilities",
      "Health Care Supplies"
    ],
    "Consumer Discretionary": [
      "Apparel, Accessories & Luxury Goods",
      "Internet Retail",
      "Specialty Stores",
      "Computer & Electronics Retail",
      "Auto Parts & Equipment",
      "Broadcasting & Cable TV",
      "Hotels, Resorts & Cruise Lines",
      "Restaurants",
      "Construction",
      "General Merchandise Stores",
      "Automobile Manufacturers",
      "Publishing",
      "Apparel Retail",
      "Consumer Electronics",
      "Tires & Rubber",
      "Motorcycle Manufacturers",
      "Leisure Products",
      "Home Improvement Retail",
      "Advertising",
      "Homebuilding",
      "Department Stores",
      "Housewares & Specialties",
      "Household Appliances",
      "Casinos & Gaming"
    ],
    Financials: [
      "Property & Casualty Insurance",
      "Life & Health Insurance",
      "Consumer Finance",
      "REITs",
      "Diversified Financial Services",
      "Insurance Brokers",
      "Multi-line Insurance",
      "Banks",
      "Multi-Sector Holdings",
      "Real Estate Management & Development",
      "Retail REITs"
    ],
    "Information Technology": [
      "IT Consulting & Services",
      "Application Software",
      "Internet Software & Services",
      "Semiconductors",
      "Computer Hardware",
      "Semiconductor Equipment",
      "Systems Software",
      "Networking Equipment",
      "Telecommunications Equipment",
      "Electronic Equipment & Instruments",
      "Computer Storage & Peripherals"
    ],
    Utilities: [
      "Electric Utilities",
      "Gas Utilities",
      "Multi-Utilities & Unregulated Power"
    ],
    Materials: [
      "Industrial Gases",
      "Aluminum",
      "Diversified Metals & Mining",
      "Metal & Glass Containers",
      "Paper Packaging",
      "Fertilizers & Agricultural Chemicals",
      "Diversified Chemicals",
      "Specialty Chemicals",
      "Paper Products",
      "Gold",
      "Steel",
      "Construction Materials"
    ],
    "Consumer Staples": [
      "Tobacco",
      "Agricultural Products",
      "Personal Products",
      "Distillers & Vintners",
      "Packaged Foods & Meats",
      "Household Products",
      "Soft Drinks",
      "Hypermarkets & Super Centers",
      "Drug Retail",
      "Food Retail",
      "Brewers",
      "Food Distributors"
    ],
    Energy: [
      "Oil & Gas Exploration & Production",
      "Oil & Gas Equipment & Services",
      "Integrated Oil & Gas",
      "Oil & Gas Drilling",
      "Oil & Gas Refining & Marketing & Transportation"
    ],
    "Telecommunications Services": [
        "Integrated Telecommunication Services",
        "Wireless Telecommunications Services"
    ]
}

 
function buildOptgroup(name) {
  const optGroup = document.createElement('optgroup')
  optGroup.setAttribute('label', name)
  return optGroup
}

function buildIndustryHTMLString(industryName) {
  let htmlString = ''
  for(let industry of sectorsAndIndustriesData[industryName]) {
    htmlString += `<option value="${industry}"> ${industry} </option>`
  }
  return htmlString
}

function populateIndustryDropdown(sectorsAndIndustriesData) {
  const industrySelector = document.getElementById('industry-selector')
  for(let sectorName of Object.keys(sectorsAndIndustriesData)) {
    const sectorOptgroup = buildOptgroup(sectorName)
    sectorOptgroup.innerHTML += buildIndustryHTMLString(sectorName)
    industrySelector.appendChild(sectorOptgroup)
  }
}


async function main() {
  // configure pyodide
  let pyodide = await loadPyodide();
  pyodide.pyimport('SPProcessing')

  // populate industry dropdown
  pyodide.runPython(`
    import SPProcessing.TickerData.TickerData as TickerData
    print(TickerData)
    # tTree = TickerTree("SP_500.xml")

  `)
  // const sectorsAndIndustriesData = tTree.read_tree().get_data()
  populateIndustryDropdown(sectorsAndIndustriesData)

  // load tickerData
  const tickerData = pyodide.runPython(`
    import SPProcessing.TickerData.TickerData as TickerData
    # tickerData = TickerData("SP500_ind.csv")
    # tickerData.read_data()
    # return tickerData
    print(TickerData)
  `)

  console.log(pyodide.runPython(`
      import sys
      sys.version
  `));
};
main();

// industryTickers = tTree.get_industry_tickers(sector, industry)



// for ticker in industryTickers:
//     if ticker in tData.data:
//         try:
//             wAvgPrice = tData.vwap(ticker)
//             avgOpen = tData.calc_avg_open(ticker)
//         except:
//             print("One of your inputs caused an error.")
//             return
//         print([ticker, wAvgPrice, avgOpen])
