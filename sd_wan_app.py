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
def GetDevices():
    """
    Returns all devices registered in vManage
    :return: dictionary with devices data
    """
    # Define URL
    url = VMANAGE_URL + "dataservice/device"

    print("Getting devices from " + url)

    # Make http GET request
    response = requests.request("GET", url, headers=HTTP_HEADERS, verify=False)

    # Check for errors
    if response.status_code < 200 or response.status_code > 299:
        raise Exception("Error trying to fetch devices: " + response.text)

    return response.json()


# ********* Option 2 - Get Control Policies
def GetControlPolicies():
    """
    Returns all control policies in vManage
    :return: dictionary with control policies data
    """
    # Define URL
    url = VMANAGE_URL + "dataservice/template/policy/definition/control/"

    print("Getting control policies from " + url)

    # Make http GET request
    response = requests.request("GET", url, headers=HTTP_HEADERS, verify=False)

    # Check for errors
    if response.status_code < 200 or response.status_code > 299:
        raise Exception("Error trying to fetch control policies: " + response.text)

    return response.json()


# ********* Option 3 - Get VPN List Policies

def GetVPNListPolicies():
    """
    Returns VPN list policies in vManage
    :return: dictionary with VPN list policies data
    """
    # Define URL
    url = VMANAGE_URL + "dataservice/template/policy/list/vpn/"

    print("Getting VPN list policies from " + url)

    # Make http GET request
    response = requests.request("GET", url, headers=HTTP_HEADERS, verify=False)

    # Check for errors
    if response.status_code < 200 or response.status_code > 299:
        raise Exception("Error trying to fetch VPN list: " + response.text)

    return response.json()


# ********* Option 4 - Get Site List Policies
def GetSiteListPolicies():
    """
    Returns site policies in vManage
    :return: dictionary with site policies data
    """
    # Define URL
    url = VMANAGE_URL + "dataservice/template/policy/list/site/"

    print("Getting Site list policies from " + url)

    # Make http GET request
    response = requests.request("GET", url, headers=HTTP_HEADERS, verify=False)

    # Check for errors
    if response.status_code < 200 or response.status_code > 299:
        raise Exception("Error trying to fetch site list: " + response.text)

    return response.json()


# ********* Option 5 - Get Centralized Policies

def GetCentralizedPolicies():
    """
    Returns all the centralized/vsmart policies
    :return: dictionary with centralized/vsmart policy data
    """

    # Define URL
    url = VMANAGE_URL + "dataservice/template/policy/vsmart/"

    print("Getting centralized vsmart policies from " + url)

    # Make http GET request
    response = requests.request("GET", url, headers=HTTP_HEADERS, verify=False)

    # Check for errors
    if response.status_code < 200 or response.status_code > 299:
        raise Exception("Error trying to fetch site list: " + response.text)

    return response.json()


# ********* Option 6 - Create FW Insertion Policy
def CreateFWCentralizedPolicy():
    """
    Creates a centralized policy that forwards all the traffic to a firewall in one of the datacenters
    :return: None
    """

    # Define variables to store selected policies and lists
    selected_control_policies = []
    selected_data_policies = []
    selected_vpn_mem_policies = []
    selected_site_list = []

    print("Looking for needed site list...")
    # Look for AllBranches site list and append it to selected_site_list
    site_lists = GetSiteListPolicies()
    for site_list in site_lists["data"]:
        if site_list["name"] == "AllBranches":
            selected_site_list.append(site_list["listId"])
            break


    print("Looking for needed control policies...")
    # Look for MultiTopologyFWInsertion control policy and append it to selected_control_policies
    control_policies = GetControlPolicies()
    for control_policy in control_policies["data"]:
        if control_policy["name"] == "MultiTopologyFWInsertion":
            control_policy["siteLists"] = selected_site_list
            selected_control_policies.append(control_policy)
            break

    # Define URL
    url = VMANAGE_URL + "dataservice/template/policy/vsmart/"

    print("Creating vSmart new policy via " + url)
    # Render the payload with the data gathered
    template = JSON_TEMPLATES.get_template('create_vsmart_fw_policy.j2.json')
    payload = template.render(policy_name="FWInsertionVPN10-API",
                              data_policies=selected_data_policies,
                              control_policies=selected_control_policies,
                              vpn_member_group_policies=selected_vpn_mem_policies
                              ).replace("\n", "")

    # Make http POST request
    response = requests.request("POST", url, headers=HTTP_HEADERS, data=payload, verify=False)

    # Check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("Error trying to create FW vSmart policy: " + response.text)
    else:
        print("Policy created!")

    # Look for a centralized policy named FWInsertionVPN10-API. If found print the ID
    centralized_policies = GetCentralizedPolicies()["data"]
    for policy in centralized_policies:
        if policy["policyName"] == "FWInsertionVPN10-API":
            print ("ID:")
            print (policy["policyId"])





# ********* Option 7 - - Get Interface Statistics

def GetInterfaceStatistics():
    """
    Returns all interface statistics
    :return: dictionary with statistics
    """
    # Define URL
    url = VMANAGE_URL + "dataservice/statistics/interface/"

    print("Getting interface statistics from " + url)

    # Make http GET request
    response = requests.request("GET", url, headers=HTTP_HEADERS, verify=False)

    # Check for errors
    if response.status_code < 200 or response.status_code > 299:
        raise Exception("Error trying to fetch site list: " + response.text)

    return response.json()


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
