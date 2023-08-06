from datalakebundle.table.config.TableConfig import TableConfig


class UpsertQueryCreator:
    def create(self, table_config: TableConfig, temp_source_table: str) -> str:
        conditions = []
        updates = []
        columns_to_update = set(table_config.schema.fieldNames()) - set(table_config.schema.primary_key_columns)

        for primary_key in table_config.schema.primary_key_columns:
            conditions.append(f"source.`{primary_key}` = target.`{primary_key}`")

        for col in columns_to_update:
            updates.append(f"target.`{col}` = source.`{col}`")

        query = (
            f"MERGE INTO {table_config.full_table_name} AS target\n"
            f"USING {temp_source_table} AS source\n"
            f"ON {' AND '.join(conditions)}\n"
            f"{{matched_clause}}"
            f"WHEN NOT MATCHED THEN INSERT *\n"
        )

        if len(updates) > 0:
            query = query.format(matched_clause=f"WHEN MATCHED THEN UPDATE SET {', '.join(updates)}\n")
        else:
            query = query.format(matched_clause="")

        return query
