# Name:         Josh Cacayan, Nathanael Garner, Zachary Kochiban
# Course:       CSC328
# Semester:     Fall 2023
# Assignment:   Final

all: server client

server: server.py
	cp server.py server
	chmod u+x server

client: client.py
	cp client.py client
	chmod u+x client
	
.PHONY: clean

clean:
	rm -rf server
	rm -rf client
