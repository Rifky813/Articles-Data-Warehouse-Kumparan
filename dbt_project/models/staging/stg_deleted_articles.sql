{{ config(materialized='view') }}

SELECT
    CAST(article_id AS UInt64) AS article_id,
    CAST(deleted_at AS DateTime) AS deleted_at
FROM {{ source('default', 'raw_deleted_log') }}
WHERE article_id IS NOT NULL