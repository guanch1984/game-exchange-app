DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE  rolname = 'gatechUser') THEN

      CREATE ROLE gatechUser LOGIN PASSWORD 'gatech123';
   END IF;
END
$do$;

DROP DATABASE IF EXISTS cs6400_summer2022_team065;

CREATE DATABASE cs6400_summer2022_team065 

GRANT all PRIVILEGES ON all tables in schema PUBLIC TO gatechUser;
GRANT all PRIVILEGES ON all tables in schema gametrade TO gatechUser;


-- Tables🪟

CREATE TABLE if not exists "USER" (
    Email VARCHAR(10) PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    "password" VARCHAR(50) NOT NULL, 
    postal_code VARCHAR(50) NOT null,
    UNIQUE(postal_code),
    CONSTRAINT fk_Address_postal_code_User_postal_code
      FOREIGN KEY(postal_code) 
      REFERENCES "Address"(postal_code)
 );

CREATE table if not exists Address (
    postal_code VARCHAR(50) PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    "state" VARCHAR(50) NOT NULL,
    longtitude DECIMAL(12,9) NOT NULL,
    latitude  DECIMAL(12,9) NOT NULL
 );

 CREATE TABLE if not exists ItemListing (
  email VARCHAR(10) NOT NULL,
  item_number INT NOT NULL,
  name_title VARCHAR(250) NOT NULL,
  "condition" VARCHAR(50) NOT NULL,
  "description" VARCHAR(250) NULL,
  primary key (item_number),
  CONSTRAINT fk_ItemListing_email_User_email
    FOREIGN KEY(email) 
    REFERENCES "USER"(email),
  UNIQUE(item_number)
);


CREATE TABLE if not exists ComputerGame (
    item_number INT NOT NULL,
    platform_id VARCHAR(250) NOT NULL,
    CONSTRAINT fk_ComputerGame_item_number_ItemListing_item_number
      FOREIGN KEY(item_number) 
      REFERENCES ItemListing (item_number),
    CONSTRAINT fk_CG_platform_Platform_platform_name
      FOREIGN KEY(platform_id) 
      REFERENCES CG_Platform(platform_id),
    UNIQUE(item_number)
 );


CREATE TABLE if not exists CollectibleCardGame (
    item_number INT NOT NULL,
    no_of_cards INT NOT NULL,
    CONSTRAINT fk_CollectibleCardGame_item_number_ItemListing_item_number
      FOREIGN KEY(item_number) 
      REFERENCES ItemListing (item_number),
    UNIQUE(item_number)
 );

CREATE TABLE if not exists VG_Platform (  
    platform_id INT primary KEY,
    platform_name VARCHAR(250) NOT NULL
    );

CREATE TABLE if not exists CG_Platform (  
    platform_id INT primary KEY,
    platform_name VARCHAR(250) NOT NULL
    );

CREATE TABLE if not exists media (  
    media_id INT primary KEY,
    media_name VARCHAR(250) NOT NULL
    );

CREATE TABLE if not exists VideoGame (
    item_number INT NOT NULL,
    platform_id  VARCHAR(250) NOT NULL,
    media_id VARCHAR(250) NOT NULL,
    CONSTRAINT fk_VideoGame_item_number_ItemListing_item_number
      FOREIGN KEY(item_number) 
      REFERENCES ItemListing (item_number),
    CONSTRAINT fk_Video_platform_Platform_platform_name
      FOREIGN KEY(platform_id) 
      REFERENCES VG_Platform(platform_id),
    CONSTRAINT fk_media
      FOREIGN KEY(media_id) 
      REFERENCES media(media_id),
    UNIQUE(item_number)
 );



CREATE TABLE if not exists Trade (
    proposed_item_number INT ,
    desired_item_number  INT ,
    TradeId  INT ,
    proposed_date TIMESTAMP NOT NULL,
    accept_or_reject_date TIMESTAMP not null,
  	trade_status VARCHAR(8) null,
    CONSTRAINT fk_trade_proposed_item_number_id_ItemListing_item_number_id
        FOREIGN KEY(proposed_item_number)
        REFERENCES ItemListing(item_number),
    CONSTRAINT fk_trade_desired_item_number_id_ItemListing_item_number_id
        FOREIGN KEY(desired_item_number)
        REFERENCES ItemListing(item_number),
    primary KEY(TradeId)
);

