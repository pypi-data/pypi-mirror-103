"""produttore_e_consumatore2
"""
from sys import argv
import os
import subprocess
from csv import DictWriter
from tabular_log import tabular_log
from json import loads, dumps
import requests
from programGUI import programGUI
from time import sleep
from random import random
from multiprocessing import Process, Lock, Manager
from psutil import Process as Pprocess
from threading import Thread, active_count
from ctypes import c_char_p, c_int

__author__ = "help@castellanidavide.it"
__version__ = "01.01 2021-04-28"


class produttore_e_consumatore2:
    def __init__(self,
                 verbose=False,
                 csv=False,
                 choise="single",
                 dbenable=False,
                 dburl=None,
                 dbtoken=None,
                 dbtable=None):
        """Where it all begins
        """
        self.setup(verbose, csv, choise, dbenable, dburl,
                   dbtoken, dbtable)  # Setup all the requirements

        self.core()  # Try to run the core
        try:
            pass
        except BaseException:
            print("Error :(")

        self.end()

    def setup(self, verbose, csv, choise, dbenable, dburl, dbtoken, dbtable):
        """Setup
        """
        # Define main variabiles
        self.verbose = verbose
        self.csv = csv
        self.choise = choise
        self.dbenable = dbenable
        self.dburl = dburl
        self.dbtoken = dbtoken
        self.dbtable = dbtable
        self.list_len = 10
        self.locks = [Lock()] * self.list_len
        self.values = []
        for _ in range(self.list_len):
            self.values.append(Manager().Value(c_char_p, None))
        self.pLeft = Manager().Value(c_int, 0)

        # Define log
        try:
            self.log = tabular_log(
                "C:/Program Files/produttore_e_consumatore2/trace.log"
                if os.name == 'nt' else "~/trace.log",
                title="produttore_e_consumatore2", verbose=self.verbose)
        except BaseException:
            self.log = tabular_log(
                "trace.log", title="produttore_e_consumatore2",
                verbose=self.verbose)
        self.log.print("Created log")

        # Headers
        self.multiprocessing_header = "CP,msg"
        self.log.print("Headers inizialized")

        # Inizialize DB
        if self.dbenable:
            try:
                response = requests.request(
                    "POST", f"{self.dburl}",
                    headers={
                            'Content-Type': 'application/json',
                        'Authorization': f'''Basic {self.dbtoken}'''},
                    data=dumps({
                        "operation": "create_schema",
                        "schema": "dev"
                    })
                )
                self.log.print(f"By DB: {response.text}")
            except BaseException:
                self.log.print(f"Failed to create dev schema")

            for table, params in zip([self.dbtable],
                                     [self.multiprocessing_header]):
                try:
                    response = requests.request(
                        "POST", f"{self.dburl}",
                        headers={
                                'Content-Type': 'application/json',
                            'Authorization': f'''Basic {self.dbtoken}'''},
                        data=dumps({
                            "operation": "create_table",
                            "schema": "dev",
                            "table": table,
                            "hash_attribute": "id"
                        })
                    )
                    self.log.print(f"By DB: {response.text}")
                except BaseException:
                    self.log.print(f"Failed to create {table} table")

                for param in params.split(","):
                    try:
                        response = requests.request(
                            "POST", f"{self.dburl}",
                            headers={
                                    'Content-Type': 'application/json',
                                'Authorization': f'''Basic {self.dbtoken}'''},
                            data=dumps({
                                "operation": "create_attribute",
                                "schema": "dev",
                                "table": table,
                                "attribute": param
                            })
                        )
                        self.log.print(f"By DB: {response.text}")
                    except BaseException:
                        self.log.print(
                            f"Failed to create {param} into {table} table")
            self.log.print("Inizialized DB")

        # If selected setup csv
        if self.csv:
            # Define files
            self.multiprocessing = "multiprocessing.csv"
            self.log.print("Defined CSV files' infos")

            # Create header if needed
            try:
                if open(self.multiprocessing, 'r+').readline() == "":
                    assert(False)
            except BaseException:
                open(self.multiprocessing,
                     'w+').write(self.multiprocessing_header + "\n")

            self.log.print("Inizialized CSV files")

    def core(self):
        """Core of all project
        """
        processes = []

        if self.choise == "singular":
            processes.append(
                Process(
                    target=self.produttore,
                    args=(
                        0,
                        "singular")))
            processes.append(Process(target=self.consumatore, args=(0,)))
            self.pLeft.value = 1 * 2
        elif self.choise == "linear":
            for i in range(len(self.values)):
                processes.append(
                    Process(
                        target=self.produttore,
                        args=(i, f"linear #{i}")))
                processes.append(
                    Process(
                        target=self.consumatore,
                        args=(i,)))
            self.pLeft.value = len(self.values) * 2
        elif self.choise == "circular":
            for i in range(5 * len(self.values)):
                processes.append(
                    Process(
                        target=self.produttore,
                        args=(i % len(self.values),
                              f"circular #{i}")))
                processes.append(
                    Process(
                        target=self.consumatore,
                        args=(i % len(self.values),)))
            self.pLeft.value = 5 * len(self.values) * 2

        self.log.print("Setuped processes")

        for process in processes:
            process.start()

        self.log.print("Started processes")

        while self.pLeft.value != 0 or active_count() != 1:
            pass

        sleep(1)  # Wait a while for the DB/ csv print(s)

        self.log.print("Finished processes")

    def produttore(self, index, value):
        """productor
        """
        sleep(random() / 10)

        try:
            with self.locks[index]:
                assert(self.values[index].value is None)
                self.values[index].value = value
                Thread(
                    target=self.write,
                    args=(
                        "productor",
                        "{index: " +
                        str(index) +
                        ", value: " +
                        str(value) +
                        "}")).start()
                self.pLeft.value -= 1
        except BaseException:
            Process(target=self.produttore, args=(index, value)).start()

    def consumatore(self, index):
        """consumer
        """
        sleep(random() / 10)

        try:
            with self.locks[index]:
                assert(self.values[index].value is not None)
                Thread(
                    target=self.write,
                    args=("consumer", "{index: " + str(index) + ", value: " +
                          str(self.values[index].value) + "}")).start()
                self.values[index].value = None  # Reset value
                self.pLeft.value -= 1
        except BaseException:
            Process(target=self.consumatore, args=(index,)).start()

    def write(self, consumer_productor, message):
        """Write everywhere
        """
        self.log.print(f"{consumer_productor}: {message}")

        msg = {
            "CP": consumer_productor,
            "msg": message
        }

        try:
            # If CSV enabled write into csv file
            if self.csv:
                DictWriter(
                    open(self.multiprocessing, 'a+', newline=''),
                    fieldnames=self.multiprocessing_header.split(","),
                    restval='').writerow(msg)

            # If DB enabled try to insert infos
            if self.dbenable:
                try:
                    response = requests.request(
                        "POST", f"{self.dburl}",
                        headers={
                                'Content-Type': 'application/json',
                                'Authorization': f'''Basic {self.dbtoken}'''
                        },
                        data=dumps({
                            "operation": "insert",
                            "schema": "dev",
                            "table": self.dbtable,
                            "records": [msg]
                        })
                    )
                    self.log.print(f"By DB: {response.text}")
                except BaseException:
                    self.log.print(f"Failed the DB insert")
        except BaseException:
            self.log.print(f"Error writing...")

    def end(self):
        """End logo
        """
        self.log.print("End")

        print()
        print("I hope this tool help you.")
        print("If you want see the project you can find it: "
              "https://github.com/CastellaniDavide/produttore_e_consumatore2")
        print()
        print("Made w/ ❤️ by Castellani Davide")


