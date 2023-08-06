import numpy as np
import pandas as pd


def len_points(points):
    return points.shape[0]

def distance_matrix(points):
    """
    calculate the distance among each suggest solution points

    input:
        points: array containig the points to be visited
    outputs:
        matrix: nxn array with distances among solution points
    """
    coordinates = points
    matrix = []
    for i in range(len(coordinates)):
        for j in range(len(coordinates)):
            p = np.linalg.norm(coordinates[i] - coordinates[j])
            matrix.append(p)
    return np.reshape(matrix, (len(coordinates), len(coordinates)))

def random_solution(points):
    """
    create a random solution with the places to be visited
    input:
        points: array with the places for visiting
    output:
        array: input randomly rearrange
    """
    number_points = len_points(points)
    points_order = list(range(0, number_points))
    temp_solution = []
    for i in range(number_points):
        random_point = np.random.choice(points_order)
        temp_solution.append(random_point)
        points_order.remove(random_point)
    temp_solution.append(temp_solution[0])
    return temp_solution

def calculate_distance(points):
    """
    returns the distance associated with a solution
    input:
        points:
    """
    random_sol = random_solution(points)
    matrix = distance_matrix(points)
    distance = 0
    for i in range(len(random_sol)):
        distance += matrix[random_sol[i]][random_sol[i - 1]]
    return distance


def other_solutionts(points, num_solution, best_sol):
    number_points = points.shape[0]
    pos_sol = [best_sol]
    for i in range(num_solution - 1):
        temp_sol = random_solution(points)

        if temp_sol not in pos_sol:
            pos_sol.append(temp_sol)

    return pos_sol

def best_solution(points, num_solution):
    best_sol = random_solution(points)
    distance = calculate_distance(points)
    best_distance = distance
    solutions = other_solutionts(points, num_solution, best_sol)
    for pos_sol in solutions:
        pos_dist = calculate_distance(points)
        if best_distance > pos_dist:
            best_distance = pos_dist
            best_sol = pos_sol
    return best_distance, best_sol