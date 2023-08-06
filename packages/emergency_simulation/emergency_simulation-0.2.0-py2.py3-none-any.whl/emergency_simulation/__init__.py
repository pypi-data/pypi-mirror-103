"""Emergency Response Simulation"""

__version__ = "0.2.0"

# import modules
import heapq
import random
import scipy.stats as sts
import numpy as np
import networkx as nx
import matplotlib  
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class Event:
    '''
    Store the properties of one event in the Schedule class defined below. Each
    event has a time at which it needs to run, a function to call when running
    the event, along with the arguments and keyword arguments to pass to that
    function.
    '''
    def __init__(self, timestamp, function, *args, **kwargs):
        self.timestamp = timestamp
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __lt__(self, other):
        '''
        This overloads the less-than operator in Python. We need it so the
        priority queue knows how to compare two events. We want events with
        earlier (smaller) times to go first.
        '''
        return self.timestamp < other.timestamp

    def run(self, schedule):
        '''
        Run an event by calling the function with its arguments and keyword
        arguments. The first argument to any event function is always the
        schedule in which events are being tracked. The schedule object can be
        used to add new events to the priority queue.
        '''
        self.function(schedule, *self.args, **self.kwargs)


class Schedule:
    '''
    Implement an event schedule using a priority queue. You can add events and
    run the next event.
    
    The `now` attribute contains the time at which the last event was run.
    '''
    
    def __init__(self):
        self.now = 0  # Keep track of the current simulation time
        self.priority_queue = []  # The priority queue of events to run
    
    def add_event_at(self, timestamp, function, *args, **kwargs):
        # Add an event to the schedule at a particular point in time.
        heapq.heappush(
            self.priority_queue,
            Event(timestamp, function, *args, **kwargs))
    
    def add_event_after(self, interval, function, *args, **kwargs):
        # Add an event to the schedule after a specified time interval.
        self.add_event_at(self.now + interval, function, *args, **kwargs)
    
    def next_event_time(self):
        return self.priority_queue[0].timestamp

    def run_next_event(self):
        # Get the next event from the priority queue and run it.
        event = heapq.heappop(self.priority_queue)
        self.now = event.timestamp
        event.run(self)
        
    def __repr__(self):
        return (
            f'Schedule() at time {self.now} ' +
            f'with {len(self.priority_queue)} events in the queue')
    
    def print_events(self):
        print(repr(self))
        for event in sorted(self.priority_queue):
            print(f'   {event.timestamp}: {event.function.__name__}')

class Ambulance:
    '''
    Creates an Ambulance assigned to a given Ambulance Station.
    
    Inputs:
        ambulance_station (AmbulanceStation object) neighborhood that contains
        this ambulance.
    
    '''
    
    def __init__(self, ambulance_station):
        self.ambulance_station = ambulance_station
        self.in_service = False

class AmbulanceStation:
    '''
    Creates an Ambulance Station in a given neighborhood.
    
    Inputs:
        neighborhood (string) neighborhood name that contains
        an ambulance station.
        
        ambulances (int) number of ambulances available
        in this neighborhood.
    
    '''
    
    def __init__(self, neighborhood, ambulances):
        self.neighborhood = neighborhood
        self.ambulances = []
        for ambulance in range(ambulances):
            self.ambulances.append(Ambulance(self))
        self.available_ambulances = len(self.ambulances)
        self.available_ambulances_evolution = [len(self.ambulances)]
    
    def ambulance_track(self, schedule):
        """
        Function that keeps track of how many ambulances from this station
        is available at every given minute. This function calls itself every minute
        so that it can record the ambulance availability of the station.
        """
        self.available_ambulances_evolution.append(self.available_ambulances)
        schedule.add_event_after(1, self.ambulance_track)
        
    
    def use_ambulance(self):
        """
        Function for using a given ambulance. If we still have ambulances to be used
        it uses the last one.
        """
        if self.available_ambulances > 0:
            self.available_ambulances -= 1
    
    def free_ambulance(self):
        """
        Function for freeing a given ambulance, after it goes to the emergency and comes back. 
        """
        self.available_ambulances += 1
        
    
    def has_available_ambulance(self):
        """
        Checks if this station has an available ambulance
        if it has it returns the first available one
        """
        for ambulance in self.ambulances:
            if ambulance.in_service == False:
                return ambulance
        return False
    
