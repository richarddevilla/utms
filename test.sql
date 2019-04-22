
--Table Creation
CREATE TABLE Probes (
  name varchar(20),
  last_lat float,
  last_lng float,
  last_seen datetime,
  status varchar(20),
  PRIMARY KEY (name)
);

CREATE TABLE Sensors (
  id int NOT NULL IDENTITY(1,1) PRIMARY KEY,
  probe_name varchar(20),
  temperature float,
  humidity float,
  pressure float,
  timestamp datetime
);

--Stored Procedure 1
INSERT Sensors (probe_name, temperature, humidity, pressure, timestamp) VALUES (?,?,?,?,?);
UPDATE Probes SET last_lat = ?, last_lng = ?, last_seen = ? WHERE name = ?;

