CREATE TABLE `events` (
	`ID` INT,
	`name` TEXT,
	`desc` TEXT
);

CREATE TABLE `city` (
    `name` varchar(255),
    `country` varchar(255),
    `population` INT,
    `latitude`  float,
    `longitude` float,
    `desc` TEXT,
    `wealth` INT,
    `store` TEXT
);

CREATE TABLE `store` (
    `name` varchar(255),
    `cost`  BIGINT,
    `production` INT
);

CREATE TABLE `product` (
    `name` varchar(255),
    `value`  BIGINT,
    `cost` BIGINT
);