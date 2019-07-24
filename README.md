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

# :mag: Example

These are the example messages based on regex_matches the skill will respond to:

* `Take a snapshot of vmware vm {vm_name}`
* `Take a snapshot of mssql_db {db_name} on {sql_instance} on host {sql_host}`
* `Live mount vm {vm_name}`
* `Live mount db {db_name} from {MM:DD:YYYY} on {HH:MM AM/PM} as {mount_name} on {sql_instance} on host {sql_host}`
* `Unmount db {mount_name} on {sql_instance} on host {sql_host}`
* `Unmount vm {mounted_vm_name}`
* `Take a snapshot of ahv vm {vm_name}`

The syntax above uses regex for matching your messages to the skill
