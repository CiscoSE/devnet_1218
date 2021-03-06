import requests
from tabulate import tabulate

from jinja2 import Environment
from jinja2 import FileSystemLoader
import os

# Suppress https security warnings
requests.packages.urllib3.disable_warnings()

# Static variables

# Base vManage URL
VMANAGE_URL = "https://198.18.1.10/"

# IMPORTANT: Credentials are hardcoded for training purpose only. DO NOT DO THIS IN PRODUCTION
HTTP_HEADERS = {
    'Content-Type': "application/json",
    'Authorization': "Basic YWRtaW46YWRtaW4="
}

# Templates. Needed to render json payloads in POST requests
DIR_PATH = os.path.dirname((os.path.realpath(__file__)))
JSON_TEMPLATES = Environment(loader=FileSystemLoader(DIR_PATH + '/json_templates'))


def PrintMenu():
    """
    Print menu in console
    :return:
    """
    print("Please choose one option and press return: ")
    print("1- Get devices")
    print("2- Get control policies")
    print("3- Get VPN List Policies")
    print("4- Get Site List Policies")
    print("5- Get centralized policies")
    print("6- Create FW Insertion Policy ")
    print("7- Get interface statistics ")
    print("8- Exit")


# ********* Option 1 - Get Devices




# ********* Option 2 - Get Control Policies




# ********* Option 3 - Get VPN List Policies




# ********* Option 4 - Get Site List Policies




# ********* Option 5 - Get Centralized Policies




# ********* Option 6 - Create FW Insertion Policy




# ********* Option 7 - - Get Interface Statistics







# ********* DO NOT MODIFY CODE BELOW *********

if __name__ == "__main__":
    """
    Entry point for the application
    """
    while True:
        # Keep they loop running until is manually canceled with ctrl+c or option 10.
        try:
            PrintMenu()

            # Read option
            option = raw_input().strip()

            # Check option selection. If something needs to be printed, use tabulate for a more readable output

            if option == "1":
                # Get and print devices
                result = GetDevices()
                devices = []
                for device in result["data"]:
                    devices.append([device["host-name"], device["device-type"], device["system-ip"], device["state"]])
                print("\nDevices:\n")
                print(tabulate(devices, headers=['Device Name', 'Type', 'IP', 'State']))
                print("\n")

            elif option == "2":
                # Get and print Control policies
                result = GetControlPolicies()
                policies = []
                for policy in result["data"]:
                    policies.append([policy["name"], policy["description"], policy["type"], policy["definitionId"]])
                print("\nControl Policies:\n")
                print(tabulate(policies, headers=['Policy Name', 'Description', 'Type', 'ID']))
                print("\n")

            elif option == "3":
                # Get and VPN List policies
                result = GetVPNListPolicies()
                vpn_list = []
                for vpn in result["data"]:
                    vpn_entries = []
                    for entry in vpn["entries"]:
                        vpn_entries.append(entry["vpn"])

                    vpn_list.append([vpn["name"], vpn_entries, vpn["type"], vpn["listId"]])
                print("\nVPN List Policies:\n")
                print(tabulate(vpn_list, headers=['VPN Name', 'Entries', 'Type', 'ID']))
                print("\n")

            elif option == "4":
                # Get and site list policies
                result = GetSiteListPolicies()
                site_list = []
                for site in result["data"]:
                    site_entries = []
                    for entry in site["entries"]:
                        site_entries.append(entry["siteId"])

                    site_list.append([site["name"], site_entries, site["type"], site["listId"]])
                print("\nSite List Policies:\n")
                print(tabulate(site_list, headers=['Site List Name', 'Entries', 'Type', 'ID']))
                print("\n")

            elif option == "5":
                # Get and print Centralized Policies
                result = GetCentralizedPolicies()
                centralized_policies = []
                for policy in result["data"]:
                    centralized_policies.append([
                        policy["policyName"],
                        policy["policyDescription"],
                        policy["isPolicyActivated"],
                        policy["policyId"]])
                print("\nCentralized vSmart Policies:\n")
                print(tabulate(centralized_policies, headers=['Policy Name', 'Description', 'Is Active?', 'ID']))
                print("\n")
            elif option == "6":
                # Create a pre-defined firewall centralized policy
                CreateFWCentralizedPolicy()

            elif option == "7":
                # Get and print interface statistics
                result = GetInterfaceStatistics()
                if_statistics = []
                for if_statistic in result["data"][:10]:
                    if_statistics.append([
                        if_statistic["host_name"],
                        if_statistic["interface"],
                        if_statistic["oper_status"],
                        if_statistic["tx_pkts"],
                        if_statistic["tx_errors"],
                        if_statistic["rx_pkts"],
                        if_statistic["rx_errors"]])

                print("\nInterface statistics (First 10 results):\n")
                print(tabulate(if_statistics,
                               headers=['Device', 'Interface', 'Status', 'TX Pkts', 'TX Errors', 'RX Pkts',
                                        'RX Errors']))
                print("\n")

            elif option == "8":
                # Exit the application
                exit(0)
            else:
                # Check for invalid inputs
                print("Invalid Option")
        except Exception as e:
            # Check for unexpected errors
            print("Error occurred: " + str(e))

        # Wait for a return before printing the menu again
        print("Press return to come back to the main menu.")
        raw_input()
