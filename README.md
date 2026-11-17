# How_Cats_decide_where_to_sit
this is a model that depends on limited factors, is generalized via the data of 8 cats:) feel free not trust 

A 2D heat-diffusion and agent-based simulation written in Python that models how a cat chooses where to rest in a room with competing heat sources and cold spots.

## Overview

Cats are notorious heat-seekers, often curling up on warm laptops before moving away once things get too hot. This simulation models a 20×20 grid room containing:
* **A warm PC (`50°C`)** at the bottom-left corner `(0, 0)` acting as a constant heat source.
* **A cold window (`-10°C`)** at the top-right corner `(19, 19)` acting as a constant heat sink.
* **Ambient room air (`20°C`)** that gradually conducts heat across the grid over 50,000 time steps.
* **A cat** that generates its own body heat, warms the spot it sits on, and relocates when its current spot becomes uncomfortably hot.

## How the Simulation Works

### 1. Heat Diffusion (`laplacian`)
At every time step (`dt = 0.1`), heat spreads across the room using a discrete 2D Laplacian operator with insulated (Neumann) boundary conditions. The PC and window remain fixed at their extreme temperatures, creating a continuous thermal gradient across the room.

### 2. Body Heat & Comfort Thresholds
* **Self-heating:** Wherever the cat sits, it adds a small amount of body heat (`cat_heat_power = 2.0`) to that grid cell, slowly warming up its own spot over time.
* **Thermal tolerance:** The cat tolerates temperatures between `10°C` (`cat_Tmin`) and `40°C` (`cat_Tmax`), with an ideal comfort temperature of `30°C` (`cat_temp_ideal`).
* **Relocation rule:** Once the cell beneath the cat exceeds `40°C`, the cat searches adjacent neighboring cells for an acceptable temperature (`score > 0`) and moves to a new spot.

## Output Visualizations

Running the script generates a 2×2 dashboard showing the simulation results:
1. **Final Room Temperature & Cat Path (Top-Left):** A heatmap of the room at the end of the run overlaid with the cat's movement trajectory (white dot = start, green dot = end, cyan dot = PC, blue dot = window).
2. **Occupancy Heatmap (Top-Right):** Total cumulative time the cat spent resting in each cell of the room.
3. **Temperature Experienced Over Time (Bottom-Left):** A time-series plot tracking the exact temperature beneath the cat against its upper (`40°C`) and lower (`10°C`) comfort limits.
4. **Residence Duration Histogram (Bottom-Right):** A distribution of how long the cat stayed in individual spots before moving.

