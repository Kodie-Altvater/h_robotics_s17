%% Send data to python server
data = floor(2^8*rand(1,480000)); % 100x100x3
send_data2python('127.0.0.1',51031,data)
 

 
%% Send Data to the python server
% write a message
x = [3,232,mod(1:1000,256)];
fwrite(t, x);
 
pause(.1)

 % read the echo
bytes = fread(t, [1, t.BytesAvailable]);
char(bytes)

%% Close socket
fclose(t); 
instrreset