-- Database: DB_SupportPortal

-- DROP DATABASE IF EXISTS "DB_SupportPortal";

CREATE DATABASE "DB_SupportPortal"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE "DB_SupportPortal"
    IS 'База данных для портала самообслуживания';