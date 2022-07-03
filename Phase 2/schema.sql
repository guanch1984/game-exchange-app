CREATE USER IF NOT EXISTS gatechUser@localhost IDENTIFIED by 'gatech123';

DROP DATABASE IF EXISTS cs6400_sum22_team065;
SET default_storage_engine=InnoDB;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS cs6400_sum22_team065
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE cs6400_sum22_team065;

GRANT SELECT, INSERT, UPDATE, DELETE, FILE On *.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `gatechuser`.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `cs6400_sum22_team065`.* TO 'gatechUser'@'localhost';

CREATE TABLE User (
    Email VARCHAR(20) NOT NULL,
    PostalCode VARCHAR(5) NOT NULL,
    Password VARCHAR(20) NOT NULL,
    Nickname VARCHAR(20) UNIQUE,
    FirstName VARCHAR(20) NOT NULL,
    LastName VARCHAR(20) NOT NULL,
    PRIMARY KEY(Email)
);

CREATE TABLE Item (
    ItemNumber INT(16) NOT NULL,
    UserEmail VARCHAR(20) NOT NULL,
    Title VARCHAR(20) NOT NULL,
    Description VARCHAR(50),
    PRIMARY KEY(ItemNumber)
);

CREATE TABLE ItemCondition (
    Type VARCHAR(20) NOT NULL,
    ItemNumber INT(16) NOT NULL,
    PRIMARY KEY(Type, ItemNumber)
);

CREATE TABLE Address (
    PostalCode VARCHAR(5) NOT NULL,
    City VARCHAR(20) NOT NULL,
    State VARCHAR(20) NOT NULL,
    Latitude INT(16) NOT NULL,
    Longitude INT(16) NOT NULL,
    PRIMARY KEY(PostalCode)
);

CREATE TABLE Trade (
    ProposedItemNumber INT(16) NOT NULL,
    CounterItemNumber INT(16),
    IsTradeAccepted BOOLEAN NOT NULL DEFAULT 0,
    ProposedDate datetime NOT NULL,
    TradeStatus VARCHAR(10),
    FulfilledDate datetime,
    PRIMARY KEY(ProposedItemNumber, CounterItemNumber)
);

CREATE TABLE BoardGame (
    ItemNumber INT(16) NOT NULL AUTO_INCREMENT,
    PRIMARY KEY(ItemNumber)
);

CREATE TABLE PlayingCardGame (
    ItemNumber INT(16) NOT NULL,
    PRIMARY KEY(ItemNumber)
);

CREATE TABLE CollectibleCardGame (
    ItemNumber INT(16) NOT NULL,
    NoCards INT(16) NOT NULL,
    PRIMARY KEY(ItemNumber)
);

CREATE TABLE VideoGame (
    ItemNumber INT(16) NOT NULL,
    PlatformName VARCHAR(20) NOT NULL,
    MediaName VARCHAR(20) NOT NULL,
    PRIMARY KEY(ItemNumber)
);

CREATE TABLE ComputerGame (
    ItemNumber INT(16) NOT NULL,
    PlatformName VARCHAR(20) NOT NULL,
    PRIMARY KEY(ItemNumber)
);

CREATE TABLE Media (
    Name VARCHAR(20) NOT NULL,
    PRIMARY KEY (Name)
);

CREATE TABLE Platform (
    Name VARCHAR(20) NOT NULL,
    PRIMARY KEY (Name)
);

-- Add foreign key relationships now that all the attributes exists
ALTER TABLE User
    ADD CONSTRAINT fk_UserAddress FOREIGN KEY (PostalCode) REFERENCES Address(PostalCode);

ALTER TABLE Item
    ADD CONSTRAINT fk_ItemUser FOREIGN KEY (UserEmail) REFERENCES USER(Email);

ALTER TABLE ItemCondition
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

ALTER TABLE ComputerGame
    AdD CONSTRAINT fk_ComputerGameItem FOREIGN KEY (ItemNumber) REFERENCES Item(ItemNumber),
    ADD CONSTRAINT fk_ComputerGamePlatform FOREIGN KEY (PlatformName) REFERENCES Platform(Name);