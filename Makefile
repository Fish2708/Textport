nonono:
	@echo "valid options: client, server, clean, all"
client:
	@rm -rf dist build client.spec server.spec info.log __pycache__
	@mkdir build
	@cd build
	pyinstaller --onefile ../client.py
server:
	@rm -rf dist build client.spec server.spec info.log __pycache__
	@mkdir build
	@cd build
	pyinstaller --onefile ../server.py
clean:
	@rm -rf dist build client.spec server.spec info.log __pycache__
all:
	@rm -rf dist build client.spec server.spec info.log __pycache__
	@mkdir build
	@cd build
	pyinstaller --onefile ../client.py
	pyinstaller --onefile ../server.py
