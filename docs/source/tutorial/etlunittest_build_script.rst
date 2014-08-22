Sample MySQL Database
=====================
Here is the sample MySQL database script used for the tutorial and for etlTest's own unit tests: ::

    CREATE SCHEMA IF NOT EXISTS etlUnitTest;

    USE etlUnitTest;

    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS user_dim;

    CREATE TABLE users (
                    user_id INT NOT NULL,
                    first_name VARCHAR(75) NOT NULL,
                    last_name VARCHAR(75) NOT NULL,
                    birthday DATE NOT NULL,
                    zipcode CHAR(5) NOT NULL,
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

    CREATE UNIQUE INDEX users_idx
     ON user_dim
     ( user_id );
