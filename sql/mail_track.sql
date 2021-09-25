create table mail_track(
    mail_id INT NOT NULL AUTO_INCREMENT,
    date_received INT NOT NULL,
    date_processed INT NOT NULL,
    from_addr VARCHAR(128) NOT NULL,
    to_addr VARCHAR(128) NOT NULL,
    subject VARCHAR(256) NOT NULL,
    message_md5 CHAR(32),
    message_sha1 CHAR(40),
    message_sha256 CHAR(64),
    message_ssdeep VARCHAR(128),
    message_text TEXT,
    attachment_md5 CHAR(32),
    attachment_sha1 CHAR(40),
    attachment_sha256 CHAR(64),
    attachment_ssdeep VARCHAR(128),
    attachment_data MEDIUMBLOB,
    PRIMARY KEY ( mail_id )
);
