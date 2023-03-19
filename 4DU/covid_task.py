import matplotlib.pyplot as plt

import pandas as pd
import datetime as dt



def import_data(states, url, date1, date2):
    """
    this function imports COVID-19 data
    filters out countries that you have defined
    filters out dates that you have defined
    """
    # reading csv from url
    df = pd.read_csv(url)

    # making mask for all countries
    country_masks = [df["Country/Region"] == state for state in states]

    # applying mask for all countries
    df_states = [df[country_mask] for country_mask in country_masks]

    # clearing datas
    df_states = [df_state.melt(
            id_vars=["Province/State", "Country/Region", "Lat", "Long"],
            var_name="date",
            value_name="cases")
            for df_state in df_states]

    df_states = [df_state.drop(columns=["Province/State"]) for df_state in df_states]

    # filtering out dates
    def reformat_date(date):
        return dt.datetime.strptime(date, "%m/%d/%y").date()

    for df_state in df_states:
        df_state["date"] = df_state["date"].apply(reformat_date)

    for i, df_state in enumerate(df_states):
        df_state = df_state.loc[(df_state['date'] >= date1) & (df_state['date'] < date2)]
        df_states[i] = df_state

    # adding diff column
    for df_state in df_states:
        df_state["diff"] = df_state["cases"].diff()

    # plotting results

    fig, axis = plt.subplots(4)
    for i, df_state in enumerate(df_states):
        axis[i].plot(df_state["date"], df_state["diff"])
        axis[i].set_title(df_state["Country/Region"].iloc[0])
        axis[i].set_xlabel("Date")
        axis[i].set_ylabel("Diff")

    # creating correlation matrix
    df_corr = {"Czechia":df_states[0]["diff"],
               "Croatia":df_states[1]["diff"],
                "Poland":df_states[2]["diff"],
                "Italy":df_states[3]["diff"]}
    df_corr = pd.DataFrame(df_corr)
    corr_matrix = df_corr.corr()
    fig2, corr = plt.subplots(1)
    corr.matshow(corr_matrix)
    plt.show()

    for df_state in df_states:
        filename = str(df_state["Country/Region"].iloc[0])+".csv"
        df_state.to_csv(filename)



if __name__ == "__main__":
    states = ["Czechia", "Croatia", "Poland", "Italy"]

    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

    date1 = dt.date(year = 2021, day=8, month=11)
    date2 = dt.date(year = 2022, day=8, month=11)

    data = import_data(states, url,date1,date2)