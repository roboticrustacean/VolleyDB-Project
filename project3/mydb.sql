DROP DATABASE IF EXISTS VolleyDB;
CREATE DATABASE VolleyDB;
USE VolleyDB;

CREATE TABLE Positions 
(
    position_ID	INT NOT NULL,
    position_name	VARCHAR(512),
    PRIMARY KEY (position_ID)
);

CREATE TABLE Player 
(
    username	VARCHAR(512) NOT NULL,
    password	VARCHAR(512) NOT NULL,
    name	VARCHAR(512),
    surname	VARCHAR(512),
    date_of_birth	DATE,
    height	INT,
    weight	INT,
    PRIMARY KEY (username)
);


CREATE TABLE PlayerPositions (
    player_positions_id INT NOT NULL,
    username VARCHAR(512) NOT NULL,
    position_id INT NOT NULL, -- AT LEAST 1 POSITION FOR A PLAYER IS REQUIRED
    PRIMARY KEY (player_positions_id),
    FOREIGN KEY (username) REFERENCES Player(username) ON DELETE CASCADE,
    FOREIGN KEY (position_id) REFERENCES positions(position_id)
);

CREATE TABLE PlayerTeams (
    player_teams_id INT NOT NULL,
    username VARCHAR(512) NOT NULL,
    team INT NOT NULL,
    PRIMARY KEY (player_teams_id),
    FOREIGN KEY (username) REFERENCES Player(username) ON DELETE CASCADE,
    FOREIGN KEY (team) REFERENCES Team(team_id)
);


CREATE TABLE Coach 
(
    username	VARCHAR(512) NOT NULL,
    password	VARCHAR(512) NOT NULL,
    name	VARCHAR(512),
    surname	VARCHAR(512),
    nationality	VARCHAR(512) NOT NULL, 
    PRIMARY KEY (username)
);

