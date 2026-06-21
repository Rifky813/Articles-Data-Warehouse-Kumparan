# Kumparan Data Engineer Assessment

## Architecture Overview
This project implements a Modern Data Stack leveraging an **ELT (Extract, Load, Transform)** paradigm. It transitions away from traditional batch processing toward a real-time, streaming CDC architecture.

**Tech Stack:**
- **Source:** PostgreSQL (Logical Replication enabled).
- **Ingestion (CDC):** PeerDB.
- **Data Warehouse:** ClickHouse.
- **Transformation:** dbt.
- **Orchestration:** Mage.ai.

## Fulfilling the Requirements

1. **Hourly ELT Pipeline**
   - **Extract & Load:** Handled continuously in real-time by **PeerDB** reading the PostgreSQL Write-Ahead Log (WAL). Data lands in the ClickHouse staging layer instantly without heavy polling queries.
   - **Transform:** **Mage.ai** orchestrates a `dbt run` block every hour. This hourly trigger processes the freshly loaded data in ClickHouse and materializes the final dimensional models.

2. **Dimensional Modeling (Bonus 1)**
   - The DWH uses a Star Schema. `stg_articles` acts as the raw view, while `fact_articles` contains the core metrics and statuses. Content text is separated to keep the analytical fact table highly performant on ClickHouse.

3. **Handling 2016 Historical Data (Bonus 2)**
   - Querying a decade of data simultaneously causes source system degradation. By utilizing **PeerDB**, the system performs an *Initial Snapshot*. It safely streams all historical rows from 2016 into ClickHouse before seamlessly transitioning into real-time CDC mode. This requires zero manual batch chunking scripts.

4. **Hard Delete Synchronization (Bonus 3)**
   - Standard incremental queries (`WHERE updated_at > ...`) cannot detect hard deletes. 
   - Instead of running an expensive daily `Anti-Join` between the DWH and the source, this architecture uses CDC. When a hard delete occurs in Postgres, PeerDB captures the exact WAL event and instantly replicates the deletion (or appends a deletion flag) to the ClickHouse staging table. The subsequent hourly dbt run finalizes this state in the `fact_articles` table.