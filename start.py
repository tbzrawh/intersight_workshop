#!/usr/bin/env python3    

import intersight
from intersight.intersight_api_client import IntersightApiClient
import json
import sys

api_key_file = "api.txt"
api_secret_file = "SecretKey.txt"

if __name__ == "__main__":
    print("Intersight Workshop")
    # step 1 - get keys
    # add file api.txt and SecretKey.txt to the folder

    # step 2 - install sdk, create auth
    # python3 -m pip install git+https://github.com/CiscoUcs/intersight-python.git
    api_key = ""
    with open(api_key_file) as file:
        api_key = file.read()
        api_key = api_key.strip()
    api_instance = IntersightApiClient(
        private_key=api_secret_file,
        api_key_id=api_key
    )
    #Require Argument to allow different options in script
    if len(sys.argv) < 2:    
        print("more arguments required")    
        sys.exit()
    cmd = sys.argv[1]
    #API Useage Example for Organization
    if cmd == "org":
        orgAPI = intersight.OrganizationOrganizationApi(api_instance)
        orgs = orgAPI.organization_organizations_get()
        for org in orgs.results:
            print("Name: {}, MOID: {}".format(org.name, org.moid))

    if cmd == "show":
        print("Liste Rackserver")
