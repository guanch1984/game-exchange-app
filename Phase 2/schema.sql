CREATE USER IF NOT EXISTS gatechUser@localhost IDENTIFIED by 'gatech123';

DROP DATABASE IF EXISTS `cs6400_sm22_team_065`;
SET default_storage_engine=InnoDB;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS cs6400_sum22_team065
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE cs6400_sm22_team_065;

GRANT SELECT, INSERT, UPDATE, DELETE, FILE On *.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `gatechuser`.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `cs6400_sum22_team065`.* TO 'gatechUser'@'localhost';

CREATE TABLE User (
    Email VARCHAR(20) PRIMARY KEY,
    PostalCode VARCHAR(5),
    Password VARCHAR(20),
    Nickname VARCHAR(20) UNIQUE,
    FirstName VARCHAR(20),
    LastName VARCHAR(20)
);;

CREATE TABLE Item (
    ItemNumber INT(16) PRIMARY KEY,
    UserEmail VARCHAR(20),
    Title VARCHAR(20),
    Description VARCHAR(50)
);

CREATE TABLE Condition(
    Type VARCHAR(20) PRIMARY KEY,
    ItemNumber INT(16)
);

CREATE TABLE Address (
    PostalCode VARCHAR(5) PRIMARY KEY,
    City VARCHAR(20),
    State VARCHAR(20),
    Latitude INT(16),
    Longitude INT(16)
);

CREATE TABLE Trade (
    ProposedItemNumber INT(16),
    CounterItemNumber INT(16),
    IsTradeAccepted BOOLEAN,
    ProposedDate datetime,
    TradeStatus VARCHAR(10),
    FulfilledDate datetime
);

CREATE TABLE BoardGame (
    ItemNumber INT(16)
);

CREATE TABLE PlayingCardGame (
    ItemNumber INT(16)
);

CREATE TABLE CollectibleCardGame (
    ItemNumber INT(16),
    NoCards INT(16)
);

CREATE TABLE VideoGame (
    ItemNumber INT(16),
    PlatformName VARCHAR(20),
    MediaName VARCHAR(20)
);

CREATE TABLE ComputerGame (
    ItemNumber INT(16),
    PlatformName VARCHAR(20)
);

CREATE TABLE Media (
    Name VARCHAR(20) PRIMARY KEY
);

CREATE TABLE Platform (
    Name VARCHAR(20) PRIMARY KEY
);


ALTER TABLE User
    ADD CONSTRAINT fk_UserAddress FOREIGN KEY (PostalCode) REFERENCES Address(PostalCode);

ALTER TABLE Item
    ADD CONSTRAINT fk_ItemUser FOREIGN KEY (UserEmail) REFERENCES USER(Email);

ALTER TABLE Condition
    ADD CONSTRAINT fk_ConditionItem FOREIGN KEY (ItemNumber) REFERENCES Item(ItemNumber);

ALTER TABLE Trade
    ADD CONSTRAINT fk_TradeProposedNumber FOREIGN KEY (ProposedItemNumber) REFERENCES Item(ItemNumber),
    ADD CONSTRAINT fk_TradeCounterNumber FOREIGN KEY (CounterItemNumber) REFERENCES Item(ItemNumber);

ALTER TABLE BoardGame
    ADD CONSTRAINT fk_BoardGameItem FOREIGN KEY (ItemNumber) REFERENCES Item(ItemNumber);

ALTER TABLE PlayingCardGame
    ADD CONSTRAINT fk_PlayingCardGameItem FOREIGN KEY (ItemNumber) REFERENCES Item(ItemNumber);

ALTER TABLE CollectibleCardGame
    ADD CONSTRAINT fk_CollectibleCardGameItem FOREIGN KEY (ItemNumber) REFERENCES Item(ItemNumber);

ALTER TABLE VideoGame
    ADD CONSTRAINT fk_VideoGameItem FOREIGN KEY (ItemNumber) REFERENCES Item(ItemNumber),
    ADD CONSTRAINT fk_VideoGamePlatform FOREIGN KEY (PlatformName) REFERENCES Platform(Name),
    ADD CONSTRAINT fk_MediaName FOREIGN KEY (MediaName) REFERENCES Media(Name);

ADD TABLE ComputerGame
    AdD CONSTRAINT fk_ComputerGameItem FOREIGN KEY (ItemNumber) REFERENCES Item(ItemNumber),
    ADD CONSTRAINT fk_ComputerGamePlatform FOREIGN KEY (PlatformName) REFERENCES Platform(Name);