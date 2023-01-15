import os
from scene_validator.core.common import log
from scene_validator.core.resources import Resources

root_ = os.path.dirname(__file__)
project_root = os.path.dirname(root_)

class BatchValidator(object):
    def __init__(self):
        self.resources = Resources.get_instance()
        self.preset_rules = None

    def start(self, preset=None, auto_fix=False):
        preset_rules = self.resources.get_preset_rules(preset_name=preset)
        self.run_rules(preset_rules, auto_fix)

    def run_rules(self, preset_rules, auto_fix):

        log(message='Run rules..........', category='Start')

        for i in preset_rules:
            cmd = "from scene_validator.rules.{}.rule import Rule".format(i)
            exec (cmd)

            rule = Rule()
            output = rule.check()
            if output:
                log(message=output, category=i)

                if auto_fix:
                    rule.fix()


