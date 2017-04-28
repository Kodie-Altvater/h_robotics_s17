%% Kodie Altvater
% Human robotics and interaction
% 4/22/17
% API for capture image data, depth data, or sending color image and apply
% detection algorithm to it

% includes a simple API for controlling the kinect and detecting objects.


%% Open socket
instrreset
conn = open_tcp_socket('127.0.0.1',60000);

% total size of picture (needed to plot images only)
total = 640*480*3;

%% Send COLOR: from MATLAB to Python.
% Data variable must be image file or it will not work
fwrite(conn,'detc')
imgData = reshape(data,1,numel(data));
send_data2python(conn,imgData);
coordinates = readdata_from_python(conn)

%% Capture DEPTH: from python and plot in MATLAB
fwrite(conn,'gray')
data = readdata_from_python(conn);
dimension = uint8(3*numel(data)/total);
img_data = uint8(reshape(data,480,640,dimension));
imshow(img_data);

%% Capture COLOR: from python and plot in MATLAB
fwrite(conn,'colr')
data = readdata_from_python(conn);
% dimension = 3 or 1 (color or gray)
dimension = uint8(3*numel(data)/total);
data = uint8(reshape(data,480,640,dimension));
% show image
imshow(data);

%% Close socket and exit (program will terminate)
fwrite(conn,'exit')
