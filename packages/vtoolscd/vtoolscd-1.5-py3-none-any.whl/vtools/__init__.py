"""vtools
"""
from sys import argv
import os
import subprocess
from csv import DictWriter
from tabular_log import tabular_log
from json import loads, dumps
import requests
from programGUI import programGUI

__author__ = "help@castellanidavide.it"
__version__ = "01.04 2021-04-23"


class vtools:
    def __init__(self,
                 verbose=False,
                 csv=False,
                 dbenable=False,
                 dburl=None,
                 dbtoken=None,
                 dbOStable=None,
                 dbNETtable=None,
                 dbFStable=None):
        """Where it all begins
        """
        self.setup(verbose, csv, dbenable, dburl, dbtoken, dbOStable,
                   dbNETtable, dbFStable)  # Setup all the requirements

        try:
            self.get_machines()  # Get all disponible virtualmachines
            self.core()  # Get and elaborate functions
        except BaseException:
            print("Error: make sure you have installed vbox on your PC")

    def setup(
            self,
            verbose,
            csv,
            dbenable,
            dburl,
            dbtoken,
            dbOStable,
            dbNETtable,
            dbFStable):
        """Setup
        """
        # Define main variabiles
        self.verbose = verbose
        self.csv = csv
        self.dbenable = dbenable
        self.dburl = dburl
        self.dbtoken = dbtoken
        self.dbOStable = dbOStable
        self.dbNETtable = dbNETtable
        self.dbFStable = dbFStable
        self.vboxmanage = '"C:\\Work\\VBoxManage"' if os.name == 'nt' \
            else "vboxmanage"

        # Define log
        try:
            self.log = tabular_log(
                "C:/Program Files/vtools/trace.log"
                if os.name == 'nt' else "~/trace.log", title="vtools",
                verbose=self.verbose)
        except BaseException:
            self.log = tabular_log(
                "trace.log",
                title="vtools",
                verbose=self.verbose)
        self.log.print("Created log")

        # Headers
        self.OSheader = "PC_name,OS"
        self.net_header = "PC_name,network_card_name,IPv4,MAC,Attachment"
        self.shared_files_header = "name,hostPath,writable,mount"
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

            for table, params in zip([
                self.dbOStable,
                self.dbNETtable,
                self.dbFStable
            ],
                [
                self.OSheader,
                self.net_header,
                self.shared_files_header
            ]):
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

        # If selected setup csv
        if self.csv:
            # Define files
            self.OS = "OS.csv"
            self.net = "net.csv"
            self.shared_files = "shared_files.csv"
            self.log.print("Defined CSV files' infos")

            # Create header if needed
            try:
                if open(self.OS, 'r+').readline() == "":
                    assert(False)
            except BaseException:
                open(self.OS, 'w+').write(self.OSheader + "\n")

            try:
                if open(self.net, 'r+').readline() == "":
                    assert(False)
            except BaseException:
                open(self.net, 'w+').write(self.net_header + "\n")

            try:
                if open(self.shared_files, 'r+').readline() == "":
                    assert(False)
            except BaseException:
                open(self.shared_files,
                     'w+').write(self.shared_files_header + "\n")

            self.log.print("Inizialized CSV files")

    def core(self):
        """Core of all project
        """
        for PC, PCcode in zip(
                self.vmachines, self.vmachinescodes):  # For every PC
            # OS
            try:
                OS = self.get_os(PCcode)  # Get OS

                # If CSV enabled write into csv file
                if self.csv:
                    DictWriter(
                        open(self.OS, 'a+', newline=''),
                        fieldnames=self.OSheader.split(","),
                        restval='').writerow({
                            "PC_name": PC,
                            "OS": OS
                        })

                # If DB enabled try to insert infos
                if self.dbenable:
                    try:
                        response = requests.request(
                            "POST", f"{self.dburl}",
                            headers={
                                'Content-Type': 'application/json',
                                'Authorization': f'''Basic {self.dbtoken}'''},
                            data=dumps({
                                "operation": "insert",
                                "schema": "dev",
                                "table": self.dbOStable,
                                "records": [
                                    {
                                        "PC_name": PC,
                                        "OS": OS
                                    }
                                ]
                            })
                        )
                        self.log.print(f"By DB: {response.text}")
                    except BaseException:
                        self.log.print(f"Failed the DB insert")
            except BaseException:
                self.log.print(f"Error taking {PC} OS")

            # NET
            for i in self.get_net(PCcode):
                try:
                    net = {"PC_name": PC}
                    for key, value in zip(self.net_header.split(",")[1:], i):
                        net[key] = value

                    # If CSV enabled write into csv file
                    if self.csv:
                        DictWriter(
                            open(self.net, 'a+', newline=''),
                            fieldnames=self.net_header.split(","),
                            restval='').writerow(net)

                    # If DB enabled try to insert infos
                    if self.dbenable:
                        try:
                            response = requests.request(
                                "POST", f"{self.dburl}",
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization':
                                        f'''Basic {self.dbtoken}'''
                                }, data=dumps({
                                    "operation": "insert",
                                    "schema": "dev",
                                    "table": self.dbNETtable,
                                    "records": [net]
                                })
                            )
                            self.log.print(f"By DB: {response.text}")
                        except BaseException:
                            self.log.print(f"Failed the DB insert")
                except BaseException:
                    self.log.print(f"Error taking {PC} network ifos")

            self.log.print("Stored into csv file(s)")

            # Shared files
            try:
                shared_files = self.get_sharedfolders(PCcode)

                # If CSV enabled write into csv file
                if self.csv:
                    DictWriter(
                        open(self.shared_files, 'a+', newline=''),
                        fieldnames=self.shared_files_header.split(","),
                        restval=''
                    ).writerows(
                        shared_files
                    )

                # If DB enabled try to insert infos
                if self.dbenable:
                    try:
                        response = requests.request(
                            "POST",
                            f"{self.dburl}",
                            headers={
                                'Content-Type': 'application/json',
                                'Authorization': f'''Basic {self.dbtoken}'''
                            },
                            data=dumps(
                                {
                                    "operation": "insert",
                                    "schema": "dev",
                                    "table": self.dbFStable,
                                    "records": shared_files
                                }
                            )
                        )
                        self.log.print(f"By DB: {response.text}")
                    except BaseException:
                        self.log.print(f"Failed the DB insert")
            except BaseException:
                self.log.print(f"Error taking {PC} OS")

    def get_machines(self):
        """Get virtual machines' name
        """
        # Some variabiles
        self.vmachines = []
        self.vmachinescodes = []
        temp = ""
        take = False
        temp2 = ""
        take2 = False

        # Get and elaborate the output
        for i in self.get_output(["list", "vms"]):
            if i == '"':
                if take:
                    self.vmachines.append(temp)
                    temp = ""
                take = not take
            elif take:
                temp += i

            if i == '{' or i == '}':
                if take2:
                    self.vmachinescodes.append(temp2)
                    temp2 = ""
                take2 = not take2
            elif take2:
                temp2 += i

        self.log.print(f"Get VM names {self.vmachines} {self.vmachinescodes}")

    def get_output(self, array):
        """ Gets the output by the shell
        """
        if os.name == 'nt':  # If OS == Windows
            cmd = self.vboxmanage
            for i in array:
                if " " in i:
                    i = "'" + i + "'"
                cmd += " " + i

            return vtools.remove_b(subprocess.check_output(cmd, shell=False))
        else:
            return vtools.remove_b(
                subprocess.Popen([self.vboxmanage] + array,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE
                                 ).communicate()[0])

    def get_os(self, machine_name):
        """ Gets the vitual machine os
        """
        OS = self.get_output(
            [
                "guestproperty",
                "get",
                machine_name,
                "/VirtualBox/GuestInfo/OS/Product"
            ]).replace("Value: ", "").replace("\\n", "").replace("\\r", "")
        self.log.print(f"Getted OS {OS}")
        return OS

    def remove_b(string):
        """Removes b'' by string
        """
        return str(string).replace("b'", "")[:-1:]

    def get_net(self, machine_name):
        """ Gets the vitual machine network's infos
        """
        network = []
        temp = []
        attachments = self.get_attachments(machine_name)
        self.get_sharedfolders(machine_name)
        vbox_net = "/VirtualBox/GuestInfo/Net/"

        try:
            propriety = "Count"

            for i in range(int(self.get_output(
                [
                    "guestproperty",
                    "get",
                    machine_name,
                    f"{vbox_net}{propriety}"
                ]
            ).replace("Value: ", "").replace("\\n", "").replace("\\r", ""))):
                for propriety in ["Name", "V4/IP", "MAC"]:
                    temp.append(
                        vtools.remove_b(
                            self.get_output(
                                [
                                    "guestproperty",
                                    "get",
                                    machine_name,
                                    f"{vbox_net}{i}/{propriety}"
                                ]
                            ).replace("Value: ", "").replace(
                                "\\n", "").replace("\\r", "")))

                network.append(temp + [attachments[i]])
                temp = []
        except BaseException:
            pass

        self.log.print(f"Getted network infos {network}")
        return network

    def get_attachments(self, machine_name):
        """ Gets the vitual machine attachment
        """
        attachments = []

        for i in self.get_output(["showvminfo", machine_name]).replace(
                "\\r", "").split("\\n"):
            if "NIC" in i and "disabled" not in i:
                for j in i[i.find('MAC'):].split(", "):
                    if "Attachment" in j:
                        attachments.append(j.replace("Attachment: ", ""))

        self.log.print("Getted attachments")
        return attachments

    def get_sharedfolders(self, machine_name):
        """ Gets the vitual machine attachment
        """
        take = False
        shared_folders = []

        for i in self.get_output(["showvminfo", machine_name]).replace(
                "\\r", "").split("\\n"):
            if "Shared folders:" in i:
                take = True

            if "Capturing:" in i:
                take = False

            i = i.replace(
                "Shared folders:",
                "").replace(
                "<none>",
                "").replace(
                "\\\\",
                "\\").replace(
                "Name: ",
                "").replace(
                    "Host path: ",
                    "").replace(
                        " (machine mapping)",
                "")
            if take and len(i) != 0:
                temp = {}
                for key, value in zip(
                    ["name", "hostPath", "writable", "mount"],
                        i.split(", ")):
                    temp[key] = value.replace("'", "")
                shared_folders.append(temp)

        return shared_folders


