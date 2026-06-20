-- Ekstrak data artikel yang baru/berubah
SELECT * FROM articles 
WHERE updated_at >= NOW() - INTERVAL '1 HOUR';