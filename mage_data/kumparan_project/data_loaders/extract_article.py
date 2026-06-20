from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data_from_postgres(*args, **kwargs):
    # 1. Tangkap variabel waktu dari Trigger / Backfill Mage
    start_time = kwargs.get('interval_start_datetime')
    end_time = kwargs.get('interval_end_datetime')
    
    # 2. Susun Query Dinamis (Time-Window)
    if not start_time or not end_time:
        # Jika di-run manual (play button UI), fallback narik 1 jam terakhir
        query = "SELECT * FROM articles WHERE updated_at >= NOW() - INTERVAL '1 HOUR'"
        print("Run Manual: Mengekstrak data 1 jam terakhir.")
    else:
        # Jika di-run oleh Trigger / Backfill
        query = f"""
            SELECT * FROM articles 
            WHERE updated_at >= '{start_time}' 
            AND updated_at < '{end_time}'
        """
        print(f"Time-Window Run: Mengekstrak dari {start_time} sampai {end_time}")

    # 3. Eksekusi menggunakan io_config.yaml (Tanpa Hardcode)
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        # Pemuat bawaan Mage ini otomatis mengembalikan Pandas DataFrame
        return loader.load(query)