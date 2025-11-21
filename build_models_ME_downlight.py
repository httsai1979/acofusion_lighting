import pandas as pd


def extract_model_id(item_value: str) -> str:
    """Extract the last non-empty line from the Item No. field.

    Some cells contain multiple lines (e.g., "New\nD124-1"). This function
    returns the last non-empty line with surrounding whitespace removed.
    """
    if pd.isna(item_value):
        return ""

    lines = str(item_value).splitlines()
    for line in reversed(lines):
        cleaned = line.strip()
        if cleaned:
            return cleaned
    return ""


def build_models(input_path: str, output_path: str) -> None:
    """Read the raw CSV, map columns, and write the cleaned models file."""
    # Read the raw data with UTF-8 encoding
    raw_df = pd.read_csv(input_path, encoding="utf-8")

    # Keep only rows that have a non-empty Item No.
    item_series = raw_df["Item No."].fillna("").astype(str)
    data_df = raw_df[item_series.str.strip() != ""].copy()

    # Map columns to the desired schema
    models_df = pd.DataFrame(
        {
            "model_id": data_df["Item No."].apply(extract_model_id),
            "series": "Downlight-ME",
            "category": "Downlight",
            "price_list": "ME_Downlight_2024_USD",
            "currency": "USD",
            "wattage": data_df["Unnamed: 7"],
            "cct_options_raw": data_df["Unnamed: 6"],
            "beam_type": data_df["Unnamed: 8"],
            "material": data_df["規格"],
            "finish_options_raw": data_df["Unnamed: 4"],
            "dimensions": data_df["Unnamed: 9"],
            "cutout": data_df["Unnamed: 10"],
            "driver_spec_raw": data_df["Unnamed: 11"],
            "led_spec_raw": data_df["Unnamed: 5"],
            "base_price_moq_200": data_df["Unit price (USD)"],
            "remarks_raw": data_df["Remarks"],
            "active_flag": "Y",
        }
    )

    # Write the mapped data to CSV with UTF-8 encoding
    models_df.to_csv(output_path, index=False, encoding="utf-8")


if __name__ == "__main__":
    build_models("ME_Downlight_2024_raw.csv", "models_ME_Downlight_2024.csv")
