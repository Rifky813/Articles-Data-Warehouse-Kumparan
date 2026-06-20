{{ config(materialized='table') }}

WITH stg_articles AS (
    SELECT * FROM {{ ref('stg_articles') }}
)

-- Mengambil daftar penulis unik untuk tabel dimensi
SELECT DISTINCT 
    author_id
FROM stg_articles
WHERE author_id IS NOT NULL