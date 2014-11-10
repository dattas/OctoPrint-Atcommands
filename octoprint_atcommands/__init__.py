from __future__ import absolute_import
from octoprint.events import eventManager, Events
from octoprint.comm.protocol.reprap.util import GcodeCommand
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


def hook_atcommand(protocol, command, with_line_number):
	if command is not None and command.unknown:
		logging.getLogger("octoprint.plugins.atcommands").debug("searching through '{0}'".format(command.original))
		atcommand = _regex_at_command.search(command.original)
		if atcommand:
			atcommand = atcommand.group(1)
			atcommandHandler = "atcommand_"+atcommand
			if atcommandHandler in methods:
				return methods[atcommandHandler](protocol, command, with_line_number)
	return command, with_line_number

def atcommand_pause(protocol, command, with_line_number):
	for line in s.get(["at_pause_commands"]).splitlines():
		if ';' in line:
			line = line.partition(';')[0]
			line = line.rstrip()
		if line:
			protocol._send(line)

	protocol.pause_print(only_pause=True)
	command = None
	return command, with_line_number

methods = {'atcommand_pause': atcommand_pause}

__plugin_name__ = "Atcommand Hook Plugin"
__plugin_version__ = "0.1"
__plugin_description__ = "Looks for @commands and handles them"
__plugin_hooks__ = {'octoprint.comm.protocol.gcode.queued': hook_atcommand}
__plugin_implementations__ = [AtCommandsPlugin()]