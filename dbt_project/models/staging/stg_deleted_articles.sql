{{ config(materialized='view') }}

SELECT
    article_id,
    deleted_at
FROM {{ source('default', 'raw_deleted_log') }}