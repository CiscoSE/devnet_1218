import requests
from tabulate import tabulate

from jinja2 import Environment
from jinja2 import FileSystemLoader
import os

requests.packages.urllib3.disable_warnings()

VMANAGE_URL = "https://198.18.1.10/"
HTTP_HEADERS = {
    'Content-Type': "application/json",
    'Authorization': "Basic YWRtaW46YWRtaW4="
}
DIR_PATH = os.path.dirname((os.path.realpath(__file__)))
JSON_TEMPLATES = Environment(loader=FileSystemLoader(DIR_PATH + '/json_templates'))


def PrintMenu():
    print("Please choose one option: ")
    print("1- Get devices")
    print("2- Get control policies")
    print("3- Get vpn memberships policies")
    print("4- Get data policies")
    print("5- Get VPN List Policies")
    print("6- Get Site List Policies")
    print("7- Get centralized policies")
    print("8- Create FW Insertion Policy ")
    print("9- Get interface statistics ")
    print("10- Exit")


def GetDevices():
    raise Exception("Not Implemented")


def GetControlPolicies():
    raise Exception("Not Implemented")


def GetVPNMembershipPolicies():
    raise Exception("Not Implemented")


def GetDataPolicies():
    raise Exception("Not Implemented")


def GetVPNListPolicies():
    raise Exception("Not Implemented")


def GetSiteListPolicies():
    raise Exception("Not Implemented")


def CreateFWCentrilizedPolicy():
    raise Exception("Not Implemented")


def GetCentralizedPolicies():
    raise Exception("Not Implemented")


def ActivatePolicy(policyId):
    raise Exception("Not Implemented")


def GetInterfaceStatistics():
    raise Exception("Not Implemented")


if __name__ == "__main__":
    while True:
        try:
            PrintMenu()
            option = raw_input().strip()
            if option == "1":
                result = GetDevices()

            elif option == "2":
                result = GetControlPolicies()


            elif option == "3":
                result = GetVPNMembershipPolicies()


            elif option == "4":
                result = GetDataPolicies()

            elif option == "5":
                result = GetVPNListPolicies()

            elif option == "6":
                result = GetSiteListPolicies()

            elif option == "7":
                result = GetCentralizedPolicies()

            elif option == "8":
                CreateFWCentrilizedPolicy()

            elif option == "9":
                result = GetInterfaceStatistics()


            elif option == "10":
                exit(0)
            else:
                print("Invalid Option")
        except Exception as e:
            print("Error occurred: " + str(e))

        print("Press return to come back to the main menu.")
        raw_input()