class EmergencyQueue():
    '''
    Creates a Queue for emergencies.
    
    Inputs:
        neighborhood_graph (NetworkX Graph object) Graph representing the current neighborhood.
        
        ambulance_stations (Array of AmbulanceStation objects) Array with all ambulance stations
        available.
        
        location_and_assitance_distribution (scipy.stats distribution) Distribution used to sample
        the random time that it will take to get to the location of the emergency.
        
        log (bool) If set to True print steps of the simulation.
    '''
    def __init__(self, neighborhood_graph, ambulance_stations, location_and_assitance_distribution, log):
        self.neighborhood_graph = neighborhood_graph
        self.ambulance_stations = ambulance_stations
        self.location_and_assitance_distribution = location_and_assitance_distribution
        self.log=log
        
        # creating our queue and a variable to store the wait time for every emergency
        self.emergency_queue = [] 
        self.wait_time_per_emergency = []
    
    def get_closest_available_ambulance(self, schedule, target_neighborhood):
        min_distance = float("inf")
        station_index = -1
        ambulance = False
        # checking in all ambulance stations
        for i, source in enumerate(self.ambulance_stations):
            
            distance = nx.dijkstra_path_length(self.neighborhood_graph, source=source.neighborhood, target=target_neighborhood)
            if distance < min_distance:
                available_ambulance = self.ambulance_stations[i].has_available_ambulance()
                if available_ambulance:
                    # setting the closest distance we found, so we don't need to search in stations
                    # that are further away
                    min_distance = distance
                    station_index = i
                    ambulance = available_ambulance
        
        return station_index, ambulance, distance
    
    def ambulance_available_callback(self, schedule, ambulance):
        # if we have an emergency that was waiting for an ambulance to be
        # available, we can send this avaialable ambulance to it
        if self.log:
            print("Ambulance returned to station:", ambulance.ambulance_station.neighborhood)
            print("=====================")
        
        if self.emergency_queue:
            next_emergency, waiting_since = self.emergency_queue.pop(0)
            wait_time = schedule.now - waiting_since
            
            distance = nx.dijkstra_path_length(
                self.neighborhood_graph, 
                source= ambulance.ambulance_station.neighborhood, 
                target= next_emergency
            )
            
            self.send_ambulance(schedule, ambulance, distance, wait_time)
        else:
            # setting ambulance as available in case there's no emergency
            # waiting for it
            ambulance.in_service = False
            ambulance.ambulance_station.free_ambulance()
    
    def send_ambulance(self, schedule, ambulance, distance, wait_time):
        # setting closest available ambulance in use
        ambulance.in_service = True
        ambulance.ambulance_station.use_ambulance()

        random_sample = self.location_and_assitance_distribution.rvs()
        # ensuring that we don't get 0 or negative values for the additional wait time
        while random_sample <= 0:
            random_sample = self.location_and_assitance_distribution.rvs()

        # (min_length*2) the ambulance takes the minimum length path to go to the location 
        # and to come back plus a random value (self.location_and_assitance_distribution.rvs())
        time_to_be_available_again = distance*2 + self.location_and_assitance_distribution.rvs()
        time_waiting_for_ambulance = wait_time + time_to_be_available_again / 2
        
        if self.log:
            print("Ambulance leaving station:", ambulance.ambulance_station.neighborhood, "at", schedule.now)
            print("Should return in:", time_to_be_available_again, "minutes")
            print("Current number of ambulances available at", ambulance.ambulance_station.neighborhood, ":", ambulance.ambulance_station.available_ambulances)
            print("=====================")
            
        self.wait_time_per_emergency.append(time_waiting_for_ambulance)
        
        schedule.add_event_after(
            time_to_be_available_again,
            self.ambulance_available_callback, 
            ambulance
        )
   
    def add_emergency(self, schedule, node_name):
        station_index, available_ambulance, distance = self.get_closest_available_ambulance(schedule, node_name)
        if station_index != -1:
            # if we found an available ambulance > send it to emergency
            self.send_ambulance(schedule, available_ambulance, distance, 0)
        else:
            # if there's no available ambulance we add the emergency to our queue
            self.emergency_queue.append((node_name, schedule.now))
    
