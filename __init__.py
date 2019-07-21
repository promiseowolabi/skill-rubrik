from opsdroid.skill import Skill
from opsdroid.matchers import match_regex
import rubrik_cdm


class RubrikSkill(Skill):

    def __init__(self, opsdroid, config):
        super(RubrikSkill, self).__init__(opsdroid, config)

    @match_regex('live mount vm (?P<vm_name>[\w\'-]+)')
    async def vspherelivemount(self, message):
        vm_name = message.regex.group('vm_name')
        rubrik = rubrik_cdm.Connect()
        rubrik.vsphere_live_mount(vm_name)
        await message.respond('All done! {} has been live mounted'.format(vm_name))

    @match_regex('unmount vm (?P<mounted_vm_name>[\w\'-:\s]+)')
    async def vsphereliveunmount(self, message):
        mounted_vm_name = message.regex.group('mounted_vm_name')
        rubrik = rubrik_cdm.Connect()
        rubrik.vsphere_live_unmount(mounted_vm_name)
        await message.respond('All done! {} has been unmounted'.format(mounted_vm_name))

    @match_regex('live mount db (?P<db_name>[\w\'-]+) from date (?P<date>[\w\'-]+) on time (?P<time>[0-9:]+\s[AMP]+) as a clone called (?P<mount_name>[\w-]+) on instance (?P<sql_instance>[\w-]+) host (?P<sql_host>.+)')
    async def sqllivemount(self, message):
        db_name = message.regex.group('db_name')
        date = message.regex.group('date')
        time = message.regex.group('time')
        mount_name = message.regex.group('mount_name')       
        sql_instance = message.regex.group('sql_instance')
        sql_host = message.regex.group('sql_host')
        sql_host = sql_host[4:-4]
        rubrik = rubrik_cdm.Connect()
        rubrik.sql_live_mount(db_name, date, time, sql_instance, sql_host, mount_name)
        await message.respond('All done! {} has been live mounted as {}'.format(db_name, mount_name))

    @match_regex('unmount db (?P<mounted_db_name>[\w\'-:\s]+) on instance (?P<sql_instance>[\w-]+) host (?P<sql_host>.+)')
    async def sqlliveunmount(self, message):
        mounted_db_name = message.regex.group('mounted_db_name')
        sql_instance = message.regex.group('sql_instance')
        sql_host = message.regex.group('sql_host')
        sql_host = sql_host[4:-4]
        rubrik = rubrik_cdm.Connect()
        rubrik.sql_live_unmount(mounted_db_name, sql_instance, sql_host)
        await message.respond('All done! {} has been unmounted'.format(mounted_db_name))