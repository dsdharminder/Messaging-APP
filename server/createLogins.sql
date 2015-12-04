/*This SQL SCRIPT is used by the server Unit Test program to create a fresh database with sample data*/
/* This table is used to information about the clients */
DROP TABLE IF EXISTS Users;
CREATE TABLE Users(Username TEXT NOT NULL PRIMARY KEY, Password TEXT NOT NULL, Client_IP TEXT NOT NULL, Client_Port INTEGER NOT NULL);
INSERT INTO Users VALUES("Arevor" , "pw1", "127.0.0.220", 42020);
INSERT INTO Users VALUES("Dharm" , "pw2", "127.0.0.218", 42018);
INSERT INTO Users VALUES("Calvin" , "pw3", "127.0.0.216", 42016);
INSERT INTO Users VALUES("Nolan"  , "pw4", "127.0.0.214", 42014);



/* This table is used for storing offline messages until they are requested client comes online again */
DROP TABLE IF EXISTS OfflineMsgs;
CREATE TABLE OfflineMsgs(Username TEXT NOT NULL, Msg TEXT NOT NULL, MsgSender TEXT NOT NULL);
INSERT INTO OfflineMsgs VALUES("Arevor", "offline message text", "Nolan");
INSERT INTO OfflineMsgs VALUES("Nolan", "offline message text", "Arevor");
INSERT INTO OfflineMsgs VALUES("Arevor", "offline message text 2", "Nolan");
INSERT INTO OfflineMsgs VALUES("Nolan", "offline message text 2", "Arevor");