class City:
    '''
    Creates a city to run our simulation on. We'll need the graph relation for all neighborhoods, 
    and neighborhoods where we'll have
    
    Inputs:
        neighborhood_graph (netwrokx Graph object) neighborhood undirected graph with weights
        on edges representing the time distance between neighborhoods.
        
        neighborhood_ambulance_stations (Array of string [string]) each string represents a 
        neighborhood that contains an ambulance station.
        
        ambulance_allocation (Array of [string, int]) Array of arrays containing neighborhood name
        and the number of ambulances allocated to that neighborhood
        
    '''
    
    def __init__(self, neighborhood_graph, ambulance_allocation, location_and_assitance_distribution, log):
        self.neighborhood_graph = neighborhood_graph
        self.ambulance_stations = []
        # creating our ambulance stations accordingly to ambulance allocation array
        for neighborhood, ambulances in ambulance_allocation:
            self.ambulance_stations.append(AmbulanceStation(neighborhood, ambulances))
        self.emergency_queue = EmergencyQueue(neighborhood_graph, self.ambulance_stations, location_and_assitance_distribution, log)
    
    
    def create_emergency(self, schedule, node_name):
        # send emergency to our queueing system because it just happened
        self.emergency_queue.add_emergency(schedule, node_name)
        
        # schedule next emergency in this neighborhood
        emergency_distribution = self.neighborhood_graph.node[node_name]["emergency_distribution"]
        schedule.add_event_after(
            emergency_distribution.rvs(),
            self.create_emergency, 
            node_name
        )
    
    def run(self, schedule):
        # Schedule first emergency for every neighborhood 
        for node_name in self.neighborhood_graph.node:
            emergency_distribution = self.neighborhood_graph.node[node_name]["emergency_distribution"]
            
            schedule.add_event_after(
                emergency_distribution.rvs(),
                self.create_emergency, 
                node_name
            )
        for station in self.ambulance_stations:
            station.ambulance_track(schedule)

def combinations_summing_to_n(elements, n):
    """
    This function returns a set of all possible arrays that sums to 'n'

    Inputs:
        elements (int) number of elements used in an array

        n (int) target sum
    
    """
    comb = set()
    for a in range(n+1):
        for b in range(n+1):
            for c in range(n+1):
                if sum([a, b, c]) == n:
                    comb.add((a, b, c))
    return comb

def neighborhood_ambulance_combinations(neighborhoods, total_ambulance):
    """
    This function returns all possible combinatios for neighborhoods and
    the number of ambulances they hold.

    Inputs:
        neighborhoods (Array of string) neighborhood names that contains ambulance stations

        total_ambulance (int) total ambulances available for use
    
    Output:
        neighborhood_ambulance_allocations (Array of Arrays of Arrays containing [string, int]) Each 
        item in the array contains an array containing all neighborhood names and the 
        number of ambulances allocated to that neighborhood in an array where the first element
        is the neighborhood name and the second the number of ambulances in that neighborhood. 
        Ex:
            [
                [["neigh_1", 3], ["neigh_2", 1], ["neigh_3", 4]],
                [["neigh_1", 2], ["neigh_2", 2], ["neigh_3", 4]],
                ...
            ]
    """
    neighborhods_number = len(neighborhoods)
    combinations = combinations_summing_to_n(neighborhods_number, total_ambulance)
    
    neighborhood_ambulance_allocations = []
    
    for comb in combinations:
        possible_allocation = []
        for n in range(neighborhods_number):
            possible_allocation.append([neighborhoods[n], comb[n]])
            
        neighborhood_ambulance_allocations.append(possible_allocation)
    return neighborhood_ambulance_allocations
    
def run_simulation(G, ambulance_allocation, location_and_assitance_distribution, steps, log):
    """
    Run a single simulation for parameters given to this function.
    """
    schedule = Schedule()
    san_francisco = City(G, ambulance_allocation, location_and_assitance_distribution, log)
    san_francisco.run(schedule)
    while schedule.now < steps:
        schedule.run_next_event()
    return san_francisco