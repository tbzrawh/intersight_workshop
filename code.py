# Uebung 1 --> in Intersight


# Uebung 2
import intersight
from intersight.intersight_api_client import IntersightApiClient
import json

api_instance = IntersightApiClient(
    private_key="./SecretKey.txt",
    api_key_id="EIGENE_KEY_ID_HIER_EINFÜGEN",
)


# Uebung 3
rackApi = intersight.ComputeRackUnitApi(api_instance)
rack_servers = rackApi.compute_rack_units_get()

for server in rack_servers.results:
    print('Serial: {}, MOID: {}, Model: {}'.format(server.serial,server.model,server.moid))


# Uebung 4
faultApi = intersight.FaultInstanceApi(api_instance)
faults = faultApi.fault_instances_get()

for fault in faults.results:
    if fault.severity in ['critical', 'major']:
        print('{} - {}'.format(fault.ancestor_mo_id,fault.description))


# Uebung 5
for fault in faults.results:
    if fault.affected_mo_type == 'memory.Unit':
        for server in rack_servers.results:
            if(server.moid == fault.ancestor_mo_id):
                print('Broken DIMM on server with serial {}'.format(server.serial))


# Uebung 6
profileApi = intersight.ServerProfileApi(api_instance)

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

profileApi.server_profiles_post(body=profile)

server_profiles = profileApi.server_profiles_get()

for profile in server_profiles.results:
    if profile.name == 'workshop-profile':
        profile_moid = profile.moid


# Uebung 7
ntpApi = intersight.NtpPolicyApi(api_instance)

policy = {
      "Description": "",
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


# Uebung 8 --> in Intersight
