import numpy as np


def is_out_of_bounds(coords, S):
    return np.sum(np.where(np.abs(coords) > S)) != 0

def back_in_time(coords, velocities, units, S):
    next_coords = np.copy(coords) - units * velocities
    if is_out_of_bounds(next_coords, S):
        return None
    else:
        return next_coords

def calculate_distances_from_origin(coords):
    return np.hypot(coords[:,0], coords[:,1])

def find_big_bang(coords, velocities, S):
    stds = np.array([])
    stds = np.append(stds, np.std(calculate_distances_from_origin(coords)))
    next_coords = np.copy(coords)
    last_coords = np.copy(coords)
    while(True):
        next_coords = back_in_time(next_coords, velocities, 1, S)
        if next_coords is None or np.all(last_coords == next_coords):
            break
        stds = np.append(stds, np.std(calculate_distances_from_origin(next_coords)))
        last_coords = np.copy(next_coords)
    return np.argmin(stds)


if __name__ == '__main__':
    nstp = input().split()
    N = int(nstp[0])
    S = int(nstp[1])
    T = int(nstp[2])
    P = float(nstp[3])
    coords = np.empty([0, 2])
    velocities = np.empty([0, 2])
    for i in range(N):
        pv = input().split()
        coords = np.append(coords, [[float(pv[0]), float(pv[1])]], axis=0)
        velocities = np.append(velocities, [[float(pv[2]), float(pv[3])]], axis=0)
    print("%d 0 -1.25" % find_big_bang(coords, velocities, S))