USE {DB_NAME};

-- SBERT ====================================================================

ALTER TABLE {MSG_TABLE_NAME}
    ADD COLUMN autoinc_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY;

ALTER TABLE feat$sbert${MSG_TABLE_NAME}$autoinc_id
    ENGINE = MyISAM;

CREATE TABLE feat$sbert${MSG_TABLE_NAME}$user_id
    LIKE feat$sbert${MSG_TABLE_NAME}$autoinc_id;

ALTER TABLE feat$sbert${MSG_TABLE_NAME}$user_id
    ENGINE = MyISAM;

INSERT INTO feat$sbert${MSG_TABLE_NAME}$user_id (group_id, feat, value, group_norm)
    SELECT user_id, feat, avg(value), avg(group_norm)
    FROM feat$sbert${MSG_TABLE_NAME}$autoinc_id AS a,
    {MSG_TABLE_NAME} AS b
    WHERE a.group_id = b.autoinc_id
    GROUP BY user_id, feat;
CREATE INDEX fdex ON feat$sbert${MSG_TABLE_NAME}$user_id (feat);
CREATE INDEX gdex ON feat$sbert${MSG_TABLE_NAME}$user_id (group_id);

-- DiscRE ==================================================================

ALTER TABLE feat$discre${MSG_TABLE_NAME}$autoinc_id
    ENGINE = MyISAM;
CREATE INDEX gdex ON feat$discre${MSG_TABLE_NAME}$autoinc_id (group_id);
CREATE INDEX fdex ON feat$discre${MSG_TABLE_NAME}$autoinc_id (feat);

UPDATE feat$discre${MSG_TABLE_NAME}$autoinc_id
    SET group_id = group_id - 1;

CREATE TABLE feat$discre${MSG_TABLE_NAME}$user_id
    LIKE feat$discre${MSG_TABLE_NAME}$autoinc_id;
ALTER TABLE feat$discre${MSG_TABLE_NAME}$user_id
    ENGINE = MyISAM;
ALTER TABLE feat$discre${MSG_TABLE_NAME}$user_id
    CHANGE COLUMN group_id group_id VARCHAR(45);
INSERT INTO feat$discre${MSG_TABLE_NAME}$user_id (group_id, feat, value, group_norm)
    SELECT user_id, feat, avg(value), avg(group_norm)
    FROM feat$discre${MSG_TABLE_NAME}$autoinc_id AS a,
    {MSG_TABLE_NAME} AS b
    WHERE a.group_id = b.autoinc_id
    GROUP BY user_id, feat;