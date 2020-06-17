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
        rackApi = intersight.ComputeRackUnitApi(api_instance)
        rack_servers = rackApi.compute_rack_units_get()
        for server in rack_servers.results:
            print('Serial: {}, MOID: {}, Model: {}'.format(server.serial,server.model,server.moid))

        print("Liste Faults")
        faultApi = intersight.FaultInstanceApi(api_instance)
        faults = faultApi.fault_instances_get()
        for fault in faults.results:
            if fault.severity in ['critical', 'major']:
                print('{} - {}'.format(fault.ancestor_mo_id,fault.description))
            if fault.affected_mo_type == 'memory.Unit':
                for server in rack_servers.results:
                    if(server.moid == fault.ancestor_mo_id):
                        print('Broken DIMM on server with serial {}'.format(server.serial))
    if cmd == "profile":
        print("Creating Server Profile")
        profile =     { 
      "Description": "",            
      "Name": "workshop-profile",
      "Type": "instance",
      "Action": "No-op",                  
      "ConfigContext": {                     
        "ClassId": "policy.ConfigContext",   
        "ObjectType": "policy.ConfigContext",
        "ConfigState": "Not-assigned",
        "ControlAction": "No-op",
        "ErrorState": "",
        "OperState": ""
      },                                 
      "ConfigChanges": {                    
        "ClassId": "policy.ConfigChange",   
        "ObjectType": "policy.ConfigChange",
        "Changes": [],   
        "Disruptions": []
      },                                        
      "IsPmcDeployedSecurePassphraseSet": False,  
      "Organization": {                           
        "ObjectType": "organization.Organization",
        "ClassId": "mo.MoRef",                                                                          
        "Moid": "5ee612af6972652d33271daf",                                                            
        "link": "https://www.intersight.com/api/v1/organization/Organizations/5ee612af6972652d33271daf"
      }
    }
        profileApi = intersight.ServerProfileApi(api_instance)
        profileApi.server_profiles_post(body=profile)

    if cmd == "ntp":
        print("ntp find profile")
        profile_moid = ""
        profileApi = intersight.ServerProfileApi(api_instance)
        server_prfoiles = profileApi.server_profiles_get()
        for profile in server_prfoiles.results:
            if profile.name == "workshop-profile":
                profile_moid = profile.moid

        print("create ntp policy")
        ntpApi = intersight.NtpPolicyApi(api_instance)
        policy = {
      "ObjectType": "ntp.Policy",
      "ClassId": "ntp.Policy",
      "Description": "API",
      "Name": "workshop-ntp-policy",
      "Enabled": True,
      "NtpServers": [
        "pool.ntp.org"
      ],
      "Organization": {
        "ObjectType": "organization.Organization",
        "ClassId": "mo.MoRef",
        "Moid": "5ee612af6972652d33271daf",
        "link": "https://www.intersight.com/api/v1/organization/Organizations/5ee612af6972652d33271daf"
      },
      "Profiles": [
        {
          "ObjectType": "server.Profile",
          "ClassId": "mo.MoRef",
          "Moid": profile_moid,
          "link": "https://www.intersight.com/api/v1/server/Profiles/{}".format(profile_moid)
        }
      ]
    }
        ntpApi.ntp_policies_post(body=policy)

