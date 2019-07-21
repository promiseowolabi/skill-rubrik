# OPSDROID Rubrik skill

This is a chatops project that uses opsdroid and Rubrik SDK for Python to makes it easy to interact with the Rubrik CDM API.


# :hammer: Installation

Install opsdroid from pip:

```
$ pip install opsdroid
$ opsdroid
```

Modify the opsdroid configuration.yaml file and select your desired chat service e.g. to use Slack provide an API token.
Add the rubrik skill to the opsdroid configuration.yaml file e.g.
```
  ## Rubrik CDM vsphere mount
  - name: rubrik
    rubrik_cdm_node_ip: '10.10.10.10'
    rubrik_cdm_password: 'password'
    rubrik_cdm_username: 'python-sdk@rubrik.com'
    path: '/path/to/the/gitrepo/clone'
    no-cache: True
```

Clone this repository and run the 'opsdroid' command. 

# :mag: Example

These are the example messages based on regex_matches the skill will respond to:

* `take a snapshot of vmware vm em1-promowol-l1`
* `live mount vm em1-promowol-l1`
* `live mount db AdventureWorks2016 from date 07-19-2019 on time 01:30 AM as a clone called AdventureClone instance MSSQLSERVER host <em1-promowol-w1.rubrikdemo.com>`
* `unmount db AdventureClone on instance MSSQLSERVER host <em1-promowol-w1.rubrikdemo.com>`
* `unmount vm em1-promowol-l1 07-21 10:17 0`
