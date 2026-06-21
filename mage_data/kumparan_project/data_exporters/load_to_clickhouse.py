from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.clickhouse import ClickHouse
from os import path
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data(df_articles, df_logs, *args, **kwargs):
    # 1. Panggil konfigurasi dari io_config.yaml
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    # 2. Buka koneksi menggunakan ClickHouse Loader bawaan Mage
    loader = ClickHouse.with_config(ConfigFileLoader(config_path, config_profile))
        
    # 3. Push Article DataFrame ke ClickHouse (jika tidak kosong)
    if isinstance(df_articles, pd.DataFrame) and not df_articles.empty:
        # Sinkronkan tipe data agar cocok dengan schema ClickHouse
        df_articles['id'] = df_articles['id'].astype(int)
        df_articles['author_id'] = df_articles['author_id'].astype(int)

        loader.export(
            df_articles,
            table_name='raw_articles',
            database='dwh_db',
            index=False,
            if_exists='append', # Menambahkan data tanpa menghapus tabel
        )
        print(f"Successfully loaded {len(df_articles)} rows to raw_articles")
    else:
        print(f"No new articles at this hour. {len(df_articles)}")
        
    # 4. Push Deletion Logs DataFrame ke ClickHouse (jika tidak kosong)
    if isinstance(df_logs, pd.DataFrame) and not df_logs.empty:
        df_logs['log_id'] = df_logs['log_id'].astype(int)
        df_logs['article_id'] = df_logs['article_id'].astype(int)
        
        loader.export(
            df_logs,
            table_name='raw_deleted_log',
            database='dwh_db',
            index=False,
            if_exists='append',
        )
        print(f"Successfully loaded {len(df_logs)} rows to raw_deleted_log")
    else:
        print("No deletion logs at this hour.")

    return "Load Finished"