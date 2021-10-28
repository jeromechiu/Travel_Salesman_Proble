import googlemaps
from datetime import datetime
from itertools import tee
import pandas as pd
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from address_to_wgs84 import transfer_address_geocord


gmaps = googlemaps.Client(key='AIzaSyChK3j3VtgLFgFDuep6dNU_NzXqztGpqxk')


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
    # print(square_matrix)
    return square_matrix

def create_data_model(destinations):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] =   gen_square_form(destinations) # yapf: disable
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


def get_routes(solution, routing, manager):
  """Get vehicle routes from a solution and store them in an array."""
  # Get vehicle routes and store them in a two dimensional array whose
  # i,j entry is the jth location visited by vehicle i along its route.
  routes = []
  for route_nbr in range(routing.vehicles()):
    index = routing.Start(route_nbr)
    route = [manager.IndexToNode(index)]
    while not routing.IsEnd(index):
      index = solution.Value(routing.NextVar(index))
      route.append(manager.IndexToNode(index))
    routes.append(route)
  return routes

def calculate_tsp(destinations):    
    group_id = destinations.groupby(['group'],as_index=True)
    
    for i in group_id:
        id = i[1].index.values
        group_dest = pd.DataFrame(columns=['coord'], index=id)
        for j in id:
            data = (i[1].loc[j,'lat'], i[1].loc[j,'long'])
            group_dest.loc[j,'coord'] = data
        group_dest.reset_index(inplace=True)

        group_dest.rename(columns={"index":"id"},inplace=True)    
        data = create_data_model(group_dest)
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

        routes = get_routes(solution, routing, manager)[-1][:-1]
        
        for i in routes:
            destinations.loc[group_dest.iloc[i]['id'],'stop'] = int(routes[i])
            
    return destinations

if __name__ == '__main__':
    from address_to_wgs84 import destinations
    calculate_tsp(destinations)  
 
