# coding=utf-8
import setuptools

def package_data_dirs(source, sub_folders):
	import os
	dirs = []

	for d in sub_folders:
		for dirname, _, files in os.walk(os.path.join(source, d)):
			dirname = os.path.relpath(dirname, source)
			for f in files:
				dirs.append(os.path.join(dirname, f))

	return dirs

def params():
	name = "OctoPrint-Atcommands"
	version = "0.1.0"

	description = "Adds support for @ commands to OctoPrint"
	long_description = "TODO"
	author = "Dattas Moonchaser"
	author_email = "dattas@dattasmoon.com"
	url = "https://github.com/dattas/OctoPrint-Atcommands"
	license = "AGPLv3"

	packages = ["octoprint_atcommands"]
	package_data = {"octoprint": package_data_dirs('octoprint_atcommands', ['static', 'templates'])}

	include_package_data = True
	zip_safe = False
	install_requires = open("requirements.txt").read().split("\n")

	entry_points = {
		"octoprint.plugin": [
			"atcommands = octoprint_atcommands"
		]
	}

	return locals()

setuptools.setup(**params())