from opsdroid.skill import Skill
from opsdroid.matchers import match_regex
import rubrik_cdm


class RubrikSkill(Skill):

    def __init__(self, opsdroid, config):
        super(RubrikSkill, self).__init__(opsdroid, config)

    @match_regex('Live mount vm (?P<vm_name>[\w\'-]+)')
    async def vspherelivemount(self, message):
        vm_name = message.regex.group('vm_name')
        rubrik = rubrik_cdm.Connect()
        live_mount = rubrik.vsphere_live_mount(vm_name)
        await message.respond('All done! {} has been live mounted. Response: {}'.format(vm_name, live_mount))

    @match_regex('Unmount vm (?P<mounted_vm_name>[\w\'-:\s]+)')
    async def vsphereliveunmount(self, message):
        mounted_vm_name = message.regex.group('mounted_vm_name')
        rubrik = rubrik_cdm.Connect()
        live_unmount = rubrik.vsphere_live_unmount(mounted_vm_name)
        await message.respond('All done! {} has been unmounted. Response: {}'.format(mounted_vm_name, live_unmount))

    @match_regex('Live mount db (?P<db_name>[\w\'-]+) from (?P<date>[\w\'-]+) at (?P<time>[0-9:]+\s[AMP]+) as (?P<mount_name>[\w-]+) on (?P<sql_instance>[\w-]+) on host (?P<sql_host>.+)')
    async def sqllivemount(self, message):
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

    @match_regex('unmount db (?P<mounted_db_name>[\w\'-:\s]+) on instance (?P<sql_instance>[\w-]+) host (?P<sql_host>.+)')
    async def sqlliveunmount(self, message):
        mounted_db_name = message.regex.group('mounted_db_name')
        sql_instance = message.regex.group('sql_instance')
        sql_host = message.regex.group('sql_host')
        sql_host = sql_host[4:-4]
        rubrik = rubrik_cdm.Connect()
        live_unmount = rubrik.sql_live_unmount(mounted_db_name, sql_instance, sql_host)
        await message.respond('All done! {} has been unmounted. Response: {}'.format(mounted_db_name, live_unmount))
    
    @match_regex('take a snapshot of (?P<object_type>[\w\'-]+) vm (?P<vsphere_vm_name>[\w\'-]+)')
    async def vsphereondemandsnapshot(self, message):
        vsphere_vm_name = message.regex.group('vsphere_vm_name')
        object_type = message.regex.group('object_type')
        rubrik = rubrik_cdm.Connect()
        snapshot = rubrik.on_demand_snapshot(vsphere_vm_name, object_type)
        await message.respond('All done! A snapshot of {} has been taken. Response: {}'.format(vsphere_vm_name, snapshot))
