import heapq
import math
 
from data_structures.city_map import CityMap
 
def straight_line_distance(city_map, a, b):
    x1, y1 = city_map.intersections[a]
    x2, y2 = city_map.intersections[b]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
 
def longest_road_length(city_map):
    longest = 0.0
    for node, neighbors in city_map.roads.items():
        for neighbor in neighbors:
            length = straight_line_distance(city_map, node, neighbor)
            if length > longest:
                longest = length
    return longest or 1.0
 
def heuristic(city_map, current, goal, scale):
    return straight_line_distance(city_map, current, goal) / scale
 
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
 
def find_path(city_map: CityMap, start: int, goal: int) -> list[int]:
    if start == goal:
        return [start]
 
    scale = longest_road_length(city_map)
 
    open_set = []
    heapq.heappush(open_set, (heuristic(city_map, start, goal, scale), start))
 
    came_from = {}
    g_score = {start: 0}
    closed_set = set()
 
    while open_set:
        _, current = heapq.heappop(open_set)
 
        if current in closed_set:
            continue
        closed_set.add(current)
 
        if current == goal:
            return reconstruct_path(came_from, current)
 
        for neighbor in city_map.roads[current]:
            tentative_g_score = g_score[current] + 1
 
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(city_map, neighbor, goal, scale)
                heapq.heappush(open_set, (f_score, neighbor))
 
    return []