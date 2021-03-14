import numpy as np


def is_out_of_bounds(coords, S):
    return np.sum(np.where(np.abs(coords) > S)) != 0

def move_in_time(coords, velocities, time, S, ignore_bounds = False):
    next_coords = np.copy(coords) + time * velocities
    if ignore_bounds or not is_out_of_bounds(next_coords, S):
        return next_coords
    else:
        return None

def calculate_distances_from_origin(coords):
    return np.hypot(coords[:,0], coords[:,1])

def find_big_bang(coords, velocities, S):
    stds = np.array([])
    stds = np.append(stds, np.std(calculate_distances_from_origin(coords)))
    next_coords = np.copy(coords)
    last_coords = np.copy(coords)
    while(True):
        next_coords = move_in_time(next_coords, velocities, -1, S)
        if next_coords is None or np.all(last_coords == next_coords):
            break
        stds = np.append(stds, np.std(calculate_distances_from_origin(next_coords)))
        last_coords = np.copy(next_coords)
    return np.argmin(stds)

def find_world_hits(coords, velocities, S, T, P):
    coords = move_in_time(coords, velocities, T, None, ignore_bounds=True)
    coords = coords[np.any(np.abs(coords) > S, axis=0), :]
    angles = np.arctan2(coords[:, 1], coords[:, 0]).reshape((coords.shape[0], 1))
    print(coords)
    starting_points = np.zeros(coords.shape)
    starting_points = starting_points + \
        np.array([S, 0]) * np.logical_and(angles>=-np.pi/4, angles<=np.pi/4) + \
            np.array([-S, 0]) * np.logical_or(angles<=-3*np.pi/4, angles>=3*np.pi/4) + \
                np.array([0, S]) * np.logical_and(angles>=np.pi/4, angles<=3*np.pi/4) + \
                    np.array([0, -S]) * np.logical_and(angles>=-3*np.pi/4, angles<=-np.pi/4)
    print(angles)
    print(starting_points)
    starting_points = starting_points + np.hstack((
        (((starting_points[:, 1] - coords[:, 1]) / np.tan(angles).reshape(angles.shape[0]) + coords[:, 0]) * (starting_points[:, 0] == 0)).reshape((angles.shape[0], 1)),
        ((np.tan(angles).reshape(angles.shape[0]) * (starting_points[:, 0] - coords[:, 0]) + coords[:, 1]) * (starting_points[:, 1] == 0)).reshape((angles.shape[0], 1))
    ))
    wall_bangs = np.ones(coords.shape[0])
    coords = coords - starting_points # now coords holds the remaining path of point
    print(starting_points)
    while np.any(coords != 0):
        new_angles = - angles * np.where(np.abs(starting_points[:, 1]) == 10, 1, 0).reshape((2,1)) + \
            (np.pi - angles) * np.where(np.abs(starting_points[:, 0]) == 10, 1, 0).reshape((2,1)) * (angles >= 0).reshape((2,1)) + \
            (-np.pi - angles) * np.where(np.abs(starting_points[:, 0]) == 10, 1, 0).reshape((2,1)) * (angles < 0).reshape((2,1))
        rotation_angles = new_angles - angles
        angles = new_angles
        print("a", rotation_angles.shape, rotation_angles)
        new_starting_points = np.zeros(coords.shape)
        print(-angles * np.where(np.abs(starting_points[:, 1]) == 10, 1, 0).reshape((2,1)))
        for i in range(rotation_angles.shape[0]):
            coords[i] = (np.array([[np.cos(rotation_angles[i][0]), -np.sin(rotation_angles[i][0])], [np.sin(rotation_angles[i][0]), np.cos(rotation_angles[i][0])]]) @ ((coords[i,:] + starting_points[i,:]) / np.linalg.norm((coords[i,:] + starting_points[i,:]))) * np.linalg.norm((coords[i,:] + starting_points[i,:]))) - starting_points[i,:]
        x_plus_10 = 1*(starting_points[:, 0] != 10) * np.hstack((
            (10 * np.ones(angles.shape[0])).reshape((angles.shape[0], 1)),
            ((np.tan(angles).reshape(angles.shape[0]) * (10 - coords[:, 0]) + coords[:, 1]) * (starting_points[:, 1] == 0)).reshape((angles.shape[0], 1))
        ))
        x_plus_10 = x_plus_10 * np.logical_and(x_plus_10[:, 1] <= 10, x_plus_10[:, 1] >= -10)
        x_minus_10 = 1*(starting_points[:, 0] != -10) * np.hstack((
            (-10 * np.ones(angles.shape[0])).reshape((angles.shape[0], 1)),
            ((np.tan(angles).reshape(angles.shape[0]) * (-10 - coords[:, 0]) + coords[:, 1]) * (starting_points[:, 1] == 0)).reshape((angles.shape[0], 1))
        ))
        x_minus_10 = x_minus_10 * np.logical_and(x_minus_10[:, 1] <= 10, x_minus_10[:, 1] >= -10)
        y_plus_10 = 1*(starting_points[:, 1] != 10) * np.hstack((
            (((10 - coords[:, 1]) / np.tan(angles).reshape(angles.shape[0]) + coords[:, 0]) * (starting_points[:, 0] == 0)).reshape((angles.shape[0], 1)),
            (10 * np.ones(angles.shape[0])).reshape((angles.shape[0], 1))
        ))
        y_plus_10 = y_plus_10 * np.logical_and(y_plus_10[:, 0] <= 10, y_plus_10[:, 0] >= -10)
        y_minus_10 = 1*(starting_points[:, 0] != -10) * np.hstack((
            (((-10 - coords[:, 1]) / np.tan(angles).reshape(angles.shape[0]) + coords[:, 0]) * (starting_points[:, 0] == 0)).reshape((angles.shape[0], 1)),
            (-10 * np.ones(angles.shape[0])).reshape((angles.shape[0], 1))
        ))
        y_minus_10 = y_minus_10 * np.logical_and(y_minus_10[:, 1] <= 10, y_minus_10[:, 1] >= -10)
        new_starting_points = x_minus_10 + x_plus_10 + y_minus_10 + y_plus_10
        starting_points = new_starting_points
        coords = coords * np.logical_not(np.any(np.abs(coords + starting_points) > S, axis=0))
        wall_bangs = wall_bangs + np.any(np.abs(coords + starting_points) > S, axis=0)
    return np.sum(wall_bangs), np.sum(np.power(P, wall_bangs))

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
    world_hit_data = find_world_hits(coords, velocities, S, T, P)
    print("{0} {1} {2}".format(find_big_bang(coords, velocities, S), world_hit_data[0], world_hit_data[1]))