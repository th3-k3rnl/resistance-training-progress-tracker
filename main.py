# Third Party imports
import pandas as pd
from datetime import datetime, date
from pathlib import Path
from argparse import ArgumentParser
import json

from pprint import pprint
from typing import List, Dict

# Local imports
from constants import *


class WorkoutEntry:
    """
    Date level Workout Entry.
    """

    # TODO: Docstring

    def __init__(self, date: datetime,
                 movement: str, weight: float, reps: List[int]) -> None:
        self.date = date
        self.movement = movement
        self.weight = weight
        self.reps = reps

    def __del__(self):
        print('Removing workout entry.')

    def print_workout_entry(self):
        print(f'date        = {self.date}\n'
              f'movement    = {self.movement}\n'
              f'weight      = {self.weight}\n'
              f'reps        = {self.reps}\n')

    def convert_to_dict(self) -> dict:
        """
        movement: {
            date: {
                weight: reps
            }
        }
        """
        return dict({
            self.movement: {
                self.date: {
                    self.weight: self.reps
                }
            }
        })

    def convert_to_lbs(self):
        return self.weight * NUM_LBS_IN_KG

    def convert_to_kgs(self):
        return self.weight / NUM_LBS_IN_KG


class Store:
    """
    Initialise an object comprising of a list of WorkoutEntry objects,
    caching the data from the store.
    """
    _store_entries = []  # Dictionary of movements as keys and lists of WorkoutEntry objects
    createOne = None

    def __init__(self, store_path: str) -> None:
        try:
            with open(store_path, 'r') as fd:
                store_contents = json.load(fd)
            self._cache_store_entries(store_contents)
        except FileNotFoundError:
            print(f'Store does not appear to exist.\n')

            # TODO: Provide options and don't allow free-form input
            create_store = input(f'Would you like to create a store?')

            # TODO: Regular expression on input
            if create_store.lower() == 'y':
                store = open(store_path, 'w')
                store.close()

    def __del__(self):
        # TODO: Write updated store date to store and destruct Store object.
        # with open(STORE_PATH, 'w') as fd:
        #     json.load()
        self._convert_store_to_dict()

    def _cache_store_entries(self, store_contents: dict) -> None:
        for movement, workout in store_contents.items():
            for date, sets in workout.items():
                for weight, reps in sets.items():
                    workout_entry = WorkoutEntry(
                        date=date, movement=movement, weight=weight, reps=reps)

                    self._store_entries.append(workout_entry)

    def _convert_store_to_dict(self) -> dict:
        for entry in self._store_entries:
            print(entry.convert_to_dict())  # TODO: Convert these entries into the JSON format ready for writing to the store.


    def add_entry(self, date: datetime,
                 movement: str, weight: float, reps: List[int]) -> None:
        """
        Add a Workout Entry to the local store cache.
        """

        """
        Workout entries to add:
            12/12/2021 Deadlifts 3 sets of 4 reps with 100kg
        """
        # Check if entry exists with user supplied date and movement
        for entry in self._store_entries:
            if entry.date == date and entry.movement == movement:
                if entry.weight == weight and entry.reps == reps:  # This might not always work with the reps as a list of ints
                    print("Entry already exists. Leaving store unchanged.")
                print("Workout entry exists. Adding sets.")
                return

        # Entry does not already exist in the store, therefore, create a new one.
        new_entry = WorkoutEntry(date=date, movement=movement, weight=weight, reps=reps)
        self._store_entries.append(new_entry)

    def get_store_entries(self) -> List[WorkoutEntry]:
        # TODO: Docstrings
        return self._store_entries

    def print_store_contents(self) -> None:
        """
        Open the data store and convert it to a list of
        WorkoutEntry objects for ease access and modification.
        """
        for entry in self._store_entries:
            entry.print_workout_entry()


def skeleton_store() -> dict:
    return {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "profile": {
            "Forename": None,
            "Surname": None,
            "Age": None,
            "Gender": None
        },
        "preferences": {
            "Training Days": {
                "Monday": None,
                "Tuesday": None,
                "Wednesday": None,
                "Thursday": None,
                "Friday": None,
                "Saturday": None,
                "Sunday": None
            }
        }
    }


def main() -> None:
    """
    The main runtime of the application.
    """
    # TODO: Argument parser

    store = Store(STORE_PATH)
    store.print_store_contents()

    store_entries = store.get_store_entries()

    # for entry in store_entries:
    #     print(entry.convert_to_dict())

    # TODO: Write local store cache to the store.json when finished,
    # or when user requests to save the updates.

    print("======="
          " UPDATES MADE "
          "=======\n")

    # 12/12/2021 Deadlifts 3 sets of 4 reps with 100kg
    store.add_entry(date=date(2021, 12, 12).isoformat(),
        movement=DEADLIFT, weight=100, reps= [4, 4, 4])

    store.print_store_contents()

    # TODO: Put the store back together in a dictionary form and write to file as a JSON object.
    # Finished updates. Flush object from runtime memory.
    del store


if __name__ == "__main__":
    main()
