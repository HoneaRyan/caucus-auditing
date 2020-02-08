from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = "https://results.thecaucuses.org/"


def grab_string(item):
    return getattr(item, 'string')


def extract_cols(parent, header_row):
    _items = parent.find('ul', {'class': header_row}).contents
    return tuple(map(grab_string, _items))


if __name__ == "__main__":
    data = requests.get(URL).text
    soup = BeautifulSoup(data, 'lxml')
    # header = soup.find("ul", {"class": "thead"})
    # heads = header.find_all("li")
    # subheader = soup.find("ul", {"class": "sub-head"})
    # subheads = subheader.find_all("li")
    # headers = ["county", "precinct", "candidate", "1stalign", "2ndalign", "sde"]
    precinct_table = soup.find('div', {'class': 'precinct-table'})
    # precinct_table limits our finds to only the contents we actually want
    source_heads = tuple(
        zip(
            extract_cols(precinct_table, 'thead'),
            extract_cols(precinct_table, 'sub-head')
        )
    )
    # source_heads gets our column names as rendered in the table
    headers = list()
    prev_pref = None
    for pref, suff in source_heads:
        prev_pref = pref or prev_pref
        if suff is None:
            suff = ''
        else:
            suff = '.' + suff
        headers.append(prev_pref + suff)
    # Configures our headers to be of form
    # [Upper Header] or [Upper Header].[Lower Header]
    # for those columns that have sub-sections
    # df = pd.DataFrame(columns=headers)
    # for divs in soup.find_all("div", {"class": "precinct-rows"}):
    #     county_nm = divs.find_all("div", {"class": "wrap"})[0]
    #     precincts = divs.find_all("div", {"class": "precinct-data"})
    #     vals = precincts[0].find_all('li')
    #     rows = int(len(vals) / 43)
    #     for i in range(0, rows - 1):
    #         for j in range(0, 14):
    #             precinct = vals[i * 43]
    #             candidate = heads[2 + j * 3]
    #             align_1 = vals[i * 43 + j * 3 + 1]
    #             align_2 = vals[i * 43 + j * 3 + 2]
    #             sde = vals[i * 43 + j * 3 + 3]
    #             df = df.append({
    #                 'county': county_nm.string,
    #                 'precinct': precinct.string,
    #                 'candidate': candidate.string,
    #                 '1stalign': align_1.string,
    #                 '2ndalign': align_2.string,
    #                 'sde': sde.string
    #             }, ignore_index=True)
    # df.to_csv('iowa_caucuses.csv')
