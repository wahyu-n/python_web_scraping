import pandas as pd
import re
import logging
from typing import List


logging.basicConfig(level=logging.INFO)


def is_money_miliar(string_money: str) -> bool:
    return string_money.lower().endswith("miliar")


def transform_money_format(string_money: str) -> str:
    half_clean_string = string_money.lower().replace(",", ".").replace(" ", "")
    return re.sub(r"[?\[M\]miliar|\[J\]juta]", "", half_clean_string)


def transform(dfs: List[pd.DataFrame], tahun: List[int]) -> pd.DataFrame:
    logging.info("Transforming and Cleaning DataFrame ...")
    
    cleaned_df = []
    for df_ke, df in enumerate(dfs):
        
        if df_ke <= 2:
            columns_mapping = {
                "Nomor Urut": "nomor_urut",
                "Nama": "nama",
                "Perusahaan/Pekerjaan": "perusahaan",
                "Kekayaan Bersih (US$)": "kekayaan_bersih_usd"
            }
        else:
            columns_mapping = {
                "Nomor Urut": "nomor_urut",
                "Nama": "nama",
                "Perusahaan": "perusahaan",
                "Kekayaan Bersih (US$)": "kekayaan_bersih_usd"
            }

        renamed_df = df.rename(columns=columns_mapping)
        renamed_df["tahun"] = tahun[df_ke]
        renamed_df["kekayaan_bersih_usd_juta"] = renamed_df["kekayaan_bersih_usd"].apply(
            lambda data: float(transform_money_format(data)) * 1000 if is_money_miliar(data) else float(transform_money_format(data))
        )
        
        renamed_df = renamed_df[["nomor_urut", "nama", "tahun", "perusahaan", "kekayaan_bersih_usd_juta"]]
        cleaned_df.append(renamed_df)
    
    concat_cleaned_df = pd.concat(cleaned_df)
    return concat_cleaned_df