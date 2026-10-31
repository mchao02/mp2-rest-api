import logging 
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    rows_before = len(df)
    cleaned = df.drop_duplicates()

    rows_removed = rows_before - len(cleaned)
    logger.debug(f"Number of rows removed: {rows_removed}")

    return cleaned

def handle_missing(df, axis = "rows"):
    """Drop rows or columns containing missing values"""
    if axis == "rows":
        count_before = len(df)
        cleaned = df.dropna(axis=0)
        count_removed = count_before - len(cleaned)
    elif axis == "columns":
        count_before = len(df.columns)
        cleaned = df.dropna(axis=1)
        count_removed = count_before - len(cleaned)
    else:
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError(f"Unsupoorted axis: {axis}")
    logger.debug(f"removed {count_removed} {axis}")
    return cleaned

def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specificed numeric columns"""
    if method not in ["iqr", "zscore"]:
        logger.error(f"Unsupported method: {method}")
        raise ValueError(f"Unsupported method: {method}")
    for column in columns:
        if column not in df.columns:
            logger.warning(f"Column not found: {column}")
        elif not pd.api.types.is_numeric_dtype(df[column]):
            logger.warning(f"Column is not numeric: {column}")
        else:
            if method == "iqr":
                values = df[column]
                q1 = values.quantile(0.25)
                q3 = values.quantile(0.75)
                iqr = q3 - q1
                lower = q1 - threshold * iqr
                upper = q3 + threshold * iqr

                rows_before = len(df)
                df = df[(df[column] >= lower) & (df[column] <= upper)]
                rows_removed = rows_before - len(df)
                logger.debug(f"{column} removed, threshold = {threshold}, removed={rows_removed}, method={method}")
            elif method == "zscore":
                values = df[column]
                mean = values.mean()
                standard_dev = values.std()

                z_scores = (values - mean) / standard_dev
                rows_before = len(df)
                df = df[z_scores.abs() <= threshold]
                rows_removed = rows_before - len(df)

                logger.debug( f"{column} removed, method: {method}, threshold{threshold}, removed: {rows_removed} rows")
    return df
def process_data(df, config):
    """"Apply the processing steps enabled in the configuration"""
    processing = config["processing"]
    if processing["remove_duplicates"]:
        df = remove_duplicates(df)

    missing = processing["missing"]
    if missing["enabled"]:
        df = handle_missing(df, axis= missing["axis"])

    outliers = processing["outliers"]
    if outliers["enabled"]:
        df = remove_outliers(df, columns= outliers["columns"], method=outliers["method"], threshold=outliers["threshold"])

    return df

def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    rows_before = len(df_before)
    rows_after = len(df_after)
    columns_before = len(df_before.columns)
    columns_after = len(df_after.columns)

    return {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "rows_removed": rows_before - rows_after,
        "columns_before": columns_before,
        "columns_after": columns_after,
        "columns_removed": columns_before - columns_after
    }
    
