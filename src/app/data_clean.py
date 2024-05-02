import os
import pandas as pd


def clean_header_rows(df: pd.DataFrame) -> pd.DataFrame:
    ## Header rows that are in data rows
    df = df.loc[df["year_max"] != "To"]
    return df


def clean_non_playing_players(df: pd.DataFrame) -> pd.DataFrame:
    ## Some players that have never played
    non_playing = df.loc[pd.isna(df["year_max"]) == True]
    filename = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "raw",
        "non_playing_players.csv",
    )
    non_playing.to_csv(filename)
    df = df.loc[pd.isna(df["year_max"]) == False]
    return df


def main():
    filename = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "raw", "draft_data_raw.csv"
    )
    df = pd.read_csv(filename)

    print(df.head())

    df = clean_header_rows(df)
    df = clean_non_playing_players(df)

    print(df.head())
    clean_filename = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "clean",
        "draft_data_clean.csv",
    )
    df.to_csv(
        clean_filename,
        index=False,
    )