def laucher():
    """ Lauch all getting the params by the arguments passed on launch
    """
    # Get all arguments
    if "--help" in argv or "-h" in argv:
        print("To get an help to know how to use"
              "this program write into the shell:"
              "'man agentless', only for Linux.")
    elif "--batch" in argv or "-b" in argv:
        debug = "--debug" in argv or "-d" in argv
        csv = "--csv" in argv
        dbenable = dburl = dbtoken = dbtable = None
        choise = "singular"

        for arg in argv:
            if "--url=" in arg:
                dburl = arg.replace("--url=", "")
            if "--token=" in arg:
                dbtoken = arg.replace("--token=", "")
            if "--table=" in arg:
                dbtable = arg.replace("--table=", "")
            if "--choise=" in arg:
                choise = arg.replace("--choise=", "")

        # Launch the principal part of the code
        if dburl is not None and \
           dbtoken is not None and \
           dbtable is not None:
            produttore_e_consumatore2(
                debug, csv, choise, True, dburl, dbtoken, dbtable)
        else:
            produttore_e_consumatore2(debug, csv, choise)
    else:
        gui = programGUI(title="produttore_e_consumatore2", instructions=[
            [
                {
                    "type": "bool",
                    "title": "Want you to run it in the verbose mode?",
                    "id": "verbose"
                },
                {
                    "type": "bool",
                    "title": "Want you have a csv output?",
                    "id": "csv"
                },
                {
                    "type": "list",
                    "title": "Choose your opinion",
                    "id": "choise",
                    "options": [
                            "singular",
                            "linear",
                            "circular"
                    ]
                }
            ],
            [
                {
                    "type": "text",
                    "title": "Insert url:",
                    "id": "url"
                },
                {
                    "type": "text",
                    "title": "Insert token:",
                    "id": "token"
                },
                {
                    "type": "text",
                    "title": "Insert table name:",
                    "id": "table"
                }
            ]
        ])

        if gui.get_values()["url"] != "" and gui.get_values()[
                "token"] != "" and gui.get_values()["table"] != "":
            produttore_e_consumatore2(
                gui.get_values()["verbose"],
                gui.get_values()["csv"],
                gui.get_values()["choise"],
                True,
                gui.get_values()["url"],
                gui.get_values()["token"],
                gui.get_values()["table"]
            )
        else:
            produttore_e_consumatore2(
                gui.get_values()["verbose"],
                gui.get_values()["csv"],
                gui.get_values()["choise"]
            )


if __name__ == "__main__":
    laucher()
