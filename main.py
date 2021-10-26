import googlemaps
from datetime import datetime
from itertools import tee
import pandas as pd
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


gmaps = googlemaps.Client(key='google_map_key')


destinations = [[0, '新北市中和區中正路209號'],
                [1, '新北市中和區建一路92號'],
                [3, '新北市中和區景平路634-2號B1'],
                [2, '新北市中和區連城路258號18樓']
                ]



def to_coord(address):
    return gmaps.geocode(address)

def transfer_address_geocord(destinations):
    dest_coord = list()
    for i, addr in destinations:
        data = to_coord(addr)
        lat, long = data[0]['geometry']['location']['lat'], data[0]['geometry']['location']['lng']
        dest_coord.append([i, (lat, long)])


    # dest_coord = [[0, (24.993484, 121.497134)], 
    #               [1, (25.0007671, 121.4879088)], 
    #               [3, (24.9986295, 121.5007544)], 
    #               [2, (24.99663, 121.4869139)]]
    dest_coord = pd.DataFrame(dest_coord, columns=['id', 'coord'])
    dest_coord.set_index('id', inplace=True)
    dest_coord.sort_index(inplace=True)
    return dest_coord



def gen_square_form(locations):
    square_matrix = list()

    for i in range(len(locations)):
        square_matrix.append([0] * len(locations))
    for i in range(len(locations)):
        for j in range(len(locations)):                
            if i == j:
                pass #already have default value 0
                
            elif i < j:
                distance = gmaps.directions(locations.iloc[i]['coord'],
                                        locations.iloc[j]['coord'],
                                        mode='driving')
                square_matrix[i][j] = distance[0]['legs'][-1]['distance']['value']
                square_matrix[j][i] = square_matrix[i][j]
            elif j < i:
                #Already done
                pass            
    print(square_matrix)
    return square_matrix

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] =   gen_square_form(transfer_address_geocord(destinations)) # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {}'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Objective: {}m\n'.format(route_distance)


def main():
    data = create_data_model()
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                       data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)


if __name__ == '__main__':
    main()  
    