CREATE TABLE Jury 
(
    username	VARCHAR(512) NOT NULL,
    password	VARCHAR(512) NOT NULL,
    name	VARCHAR(512),
    surname	VARCHAR(512),
    nationality	VARCHAR(512) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE channel (
channel_id INT NOT NULL,
channel_name VARCHAR(255),
PRIMARY KEY (channel_id)
);

CREATE TABLE Team (
    team_id INT PRIMARY KEY NOT NULL,
    team_name VARCHAR(255) NOT NULL,
    coach_username VARCHAR(255) NOT NULL,
    contract_start DATE,
    contract_finish DATE,
    channel_id INT,
    FOREIGN KEY (coach_username) REFERENCES coach(username),
    FOREIGN KEY (channel_id) REFERENCES channel(channel_id),
    UNIQUE (coach_username, team_id)  -- Ensures each coach can only direct one team
);


CREATE TABLE SessionSquads (
squad_id INT NOT NULL,
session_id INT NOT NULL,
player_username VARCHAR(255) NOT NULL,
position_id INT NOT NULL,
PRIMARY KEY (squad_id),
FOREIGN KEY (session_id) REFERENCES Matchsessions(session_id) ON DELETE CASCADE,
FOREIGN KEY (player_username) REFERENCES player(username),
FOREIGN KEY (position_id) REFERENCES Positions(position_id)
);

CREATE TABLE MatchSessions (
session_id INT NOT NULL,
team_id INT NOT NULL,
stadium_id INT NOT NULL,
time_slot INT NOT NULL,
date DATE NOT NULL,
assigned_jury_username VARCHAR(255) NOT NULL,
rating FLOAT,
PRIMARY KEY (session_id),
FOREIGN KEY (team_id) REFERENCES Team(team_id),
FOREIGN KEY (stadium_id) REFERENCES Stadium(stadium_id),
FOREIGN KEY (assigned_jury_username) REFERENCES jury(username),
CONSTRAINT unique_stadium_time_slot UNIQUE (stadium_id, time_slot, date)
);

CREATE TABLE stadium (
stadium_id INT NOT NULL,
stadium_name VARCHAR(255),
stadium_country VARCHAR(255),
PRIMARY KEY (stadium_id)
);

DELIMITER //
DELIMITER //

CREATE TRIGGER check_time_slot_overlap
BEFORE INSERT ON MatchSessions
FOR EACH ROW
BEGIN
    DECLARE is_overlapping INT;
    
    -- Check if there are any overlapping sessions
    SELECT COUNT(*)
    INTO is_overlapping
    FROM MatchSessions
    WHERE stadium_id = NEW.stadium_id
    AND date = NEW.date
    AND (
        (NEW.time_slot >= time_slot AND NEW.time_slot < time_slot + 2) -- Check if new session starts during an existing session
        OR (NEW.time_slot + 2 > time_slot AND NEW.time_slot + 2 <= time_slot + 2) -- Check if new session ends during an existing session
        OR (NEW.time_slot <= time_slot AND NEW.time_slot + 2 >= time_slot + 2) -- Check if new session encompasses an existing session
    );

    IF is_overlapping > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot insert. Match session overlaps with existing session.';
    END IF;
END //

DELIMITER ;
DELIMITER //

CREATE TRIGGER check_jury_rating_trigger
BEFORE UPDATE ON MatchSessions
FOR EACH ROW
BEGIN
    DECLARE is_already_rated BOOLEAN;

    -- Check if the jury has already rated this session
    SELECT EXISTS (
        SELECT *
        FROM MatchSessions
        WHERE session_id = NEW.session_id
        AND assigned_jury_username = NEW.assigned_jury_username
        AND rating IS NOT NULL
    ) INTO is_already_rated;

    IF NOT is_already_rated THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Jury has already rated this match session.';
    END IF;
END //

DELIMITER ;
DELIMITER $$

CREATE TRIGGER coach_contract_conflict
BEFORE INSERT ON team FOR EACH ROW
BEGIN
	IF EXISTS (
		SELECT *
        FROM team AS TM
        WHERE TM.coach_username = NEW.coach_username AND (STR_TO_DATE(NEW.contract_start, '%d.%m.%Y') <= STR_TO_DATE(TM.contract_end, '%d.%m.%Y') OR STR_TO_DATE(NEW.contract_end, '%d.%m.%Y') >= STR_TO_DATE(TM.contract_start, '%d.%m.%Y') )
        )
	THEN 
		SIGNAL SQLSTATE '45000' SET message_text = "Coach has a conflict.";
	END IF;
END$$

DELIMITER ;

DELIMITER $$
CREATE TRIGGER max4TimeSlot
BEFORE INSERT ON matchsessions
FOR EACH ROW
BEGIN
    IF ( NEW.time_slot < 1 OR NEW.time_slot > 3
    ) THEN 
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = "TimeSlot must be 1,2 or 3. ";
    END IF;
END$$

DELIMITER ;
DELIMITER $$

CREATE TRIGGER player_schedule_conflict
BEFORE INSERT ON SessionSquads
FOR EACH ROW
BEGIN
    -- Check if there exists another session at the same time
    IF EXISTS (
        SELECT 1
        FROM SessionSquads SS
        JOIN MatchSessions MS1 ON MS1.session_id = SS.session_id
        JOIN MatchSessions MS2 ON MS1.session_id = MS2.session_id
        WHERE SS.username = NEW.username
          AND MS1.date = MS2.date
          AND (MS1.time_slot = MS2.time_slot OR MS1.time_slot = MS2.time_slot + 1 OR MS1.time_slot + 1 = MS2.time_slot)
          AND SS.session_id != NEW.session_id
    ) THEN 
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = "Player has a conflict.";
    END IF;
END$$

DELIMITER ;
DELIMITER $$
CREATE TRIGGER check_squad_size
BEFORE INSERT ON SessionSquads
FOR EACH ROW
BEGIN
    DECLARE squad_size INT;
    SELECT COUNT(*) INTO squad_size
    FROM SessionSquads
    WHERE session_id = NEW.session_id;

    IF squad_size >= 6 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot add more than 6 players to a session.';
    END IF;
END;
DELIMITER ;
DELIMITER $$

CREATE TRIGGER check_player_position
BEFORE INSERT ON SessionSquads
FOR EACH ROW
BEGIN
    DECLARE valid_position INT;
    SELECT COUNT(*) INTO valid_position
    FROM PlayerPositions
    WHERE username = NEW.player_username AND position_id = NEW.position_id;

    IF valid_position = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Player is not registered for the specified position.';
    END IF;
END;
DELIMITER ;
DELIMITER //

CREATE TRIGGER check_coach_nationality
BEFORE INSERT ON Coach
FOR EACH ROW
BEGIN
    DECLARE nationality_exists INT;

    SELECT COUNT(*)
    INTO nationality_exists
    FROM Coach
    WHERE username = NEW.username AND nationality = NEW.nationality;

    IF nationality_exists > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Each coach can have only one nationality.';
    END IF;
END //

DELIMITER ;
DELIMITER $$

CREATE TRIGGER check_jury_nationality
BEFORE INSERT ON Jury
FOR EACH ROW
BEGIN
    DECLARE nationality_count INT;
    
    SELECT COUNT(*)
    INTO nationality_count
    FROM Jury
    WHERE username = NEW.username AND nationality = NEW.nationality;

    IF nationality_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Each jury member can have only one nationality.';
    END IF;
END$$

DELIMITER ;








