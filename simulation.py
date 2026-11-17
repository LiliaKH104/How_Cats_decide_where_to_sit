import numpy as np
import random
import matplotlib.pyplot as plt

nx, ny = 20, 20
dt = 0.1
D = 0.02
C = 8.0
total_steps = 50000

pc_pos = (0, 0)
pc_temp = 50.0
window_pos = (nx-1, ny-1)
window_temp = -10.0
initial_room_temp = 20.0

cat_initial_pos = (0,0)
cat_heat_power = 2.0
cat_Tmin = 10.0
cat_Tmax = 40.0
cat_sigma = 5.0
cat_temp_ideal = 30.0

record_every = 50
max_neighbor_tries = 10

T = np.full((nx, ny), initial_room_temp, dtype=float)
occupancy = np.zeros((nx, ny), dtype=float)
residence_times = np.zeros((nx, ny), dtype=float)

# EMOJI CHECK FOR INITIAL TEMPERATURE
initial_temp = T[cat_initial_pos]
if initial_temp <= cat_Tmin:
    print("Cat starts in a very cold place ❄️")
elif initial_temp >= cat_Tmax:
    print("Cat starts in a very hot place 🔥")

cat_pos = tuple(cat_initial_pos)
cat_time_in_current = 0
path = [cat_pos]
temp_time_series = []
time_series_steps = []

def laplacian(T):
    T_pad = np.pad(T, pad_width=1, mode='edge')
    center = T_pad[1:-1, 1:-1]
    up = T_pad[0:-2, 1:-1]
    down = T_pad[2:, 1:-1]
    left = T_pad[1:-1, 0:-2]
    right = T_pad[1:-1, 2:]
    return (up + down + left + right - 4.0 * center)

def propose_neighbor(pos):
    x, y = pos
    neighbors = []
    if x > 0: neighbors.append((x-1, y))
    if x < nx-1: neighbors.append((x+1, y))
    if y > 0: neighbors.append((x, y-1))
    if y < ny-1: neighbors.append((x, y+1))
    return random.choice(neighbors) if neighbors else pos

def preference_score(T_cell):
    if T_cell < cat_Tmin or T_cell > cat_Tmax:
        return 0.0
    return np.exp(-((T_cell - cat_temp_ideal) ** 2) / (2 * cat_sigma**2))

for step in range(total_steps):

    T += (D / C) * laplacian(T) * dt

    px, py = pc_pos
    T[px, py] = pc_temp
    wx, wy = window_pos
    T[wx, wy] = window_temp

    cx, cy = cat_pos
    T[cx, cy] += (cat_heat_power / C) * dt

    if step % max(1, total_steps // 1000) == 0:
        temp_time_series.append(T[cx, cy])
        time_series_steps.append(step)

    cell_temp = T[cx, cy]
    cat_time_in_current += dt
    occupancy[cx, cy] += dt

    if cell_temp > cat_Tmax:
        moved = False
        attempts = 0

        while attempts < max_neighbor_tries and not moved:
            candidate = propose_neighbor(cat_pos)
            cx2, cy2 = candidate
            T_candidate = T[cx2, cy2]
            score = preference_score(T_candidate)

            if score > 0.0:
                cx_old, cy_old = cat_pos
                residence_times[cx_old, cy_old] += cat_time_in_current

                cat_pos = candidate
                path.append(cat_pos)
                cat_time_in_current = 0
                moved = True
            else:
                attempts += 1

        if not moved:
            x0, y0 = cat_pos
            neighbors = []
            if x0 > 0: neighbors.append((x0-1, y0))
            if x0 < nx-1: neighbors.append((x0+1, y0))
            if y0 > 0: neighbors.append((x0, y0-1))
            if y0 < ny-1: neighbors.append((x0, y0+1))

            valid = [p for p in neighbors if preference_score(T[p[0], p[1]]) > 0]

            if valid:
                best = random.choice(valid)
                cx_old, cy_old = cat_pos
                residence_times[cx_old, cy_old] += cat_time_in_current

                cat_pos = best
                path.append(cat_pos)
                cat_time_in_current = 0

if cat_time_in_current > 0:
    cx, cy = cat_pos
    residence_times[cx, cy] += cat_time_in_current

occupancy_time = occupancy
path_x = [p[0] + 0.5 for p in path]
path_y = [p[1] + 0.5 for p in path]

plt.figure(figsize=(12,10))

plt.subplot(2,2,1)
plt.imshow(T.T, origin='lower', interpolation='nearest', cmap='inferno')
plt.colorbar(label='Temperature (°C)')
plt.scatter([px+0.5],[py+0.5], color='cyan', s=120)
plt.scatter([wx+0.5],[wy+0.5], color='blue', s=120)
plt.plot(path_x, path_y, lw=1, alpha=0.8)
plt.scatter(path_x[0], path_y[0], color='white', s=30)
plt.scatter(path_x[-1], path_y[-1], color='green', s=40)

plt.subplot(2,2,2)
plt.imshow(occupancy_time.T, origin='lower', interpolation='nearest', cmap='magma')
plt.colorbar(label='Time cat spent in cell')

plt.subplot(2,2,3)
plt.plot(time_series_steps, temp_time_series)
plt.axhline(cat_Tmax, color='red', linestyle='--')
plt.axhline(cat_Tmin, color='blue', linestyle='--')
plt.xlabel('Step')
plt.ylabel('Temperature at cat')

plt.subplot(2,2,4)
plt.hist(residence_times.flatten(), bins=30)
plt.xlabel('Residence duration')
plt.ylabel('Count')

plt.tight_layout()
plt.show()
