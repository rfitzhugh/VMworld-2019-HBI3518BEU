Import-Module .\Rubrik -Force
# Force import Rubrik module.

Connect-Rubrik -Server 0.0.0.0 -Username rebecca@rubrik.us
# This will connect to Rubrik with a username of "admin" to the IP address.
# The prompt will request a secure password.      
      
Get-RubrikVCD -Status 'Connected'
# This returns the vCD settings on the currently connected Rubrik cluster with the status of 'Connected'

Get-RubrikVApp -Name 'CentOS7_min' | Get-RubrikSnapshot -Latest
# Get latest snapshot for vApp Template.

Export-RubrikVCDTemplate -id '01234567-8910-1abc-d435-0abc1234d567' -Name 'Template-Export' -catalogid '01234567-8910-1abc-d435-0abc1234d567' -orgvdcid '01234567-8910-1abc-d435-0abc1234d567'
# Export vApp Template using existing catalog.