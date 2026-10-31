import logging
import pandas as pd
logger = logging.getLogger(__name__)

def validate_dataframe(df, required_columns, numeric_columns):
    """Validate the DataFrame and return valid data"""
    rows_before = len(df)
    for column in required_columns:
        if column not in df.columns:
            logger.error(f"Required Column missing: {column}")
            raise ValueError(f"Required column missing: {column}")
    for col in numeric_columns:
        invalid_rows = []
        for i, value in df[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except ValueError:
                    logger.warning(f"Invalid numeric value in {col}, value: {value}")
                    invalid_rows.append(i)
        df = df.drop(index=invalid_rows)
        df[col] = pd.to_numeric(df[col])
    rows_after = len(df)
    rows_removed = rows_before - rows_after
    logger.debug(f"Valid rows: {rows_after}, rows removed: {rows_removed}")
    return df
