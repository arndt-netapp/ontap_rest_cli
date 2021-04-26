Example code using the ONTAP REST API CLI passthrough (ontap_rest_cli)

This sample code implements example code for various types of commands run
via the ONTAP REST API CLI passthrough interface. 

```
Requirements:
  1. Python 3.5 or higher.
  2. The netapp-ontap Python package as described at:
     https://pypi.org/project/netapp-ontap/
     Note: Use module version 9.8.0 or higher, even with ONTAP 9.7!
  3. ONTAP 9.7 or higher.

Run "./ontap_rest_cli.py -h" to see usage and examples.
```

Using ontap_rest_cli

```
usage: ontap_rest_cli.py [options] [operation]...

Examples of GET, POST, PATCH, and DELETE ONTAP REST API CLI passthrough
operations.

positional arguments:
  {GET,POST,PATCH,DELETE}
                        One of GET, POST, PATCH, or DELETE (default: GET)

optional arguments:
  -h, --help            show this help message and exit
  -c [CLUSTER], --cluster [CLUSTER]
                        cluster name or IP
  -u [USERNAME], --username [USERNAME]
                        username to connect with (default: admin)
  -p [PASSWORD], --password [PASSWORD]
                        password for username
  -d, --debug           Use debug mode for API calls
```

Notes:
1. The ONTAP REST API CLI passthrough is only available in a cluster scope,
   which means you cannot use this API when connecting to a vserver LIF.
2. CLI commands that merely do a “do you want to continue” yes/no prompt
   are supported from the REST passthrough (with ‘yes’ assumed). Commands
   that prompt for additional input (like a password) are only supported from
   the REST passthrough if the specific command supports a hidden field
   (eg: ‘password’) to avoid the prompt.  This is done in many commands,
   but not all.
