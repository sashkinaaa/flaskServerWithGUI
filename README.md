# flaskServerWithGUI
Server For Automatic Lab Signature-GET Request with GUI

This is a script, which starts a Flask server that responds to a GET requests (used for automatic signatures in e-university.tu-sofia.bg system)

Prerequisites:
	1. Create a CSV file with the students that will get the signature and put it in the same directory as the script/exe file. 
		1.1. Each student faculty number should be on a new line in the CSV file and no other symbols should be used.
	2. Allow the server in Windows firewall or allow it on first run.

In order to start the server and use it:
	1. Start the .exe file or run the Python script from PyCharm.
	2. Choose the type of signature by opening the webpage http://yourIPaddr.
	3. Send the GET request to http://yourIPaddr/returnList from the e-university.tu-sofia.bg system and check the message that the system returns for errors.
	4. Stop the server by pressing StopServer button or Close button or by pressing the Stop button in PyCharm.


To create exe file from a Python script use the steps below:
	1. Open CMD
	2. Navigate to the script directory
	3. Run pyinstaller by: pyinstaller -F --add-data "templates;templates" SignatureSrvWithHTMLandGUI.py
	4. Copy the studentsList.csv to the same directory as the exe (exe file is located in dist folder after pyinstaller)
	5. Run the exe file
