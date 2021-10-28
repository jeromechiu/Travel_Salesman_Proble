import travel_point_grouping
# import routing
from address_to_wgs84 import transfer_address_geocord
from routing import calculate_tsp
from travel_point_grouping import wgs84_to_cartesian, grouping, wgs84_to_cartesian



destinations = [[0, '新北市中和區中正路209號'],
                [1, '新北市中和區建一路92號'],
                [3, '新北市中和區景平路634-2號B1'],
                [2, '新北市中和區連城路258號18樓']
                ]


dest_coord = [[0, (24.993484, 121.497134)], 
                [1, (25.0007671, 121.4879088)], 
                [3, (24.9986295, 121.5007544)], 
                [2, (24.99663, 121.4869139)],
                [4, (24.99675656624081, 121.50636226818159)],
                [5, (25.002060969852035, 121.51072200728377)],
                [6, (24.99648971473095, 121.50066515392008)],
                [7, (24.99725077478079, 121.50031353934627)],
                [8, (24.99674027185629, 121.49756159310002)],
                [9, (24.996839941641497, 121.49789418699332)],
                [10, (24.997515749272218, 121.49955447425104)],
                [11, (24.995498039188387, 121.50097604502005)],
                [12, (24.99587241199133, 121.50172974569763)],
                [13, (24.99577760340233, 121.4988369834885)],
                [14, (24.99635496227342, 121.50022636767291)],
                [15, (24.996587107412616, 121.50234704426815)]
                ]



def main():

    # dest_coord = transfer_address_geocord(destinations)
    groupped = grouping(wgs84_to_cartesian(dest_coord), dest_coord)
    print(groupped)
    


    delivery_plan = calculate_tsp(groupped)
    print(delivery_plan)
if __name__ == '__main__':
    main()  
 
