function [ ] = send_data2python(obj,data)

% determine length of data
len = length(data);

% first 2 characters are encoded for length
c1 = bitand(bitshift(len,-16),hex2dec('ff'));
c2 = bitand(bitshift(len,-8),hex2dec('ff'));
c3 = bitand(len,hex2dec('ff'));

% data word created
data = [c1,c2,c3,(data)];

% data send to python socket
fwrite(obj, data,'uint8');

% wait for response
while obj.BytesAvailable == 0 
end

% make sure all of data is read
while obj.BytesAvailable > 0
    fread(obj,obj.BytesAvailable);
end

%fclose(obj);

end

