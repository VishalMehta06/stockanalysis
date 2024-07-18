from setuptools import find_packages
from setuptools import setup

setup(
	name="RADIUS",
	version="0.0.0",
	description="This package will calculate DCFs for US Securities.",
	author="Vishal Mehta",
	author_email="vvmehta06@gmail.com",
	url="https://github.com/VishalMehta06/RADIUS",
	requires=[],
	packages=find_packages(exclude=("tests*", "testing*")),
	# EXAMPLE ENTRY POINTS
	# entry_points={
	# 	"console_scripts" : [
	# 		"stock_list_dcf = radius.stock_list:stock_list_dcf"
	# 	],
	# }
)