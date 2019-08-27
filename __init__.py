from opsdroid.skill import Skill
from opsdroid.matchers import match_regex
import rubrik_cdm
import urllib3

# To enable certificate warnings comment the line below:
urllib3.disable_warnings()

def _hostname_to_text(hostname):
    if hostname[:4] == '&lt;': 
        hostname = hostname[4:-4]
        return hostname
    else:
        return hostname
        
class RubrikSkill(Skill):

    
    def __init__(self, opsdroid, config):
        super(RubrikSkill, self).__init__(opsdroid, config)

    @match_regex('live mount vm (?P<vm_name>[\w\'-]+)')
    async def vspherelivemount(self, message):
        """
        A skills function to live mount a vSphere virtual machine using the current snapshot. The parser looks for the message argument.

        Arguments:
            message {str} -- live mount vm {vm_name}
        """
        vm_name = message.regex.group('vm_name')
        rubrik = rubrik_cdm.Connect()
        live_mount = rubrik.vsphere_live_mount(vm_name)
        await message.respond('All done! {} has been live mounted. Response: {}'.format(vm_name, live_mount))

    @match_regex('unmount vm (?P<mounted_vm_name>[\w\'-:\s]+)')
    async def vsphereliveunmount(self, message):
        """
        A skills function to unmount a vSphere virtual machine. The parser looks for the message argument.

        Arguments:
            message {str} -- unmount vm {vm_name}
        """
        mounted_vm_name = message.regex.group('mounted_vm_name')
        rubrik = rubrik_cdm.Connect()
        live_unmount = rubrik.vsphere_live_unmount(mounted_vm_name)
        await message.respond('All done! {} has been unmounted. Response: {}'.format(mounted_vm_name, live_unmount))

    @match_regex('live mount db (?P<db_name>[\w\'-]+) from (?P<date>[\w\'-]+) at (?P<time>[0-9:]+\s[AMP]+) as (?P<mount_name>[\w-]+) on (?P<sql_instance>[\w-]+) on host (?P<sql_host>.+)')
    async def sqllivemount(self, message):
        """
        A skills function to mount a mssql database. The parser looks for the message argument.

        Arguments:
            message {str} -- live mount db {db_name} from {date} at {time} as {mount_name} on {sql_instance} on host {<sql_host>}
        """
        db_name = message.regex.group('db_name')
        date = message.regex.group('date')
        time = message.regex.group('time')
        mount_name = message.regex.group('mount_name')       
        sql_instance = message.regex.group('sql_instance')
        sql_hostname = message.regex.group('sql_host')
        sql_host = _hostname_to_text(sql_hostname)
        rubrik = rubrik_cdm.Connect()
        live_mount = rubrik.sql_live_mount(db_name, date, time, sql_instance, sql_host, mount_name)
        await message.respond('All done! {} has been live mounted as {}. Response: {}'.format(db_name, mount_name, live_mount))

    @match_regex('unmount db (?P<mounted_db_name>[\w\'-:\s]+) on (?P<sql_instance>[\w-]+) on host (?P<sql_host>.+)')
    async def sqlliveunmount(self, message):
        """
        A skills function to unmount an mssql db. The parser looks for the message argument.

        Arguments:
            message {str} -- unmount db {mounted_db_name} on {sql_instance} on host {<sql_host>}
        """
        mounted_db_name = message.regex.group('mounted_db_name')
        sql_instance = message.regex.group('sql_instance')
        sql_host = message.regex.group('sql_host')
        sql_host = sql_host[4:-4]
        rubrik = rubrik_cdm.Connect()
        live_unmount = rubrik.sql_live_unmount(mounted_db_name, sql_instance, sql_host)
        await message.respond('All done! {} has been unmounted. Response: {}'.format(mounted_db_name, live_unmount))
    
    @match_regex('take a snapshot of (?P<object_type>[\w\'-]+) vm (?P<object_name>[\w\'-]+)')
    @match_regex('take a snapshot of (?P<object_type>[\w\'-]+) (?P<object_name>[\w\'-]+) on (?P<sql_instance>[\w-]+) on host (?P<sql_host>.+)')
    async def vsphereondemandsnapshot(self, message):
        """
        A skills function to take an on-demand snapshot using the current sla. The parser looks for the message argument.

        Arguments:
            message {str} -- take a snapshot of {vmware} {vm} {vm_name}
                          -- take a snapshot of {mssql_db} {db_name} on {sql_instance} on host {sql_host}
        """

        object_type = message.regex.group('object_type')
        rubrik = rubrik_cdm.Connect()
        
        if object_type == 'vmware' or object_type == 'ahv':
            vm_name = message.regex.group('object_name')
            snapshot = rubrik.on_demand_snapshot(vm_name, object_type)
        else:
            db_name = message.regex.group('object_name')
            sql_db = message.regex.group('object_name')
            sql_instance = message.regex.group('sql_instance')
            sql_hostname = message.regex.group('sql_host')
            sql_host = _hostname_to_text(sql_hostname)
            snapshot = rubrik.on_demand_snapshot(db_name, object_type, sql_host=sql_host, sql_instance=sql_instance, sql_db=sql_db)
        
        await message.respond('All done! A snapshot of {} has been taken. Response: {}'.format(db_name, snapshot))

    @match_regex('add physical host (?P<hostname>.+)')
    async def addphysicalhost(self, message):
        """
        A skills function to add a physical host. The parser looks for the message argument.

        Arguments:
            message {str} -- add physical host {hostname}
        """
        host = message.regex.group('hostname')
        hostname = _hostname_to_text(host)
        rubrik = rubrik_cdm.Connect()
        add_host = rubrik.add_physical_host(hostname)
        await message.respond('All done! Physical host {} has been added. Response: {}'.format(hostname, add_host))

    @match_regex('get rubrik cluster version')
    async def getclusterversion(self, message):
        """
        A skills function to get the rubrik cluster version. The parser looks for the message argument.

        Arguments:
            message {str} -- get rubrik cluster version
        """
        rubrik = rubrik_cdm.Connect()
        version = rubrik.cluster_version()
        await message.respond('All done! The current Rubrik cluster version is: {}'.format(version))

    @match_regex('get rubrik cluster node ip\'s')
    async def getclusternodeips(self, message):
        """
        A skills function to get the rubrik cluster node ip's. The parser looks for the message argument.

        Arguments:
            message {str} -- get rubrik cluster node ip's
        """
        rubrik = rubrik_cdm.Connect()
        node_ip = rubrik.cluster_node_ip()
        await message.respond('All done! The current Rubrik cluster node ip\'s are: {}'.format(node_ip)) 

    @match_regex('get rubrik cluster node names')
    async def getclusternodename(self, message):
        """
        A skills function to get the rubrik cluster node names. The parser looks for the message argument.

        Arguments:
            message {str} -- get rubrik cluster node names
        """
        rubrik = rubrik_cdm.Connect()
        node_name = rubrik.cluster_node_name()
        await message.respond('All done! The current Rubrik cluster node names are: {}'.format(node_name)) 
    
    @match_regex('get rubrik cluster node id\'s')
    async def getclusternodeids(self, message):
        """
        A skills function to get the rubrik cluster node id's. The parser looks for the message argument.

        Arguments:
            message {str} -- get rubrik cluster node names
        """
        rubrik = rubrik_cdm.Connect()
        node_id = rubrik.cluster_node_id()
        await message.respond('All done! The current Rubrik cluster node id\'s are: {}'.format(node_id)) 

    @match_regex('get vmware VMs protected by (?P<sla>[\w\'-]+)')
    async def objectsinsla(self, message):
        """
        A skills function to get the objects protected by a Rubrik SLA. The parser looks for the message argument.

        Arguments:
            message {str} -- get vmware VMs protected by {sla}
        """
        rubrik = rubrik_cdm.Connect()
        object_type = 'vmware'
        sla = message.regex.group('sla')
        objects_in_sla = rubrik.get_sla_objects(sla, object_type)
        await message.respond('All done! The current VMs protected by SLA {} are: {}'.format(sla, objects_in_sla))

    @match_regex('perform instant recovery of vmware VM (?P<vm_name>[\w\'-]+)')
    async def vsphereinstantrecoverylatest(self, message):
        """
        A skills function to perform vmware instant recovery. The parser looks for the message argument.

        Arguments:
            message {str} -- perform instant recovery of vmware VM {vm_name}
        """
        rubrik = rubrik_cdm.Connect()
        vm_name = message.regex.group('vm_name')
        instant_recovery = rubrik.vsphere_instant_recovery(vm_name)
        await message.respond('All done! {} has been recovered from the latest snapshot. Response: {}'.format(vm_name, instant_recovery))
    
    @match_regex('perform instant recovery of vmware VM (?P<vm_name>[\w\'-]+) from (?P<date>[\w\'-]+) at (?P<time>[0-9:]+\s[AMP]+)')
    async def vsphereinstantrecovery(self, message):
        """
        A skills function to perform vmware instant recovery. The parser looks for the message argument.

        Arguments:
            message {str} -- perform instant recovery of vmware VM {vm_name} from {date} at {time}
        """
        rubrik = rubrik_cdm.Connect()
        vm_name = message.regex.group('vm_name')
        date = message.regex.group('date')
        time = message.regex.group('time')
        instant_recovery = rubrik.vsphere_instant_recovery(vm_name, date, time)
        await message.respond('All done! {} has been recovered to {} at {}. Response: {}'.format(vm_name, date, time, instant_recovery))

    @match_regex('get live mounts of vmware vm (?P<vm_name>[\w\'-]+)')
    async def getvspherelivemount(self, message):
        """
        A skills function to list the current live mounts of a VMware VM. The parser looks for the message argument.

        Arguments:
            message {str} -- get live mounts of vmware vm {vm_name}
        """
        rubrik = rubrik_cdm.Connect()
        vm_name = message.regex.group('vm_name')
        live_mount = rubrik.get_vsphere_live_mount(vm_name)
        live_mount_names = rubrik.get_vsphere_live_mount_names(vm_name)
        await message.respond('All done! {} has the following live mounts: {}. Response: {}'.format(vm_name, live_mount_names, live_mount))

    @match_regex('get live mount names of vmware vm (?P<vm_name>[\w\'-]+)')
    async def getvspherelivemountnames(self, message):
        """
        A skills function to list the current live mounts of a VMware VM. The parser looks for the message argument.

        Arguments:
            message {str} -- get live mount names of vmware vm {vm_name}
        """
        rubrik = rubrik_cdm.Connect()
        vm_name = message.regex.group('vm_name')
        live_mount = rubrik.get_vsphere_live_mount_names(vm_name)
        await message.respond('All done! {} has the following live mounts: {}.'.format(vm_name, live_mount))

    @match_regex('get live mounts of sql db (?P<db_name>[\w\'-]+) on (?P<sql_instance>[\w-]+) on host (?P<sql_host>.+)')
    async def getsqllivemount(self, message):
        """
        A skills function to list the current live mounts of an MSSQL database. The parser looks for the message argument.

        Arguments:
            message {str} -- get live mount names of sql db {db_name} on {sql_instance} on host {sql_host}
        """
        rubrik = rubrik_cdm.Connect()
        db_name = message.regex.group('db_name')
        sql_instance = message.regex.group('sql_instance')
        sql_hostname = message.regex.group('sql_host')
        sql_host = _hostname_to_text(sql_hostname)
        live_mount = rubrik.get_sql_live_mount(db_name, sql_instance, sql_host)
        await message.respond('All done! {} has the following live mounts: {}.'.format(db_name, live_mount))
