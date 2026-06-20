{{ config(materialized = 'table') }}

WITH current_articles AS (
    SELECT * FROM {{ ref('stg_articles') }}
),
deleted_logs AS (
    SELECT * FROM {{ ref('stg_deleted_articles') }}
)

SELECT 
    c.article_id,
    c.author_id,
    c.title,
    c.published_at,
    c.created_at,
    c.updated_at,
    -- Jika ID ada di log hapus, ubah status jadi 1 (True)
    CASE 
        WHEN d.article_id != 0 THEN 1 
        ELSE 0 
    END AS is_deleted,
    CASE
        WHEN d.article_id != 0 THEN d.deleted_at 
        ELSE c.updated_at 
    END AS last_status_date
FROM current_articles c
LEFT JOIN deleted_logs d ON c.article_id = d.article_id