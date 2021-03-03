#!/usr/bin/env python3

### vvvvvv USER SETTINGS vvvvvv

### these are mandatory
Tenant_Name  = "aaa3441.my.centrify-kibble.net"
Scope_Name   = "admin"

### you must provide either Folder_Name and Secret_Name, OR provide the Secret_ID
Folder_Name = "RedBank"
Secret_Name = "myAPI"
Secret_ID = ""

### ^^^^^^^ USER SETTINGS ^^^^^^

###############################################

from dmc import gettoken
import os
import sys
import http.client
import json
import logging

#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

headers = {
    "X-CENTRIFY-NATIVE-CLIENT": "true",
    "X-CFY-SRC": "python",
    "Authorization": "Bearer %s" % gettoken(Scope_Name)
}
conn = http.client.HTTPSConnection(Tenant_Name)

### get PAS VERSION
conn.request("POST", "/Sysinfo/Version", headers = headers)

response = conn.getresponse()
if (response.status != 200):
    logger.error("Response status: %d", response.status)
    logger.error("Failed to connect to Tenant " + Tenant_Name)
    sys.exit(1)

logger.info("SUCCESS: Connected to Tenant '%s'", Tenant_Name)

ret = json.loads(response.read().decode())
logger.debug("Tenant Version %s", ret["Result"]["Storage"]["Server"])

### IF Secret_ID is empty, then find it using Folder_Name and Secret_Name

if (Secret_ID == ""):

    ### get all the SECRET FOLDERS
    payload = "{'Parent':''}"
    conn.request("POST", "/ServerManage/GetSecretsAndFolders", body = payload, headers = headers)
    response = conn.getresponse()
    if (response.status != 200):
        logger.error("Response status: %d", response.status)
        logger.error("Failed to get Folders from Tenant %s", Tenant_Name)
        sys.exit(1)
    ret = json.loads(response.read().decode())

    Parent_ID=""

    ### loop thru folders looking for our Folder_Name
    for folder in ret["Result"]["Results"]:
       if (folder["Row"]["SecretName"] == Folder_Name):
           Parent_ID = folder["Row"]["ID"]
           logger.debug("Parent_ID=%s", Parent_ID)

    ### abort if we didn't find our Folder_Name
    if (Parent_ID == ""):
        logger.error("Failed to get Folders from Tenant %s", Tenant_Name)
        sys.exit(1)

    ### GET all SECRETs in the Folder
    payload = "{'Parent':'" + Parent_ID + "'}"
    conn.request("POST", "/ServerManage/GetSecretsAndFolders", body = payload, headers = headers)
    response = conn.getresponse()
    if (response.status != 200):
        logger.error("Response status: %d", response.status)
        logger.error("Failed to get Secrets from Folder " + Folder_Name)
        sys.exit(1)
    ret = json.loads(response.read().decode())
    results = ret["Result"]["Results"]

    ### loop thru secrets looking for our Secret_Name
    for secret in results:
       if (secret["Row"]["SecretName"] == Secret_Name):
         Secret_ID = secret["Row"]["ID"]
         logger.debug("Secret_ID=" + Secret_ID)

    ### abort if we didn't find our Secret_Name
    if (Secret_ID == ""):
        logger.error("Failed to find Secret_Name = " + Secret_Name)
        sys.exit(1)

##### (One way or another, we should have the Secret_ID now)

### Get our SECRET contents
payload = "{'ID':'" + Secret_ID + "'}"
conn.request("POST", "/ServerManage/RetrieveSecretContents", body = payload, headers = headers)
response = conn.getresponse()
if (response.status != 200):
    logger.error("Response status: %d", response.status)
    logger.error("Failed to get contents of Secret_Name " + Secret_Name)
    sys.exit(1)

ret = json.loads(response.read().decode())
# print(ret)

if(not ret["success"]):
    logger.error("Success: %s", ret["success"])
    logger.error("Message: %s", ret["Message"])
    sys.exit(1)

logger.debug("Contents of %s", ret["Result"]["SecretName"])
logger.debug("%s", ret["Result"]["SecretText"])
SecretText = ret["Result"]["SecretText"]

if (SecretText != ""):
    logger.info("SUCCESS: Secret contents retrieved from '%s/%s'", Folder_Name, Secret_Name)
