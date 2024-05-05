import os
import requests

import pandas as pd
import bs4
import aiohttp
import asyncio


def get_draft_data(year) -> pd.DataFrame:

    url = f"https://www.pro-football-reference.com/years/{year}/draft.htm"
    print(f"Getting data for draft data for year {year}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        raise Exception(f"Error Gathering Data: {response.status_code}")

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # print(soup.prettify())

    table = soup.find("table", {"id": "drafts"})

    draft_data_raw_table = table.find("tbody")

    row = draft_data_raw_table.findAll(
        ["td", "th"],
    )

    # print(row)
    # print(row[0])

    ## Get columns for dataframe
    columns = [i["data-stat"] for i in row]
    columns = set(columns)
    columns.add("player_id")
    # print(columns)

    ## Set columns for dataframe using dict method
    data = {col: [] for col in columns}

    # print(data)
    for i in row:
        data_col = i["data-stat"]
        # print(data_col)
        if data_col == "player":
            data["player_id"].append(i["data-append-csv"])

        data[data_col].append(i.text)

        # print(data)

        df = pd.DataFrame.from_dict(data)
        df["draft_year"] = year

        filename = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "raw",
            "draft_data_raw_" + str(year) + ".csv",
        )
        df.to_csv(filename, index=False)

    return df


def get_player_adv_info(player_id: str) -> pd.DataFrame:

    url = f"https://www.pro-football-reference.com/players/{player_id[0]}/{player_id}"
    resp = requests.get(url)

    body = resp.text
    soup = bs4.BeautifulSoup(body, "html.parser")
    table = soup.findAll("tr", {"class": "full_table"})
    ## Get columns for dataframe
    rows = [t.findAll("td") for t in table]

    columns = [i["data-stat"] for i in rows]
    columns = set(columns)
    columns.add("player_id")
    # print(columns)

    ## Set columns for dataframe using dict method
    data = {col: [] for col in columns}

    # print(data)
    for i in rows:
        data_col = i["data-stat"]
        data[data_col].append(i.text)

    df = pd.DataFrame.from_dict(data)

    df["player_id"] = player_id

    filename = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "raw",
        "player_data_raw_" + str(player_id) + ".csv",
    )
    df.to_csv(filename, index=False)

    return df

    # print(f"Getting data for player id {player_id}")
    # response = requests.get(url)
    # print(response)


def main():

    year = [i for i in range(2000, 2021)]
    # df = get_draft_data(2020)
    # df = pd.concat(
    #     [get_draft_data(i) for i in year]
    # )  ### Very not efficient if pulling larger datasets

    results = []
    for year_idx, year in enumerate(year):
        draft_df = get_draft_data(year)
        results.append(draft_df)

    df = pd.concat(results)

    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "raw", "draft_data_raw.csv"
    )

    df.to_csv(file_path, index=False)

    def getting_player_data():
        for player_idx, player_id in enumerate(set(df["player_id"].to_list())):
            print(f"Getting data for player id {player_id}, {player_idx}/{len(df)}")
            player_temp_df = get_player_adv_info(player_id)
            yield player_temp_df

    player_data = getting_player_data()

    player_df = pd.concat(player_data)

    player_file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "raw", "player_data_raw.csv"
    )
    player_df.to_csv(player_file_path, index=False)

    # print(df.head())


main()
