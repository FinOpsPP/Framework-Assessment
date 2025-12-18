# Mass covert all Microsoft excel (xlsx) files to LibreOffice calc8 (ods) files.
# Can only really work in linux-like envs that has libreoffice cli installed.
# Outputs are not checked in, but is useful for testing (and viewing) of the assessments
# in linux envs without Office applications. It is assumed only assessment files are .xlsx
ods:
	find . -type f -name "*.xlsx" -execdir libreoffice --headless --convert-to ods '{}' \;