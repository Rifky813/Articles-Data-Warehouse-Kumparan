CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    published_at TIMESTAMP,
    author_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABEL BARU: Untuk mencatat ID yang dihapus
CREATE TABLE deleted_articles_log (
    log_id SERIAL PRIMARY KEY,
    article_id INT NOT NULL,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FUNGSI LOGIC: Menyalin ID yang dihapus
CREATE OR REPLACE FUNCTION log_deleted_article()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO deleted_articles_log (article_id) VALUES (OLD.id);
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER: Aktif setiap kali ada DELETE
CREATE TRIGGER trigger_article_delete
AFTER DELETE ON articles
FOR EACH ROW
EXECUTE FUNCTION log_deleted_article();

-- Insert Data Historis 2016
INSERT INTO articles (title, content, published_at, author_id, created_at, updated_at) VALUES
('Tech Startup Boom 2016', 'Content from 2016...', '2016-04-10 10:00:00', 1, '2016-04-10 10:00:00', '2016-04-10 10:00:00'),
('The Rise of AI', 'Machine learning trends...', '2019-08-15 14:00:00', 2, '2019-08-15 14:00:00', '2019-08-15 14:00:00'),
('Modern Data Stack 2023', 'ELT is the new standard...', '2023-01-20 09:00:00', 3, '2023-01-20 09:00:00', '2023-01-20 09:00:00');