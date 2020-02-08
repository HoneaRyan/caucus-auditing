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
    counties = precinct_table.find_all('div', {'class': 'precinct-rows'})
    # generates a list of all of the discovered county objects
    storage_list = list()
    pack = storage_list.append
    # make a container to store extracted data
    # attaching append to a specific variable removes method lookup time
    for county_obj in counties:
        row_pref = (county_obj.find('div', {'class': 'wrap'}).string,)
        # grabs the county name to put at the front of each row
        for row in county_obj.find('div', {'class': 'precinct-data'}).contents:
            # steps through each row in each county
            if row.contents[0].string == 'Total':
                continue
                # skip the unneeded Total row
                # One can do the math themselves later
            pack(row_pref+tuple(map(grab_string, row.contents)))
            # store the data in format (county, col1, col2, col3, ...)
    final_frame = pd.DataFrame(storage_list, columns=headers)
    final_frame.to_csv('caucuses_frame.csv')
