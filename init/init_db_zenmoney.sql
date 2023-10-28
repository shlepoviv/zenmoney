CREATE TYPE "AccauntType" AS ENUM ('cash','ccard','checking', 'loan' ,'deposit' ,'emoney' ,'debt');

CREATE TABLE "serverTimestamp" (
	"serverTimestamp" TIMESTAMP NOT NULL PRIMARY KEY
) ;

CREATE TABLE "instrument" (
	"id" integer NOT NULL PRIMARY KEY,
	"changed" TIMESTAMP NOT NULL,
	"title" varchar(200) NOT NULL,
	"shortTitle" varchar(10),
	"symbol" varchar(5) NOT NULL,
	"rate" double precision NOT NULL
) ;

CREATE TABLE "country" (
	"id" integer NOT NULL PRIMARY KEY,
    "title" varchar(200) NOT NULL UNIQUE,
    "currency" integer REFERENCES "instrument" ("id"),
    "domain" varchar(10)
);



CREATE TABLE "company" (
	"id" integer NOT NULL PRIMARY KEY,
	"changed" TIMESTAMP NOT NULL,
	"title" varchar(50) NOT NULL,
	"fullTitle" varchar(200),
	"www" varchar(200),
	"country" integer REFERENCES "country" ("id")
) ;



CREATE TABLE "zenmoneyuser" (
	"id" integer NOT NULL PRIMARY KEY,
	"changed" TIMESTAMP NOT NULL,
	"login" varchar(20) NOT NULL UNIQUE,
	"currency" integer NOT NULL  REFERENCES "instrument" ("id"),
	"parent" integer REFERENCES "zenmoneyuser" ("id")
) ;



CREATE TABLE "account" (
	"id" uuid NOT NULL PRIMARY KEY,
	"changed" TIMESTAMP NOT NULL,
	"zenmoneyuser" integer NOT NULL REFERENCES "zenmoneyuser" ("id"),
	"role" integer REFERENCES "zenmoneyuser" ("id"),
	"instrument" integer REFERENCES "instrument" ("id"),
	"company" integer REFERENCES "company" ("id"),
	"type" "AccauntType" NOT NULL,
	"balance" double precision NOT NULL,
	"title" varchar(50) NOT NULL
) ;



CREATE TABLE "transaction" (
	"id" uuid NOT NULL PRIMARY KEY,
	"changed" TIMESTAMP NOT NULL,
	"created" TIMESTAMP NOT NULL,
	"zenmoneyuser" integer NOT NULL REFERENCES "zenmoneyuser"("id"),
	"incomeInstrument" integer REFERENCES "instrument"("id"),
	"incomeAccount" uuid REFERENCES "account" ("id"),
	"income" integer NOT NULL,
	"outcomeInstrument" integer REFERENCES "instrument"("id"),
	"outcomeAccount" uuid REFERENCES "account" ("id"),
	"outcome" integer NOT NULL,
	"date" date NOT NULL
) ;