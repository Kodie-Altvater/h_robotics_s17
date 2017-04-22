function [obj] = open_tcp_socket(ip,port)

% open connection
obj = tcpip(ip, port);
obj.OutputBufferSize = 2^24;
fopen(obj);