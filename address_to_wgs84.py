import googlemaps
import pandas as pd
from key import gmap_key

gmaps = googlemaps.Client(key=gmap_key)

"""
Sample of address
destinations = [[0, '新北市中和區中正路209號'],
                [1, '新北市中和區建一路92號'],
                [3, '新北市中和區景平路634-2號B1'],
                [2, '新北市中和區連城路258號18樓']
                ]
                
Sample of WGS84
    dest_coord = [[0, (24.993484, 121.497134)], 
                  [1, (25.0007671, 121.4879088)], 
                  [3, (24.9986295, 121.5007544)], 
                  [2, (24.99663, 121.4869139)]]
"""

def to_coord(address):
    return gmaps.geocode(address)

def transfer_address_geocord(destinations):
    dest_coord = list()
    for i, addr in destinations:
        data = to_coord(addr)
        lat, long = data[0]['geometry']['location']['lat'], data[0]['geometry']['location']['lng']
        dest_coord.append([i, (lat, long)])
    dest_coord = pd.DataFrame(dest_coord, columns=['id', 'coord'])
    dest_coord.set_index('id', inplace=True)
    dest_coord.sort_index(inplace=True)
    return dest_coord

