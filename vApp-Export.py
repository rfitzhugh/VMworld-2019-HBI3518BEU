#!/usr/bin/python2.7
import requests
from requests.auth import HTTPDigestAuth
import json
import urllib
import base64
import urllib3
import getpass
import yaml

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# hostname = "10.0.115.122"
# username = "admin"
# password = "RubrikAdminPassword"

hostname = raw_input("Enter host IP: ")
username = raw_input("Enter user name: ")
password = getpass.getpass("Enter password: ")

schema = "https"
headers = {
  'Authorization': 'Basic %s' % base64.b64encode(username + ":" + password),
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}

def checkBadResponseCode(status):
	if status >= 400:
		print "request failed with status code %s %s" %(status, requests.status_codes._codes[status])
		return True
	return False

def getCatalogId(catalogName):
	urlStr = schema + "://" + hostname + "/" + 'api/internal/vcd/hierarchy/root/descendants'
	params = {
		"sort_order": "asc",
		"name": catalogName
	}

	resp = requests.get(urlStr, params = params, headers = headers, verify = False)
	if checkBadResponseCode(resp.status_code):
		raise Exception("Could not find catalog with given name")
	data = json.loads(resp.text)['data']

	if len(data) == 0:
		raise Exception("Could not find catalog with given name")
	if len(data) > 1:
		raise Exception("Found multiple catalog objects with given name")

	return data[0]["id"].split(":::")[1]

def getOrgVdcId(orgVdcName):
	urlStr = schema + "://" + hostname + "/" + 'api/internal/vcd/hierarchy/root/descendants'
	params = {
		"sort_order": "asc",
		"name": orgVdcName
	}

	resp = requests.get(urlStr, params = params, headers = headers, verify = False)
	if checkBadResponseCode(resp.status_code):
		raise Exception("Could not find org vdc with given name")
	data = json.loads(resp.text)['data']

	if len(data) == 0:
		raise Exception("Could not find catalog with given name")
	if len(data) > 1:
		raise Exception("Found multiple catalog objects with given name")

	return data[0]["id"].split(":::")[1]

while True:
	print "The following work modes are available:"
	print " 1. Find snapshot Ids from vApp template."
	print " 2. Find export options of org Vdc and storage policy for snapshot."
	print " 3. Create export job."
	print " 4. Exit."
	mode = raw_input("Enter work mode: ")

	try:
   	
		if mode == "1":
			#templateName = "Demo-Template-TO"
			templateName = raw_input("Enter template name: ")
			params = {
				"sort_order": "asc",
				"include_backup_task_info" : False,
				"name": templateName
			}
			
			urlStr = schema + "://" + hostname + "/" + 'api/internal/vcd/vapp' 
			resp = requests.get(urlStr, params = params, headers = headers, verify = False)
			if checkBadResponseCode(resp.status_code):
				continue
			
			data = json.loads(resp.text)['data']
			
			if len(data) == 0:
				raise Exception("Could not find object with given name")
			if len(data) > 1:
				raise Exception("Found multiple vApp objects with given name")

			template = data[0]
			id = template['id']
			
			partialStr = urllib.pathname2url('api/internal/vcd/vapp/%s/snapshot' % id)
			urlStr = schema + "://" + hostname + "/" + partialStr
			resp = requests.get(urlStr, headers = headers, verify = False)
			
			if checkBadResponseCode(resp.status_code):
				continue
			data = json.loads(resp.text)['data']
			for snap in data:
				print "Date: %s Id: %s" % (snap["date"], snap["id"])
			print ""
		elif mode == "2":
			#catalogName = "cat-1"
			catalogName = raw_input("Enter catalog name: ")
			catalogId = getCatalogId(catalogName)
			orgVdcId = ""
			#orgVdcName = "orgVdc-3"
			orgVdcName = raw_input("Enter org vdc name: ")

			if orgVdcName != "":
				orgVdcId = getOrgVdcId(orgVdcName)

			#snapshotId = "0e3f43b2-45fe-4ef3-8dbd-e7ad55dc44ab"
			snapshotId = raw_input("Enter snapshot Id: ")
			#name = "alecVapp"
			name = raw_input("Enter name for new template: ")
			if orgVdcId == "":
				params = {
					"catalog_id": catalogId,
					"name": name
				}
			else:
				params = {
					"catalog_id": catalogId,
					"name": name,
					"org_vdc_id": orgVdcId
				}

			urlStr = schema + "://" + hostname + "/api/v1/vcd/vapp/template/snapshot/" + snapshotId + "/export/options"
			resp = requests.get(urlStr, params = params, headers = headers, verify = False)

			if checkBadResponseCode(resp.status_code):
				continue

			print ""
			print yaml.dump(eval(resp.text), default_flow_style=False)
		elif mode == "3":
			#catalogName = "cat-1"
			catalogName = raw_input("Enter catalog name: ")
			catalogId = getCatalogId(catalogName)
			#orgVdcName = "orgVdc-3"
			orgVdcName = raw_input("Enter org vdc name: ")
			orgVdcId = getOrgVdcId(orgVdcName)

			#snapshotId = "0e3f43b2-45fe-4ef3-8dbd-e7ad55dc44ab"
			snapshotId = raw_input("Enter snapshot Id: ")
			#name = "alecVapp"
			name = raw_input("Enter name for new template: ")
			spId = ""
			spId = raw_input("Enter storage policy Id: ")

			if spId == "": 		
				config = {
					"name": name,
			  		"catalogId": catalogId,
			  		"orgVdcId": orgVdcId,
				}
			else:
				config = {
					"name": name,
			  		"catalogId": catalogId,
			  		"orgVdcId": orgVdcId,
			  		"storagePolicyId": spId
				}

			urlStr = schema + "://" + hostname + "/api/v1/vcd/vapp/template/snapshot/" + snapshotId + "/export"

			resp = requests.post(urlStr, data = json.dumps(config), headers = headers, verify = False)
			if checkBadResponseCode(resp.status_code):
				continue
			
			print ""
			print resp.text
			print ""
		elif mode == "4":
			raise SystemExit
		else:
			raise Exception("Mode not defined")	
	except Exception as e:
		print ""
		print e
		print ""
		print "Encountered error while processing request. Try again.\n"	
