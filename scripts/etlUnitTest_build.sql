USE etlUnitTest;


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
