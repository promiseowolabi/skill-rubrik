# OPSDROID Rubrik skill

This is a chatops project that uses opsdroid and Rubrik SDK for Python to makes it easy to interact with the Rubrik CDM API.


# :hammer: Installation

Install opsdroid from pip:

```
$ pip install opsdroid
$ opsdroid
```

## :blue_book: Configuration
Modify the opsdroid configuration.yaml file and select your desired chat service e.g. to use Slack provide a slack API token.
Add the rubrik skill to the opsdroid configuration.yaml file e.g.
```
  ## Rubrik CDM skill
  - name: rubrik
    rubrik_cdm_node_ip: '10.10.10.10'
    rubrik_cdm_password: 'password'
    rubrik_cdm_username: 'python-sdk@rubrik.com'
    path: '/path/to/the/gitrepo/clone'
    no-cache: True
```
Uncomment Regex for parsing in the configuration.yaml file:
```
  - name: regex
    enabled: true
```
Setup your chat service e.g. Slack in the configuration.yaml file:
```
  - name: slack
    # required
    api-token: "xxxx-xxxxxxxxxx-xxxxxxxxx-xxxxxxxx-xxxxxxxxxxxxxxxx"
    # optional
    bot-name: "opsdroid" # default "opsdroid"
    default-room: "#chatops" # default "#general"
    icon-emoji: ":robot_face:" # default ":robot_face:"
    connect-timeout: 10 # default 10 seconds
```
Clone this repository and run the 'opsdroid' command. 

# :mag: Usage

These are the example messages based on regex_matches the skill will respond to:

* `take a snapshot of vmware vm {vm_name}`
* `take a snapshot of mssql_db {db_name} on {sql_instance} on host {sql_host}`
* `live mount vm {vm_name}`
* `live mount db {db_name} from {MM:DD:YYYY} on {HH:MM AM/PM} as {mount_name} on {sql_instance} on host {sql_host}`
* `unmount db {mount_name} on {sql_instance} on host {sql_host}`
* `unmount vm {mounted_vm_name}`
* `take a snapshot of ahv vm {vm_name}`
* `add physical host {hostname}`
* `get rubrik cluster version`

Slack: Enclose {hostname|sql_host} in < > i.e. <sqlhost.rubrikdemo.com> to avoid Slack unfurling which cause sql_host not found errors.

#### Note: The message must match the syntax above including letter case.

