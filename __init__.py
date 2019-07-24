from opsdroid.skill import Skill
from opsdroid.matchers import match_regex
import rubrik_cdm


class RubrikSkill(Skill):

    def __init__(self, opsdroid, config):
        super(RubrikSkill, self).__init__(opsdroid, config)

    @match_regex('Live mount vm (?P<vm_name>[\w\'-]+)')
    async def vspherelivemount(self, message):
        """
        A skills function to live mount a vSphere virtual machine using the current snapshot. The parser looks for the message argument.

        Arguments:
            message {str} -- Live mount vm {vm_name}
        """
        vm_name = message.regex.group('vm_name')
        rubrik = rubrik_cdm.Connect()
        live_mount = rubrik.vsphere_live_mount(vm_name)
        await message.respond('All done! {} has been live mounted. Response: {}'.format(vm_name, live_mount))

    @match_regex('Unmount vm (?P<mounted_vm_name>[\w\'-:\s]+)')
    async def vsphereliveunmount(self, message):
        """
        A skills function to unmount a vSphere virtual machine. The parser looks for the message argument.

        Arguments:
            message {str} -- Unmount vm {vm_name}
        """
        mounted_vm_name = message.regex.group('mounted_vm_name')
        rubrik = rubrik_cdm.Connect()
        live_unmount = rubrik.vsphere_live_unmount(mounted_vm_name)
        await message.respond('All done! {} has been unmounted. Response: {}'.format(mounted_vm_name, live_unmount))

    @match_regex('Live mount db (?P<db_name>[\w\'-]+) from (?P<date>[\w\'-]+) at (?P<time>[0-9:]+\s[AMP]+) as (?P<mount_name>[\w-]+) on (?P<sql_instance>[\w-]+) on host (?P<sql_host>.+)')
    async def sqllivemount(self, message):
        """
        A skills function to mount a mssql database. The parser looks for the message argument.

        Arguments:
            message {str} -- Live mount db {db_name} from {date} at {time} as {mount_name} on {sql_instance} on host {<sql_host>}
        """
        db_name = message.regex.group('db_name')
        date = message.regex.group('date')
        time = message.regex.group('time')
        mount_name = message.regex.group('mount_name')       
        sql_instance = message.regex.group('sql_instance')
        sql_host = message.regex.group('sql_host')
        sql_host = sql_host[4:-4]
        rubrik = rubrik_cdm.Connect()
        live_mount = rubrik.sql_live_mount(db_name, date, time, sql_instance, sql_host, mount_name)
        await message.respond('All done! {} has been live mounted as {}. Response: {}'.format(db_name, mount_name, live_mount))

    @match_regex('Unmount db (?P<mounted_db_name>[\w\'-:\s]+) on (?P<sql_instance>[\w-]+) on host (?P<sql_host>.+)')
    async def sqlliveunmount(self, message):
        """
        A skills function to unmount an mssql db. The parser looks for the message argument.

        Arguments:
            message {str} -- Unmount db {mounted_db_name} on {sql_instance} on host {<sql_host>}
        """
        mounted_db_name = message.regex.group('mounted_db_name')
        sql_instance = message.regex.group('sql_instance')
        sql_host = message.regex.group('sql_host')
        sql_host = sql_host[4:-4]
        rubrik = rubrik_cdm.Connect()
        live_unmount = rubrik.sql_live_unmount(mounted_db_name, sql_instance, sql_host)
        await message.respond('All done! {} has been unmounted. Response: {}'.format(mounted_db_name, live_unmount))
    
    @match_regex('Take a snapshot of (?P<object_type>[\w\'-]+) vm (?P<object_name>[\w\'-]+)')
    @match_regex('Take a snapshot of (?P<object_type>[\w\'-]+) (?P<object_name>[\w\'-]+) on (?P<sql_instance>[\w-]+) on host (?P<sql_host>.+)')
    async def vsphereondemandsnapshot(self, message):
        """
        A skills function to take an on-demand snapshot using the current sla. The parser looks for the message argument.

        Arguments:
            message {str} -- Take a snapshot of {vmware} {vm} {vm_name}
                          -- Take a snapshot of {mssql_db} {db_name} on {sql_instance} on host {sql_host}
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
            sql_host = message.regex.group('sql_host')
            sql_host = sql_host[4:-4]
            snapshot = rubrik.on_demand_snapshot(db_name, object_type, sql_host=sql_host, sql_instance=sql_instance, sql_db=sql_db)
        
        await message.respond('All done! A snapshot of {} has been taken. Response: {}'.format(db_name, snapshot))