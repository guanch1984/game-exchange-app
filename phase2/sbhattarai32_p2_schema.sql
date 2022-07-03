-- CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';

CREATE USER IF NOT EXISTS gatechUser@localhost IDENTIFIED BY 'gatech123';

DROP DATABASE IF EXISTS `cs6400_su2_team65`;

SET default_storage_engine=InnoDB;

SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS cs6400_su2_team65

   DEFAULT CHARACTER SET utf8mb4

   DEFAULT COLLATE utf8mb4_unicode_ci;

USE cs6400_su2_team65;

GRANT SELECT, INSERT, UPDATE, DELETE, FILE ON *.* TO 'gatechUser'@'localhost';

GRANT ALL PRIVILEGES ON `gatechuser`.* TO 'gatechUser'@'localhost';

GRANT ALL PRIVILEGES ON `cs6400_fa17_team001`.* TO 'gatechUser'@'localhost';

FLUSH PRIVILEGES;

-- Tables

CREATE TABLE Address(
	PostalCode varchar(50) NOT NULL,
	City varchar(50) NOT NULL,
	State varchar(50) NOT NULL,
	Latitude float(9,2) NOT NULL,
	Longitude float(9,2) NOT NULL,
	PRIMARY KEY (PostalCode)
);


CREATE TABLE `User`(
	Email varchar(50) NOT NULL,
	Address varchar(50) NOT NULL,
	Password varchar(50) NOT NULL,
	NickName varchar(50) NOT NULL,
	FirstName varchar(50) NOT NULL,
	LastName varchar(50) NOT NULL,
	PRIMARY KEY (Email),
	UNIQUE KEY (NickName),
	FOREIGN KEY (Address) REFERENCES Address(PostalCode)
);

CREATE TABLE Item(
	ItemNumber int NOT NULL,
	Title varchar(50) NOT NULL,
	Description varchar(50),
	Owner varchar(50) NOT NULL,
	ItemCondition varchar(50) NOT NULL,
	PRIMARY KEY (ItemNumber),
	FOREIGN KEY (Owner) REFERENCES `User`(Email)
);


CREATE TABLE Media(
	Name varchar(50) NOT NULL,
	PRIMARY KEY (Name)
);


CREATE TABLE VideoGamePlatform(
	Name varchar(50) NOT NULL,
	PRIMARY KEY (Name)
);


CREATE TABLE ComputerGamePlatform(
	Name varchar(50) NOT NULL,
	PRIMARY KEY (Name)
);



CREATE TABLE BoardGame(
	ItemNumber int NOT NULL,
	PRIMARY KEY (ItemNumber),
	FOREIGN KEY (ItemNumber) REFERENCES Item(ItemNumber)
);

CREATE TABLE PlayingCardGame(
	ItemNumber int NOT NULL,
	PRIMARY KEY (ItemNumber),
	FOREIGN KEY (ItemNumber) REFERENCES Item(ItemNumber)
);


CREATE TABLE CollectibleCardGame(
	ItemNumber int NOT NULL,
	NumberOfCards int NOT NULL,
	PRIMARY KEY (ItemNumber),
	FOREIGN KEY (ItemNumber) REFERENCES Item(ItemNumber)
);


CREATE TABLE VideoGame(
	ItemNumber int NOT NULL,
	Platform varchar(50) NOT NULL,
	Media varchar(50) NOT NULL,
	PRIMARY KEY (ItemNumber),
	FOREIGN KEY (ItemNumber) REFERENCES Item(ItemNumber),
	FOREIGN KEY (Platform) REFERENCES VideoGamePlatform(Name),
	FOREIGN KEY (Media) REFERENCES Media(Name)
);


CREATE TABLE ComputerGame(
	ItemNumber int NOT NULL,
	Platform varchar(50) NOT NULL,
	PRIMARY KEY (ItemNumber),
	FOREIGN KEY (ItemNumber) REFERENCES Item(ItemNumber),
	FOREIGN KEY (Platform) REFERENCES ComputerGamePlatform(Name)
);

CREATE TABLE Trade(
	Proposer varchar(50) NOT NULL,
	Acceptor varchar(50) NOT NULL,
	ProposedItem int NOT NULL,
	DesiredItem int NOT NULL,
	ResponseDate datetime,
	ProposedDate datetime NOT NULL,
	TradeStatus varchar(50) NOT NULL,
	UNIQUE (Proposer,Acceptor,ProposedItem,DesiredItem),
	FOREIGN KEY (Proposer) REFERENCES `User`(Email),
	FOREIGN KEY (Acceptor) REFERENCES `User`(Email),
	FOREIGN KEY (ProposedItem) REFERENCES Item(ItemNumber),
	FOREIGN KEY (DesiredItem) REFERENCES Item(ItemNumber)
);
