'''
Closest pair problem - The closest pair of points problem or closest pair problem 
is a problem of computational geometry: given n points in metric space, find a pair 
of points with the smallest distance between them.
'''

def distance_between(a,b):
    '''
    Expected input is two pairs of (x,y) coordinates, a and b, and the output is the
    straight-line distance between them.
    '''
    (x1,y1) = a
    (x2,y2) = b
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


def find_shortest_distance_unique_values(coordinates_list):
    '''
    Input is a list of (x,y) coordinates as tuples, output is a list [[(x1,y1),(x2,y2)],distance] where (x1,y1) and (x2,y2) are
    the closest unique points from the list. Specifically, if there are two identical points in the coordinates_list, this will
    NOT assess that they are the closest two points. If more than two pairs of points have the same distance between them, this will just return
    one of them (the one that appears first).
    '''
    minimum_points = [coordinates_list[0],coordinates_list[1]]
    minimum_distance = distance_between(coordinates_list[0],coordinates_list[1])
    for (x1,y1) in coordinates_list:
        for (x2,y2) in coordinates_list:
            if (x1,y1) != (x2,y2):
                candidate_distance = distance_between((x1,y1),(x2,y2))
                if candidate_distance < minimum_distance:
                    minimum_points = [(x1,y1),(x2,y2)]
                    minimum_distance = candidate_distance
                else:
                    continue
            else:
                continue
    return minimum_points, minimum_distance


def find_shortest_distance_nonunique_values(coordinates_list):
    '''
    Input is a list of (x,y) coordinates as tuples, output is a list [[(x1,y1),(x2,y2)],distance] where (x1,y1) and (x2,y2) are
    the closest points from the list. Specifically, if there are two identical points in the coordinates_list, this WILL return
    them as the closest two points. If more than two pairs of points have the same distance between them, this will just return
    one of them (the one that appears first).
    '''
    minimum_points = [coordinates_list[0],coordinates_list[1]]
    minimum_distance = distance_between(coordinates_list[0],coordinates_list[1])
    for i in range(0,len(coordinates_list)-1):
        (x1,y1) = (coordinates_list[i][0],coordinates_list[i][1])
        for j in range(i+1,len(coordinates_list)):
            (x2,y2) = (coordinates_list[j][0],coordinates_list[j][1])
            candidate_distance = distance_between((x1,y1),(x2,y2))
            if candidate_distance < minimum_distance:
                minimum_points = [(x1,y1),(x2,y2)]
                minimum_distance = candidate_distance
            else:
                continue
    return minimum_points, minimum_distance
