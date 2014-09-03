CREATE SCHEMA IF NOT EXISTS etlUnitTest;

USE etlUnitTest;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS user_dim;
DROP TABLE IF EXISTS user_geo_ref;

CREATE TABLE users (
                user_id INT NOT NULL,
                first_name VARCHAR(75) NOT NULL,
                last_name VARCHAR(75) NOT NULL,
                birthday DATE NOT NULL,
                zipcode CHAR(5) NOT NULL,
                is_active TINYINT(1) NOT NULL DEFAULT 1,
                PRIMARY KEY (user_id)
);


CREATE UNIQUE INDEX users_idx
 ON users
 ( user_id );

CREATE TABLE user_dim (
                user_id INT NOT NULL,
                first_name VARCHAR(75) NOT NULL,
                last_name VARCHAR(75) NOT NULL,
                birthday DATE NOT NULL,
                zipcode CHAR(5) NOT NULL,
                PRIMARY KEY (user_id)
);

CREATE UNIQUE INDEX users_dim_idx
 ON user_dim
 ( user_id );

CREATE TABLE user_geo_ref (
  user_geo_ref_id INT NOT NULL,
  zipcode CHAR(5) NOT NULL,
  city VARCHAR(75) NOT NULL,
  state VARCHAR(75) NOT NULL,
  country VARCHAR(150) NOT NULL,
  PRIMARY KEY (user_geo_ref_id)
);

CREATE UNIQUE INDEX user_geo_ref_idx
  ON user_geo_ref
  ( user_geo_ref_id );