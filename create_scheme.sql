CREATE DATABASE IF NOT EXISTS GROUP11P1;
--
USE GROUP11P1;
--
CREATE TABLE IF NOT EXISTS Tags (
    tag_id INT,
    tag_name TEXT NOT NULL,
    PRIMARY KEY (tag_id),
    UNIQUE (tag_name(100))
);
--
CREATE TABLE IF NOT EXISTS Users (
    id INT,
    reputation MEDIUMINT,  -- max value: 28918
    PRIMARY KEY (id)
);
--
CREATE TABLE IF NOT EXISTS PostTypes (
    id INT,
    type_title VARCHAR(30) NOT NULL,
    PRIMARY KEY (id)
);
--
CREATE TABLE IF NOT EXISTS Badges (
    id INT,
    badge_title VARCHAR(80),
    bagde_class TINYINT NOT NULL,
    PRIMARY KEY (id)
);
--
CREATE TABLE IF NOT EXISTS Posts (
    id INT,
    created_date DATETIME NOT NULL,
    post_score MEDIUMINT,
    created_by INT NOT NULL,
    post_type_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES Users(id), -- to prevent data loss, not adding on delete cascade
    FOREIGN KEY (post_type_id) REFERENCES PostTypes(id) -- to prevent data loss, not adding on delete cascade
);
--
CREATE TABLE IF NOT EXISTS Votes (
    vote_id INT,
    post_id INT NOT NULL,
    PRIMARY KEY (vote_id),
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE
);
--
CREATE TABLE IF NOT EXISTS Comments (
    id INT,
    user_id INT NOT NULL,
    created_at DATETIME NOT NULL,
    score MEDIUMINT,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES Users(id) -- to prevent data loss, not adding on delete cascade
);
--
CREATE TABLE IF NOT EXISTS BadgeEarns (
    user_id INT,
    badge_id INT,
    allowted_date DATETIME,
    PRIMARY KEY (user_id, badge_id, allowted_date),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (badge_id) REFERENCES Badges(id) ON DELETE CASCADE
);
--
CREATE TABLE IF NOT EXISTS PostTags (
    tag_id INT,
    post_id INT,
    PRIMARY KEY (tag_id, post_id),
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id) ON DELETE CASCADE
);
