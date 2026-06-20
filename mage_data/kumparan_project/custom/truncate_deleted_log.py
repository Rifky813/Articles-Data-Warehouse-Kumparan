from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
# if 'test' not in globals():
#     from mage_ai.data_preparation.decorators import test


@custom
def truncate_log(*args, **kwargs):
    conn = psycopg2.connect(host="postgres_source", database="source_db", user="user", password="password")
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE deleted_articles_log;")
    conn.commit()
    cur.close()
    conn.close()

    query = "TRUNCATE TABLE deleted_articles_log;"

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.load(query)
        return "Audit Log Cleared"

    return "Audit Log Cleared"
