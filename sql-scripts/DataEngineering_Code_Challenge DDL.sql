CREATE DATABASE IF NOT EXISTS vivid;
USE vivid;

CREATE USER app_user IDENTIFIED BY 'app-user-secret-pw';
GRANT SELECT, INSERT, UPDATE, DELETE ON vivid.* TO app_user;

DROP TABLE IF EXISTS vivid.seed;
CREATE TABLE vivid.seed
       (
              event_id INT NOT NULL,
              section VARCHAR(255),
              quantity INT NOT NULL,
              price DECIMAL(8, 2) DEFAULT 0.00 NOT NULL,
              rownum VARCHAR(255)
       );

DROP TABLE IF EXISTS vivid.tickets;
CREATE TABLE vivid.tickets
       (
              event_id INT NOT NULL,
              section VARCHAR(255),
              rownum VARCHAR(255),
              seat VARCHAR(255),
              price DECIMAL(8, 2) DEFAULT 0.00 NOT NULL,
              seller_id INT NOT NULL,
              status SMALLINT,
              created_at DATETIME DEFAULT NOW(),
              updated_at DATETIME DEFAULT NOW(),
              PRIMARY KEY (event_id, section, rownum, seat, status),
              INDEX idx_tickets_on_event_id (event_id))
         PARTITION BY LIST( status ) (
              PARTITION p_active VALUES IN (1),
              PARTITION p_inactive VALUES IN (0),
              PARTITION p_onhold VALUES IN (2)
       );
DROP TABLE IF EXISTS vivid.sessions;
CREATE TABLE vivid.sessions
       (
              id INT NOT NULL AUTO_INCREMENT,
              session_data VARCHAR(255),
              event_id INT,
              buyer_id INT,
              referral VARCHAR(255),
              created_at DATETIME DEFAULT NOW(),
              updated_at DATETIME DEFAULT NOW(),
              PRIMARY KEY (id)
       );

DROP TABLE IF EXISTS vivid.events;
CREATE TABLE vivid.events
       (
              id INT NOT NULL AUTO_INCREMENT,
              name VARCHAR(255),
              type VARCHAR(255),
              venue_id INT NOT NULL,           
              event_dt DATETIME,
              created_at DATETIME DEFAULT NOW(),
              updated_at DATETIME DEFAULT NOW(),
              PRIMARY KEY (id),
              INDEX idx_events_on_venue_id (venue_id),
              INDEX idx_events_on_event_dt (event_dt)
       );

DROP TABLE IF EXISTS vivid.venues;
CREATE TABLE vivid.venues
       (
              id INT NOT NULL AUTO_INCREMENT,
              name VARCHAR(255),
              address_id INT,
              created_at DATETIME DEFAULT NOW(),
              updated_at DATETIME DEFAULT NOW(),
              PRIMARY KEY (id)
       );

DROP TABLE IF EXISTS vivid.seats;
CREATE TABLE vivid.seats
       (
              id INT NOT NULL AUTO_INCREMENT,
              venue_id INT NOT NULL,           
              section VARCHAR(255),
              rownum VARCHAR(255),
              seat VARCHAR(255),
              best_rank INT, -- 1 best to 10 worst
              created_at DATETIME DEFAULT NOW(),
              updated_at DATETIME DEFAULT NOW(),
              PRIMARY KEY (id),
              INDEX idx_seats_on_venue_id (venue_id)
       );

DROP TABLE IF EXISTS vivid.addresses;
CREATE TABLE vivid.addresses
       (
              id INT NOT NULL AUTO_INCREMENT,
              address1 VARCHAR(255),
              address2 VARCHAR(255),
              city VARCHAR(255),
              state VARCHAR(255),
              zipcode VARCHAR(255),
              phone VARCHAR(255),
              created_at DATETIME DEFAULT NOW(),
              updated_at DATETIME DEFAULT NOW(),
              PRIMARY KEY (id),
              INDEX idx_addresses_on_city (city)
       );

