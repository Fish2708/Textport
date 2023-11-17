# Windows 64-bit Build Instructions

1. Make sure you have all the requirements installed (see [requirements](requirements.md))
2. There shouldnt be a build and a dist folder
3. to build the client / server execute ```pyinstaller --onefile``` with either client.py or server.py
4. If the build was successfull you will find the executables in the dist folder.
5. If you encountered any errors please open an issue