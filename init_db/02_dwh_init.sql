USE dwh_db;

CREATE TABLE IF NOT EXISTS raw_articles (
    id Int32, 
    title String, 
    content String, 
    published_at DateTime, 
    author_id Int32, 
    created_at DateTime, 
    updated_at DateTime
) ENGINE = MergeTree() ORDER BY id;

CREATE TABLE IF NOT EXISTS raw_deleted_log (
    log_id Int32, 
    article_id Int32, 
    deleted_at DateTime
) ENGINE = MergeTree() ORDER BY log_id;