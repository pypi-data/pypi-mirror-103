# Emergency Response Simulation

## Installing 

`pip install emergency_simulation`

## Introduction

Emergency Response Simulation is a package that helps anyone to create a simulation where you can create a city as a Graph of neighborhoods with the networkx library, and simulate emergency responses in it. The idea is to easily allow anyone to explore what is the best configuration for ambulance allocations in a given city.

## Creating a simulation. Getting started with Sample Code.

### Part 1. Creating a Graph with networkx

```
# importing packages
from emergency_simulation import *
import scipy.stats as sts
import networkx as nx

## Creating Graph
G = nx.Graph()

# creating neighborhoods with their emergency rate
G.add_node("Civic Center", emergency_distribution = sts.expon(scale=29))
G.add_node("Nob Hill", emergency_distribution = sts.expon(scale=35))
G.add_node("Downtown", emergency_distribution = sts.expon(scale=30))
G.add_node("Tenderloin", emergency_distribution = sts.expon(scale=36))
G.add_node("South of Market", emergency_distribution = sts.expon(scale=30))
G.add_node("Financial District", emergency_distribution = sts.expon(scale=20))
G.add_node("Yerba Buena", emergency_distribution = sts.expon(scale=29))
G.add_node("South Beach", emergency_distribution = sts.expon(scale=25))
G.add_node("Mission Bay", emergency_distribution = sts.expon(scale=30))
G.add_node("Potrero Hill", emergency_distribution = sts.expon(scale=33))
G.add_node("Inner Mission", emergency_distribution = sts.expon(scale=38))
G.add_node("Dogpatch", emergency_distribution = sts.expon(scale=32))


# creating edges with weight representing the distance in minutes between 2 neighborhoods
G.add_edge("Civic Center", "Nob Hill", weight=5)
G.add_edge("Civic Center", "Downtown", weight=5)
G.add_edge("Civic Center", "Tenderloin", weight=3)
G.add_edge("Civic Center", "South of Market", weight=5)

G.add_edge("Nob Hill", "Downtown", weight=5)
G.add_edge("Nob Hill", "Financial District", weight=4)

G.add_edge("Downtown", "Financial District", weight=7)
G.add_edge("Downtown", "Yerba Buena", weight=4)
G.add_edge("Downtown", "Tenderloin", weight=4)

G.add_edge("Financial District", "Yerba Buena", weight=5)
G.add_edge("Financial District", "South Beach", weight=5)

G.add_edge("Yerba Buena", "South of Market", weight=2)
G.add_edge("Yerba Buena", "South Beach", weight=3)

G.add_edge("South of Market", "Mission Bay", weight=5)
G.add_edge("South of Market", "Potrero Hill", weight=5)
G.add_edge("South of Market", "Inner Mission", weight=6)
G.add_edge("South of Market", "Tenderloin", weight=5)

G.add_edge("Mission Bay", "South Beach", weight=5)
G.add_edge("Mission Bay", "Dogpatch", weight=5)
G.add_edge("Mission Bay", "Potrero Hill", weight=5)

G.add_edge("Dogpatch", "Potrero Hill", weight=4)

G.add_edge("Potrero Hill", "Inner Mission", weight=5)
```

### Part 2. Running the simulation

```
## Running the simulation with a single configuration

# neighborhoods that have ambulance stations
neighborhoods = ["Downtown", "Potrero Hill", "South Beach"]
# total ambulances available to be used
total_ambulances = 13
# ambulance stations per neighborhood
neighborhood_ambulance_allocations = neighborhood_ambulance_combinations(neighborhoods, total_ambulances)
# random value to account for ambulance time to get to the exact location and assist the person
location_and_assitance_distribution = sts.norm(loc=15, scale=5)

# running the simulation for the first "neighborhood_ambulance_allocations" and for 20 steps
simulation = run_simulation(G, neighborhood_ambulance_allocations[0], location_and_assitance_distribution, 20, log=True)
```

### Part 3. Exploring statistics/metrics

```
# getting simulation statistics
wait_time = simulation.emergency_queue.wait_time_per_emergency
ambulance_stations = simulation.ambulance_stations

print("======================== RESULTS ========================")
print("Average Wait Time:", np.mean(wait_time))
print("Average Number of Ambulances left idle throughout the simulation")
for station in ambulance_stations:
    print("___________")
    mean_available_ambulances = np.mean(station.available_ambulances_evolution)
    print(station.neighborhood)
    print("Average Number of Ambulances left idle")
    print(mean_available_ambulances)
    print("Ambulance Evolution")
    print(station.available_ambulances_evolution)
```