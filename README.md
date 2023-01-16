#SOM EEPROM generation utility

Prerequisite:

	1.Python 2.6.6 tool

Usage: 
	1. gen_eeprom_bin.py is used to generate EEPROM bins for different 
		Starter kit SOMs and Carrier cards by processing user data
	2. gen_data_file.py is used to generate user data from EEPROM bins which
		is useful for comparing the deltas

How to Run gen_eeprom_bin.py?

	1. Update the user input data files of respective boards in InputData directory as per specification
	2. Run the script gen_eeprom_bin.py, using cmd: "python gen_eeprom_bin.py"
	3. It will prompt for six options, Select any one option as per the requirement
	4. File with name "*_eeprom.bin" will be generated in Output directory

How to Run gen_data_file.py?

	1. Run the script gen_data_file.py, using cmd: "python gen_data_file.py <path to eeprom bin>"
	2. File with name "*_data_read.py" will be generated in Output directory


Example 1:
	1. Lets say if you want to generate EEPROM bin for K26 Starter kit SOM
	2. Update user input data file k26_data.py which is present in InputData directory as per specification
	3. Run the script gen_eeprom_bin.py, using cmd: "python gen_eeprom_bin.py"
	4. Select the option 1 at user prompt, this will generate k26_som_eeprom.bin in Output directory

Example 2:
	1. Lets say if you want to generate user input data file for K26 Starter kit SOM from EEPROM bin
	2. Run the script gen_data_file.py, using cmd: "python gen_data_file.py <path_to_the_K26_Starter_kit_som_eeprom_bin>"
	3. It will generate "k26_data_read.py" file in Output directory


