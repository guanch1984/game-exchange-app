
-- CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
CREATE USER IF NOT EXISTS team065User@localhost IDENTIFIED BY 'team065admin';

DROP DATABASE IF EXISTS cs6400_summer2022_team065;
 
SET default_storage_engine=InnoDB;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS cs6400_summer2022_team065 
    DEFAULT CHARACTER SET utf8mb4 
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE cs6400_summer2022_team065;

GRANT SELECT, INSERT, UPDATE, DELETE, FILE ON *.* TO 'team065User'@'localhost';
GRANT ALL PRIVILEGES ON `team065User`.* TO 'team065User'@'localhost';
GRANT ALL PRIVILEGES ON `cs6400_summer2022_team065`.* TO 'team065User'@'localhost';
FLUSH PRIVILEGES;

-- Tables 

CREATE TABLE Address (
  postal_code varchar(250) NOT NULL,
  city varchar(250) NOT NULL,
  state varchar(250) NOT NULL,
  longitude double(16,8) NOT NULL,
  latitude double(16,8) NOT NULL,
  PRIMARY KEY (postal_code) 
);

CREATE TABLE TradePlazaUser (
  email varchar(250) NOT NULL,
  password varchar(250) NOT NULL,
  nickname varchar(250) NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  postal_code varchar(250) NOT NULL,
  PRIMARY KEY (email), 
  FOREIGN KEY (postal_code) REFERENCES Address(postal_code),
  UNIQUE (nickname)
);

CREATE TABLE Item (
  item_number int(16) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (item_number)
);

CREATE TABLE Trade (
  proposer_item_number int(16) unsigned NOT NULL,
  counter_party_item_number int(16) unsigned NOT NULL,
  trade_status varchar(250) NOT NULL,
  proposed_date DATETIME NOT NULL,
  accept_reject_date DATETIME, 
  FOREIGN KEY (proposer_item_number) REFERENCES Item(item_number),
  FOREIGN KEY (counter_party_item_number) REFERENCES Item(item_number),
  CONSTRAINT Trade_id UNIQUE (proposer_item_number, counter_party_item_number)
);

CREATE TABLE platform (
  platform_id int(16) unsigned NOT NULL AUTO_INCREMENT,
  name varchar(250) NOT NULL,
  UNIQUE (name),
  PRIMARY KEY (platform_id) 
);

CREATE TABLE VideoGame (
  item_number int(16) unsigned NOT NULL,
  title varchar(250) NOT NULL,
  description varchar(250) NOT NULL,
  game_condition ENUM ('Like New', 'Lightly Used', 'Moderately Used', 'Heavily Used', 'Damaged/Missing'),
  media ENUM ('Optical Disk', 'Game Card', 'Cartridge'),
  platform_id int(16) unsigned NOT NULL,
  email varchar(250) NOT NULL,
  PRIMARY KEY (item_number), 
  FOREIGN KEY (item_number) REFERENCES Item(item_number),
  FOREIGN KEY (platform_id) REFERENCES platform(platform_id),
  FOREIGN KEY (owner_email) REFERENCES TradePlazaUser(email)
);

CREATE TABLE ComputerGame (
  item_number int(16) unsigned NOT NULL,
  title varchar(250) NOT NULL,
  description varchar(250) NOT NULL,
  game_condition ENUM ('Like New', 'Lightly Used', 'Moderately Used', 'Heavily Used', 'Damaged/Missing'),
  platform ENUM ('Linux', 'MacOS', 'Windows'),
  email varchar(250) NOT NULL,
  PRIMARY KEY (item_number), 
  FOREIGN KEY (item_number) REFERENCES Item(item_number),
  FOREIGN KEY (owner_email) REFERENCES TradePlazaUser(email)
);

CREATE TABLE CollectibleCardGame (
  item_number int(16) unsigned NOT NULL,
  title varchar(250) NOT NULL,
  description varchar(250) NOT NULL,
  game_condition ENUM ('Like New', 'Lightly Used', 'Moderately Used', 'Heavily Used', 'Damaged/Missing'),
  number_of_cards int(16) unsigned NOT NULL,
  email varchar(250) NOT NULL,
  PRIMARY KEY (item_number), 
  FOREIGN KEY (item_number) REFERENCES Item(item_number),
  FOREIGN KEY (owner_email) REFERENCES TradePlazaUser(email)
);

CREATE TABLE PlayingCardGame (
  item_number int(16) unsigned NOT NULL,
  title varchar(250) NOT NULL,
  description varchar(250) NOT NULL,
  game_condition ENUM ('Like New', 'Lightly Used', 'Moderately Used', 'Heavily Used', 'Damaged/Missing'),
  email varchar(250) NOT NULL,
  PRIMARY KEY (item_number), 
  FOREIGN KEY (item_number) REFERENCES Item(item_number),
  FOREIGN KEY (owner_email) REFERENCES TradePlazaUser(email)
);

CREATE TABLE BoardGame (
  item_number int(16) unsigned NOT NULL,
  title varchar(250) NOT NULL,
  description varchar(250) NOT NULL,
  game_condition ENUM ('Like New', 'Lightly Used', 'Moderately Used', 'Heavily Used', 'Damaged/Missing'),
  owner_email varchar(250) NOT NULL,
  PRIMARY KEY (item_number), 
  FOREIGN KEY (item_number) REFERENCES Item(item_number),
  FOREIGN KEY (owner_email) REFERENCES TradePlazaUser(email)
);