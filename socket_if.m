 %% Connect to the python Server running
 t = tcpip('10.0.1.13', 50007);
 fopen(t);
 
 %% Send Data to the python server
 % write a message
 fwrite(t, 'asdfasdf.');
 
 pause(.1)
 % read the echo
bytes = fread(t, [1, t.BytesAvailable]);
char(bytes)

%% Close socket
fclose(t); 

instrreset