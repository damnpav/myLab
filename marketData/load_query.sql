LOAD DATA INFILE "ANA.MC.csv"
INTO TABLE ibexData
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(Date, @cosa, High, Low, Close, @cosa, Volume)