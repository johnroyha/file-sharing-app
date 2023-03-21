# Online File Sharing Application

A Python application that allows files to be transferred using UDP and TCP connection. The commands are shown below.

• scan: The client transmits one or more SERVICE DISCOVERY broadcasts and listens for file sharing server responses. When a service response is received, the client outputs this information on the command line. If no responses are heard within a timeout period, it returns with a
“No service found.” message.<br>
• Connect <IP address> <port> : Connect to the file sharing service at \<IP address> \<port><br>
• llist (“local list”) : The client outputs a directory listing of its local file sharing
directory.<br>
• rlist (“remote list”) : The client sends a list command to the server to obtain a
file sharing directory listing. The remote listing is output to the user.<br>
• put \<filename> : Upload the file \<filename> by issuing a put command to
the server.<br>
• get \<filename> : Get \<filename> by issuing a get command to the server,
who will then respond with the file. The file will be saved locally.<br>
• bye : Close the current the server connection.<br>

### To use:
Change the local and remote directory global variables to what you desire.<br>
Run both server and client files and follow the instructions. 
