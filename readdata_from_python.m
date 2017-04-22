function [data] = readdata_from_python(obj)

data = [];
data_cnt = 0;

% burn through until data is there
while obj.BytesAvailable == 0 end
len = fread(obj, [1,3]);

% python socket interprets first 3 bytes as length of data
length2read = 2^16*len(1) + 2^8*len(2) + 2^0*len(3);

while data_cnt < length2read
    % burn clocks waiting for data to be available
    while(obj.BytesAvailable == 0)
    end
    data_cnt = data_cnt + obj.BytesAvailable;
    new_data = fread(obj, [1, obj.BytesAvailable]);
    data = [data,new_data];
end
