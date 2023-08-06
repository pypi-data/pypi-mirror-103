import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "coscine",
	version = "0.2.0",
	description = "Coscine REST API python3.x interface",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "RWTH Aachen University",
	author_email = "coscine@itc.rwth-aachen.de",
	license = "MIT License",
	packages = setuptools.find_packages(where="src"),
	keywords = [
		"Coscine", "RWTH Aachen", "RDM", "Research Data Management"
	],
	install_requires = [
		"requests",
	],
	url = "https://git.rwth-aachen.de/coscine/docs/public/coscine-api-python-client",
	project_urls = {
		"Bug Tracker":  "https://git.rwth-aachen.de/coscine/docs/public/coscine-api-python-client/-/issues"

	},
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Intended Audience :: Developers"
	],
	package_dir = {"": "src"},
	python_requires = ">=3.3"
)