def laucher():
    """ Lauch all getting the params by the arguments passed on launch
    """
    # Get all arguments
    if "--help" in argv or "-h" in argv:
        print(
            "To get an help to know how to use"
            "this program write into the shell:"
            "'man agentless', only for Linux.")
    elif "--batch" in argv or "-b" in argv:
        debug = "--debug" in argv or "-d" in argv
        csv = "--csv" in argv
        dbenable = dburl = dbtoken = dbOStable = dbNETtable = dbFStable = None

        for arg in argv:
            if "--url=" in arg:
                dburl = arg.replace("--url=", "")
            if "--token=" in arg:
                dbtoken = arg.replace("--token=", "")
            if "--OStable=" in arg:
                dbOStable = arg.replace("--OStable=", "")
            if "--NETtable=" in arg:
                dbNETtable = arg.replace("--NETtable=", "")
            if "--FStable=" in arg:
                dbFStable = arg.replace("--FStable=", "")

        # Launch the principal part of the code
        if dburl is not None and \
           dbtoken is not None and \
           dbOStable is not None and \
           dbNETtable is not None and \
           dbFStable is not None:
            vtools(
                debug,
                csv,
                True,
                dburl,
                dbtoken,
                dbOStable,
                dbNETtable,
                dbFStable)
        else:
            vtools(debug, csv)
    else:
        gui = programGUI(title="vtools", instructions=[
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
                    "title": "Insert OS table name:",
                    "id": "OStable"
                },
                {
                    "type": "text",
                    "title": "Insert NET table name:",
                    "id": "NETtable"
                },
                {
                    "type": "text",
                    "title": "Insert Shared-Folder table name:",
                    "id": "SFtable"
                }
            ]
        ])

        if gui.get_values()["url"] is not None and \
                gui.get_values()["token"] is not None and \
                gui.get_values()["OStable"] is not None and \
                gui.get_values()["NETtable"] is not None:
            vtools(
                gui.get_values()["verbose"],
                gui.get_values()["csv"],
                True,
                gui.get_values()["url"],
                gui.get_values()["token"],
                gui.get_values()["OStable"],
                gui.get_values()["NETtable"],
                gui.get_values()["SFtable"]
            )
        else:
            vtools(
                gui.get_values()["verbose"],
                gui.get_values()["csv"]
            )


if __name__ == "__main__":
    laucher()
