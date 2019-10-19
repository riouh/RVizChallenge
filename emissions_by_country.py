import requests
import csv


def extract_data():
    result = {'France': {}, 'Germany': {}}
    cookie = '_ga=GA1.2.824669195.1569879623; _hjid=fccc8d95-63ca-4b86-8245-bd5d8eee1f0c; _gid=GA1.2.1448953084.1571389879; _hjIncludedInSample=1; PHPSESSID=a7gqob62nsdhcvelp111ttk213; _hjDonePolls=323731; _hjMinimizedPolls=323731'
    urls = ['https://www.iea.org/api/stats/getFlatData.php?endYear=2018&country=GERMANY&series=ELECTRICITYANDHEAT&products=ELECTR&flows=EHCOAL%2CEHOIL%2CEHNATGAS%2CEHNUCLEAR%2CEHYDRO%2CEHBIOMASS%2CEHWASTE%2CEHSOLARTH%2CESOLARPV%2CEWIND%2CEHGEOTHERM%2CETIDE%2CEHOTHER',
            'https://www.iea.org/api/stats/getFlatData.php?endYear=2018&country=FRANCE&series=ELECTRICITYANDHEAT&products=ELECTR&flows=EHCOAL%2CEHOIL%2CEHNATGAS%2CEHNUCLEAR%2CEHYDRO%2CEHBIOMASS%2CEHWASTE%2CEHSOLARTH%2CESOLARPV%2CEWIND%2CEHGEOTHERM%2CETIDE%2CEHOTHER']
    for url in urls:
        r = requests.get(url, headers={'Authorization': cookie})
        data = r.json()
        for row in data:
            year = row['year']
            country = row['countryName']
            energy_type = row['flowLabel']
            value = row['value']
            if year in result[country].keys():
                result[country][year][energy_type] = value
            else:
                result[country][year] = {energy_type: value}
    return result


def csv_energy_mix_creation():
    iae_data = extract_data()
    csvData_fr, csvData_all = [['Year', 'Elec_Source', 'Value']], [['Year', 'Elec_Source', 'Value']]
    for year in iae_data['France'].keys():
        for type in iae_data['France'][year].keys():
            value = iae_data['France'][year][type]
            csvData_fr.append([year, type, value])
    for year in iae_data['Germany'].keys():
        for type in iae_data['Germany'][year].keys():
            value = iae_data['Germany'][year][type]
            csvData_all.append([year, type, value])
    with open('C:/Users/33640/Documents/UCL/Energy Data Analysis/VizChallenge/France_electricity_historic.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData_fr)
    with open('C:/Users/33640/Documents/UCL/Energy Data Analysis/VizChallenge/Germany_electricity_historic.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData_all)


def tsv_price_extraction():
    result = {'Germany': {}, 'France': {}}
    body_address = 'C:/Users/33640/Documents/UCL/Energy Data Analysis/VizChallenge/'
    addresses = ['nrg_pc_204_h.tsv', 'nrg_pc_204.tsv']
    for address in addresses:
        before_result = {}
        with open(body_address + address, 'r', newline='') as originFile:
            reader = csv.reader(originFile, delimiter='\t')
            l = list(reader)
        for year_S in l[0][1:]:
            y = int(year_S[:4])
            if y not in before_result.keys():
                before_result[y] = list()
                before_result[y].append(l[0].index(year_S))
            else:
                before_result[y].append(l[0].index(year_S))
        for elem in l[1:]:
            for code in ['4161901', '4161902', '4161903', '4161904', '4161905', '4161150', '4161050', '4161100', '4161200', '4161250']:
                if elem[0] == '6000    {} KWH X_TAX   EUR FR'.format(code):
                    for year in before_result.keys():
                        if year not in result['France'].keys():
                            result['France'][year] = list()
                        for i in before_result[year]:
                            result['France'][year].append(transfo(elem[i]))
                elif elem[0] == '6000    {} KWH X_TAX   EUR DE'.format(code):
                    for year in before_result.keys():
                        if year not in result['France'].keys():
                            result['Germany'][year] = list()
                        for i in before_result[year]:
                            result['Germany'][year].append(transfo(elem[i]))
    for country in result.keys():
        for year in result[country].keys():
            result[country][year] = mean_list(result[country][year])
    return result


def transfo(a):
    result = a.replace(" ","")
    try:
        return float(result)
    except:
        return None


def mean_list(l):
    c = 0
    denom = 0
    for i in l:
        if i is not None:
            c += i
            denom += 1
        else:
            continue
    try:
        result = round(c/denom, 5)
    except ZeroDivisionError:
        result = 0
    return result


def process_price():
    data = tsv_price_extraction()
    for country in data.keys():
        l = [['Year', 'Elec_cost']]
        for year in data[country].keys():
            l.append([year, data[country][year]])
        with open('C:/Users/33640/Documents/UCL/Energy Data Analysis/VizChallenge/{}_electricity_historic_cost.csv'.format(country),
                  'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(l)
