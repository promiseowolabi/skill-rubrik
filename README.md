# Rubrik Skill for Opsdroid

This is an OPSDROID skill for ChatOps using the Rubrik SDK for Python to make it easy to interact with Rubrik CDM API. Opsdroid is an open source chat bot framework written in Python. It is designed to be extendable, scalable and simple.


# :traffic_light: Prerequisites

* `Python 3`
* `Rubrik SDK for Python`

# :hammer: Installation

Install opsdroid from pip:

```
$ pip install opsdroid
$ pip install rubrik-cdm

#run the opsdroid command to create the configuration files

$ opsdroid

# Stop opsdroid  with Ctrl + C to modify the configuration
```

## :blue_book: Configuration
Modify the opsdroid configuration.yaml file and make sure it contains the following: 
* `Chat service e.g. Slack`
* `Rubrik skill added to the skills section`
* `Regex enabled, for parsing messages`

For configuration, opsdroid uses a single YAML file named configuration.yaml. When you run opsdroid it will look for the file in the following places in order:

* `./configuration.yaml`
* `/etc/opsdroid/configuration.yaml`
One of the default locations:
* `Mac: ~/Library/Application Support/opsdroid`
* `Linux: ~/.local/share/opsdroid` or `~/.config/opsdroid`
* `Windows: C:\<User>\<Application Data>\<Local Settings>\opsdroid\ or  C:\Users\<User>\AppData\Local\opsdroid`

Note: If no file named configuration.yaml can be found on one of these folders one will be created for you taken from the example configuration file.

If you are using one of the default locations you can run the command opsdroid -e or opsdroid --edit-config to open the configuration with your favorite editor(taken from the environment variable EDITOR) or the default editor vim.

Ensure that the Environmental Variables for the Rubrik Cluster have been setup. See https://github.com/rubrikinc/rubrik-sdk-for-python/blob/master/docs/quick-start.md#setting-environment-variables-in-microsoft-windows

Then add the rubrik skill to the skill section of the opsdroid configuration.yaml file.
```
  ## Interact with Rubrik CDM API
  - name: rubrik
    rubrik_cdm_node_ip: $rubrik_cdm_node_ip
    rubrik_cdm_password: $rubrik_cdm_password
    rubrik_cdm_username: $rubrik_cdm_username
    repo: https://github.com/promiseowolabi/skill-rubrik.git
    no-cache: True
```
Uncomment Regex for parsing in the configuration.yaml file:
```
parsers:
  - name: regex
    enabled: true
```
Setup your chat service e.g. Slack in the configuration.yaml file:
```
  - name: slack
    # required
    api-token: "your-slack-token-goes-here"
    # optional
    bot-name: "opsdroid" # default "opsdroid"
    default-room: "#chatops" # default "#general"
    icon-emoji: ":robot_face:" # default ":robot_face:"
    connect-timeout: 10 # default 10 seconds
```
Start opsdroid after you complete the configuration
```
$ opsdroid
```
## Usage

On you chosen chat service, these are the example messages based on regex_matches the skill will respond to:

* `take a snapshot of vmware vm {vm_name}`
* `take a snapshot of mssql_db {db_name} on {sql_instance} on host {sql_host}`
* `live mount vm {vm_name}`
* `live mount db {db_name} from {MM-DD-YYYY} on {HH:MM AM/PM} as {mount_name} on {sql_instance} on host {sql_host}`
* `unmount db {mount_name} on {sql_instance} on host {sql_host}`
* `unmount vm {mounted_vm_name}`
* `take a snapshot of ahv vm {vm_name}`
* `add physical host {hostname}`
* `get rubrik cluster version`
* `get vmware VMs protected by {sla}`
* `perform instant recovery of vmware VM {vm_name} from {MM-DD-YYYY} at {HH:MM AM/PM}`
* `perform instant recovery of vmware VM {vm_name}`

Slack: Enclose hostname/sql_host values in < > i.e. <sqlhost.rubrikdemo.com> to avoid Slack unfurling which cause hostname not found errors.

#### Note: The messages must match the syntax above including letter cases.

# :pushpin: License

* [MIT License](LICENSE)

