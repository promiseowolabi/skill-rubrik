from opsdroid.skill import Skill
from opsdroid.matchers import match_regex
import rubrik_cdm


class RubrikSkill(Skill):
    @match_regex('live mount (?P<vm_name>[\w\'-]+)')
    async def vsphere_live_mount(self, message):
        vm_name = message.regex.group('vm_name')
        rubrik = rubrik_cdm.Connect()
        live_mount = rubrik.vsphere_live_mount(vm_name)
        await message.respond('All done! {} has been live mounted'.format(vm_name))

        