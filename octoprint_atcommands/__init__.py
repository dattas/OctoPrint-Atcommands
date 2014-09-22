from __future__ import absolute_import
from octoprint.events import eventManager, Events
import re
import octoprint.plugin
import logging

default_settings = {
	"at_pause_commands": None,
}
s = octoprint.plugin.plugin_settings("atcommands", defaults=default_settings)

_regex_at_command = re.compile("^@(\w+)\s*")
atcommandsToEvent = {
	"pause": Events.WAITING,
}

class AtCommandsPlugin(octoprint.plugin.SettingsPlugin,octoprint.plugin.TemplatePlugin,
						octoprint.plugin.AssetPlugin):
	def __init__(self):
		self.logger = logging.getLogger("octoprint.plugins." + __name__)
	##~~ SettingsPlugin

	def on_settings_load(self):
		self.logger.info("Got at pause commands to be: {0}".format(s.get(["at_pause_commands"])))
		return {
			"at_pause_commands": s.get(["at_pause_commands"]),
		}

	def on_settings_save(self, data):
		self.logger.info("saving at commands with the following: {0}".format(data))
		if "at_pause_commands" in data and data["at_pause_commands"]:
			self.logger.info("saving at pause commands to be: {0}".format(data["at_pause_commands"]))
			s.set(["at_pause_commands"], data["at_pause_commands"])

	#~~ TemplatePlugin API

	def get_template_vars(self):
		return dict(
			_settings_menu_entry="@ commands"
		)

	def get_template_folder(self):
		import os
		return os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")

	##~~ AssetPlugin API

	def get_asset_folder(self):
		import os
		return os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")

	def get_assets(self):
		return {
			"js": ["js/atcommands.js"]
		}


def hook_atcommand(comm_obj, cmd):
	atcommand = _regex_at_command.search(cmd)
	if atcommand:
		atcommand = atcommand.group(1)
		if atcommand in atcommandsToEvent:
			eventManager().fire(atcommandsToEvent[atcommand])
		else:
			#no printers are going to know how to handle an @ command, return a blank string to clear the command if we can't parse it
			return ""
		atcommandHandler = "atcommand_"+atcommand
		if atcommandHandler in methods:
			return methods[atcommandHandler](comm_obj, cmd)
		else:
			return ""



	return False

def atcommand_pause(comm_obj, cmd):
	for line in s.get(["at_pause_commands"]).splitlines():
		if line:
			comm_obj._doSend(line)

	comm_obj.setPause(True)
	return "M105"

methods = {'atcommand_pause': atcommand_pause}

__plugin_name__ = "Atcommand Hook Plugin"
__plugin_version__ = "0.1"
__plugin_description__ = "Looks for @commands and handles them"
__plugin_hooks__ = {'octoprint.comm.protocol.gcode': hook_atcommand}
__plugin_implementations__ = [AtCommandsPlugin()]