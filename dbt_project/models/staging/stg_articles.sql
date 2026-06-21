{{ config(materialized='view') }}

SELECT
CAST(id AS UInt64) AS article_id,
    CAST(author_id AS UInt64) AS author_id,
    TRIM(CAST(title AS String)) AS title,
    CAST(content AS String) AS content,
    CAST(published_at AS DateTime) AS published_at,
    CAST(created_at AS DateTime) AS created_at,
    CAST(updated_at AS DateTime) AS updated_at
FROM {{ source('default', 'raw_articles') }}
WHERE id IS NOT NULL