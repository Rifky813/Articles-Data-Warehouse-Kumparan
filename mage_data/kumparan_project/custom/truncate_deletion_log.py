from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

@custom
def truncate_audit_log(*args, **kwargs):
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as db:
        db.execute("TRUNCATE TABLE deleted_articles_log;")
        
    return "Audit Log Cleared"