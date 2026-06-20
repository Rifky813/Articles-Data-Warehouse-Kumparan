{{ config(materialized='view') }}

SELECT
    id AS article_id,
    title,
    content,
    published_at,
    author_id,
    created_at,
    updated_at
FROM {{ source('default', 'raw_articles') }}