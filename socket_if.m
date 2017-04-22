%% Kodie Altvater
% Human robotics and interaction
% 4/22/17
% API for capture image data, depth data, or sending color image and apply
% detection algorithm to it


%% Open socket

conn = open_tcp_socket('127.0.0.1',60000);

% total size of picture (needed to plot images only)
total = 640*480*3;

%% Send color image to python and detect
fwrite(conn,'detc')
imgData = reshape(face_data,1,numel(face_data));
send_data2python(conn,imgData);

%% Read and plot depth data
fwrite(conn,'gray')
data = readdata_from_python(conn);
dimension = uint8(3*numel(data)/total);
img_data = uint8(reshape(data,480,640,dimension));
imshow(img_data);

%% Read and plot color data
fwrite(conn,'colr')
data = readdata_from_python(conn);
% dimension = 3 or 1 (color or gray)
dimension = uint8(3*numel(data)/total);
face_data = uint8(reshape(data,480,640,dimension));
% show image
imshow(face_data);

%% Close socket and exit
fwrite(conn,'exit')
data = readdata_from_python(conn);
dimension = uint8(3*numel(data)/total);
img_data = uint8(reshape(data,480,640,dimension));
imshow(img_data);
fclose(conn); 
