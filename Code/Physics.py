import numpy as np
from numba import njit, prange

G = 6.67430e-11  # m^3 / kg / s^2

@njit(parallel=True)
def compute_system_accelerations(pos, mass, acc):
    N = pos.shape[0]
    
    # reset acc
    for i in prange(N):
        acc[i,0] = 0.0
        acc[i,1] = 0.0
        acc[i,2] = 0.0

    # calc new acc
    for i in prange(N):  # parallel outer loop
        for j in range(N):
            if i == j:
                continue
            dx = pos[j,0] - pos[i,0]
            dy = pos[j,1] - pos[i,1]
            dz = pos[j,2] - pos[i,2]
            
            dist_sq = dx*dx + dy*dy + dz*dz
            dist = np.sqrt(dist_sq)
            inv_dist3 = 1.0 / (dist_sq * dist + 1e-10)
            
            factor = G * mass[j] * inv_dist3
            acc[i,0] += dx * factor
            acc[i,1] += dy * factor
            acc[i,2] += dz * factor


@njit(parallel=True)
def verlet_step(pos, vel, mass, acc, dt_days):
    dt = dt_days * 86400.0  # convert days → seconds
    N = pos.shape[0]
    
    # Halber Schritt vel Update
    for i in prange(N):
        for k in range(3):
            vel[i,k] += 0.5 * acc[i,k] * dt
    
    # Voller Schritt Positionsupdate
    for i in prange(N):
        for k in range(3):
            pos[i,k] += vel[i,k] * dt
    
    # neue acc berechnen
    compute_system_accelerations(pos, mass, acc)
    
    # Halber schritt vel Update mit neuer acc
    for i in prange(N):
        for k in range(3):
            vel[i,k] += 0.5 * acc[i,k] * dt