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

def find_world_hits(coords, velocities, N, S, T, P):
    coords = move_in_time(coords, velocities, T, None, ignore_bounds=True)
    coords = coords[np.any(np.abs(coords) > S, axis=1), :]
    stable_particles = float(N - coords.shape[0])
    angles = np.arctan2(coords[:, 1], coords[:, 0]).reshape((coords.shape[0], 1))
    starting_points = np.zeros(coords.shape)
    starting_points = starting_points + \
        np.array([S, 0]) * np.logical_and(angles>=-np.pi/4, angles<=np.pi/4) + \
            np.array([-S, 0]) * np.logical_or(angles<=-3*np.pi/4, angles>=3*np.pi/4) + \
                np.array([0, S]) * np.logical_and(angles>=np.pi/4, angles<=3*np.pi/4) + \
                    np.array([0, -S]) * np.logical_and(angles>=-3*np.pi/4, angles<=-np.pi/4)
    starting_points = starting_points + np.hstack((
        (((starting_points[:, 1] - coords[:, 1]) / np.tan(angles).reshape(angles.shape[0]) + coords[:, 0]) * (starting_points[:, 0] == 0)).reshape((angles.shape[0], 1)),
        ((np.tan(angles).reshape(angles.shape[0]) * (starting_points[:, 0] - coords[:, 0]) + coords[:, 1]) * (starting_points[:, 1] == 0)).reshape((angles.shape[0], 1))
    ))
    wall_bangs = np.ones(coords.shape[0])
    old_wall_bangs = np.zeros(coords.shape[0])
    coords = coords - starting_points # now coords holds the remaining path of point
    while np.any(wall_bangs != old_wall_bangs):
        coords = np.nan_to_num(coords)
        new_angles = - angles * np.where(np.abs(starting_points[:, 1]) == S, 1, 0).reshape((angles.shape[0],1)) + \
            (np.pi - angles) * np.where(np.abs(starting_points[:, 0]) == S, 1, 0).reshape((angles.shape[0],1)) * (angles >= 0).reshape((angles.shape[0],1)) + \
            (-np.pi - angles) * np.where(np.abs(starting_points[:, 0]) == S, 1, 0).reshape((angles.shape[0],1)) * (angles < 0).reshape((angles.shape[0],1))
        rotation_angles = new_angles - angles
        angles = new_angles
        new_starting_points = np.zeros(coords.shape)
        for i in range(rotation_angles.shape[0]): # rotation matrix
            coords[i] = np.array([[np.cos(rotation_angles[i][0]), -np.sin(rotation_angles[i][0])], [np.sin(rotation_angles[i][0]), np.cos(rotation_angles[i][0])]]) @ coords[i,:]
        coords = np.nan_to_num(coords)
        x_plus_S = np.repeat((1*(starting_points[:, 0] != S)).reshape((starting_points.shape[0],1)), 2, axis=1) * np.hstack((
            (S * np.ones(angles.shape[0])).reshape((angles.shape[0], 1)),
            (np.tan(angles).reshape(angles.shape[0]) * (S - coords[:, 0] - starting_points[:, 0]) + coords[:, 1] + starting_points[:, 1]).reshape((angles.shape[0], 1))
        ))
        x_plus_S = x_plus_S * np.repeat(np.logical_and(x_plus_S[:, 1] <= S, x_plus_S[:, 1] >= -S).reshape((x_plus_S.shape[0],1)), 2, axis=1) * np.repeat((np.linalg.norm(x_plus_S - starting_points, ord=2, axis=1) <= np.linalg.norm(coords, ord=2, axis=1)).reshape((angles.shape[0],1)), 2, axis=1)
        x_minus_S = np.repeat((1*(starting_points[:, 0] != -S)).reshape((starting_points.shape[0],1)), 2, axis=1) * np.hstack((
            (-S * np.ones(angles.shape[0])).reshape((angles.shape[0], 1)),
            (np.tan(angles).reshape(angles.shape[0]) * (-S - coords[:, 0] - starting_points[:, 0]) + coords[:, 1] + starting_points[:, 1]).reshape((angles.shape[0], 1))
        ))
        x_minus_S = x_minus_S * np.repeat(np.logical_and(x_minus_S[:, 1] <= S, x_minus_S[:, 1] >= -S).reshape((x_minus_S.shape[0],1)), 2, axis=1) * np.repeat((np.linalg.norm(x_minus_S - starting_points, ord=2, axis=1) <= np.linalg.norm(coords, ord=2, axis=1)).reshape((angles.shape[0],1)), 2, axis=1)
        y_plus_S = np.repeat((1*(starting_points[:, 1] != S)).reshape((starting_points.shape[0],1)), 2, axis=1) * np.hstack((
            ((S - coords[:, 1] - starting_points[:, 1]) / np.tan(angles).reshape(angles.shape[0]) + coords[:, 0] + starting_points[:, 0]).reshape((angles.shape[0], 1)),
            (S * np.ones(angles.shape[0])).reshape((angles.shape[0], 1))
        ))
        y_plus_S = y_plus_S * np.repeat(np.logical_and(y_plus_S[:, 0] <= S, y_plus_S[:, 0] >= -S).reshape((y_plus_S.shape[0],1)), 2, axis=1) * np.repeat((np.linalg.norm(y_plus_S - starting_points, ord=2, axis=1) <= np.linalg.norm(coords, ord=2, axis=1)).reshape((angles.shape[0],1)), 2, axis=1)
        y_minus_S = np.repeat((1*(starting_points[:, 1] != -S)).reshape((starting_points.shape[0],1)), 2, axis=1) * np.hstack((
            ((-S - coords[:, 1] - starting_points[:, 1]) / np.tan(angles).reshape(angles.shape[0]) + coords[:, 0] + starting_points[:, 0]).reshape((angles.shape[0], 1)),
            (-S * np.ones(angles.shape[0])).reshape((angles.shape[0], 1))
        ))
        y_minus_S = y_minus_S * np.repeat(np.logical_and(y_minus_S[:, 0] <= S, y_minus_S[:, 0] >= -S).reshape((y_minus_S.shape[0],1)), 2, axis=1) * np.repeat((np.linalg.norm(y_minus_S - starting_points, ord=2, axis=1) <= np.linalg.norm(coords, ord=2, axis=1)).reshape((angles.shape[0],1)), 2, axis=1)
        new_starting_points = np.nan_to_num(x_minus_S) + np.nan_to_num(x_plus_S) + np.nan_to_num(y_minus_S) + np.nan_to_num(y_plus_S)
        old_wall_bangs = wall_bangs.copy()
        wall_bangs = wall_bangs + np.any(np.abs(coords + starting_points) > S, axis=1) + np.any(np.abs(coords + starting_points) == S, axis=1) * np.all(np.abs(coords + starting_points) <= S, axis=1)
        coords = coords - (np.nan_to_num(new_starting_points) - np.nan_to_num(starting_points)) * np.logical_not(np.repeat(np.all(new_starting_points == 0, axis=1).reshape((new_starting_points.shape[0],1)), 2, axis=1))
        coords = coords * np.repeat(np.any(np.abs(coords + starting_points) > S, axis=1).reshape((coords.shape[0], 1)), 2, axis=1)
        starting_points = new_starting_points
    return int(np.sum(wall_bangs)), stable_particles + np.sum(np.power(P, wall_bangs))

if __name__ == '__main__':
    np.warnings.filterwarnings('ignore')
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
    world_hit_data = find_world_hits(coords, velocities, N, S, T, P)
    print("{0} {1} {2}".format(find_big_bang(coords, velocities, S), world_hit_data[0], world_hit_data[1]))