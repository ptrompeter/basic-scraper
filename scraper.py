# http://info.kingcounty.gov/health/ehs/foodsafety/inspections/Results.aspx?Output=W&Business_Name=La%20carta%20de%20oaxaca&Business_Address=&Longitude=&Latitude=&City=Seattle&Zip_Code=&Inspection_Type=All&Inspection_Start=&Inspection_End=&Inspection_Closed_Business=A&Violation_Points=&Violation_Red_Points=&Violation_Descr=&Fuzzy_Search=N&Sort=B
import requests
import io
from bs4 import BeautifulSoup
from sys import argv
import re

# DOMAIN = 'http://info.kingcounty.gov'
# PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
# QUERY = {
#     'Output': 'W',
#     'Business_Name': "",
#     'Business_Address': "",
#     'Longitude': "",
#     'Latitude': "",
#     'City': "",
#     'Zip_Code': "",
#     'Inspection_Type': "All",
#     'Inspection_Start': "",
#     'Inspection_End': "",
#     'Inspection_Closed_Business': "A",
#     'Violation_Points': "",
#     'Violation_Red_Points': "",
#     'Violation_Descr': "",
#     'Fuzzy_Search': "N",
#     'Sort': "H"

# }
INSPECTION_DOMAIN = 'http://info.kingcounty.gov'
INSPECTION_PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
INSPECTION_PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address': '',
    'Longitude': '',
    'Latitude': '',
    'City': '',
    'Zip_Code': '',
    'Inspection_Type': 'All',
    'Inspection_Start': '',
    'Inspection_End': '',
    'Inspection_Closed_Business': 'A',
    'Violation_Points': '',
    'Violation_Red_Points': '',
    'Violation_Descr': '',
    'Fuzzy_Search': 'N',
    'Sort': 'B'
}

# def get_inspection_page(**kwargs):
    # req_path = DOMAIN + PATH
    # parameters = QUERY.copy()
    # for key, val in kwargs.items():
    #     if key in parameters:
    #         parameters[key] = val
    # plist = ["?"]
    # for key in parameters:
    #     plist.append(key)
    #     plist.append('=')
    #     plist.append(parameters[key])
    #     plist.append('&')
    # del plist[-1]
    # pstring = "".join(plist)
    # full_path = req_path+pstring
    # r = requests.get(full_path)

def get_inspection_page(**kwargs):
    url = INSPECTION_DOMAIN + INSPECTION_PATH
    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        if key in INSPECTION_PARAMS:
            params[key] = val
    import pdb; pdb.set_trace()
    resp = requests.get(url, params=params)
    resp.raise_for_status() # <- This is a no-op if there is no HTTP error
    # remember, in requests `content` is bytes and `text` is unicode
    return resp.content, resp.encoding


def get_inspection_content(**kwargs):
    url = INSPECTION_DOMAIN + INSPECTION_PATH
    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        if key in INSPECTION_PARAMS:
            params[key] = val
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.content, resp.encoding

def load_inspection_page(page):
    file = io.open(page, encoding='utf-8', mode='r')
    text = file.read()
    file.close()
    return text, 'utf-8'

def write_inspection_page(content, encoding):
    file = io.open('inspection_page.html', encoding='utf-8', mode='w')
    file.write(content.decode(encoding))
    file.close()

def parse_source(html):
    parsed = BeautifulSoup(html, 'html5lib')
    return parsed

def extract_data_listings(soup):
    div_regex = re.compile(r'PR[\d]+~')
    new_soup = soup.find_all('div', id=div_regex)
    return new_soup

# def has_two_tds(soup):
#     tds = soup.findall('td')
#     if len(tds) == 2:
#         return True

def has_two_tds(elem):
    is_tr = elem.name == 'tr'
    td_children = elem.find_all('td', recursive=False)
    has_two = len(td_children) == 2
    return is_tr and has_two

def clean_data(td):
    data = td.string
    try:
        return data.strip(" \n:-")
    except AttributeError:
        return u""

def main(argv):
    params = argv[2:]
    pdict = {}
    for item in params:
        ilist = item.split('=')
        pdict[ilist[0]] = ilist[1]
    if argv[1] == 'get':
        print('get is running')
        content, encoding = get_inspection_content(**pdict)
        write_inspection_page(content, encoding)
        print('Got data!')
    elif argv[1] == 'show':
        content, encoding = load_inspection_page('kc_health_data.html')
        print(text)
    elif argv[1] == 'test':
        content, encoding = load_inspection_page('kc_health_data.html')
    else:
        print('you must pass a valid argument.  Try "get", "show", or "test"')
        return None
    doc = parse_source(content)
    containers = extract_data_listings(doc)
    # import pdb; pdb.set_trace()
    # print(doc.prettify(encoding=encoding))
    for item in containers:
        metadata_rows = item.find('tbody').find_all(has_two_tds, recursive=False)
        print(len(metadata_rows))
        for row in metadata_rows:
            for td in row.find_all('td', recursive=False):
                print(clean_data(td))
            print()
        print()
    # print(containers[0].prettify())



if __name__ == '__main__':
    main(argv)


