from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data_from_postgres(*args, **kwargs):
    start_time = kwargs.get('interval_start_datetime')
    end_time = kwargs.get('interval_end_datetime')

    is_manual_ui = kwargs.get('event') == {} and kwargs.get('context') == {} and not kwargs.get('pipeline_run_id')
    if is_manual_ui:
        # if manual run (play button UI), fallback to pulling last hour
        query = "SELECT * FROM articles WHERE updated_at >= NOW() - INTERVAL '1 HOUR'"
        print("Run Manual: Extracting last hour data.")
    else:
        # if Backfill / Trigger run
        query = f"""
            SELECT * FROM articles 
            WHERE updated_at >= '{start_time}' 
            AND updated_at < '{end_time}'
        """
        print(f"Time-Window Run: Extract from {start_time} to {end_time}")

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)