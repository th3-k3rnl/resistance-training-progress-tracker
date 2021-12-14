# Third Party imports
import pandas as pd
import datetime as dt
import pathlib
import json

from pprint import pprint
from typing import List, Dict

# Local imports
from constants import *


"""
Workout entries to add:
    12/12/2021 Deadlifts 3 sets of 4 reps with 100kg
"""


class WorkoutEntry:
    """
    Date level Workout Entry.
    """

    def __init__(self, date: dt.datetime,
                 movement: str, weight: float, reps: List[int]) -> None:
        self.date = date
        self.movement = movement
        self.weight = weight
        self.reps = reps

    def print_workout_entry(self):
        print(f'date        = {self.date}\n'
              f'movement    = {self.movement}\n'
              f'weight      = {self.weight}\n'
              f'reps        = {self.reps}\n')

    def convert_to_lbs(self):
        return self.weight * NUM_LBS_IN_KG

    def convert_to_kgs(self):
        return self.weight / NUM_LBS_IN_KG


class Store:
    """
    Initialise an object comprising of a list of WorkoutEntry objects,
    caching the data from the store.
    """
    store_entries = []  # Dictionary of movements as keys and lists of WorkoutEntry objects

    def __init__(self, store_path: str) -> None:
        try:
            with open(store_path, 'r') as fd:
                store_contents = json.load(fd)
            self._cache_store_entries(store_contents)
        except FileNotFoundError as fnfe:
            print(f'Store does not appear to exist.\n')

    def _cache_store_entries(self, store_contents: dict) -> None:
        for movement, workout in store_contents.items():
            for date, sets in workout.items():
                for weight, reps in sets.items():
                    workout_entry = WorkoutEntry(
                        date=date, movement=movement, weight=weight, reps=reps)

                    self.store_entries.append(workout_entry)

    def add_entry(self, date: dt.datetime,
                 movement: str, weight: float, reps: List[int]) -> None:
        """
        Add a Workout Entry to the local store cache.
        """
        # TODO: Check if entry exists with supplied date and movement
        # TODO: If an entry does exist, then append the new data.
        # TODO: Else, create a new entry.
        ...

    def print_store_contents(self) -> None:
        """
        Open the data store and convert it to a list of
        WorkoutEntry objects for ease access and modification.
        """
        for entry in self.store_entries:
            entry.print_workout_entry()


def main() -> None:
    """
    The main runtime of the application.
    """
    # TODO: Argument parser

    store = Store('store.json')
    store.print_store_contents()

    # TODO: Write local store cache to the store.json when finished,
    # or when user requests to save the updates.


if __name__ == "__main__":
    main()
