Import-Module .\Rubrik -Force
# Force import Rubrik module.

Connect-Rubrik -Server 192.168.150.121 -Username rebecca@rubrik.us
# This will connect to Rubrik with a username of "admin" to the IP address.
# The prompt will request a secure password.      
      
Get-RubrikVCD -Status 'Connected'
# This returns the vCD settings on the currently connected Rubrik cluster with the status of 'Connected'

Get-RubrikVApp -Name 'Demo-vApp01' -PrimaryClusterID local
# This returns details on all vCD vApps named "vApp01".

Get-RubrikVApp "Demo-vApp01" -PrimaryClusterID local | Protect-RubrikVApp -SLA 'Gold'
# This will assign the Gold SLA Domain to any vApp named "vApp1"

Get-RubrikSnapshot -id 'VcdVapp:::01234567-8910-1abc-d435-0abc1234d567' 
# This will return all snapshot (backup) data for the virtual machine id of "VirtualMachine:::aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee-vm-12345"

Export-RubrikVApp -id 'VcdVapp:::01234567-8910-1abc-d435-0abc1234d567' -snapshotid '7acdf6cd-2c9f-4661-bd29-b67d86ace70b' -ExportMode 'ExportToNewVapp' -NoMapping -PowerOn:$true
# This exports the vApp snapshot with an id of 7acdf6cd-2c9f-4661-bd29-b67d86ace70b to a new vApp in the same Org VDC and remove existing network mappings from VM NICs

# EXAMPLE
$vapp = Get-RubrikVApp -Name 'vApp01' -PrimaryClusterID local 
$snapshot = Get-RubrikSnapshot -id $vapp.id -Latest
$restorableVms = $vapp.vms
$restorableVms[0].PSObject.Properties.Remove('vcenterVm')
$vm = @()
$vm += $restorableVms[0]
Export-RubrikVApp -id $vapp.id -snapshotid $snapshot.id -Partial $vm -ExportMode ExportToTargetVapp -PowerOn:$false

This retrieves the latest snapshot from the given vApp 'vApp01' and perform a partial export on the first VM in the vApp.
The VM is exported into the existing parent vApp. Set the ExportMode parameter to 'ExportToNewVapp' parameter to create a new vApp for the partial export.
This is an advanced use case and the user is responsible for parsing the output from Get-RubrikVApp, or gathering data directly from the API.
Syntax of the object passed with the -Partial Parameter is available in the API documentation.
#>