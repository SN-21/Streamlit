import streamlit as st
import numpy as np
import pandas as pd

from nba_api.live.nba.endpoints import boxscore, scoreboard
from nba_api.stats.endpoints import boxscoreusagev2


games = scoreboard.ScoreBoard()
game_score = games.get_dict()

scoreboard = game_score["scoreboard"]
game = scoreboard["games"]
game_date = scoreboard["gameDate"]

# Boxscoreのdataframe作成関数定義
def Boxscore_DataFrame_Transform(
    df,
    sort_columns,
    loc_columns,
    rename_columns,
    format_dict,
    process_strings,
    name_columns,
):
    df_boxscore_query = df.query('status =="ACTIVE"')
    df_boxscore_query.loc[df_boxscore_query["played"] == "0", loc_columns] = "-"
    df_sorting = df_boxscore_query[sort_columns]
    df_rename = df_sorting.rename(columns=rename_columns)
    team_names = df_rename.loc[:, name_columns]
    df_set_axis = df_rename.set_axis(team_names)
    df_set_axis_drop = df_set_axis.drop([name_columns], axis=1)
    df_fillna = df_set_axis_drop.fillna("-").copy()
    df_fillna[process_strings] = df_fillna[process_strings].str[2:7]
    df_fillna[process_strings] = df_fillna[process_strings].str.replace("M", ":")
    df_fillna_style = df_fillna.style.format(format_dict)
    # df_fillna_style.loc[df_fillna_style["MIN"] == "00:00", loc_columns] = "-"

    return df_fillna_style


# teamstats dataframe 作成関数定義
def TeamStats_DataFrame_Transform(df, sort_columns, rename_columns, format_columns):
    df_TS_sort = df[sort_columns]
    df_TS_rename = df_TS_sort.rename(columns=rename_columns)
    df_TS_style = df_TS_rename.style.format(format_columns)

    return df_TS_style


# gamechart daraframe 作成関数定義
def GameChart_DataFrame_Transform(
    df, sort_columns, rename_columns, format_columns, process_strings
):
    df_GC_sort = df[sort_columns]
    df_GC_rename = df_GC_sort.rename(columns=rename_columns).copy()
    df_GC_rename[process_strings] = df_GC_rename[process_strings].str[2:7]
    df_GC_rename[process_strings] = df_GC_rename[process_strings].str.replace("M", ":")
    df_GC_style = df_GC_rename.style.format(format_columns)

    return df_GC_style


# inactive player 作成関数定義


def Inactive_Player(df):
    df_query = df.query('status == "INACTIVE"')
    try:
        df_loc = df_query.loc[:, ["name", "notPlayingReason"]]

    except KeyError:
        df_loc = df_query.loc[:, ["name"]]

    index_name = df_query.loc[:, "name"]
    df_set_axis = df_loc.set_axis(index_name)
    df_drop = df_set_axis.drop(["name"], axis=1)
    df_drop_rename = df_drop.rename(columns={"notPlayingReason": "REASON"})
    df_inactive = df_drop_rename.fillna("-")

    return df_inactive


# def Inactive_Player(df):
#     df_query = df.query('status == "INACTIVE"')
#     df_loc = df_query.loc[:, ["name", "notPlayingReason"]]
#     index_name = df_query.loc[:, "name"]
#     df_set_axis = df_loc.set_axis(index_name)
#     df_drop = df_set_axis.drop(["name"], axis=1)
#     df_drop_rename = df_drop.rename(columns={"notPlayingReason": "REASON"})
#     df_inactive = df_drop_rename.fillna("-")

#     return df_inactive

# 　usage dataframe 作成関数定義
def Usage_dataframe_transform(df, teamname, drop_columns):
    df_query_usage = df.query("TEAM_ABBREVIATION == @teamname")
    index_name_usage = df_query_usage.loc[:, "PLAYER_NAME"]
    df_set_axis_usage = df_query_usage.set_axis(index_name_usage)
    df_drop_usage = df_set_axis_usage.drop(drop_columns, axis=1)
    df_fillna_usage = df_drop_usage.fillna("-")

    return df_fillna_usage


# gameid_list = []

# for i in range(len(game)):
#     game_id = game[i]["gameId"]
#     gameid_list.append(game_id)

# ここはわざわざ　for文でgameidのリストを作らなくても下のfor文でgameidを毎回取得すれば不要だった

# 最初の行の表示を中央にする為に、３カラム化
# ３分割にして 3,3,2 の比率にすれば row2_2 の 3 が中央になる
row2_1, row2_2, row2_3 = st.columns((3, 3, 2))

# ここは1行目　　空白にする
with row2_1:
    st.subheader(" ")

# ここが2行目 game_data 試合日の表示
with row2_2:
    st.header(f"{game_date}")

# ここは3行目 空白
with row2_3:
    st.subheader(" ")

# ここから各試合のデータ取りのためのループ
for i in range(len(game)):
    game_id = game[i]["gameId"]
    gameStatus = game[i]["gameStatusText"]
    awayTeam = game[i]["awayTeam"]["teamTricode"]
    homeTeam = game[i]["homeTeam"]["teamTricode"]

    awayTeamCity = game[i]["awayTeam"]["teamCity"]
    awayTeamname = game[i]["awayTeam"]["teamName"]

    awayTeam_full_name = awayTeamCity + (" ") + awayTeamname

    homeTeamCity = game[i]["homeTeam"]["teamCity"]
    homeTeamname = game[i]["homeTeam"]["teamName"]

    homeTeam_full_name = homeTeamCity + (" ") + homeTeamname

    awayTeam_score = game[i]["awayTeam"]["score"]
    homeTeam_score = game[i]["homeTeam"]["score"]

    awayTeam_win_count = game[i]["awayTeam"]["wins"]
    awayTeam_lose_count = game[i]["awayTeam"]["losses"]

    homeTeam_win_count = game[i]["homeTeam"]["wins"]
    homeTeam_lose_count = game[i]["homeTeam"]["losses"]

    # ここのif文はovertime用
    if gameStatus == "Final/OT" or gameStatus == "OT":
        away_Team_q1point = game[i]["awayTeam"]["periods"][0]["score"]
        away_Team_q2point = game[i]["awayTeam"]["periods"][1]["score"]
        away_Team_q3point = game[i]["awayTeam"]["periods"][2]["score"]
        away_Team_q4point = game[i]["awayTeam"]["periods"][3]["score"]
        away_Team_OTpoint = game[i]["awayTeam"]["periods"][4]["score"]

        home_Team_q1point = game[i]["homeTeam"]["periods"][0]["score"]
        home_Team_q2point = game[i]["homeTeam"]["periods"][1]["score"]
        home_Team_q3point = game[i]["homeTeam"]["periods"][2]["score"]
        home_Team_q4point = game[i]["homeTeam"]["periods"][3]["score"]
        home_Team_OTpoint = game[i]["homeTeam"]["periods"][4]["score"]

    elif gameStatus == "Final/OT2" or gameStatus == "OT2":
        away_Team_q1point = game[i]["awayTeam"]["periods"][0]["score"]
        away_Team_q2point = game[i]["awayTeam"]["periods"][1]["score"]
        away_Team_q3point = game[i]["awayTeam"]["periods"][2]["score"]
        away_Team_q4point = game[i]["awayTeam"]["periods"][3]["score"]
        away_Team_OTpoint = (game[i]["awayTeam"]["periods"][4]["score"]) + (
            game[i]["awayTeam"]["periods"][5]["score"]
        )

        home_Team_q1point = game[i]["homeTeam"]["periods"][0]["score"]
        home_Team_q2point = game[i]["homeTeam"]["periods"][1]["score"]
        home_Team_q3point = game[i]["homeTeam"]["periods"][2]["score"]
        home_Team_q4point = game[i]["homeTeam"]["periods"][3]["score"]
        home_Team_OTpoint = (game[i]["homeTeam"]["periods"][4]["score"]) + (
            game[i]["homeTeam"]["periods"][5]["score"]
        )

    else:
        away_Team_q1point = game[i]["awayTeam"]["periods"][0]["score"]
        away_Team_q2point = game[i]["awayTeam"]["periods"][1]["score"]
        away_Team_q3point = game[i]["awayTeam"]["periods"][2]["score"]
        away_Team_q4point = game[i]["awayTeam"]["periods"][3]["score"]

        home_Team_q1point = game[i]["homeTeam"]["periods"][0]["score"]
        home_Team_q2point = game[i]["homeTeam"]["periods"][1]["score"]
        home_Team_q3point = game[i]["homeTeam"]["periods"][2]["score"]
        home_Team_q4point = game[i]["homeTeam"]["periods"][3]["score"]

    leader_away_assist = game[i]["gameLeaders"]["awayLeaders"]["assists"]
    leader_away_rebounds = game[i]["gameLeaders"]["awayLeaders"]["rebounds"]
    leader_away_point = game[i]["gameLeaders"]["awayLeaders"]["points"]
    leader_away_player = game[i]["gameLeaders"]["awayLeaders"]["name"]

    leader_home_assist = game[i]["gameLeaders"]["homeLeaders"]["assists"]
    leader_home_rebounds = game[i]["gameLeaders"]["homeLeaders"]["rebounds"]
    leader_home_point = game[i]["gameLeaders"]["homeLeaders"]["points"]
    leader_home_player = game[i]["gameLeaders"]["homeLeaders"]["name"]

    boxscores = boxscore.BoxScore(game_id=game_id)
    boxscore_game = boxscores.game.get_dict()

    official = boxscores.officials.get_dict()
    official_1 = official[0]["name"]
    official_2 = official[1]["name"]
    official_3 = official[2]["name"]

    arena = boxscore_game["arena"]["arenaName"]
    arena_city = boxscore_game["arena"]["arenaCity"]
    arenaState = boxscore_game["arena"]["arenaState"]
    attendance = boxscore_game["attendance"]

    awayteam_boxscore = boxscore_game["awayTeam"]["players"]
    hometeam_boxscore = boxscore_game["homeTeam"]["players"]

    awayteam_boxscore_df = pd.json_normalize(awayteam_boxscore)
    hometeam_boxscore_df = pd.json_normalize(hometeam_boxscore)

    boxscore_sort_columns = [
        "jerseyNum",
        "position",
        "name",
        "statistics.minutes",
        "statistics.fieldGoalsMade",
        "statistics.fieldGoalsAttempted",
        "statistics.fieldGoalsPercentage",
        "statistics.twoPointersMade",
        "statistics.twoPointersAttempted",
        "statistics.twoPointersPercentage",
        "statistics.threePointersMade",
        "statistics.threePointersAttempted",
        "statistics.threePointersPercentage",
        "statistics.freeThrowsMade",
        "statistics.freeThrowsAttempted",
        "statistics.freeThrowsPercentage",
        "statistics.reboundsDefensive",
        "statistics.reboundsOffensive",
        "statistics.reboundsTotal",
        "statistics.assists",
        "statistics.blocks",
        "statistics.blocksReceived",
        "statistics.steals",
        "statistics.turnovers",
        "statistics.foulsPersonal",
        "statistics.foulsTechnical",
        "statistics.points",
        "statistics.plusMinusPoints",
    ]

    boxscore_loc_columns = [
        "statistics.minutes",
        "statistics.points",
        "statistics.fieldGoalsMade",
        "statistics.fieldGoalsAttempted",
        "statistics.twoPointersMade",
        "statistics.twoPointersAttempted",
        "statistics.threePointersMade",
        "statistics.threePointersAttempted",
        "statistics.freeThrowsMade",
        "statistics.freeThrowsAttempted",
        "statistics.reboundsDefensive",
        "statistics.reboundsOffensive",
        "statistics.reboundsTotal",
        "statistics.assists",
        "statistics.blocks",
        "statistics.blocksReceived",
        "statistics.steals",
        "statistics.turnovers",
        "statistics.foulsPersonal",
        "statistics.foulsTechnical",
    ]

    boxscore_rename_columns = {
        "jerseyNum": "#",
        "position": "POS",
        "statistics.minutes": "MIN",
        "statistics.fieldGoalsMade": "FGM",
        "statistics.fieldGoalsAttempted": "FGA",
        "statistics.fieldGoalsPercentage": "FG%",
        "statistics.twoPointersMade": "2PM",
        "statistics.twoPointersAttempted": "2PA",
        "statistics.twoPointersPercentage": "2P%",
        "statistics.threePointersMade": "3PM",
        "statistics.threePointersAttempted": "3PA",
        "statistics.threePointersPercentage": "3P%",
        "statistics.freeThrowsMade": "FTM",
        "statistics.freeThrowsAttempted": "FTA",
        "statistics.freeThrowsPercentage": "FT%",
        "statistics.reboundsDefensive": "DREB",
        "statistics.reboundsOffensive": "OREB",
        "statistics.reboundsTotal": "REB",
        "statistics.assists": "AST",
        "statistics.blocks": "BLK",
        "statistics.blocksReceived": "BLKR",
        "statistics.steals": "STL",
        "statistics.turnovers": "TO",
        "statistics.foulsPersonal": "PF",
        "statistics.foulsTechnical": "TF",
        "statistics.points": "PTS",
        "statistics.plusMinusPoints": "+/-",
    }

    boxscore_format_dict = {
        "FG%": "{:.3f}",
        "2P%": "{:.3f}",
        "3P%": "{:.3f}",
        "FT%": "{:.3f}",
        "+/-": "{:.0f}",
    }

    boxscore_process_strings = "MIN"

    boxscore_name_columns = "name"

    df_Boxscore_away = Boxscore_DataFrame_Transform(
        awayteam_boxscore_df,
        sort_columns=boxscore_sort_columns,
        loc_columns=boxscore_loc_columns,
        rename_columns=boxscore_rename_columns,
        format_dict=boxscore_format_dict,
        process_strings=boxscore_process_strings,
        name_columns=boxscore_name_columns,
    )

    df_Boxscore_home = Boxscore_DataFrame_Transform(
        hometeam_boxscore_df,
        sort_columns=boxscore_sort_columns,
        loc_columns=boxscore_loc_columns,
        rename_columns=boxscore_rename_columns,
        format_dict=boxscore_format_dict,
        process_strings=boxscore_process_strings,
        name_columns=boxscore_name_columns,
    )
    # ここまでで Boxscore の入力は済　。この後は、TeamStatsの入力へ
    teamstats_away = boxscore_game["awayTeam"]["statistics"]
    teamstats_home = boxscore_game["homeTeam"]["statistics"]
    index_away = boxscore_game["awayTeam"]["teamTricode"]
    index_home = boxscore_game["homeTeam"]["teamTricode"]

    df_teamstats_away = pd.DataFrame(teamstats_away, index=[index_away])
    df_teamstats_home = pd.DataFrame(teamstats_home, index=[index_home])

    df_teamstats = pd.concat([df_teamstats_away, df_teamstats_home])

    teamstats_sort_columns = [
        "fieldGoalsMade",
        "fieldGoalsAttempted",
        "fieldGoalsPercentage",
        "threePointersMade",
        "threePointersAttempted",
        "threePointersPercentage",
        "freeThrowsMade",
        "freeThrowsAttempted",
        "freeThrowsPercentage",
        "reboundsOffensive",
        "reboundsDefensive",
        "reboundsTotal",
        "assists",
        "steals",
        "blocks",
        "turnovers",
        "foulsPersonal",
        "points",
    ]

    teamstats_rename_columns = {
        "fieldGoalsMade": "FGM",
        "fieldGoalsAttempted": "FGA",
        "fieldGoalsPercentage": "FG%",
        "threePointersMade": "3PM",
        "threePointersAttempted": "3PA",
        "threePointersPercentage": "3P%",
        "freeThrowsMade": "FTM",
        "freeThrowsAttempted": "FTA",
        "freeThrowsPercentage": "FT%",
        "reboundsOffensive": "OREB",
        "reboundsDefensive": "DREB",
        "reboundsTotal": "REB",
        "assists": "AST",
        "steals": "STL",
        "blocks": "BLK",
        "turnovers": "TO",
        "foulsPersonal": "PF",
        "points": "PTS",
    }

    teamstats_format_columns = {"FG%": "{:.3f}", "3P%": "{:.3f}", "FT%": "{:.3f}"}

    df_team_stats = TeamStats_DataFrame_Transform(
        df_teamstats,
        sort_columns=teamstats_sort_columns,
        rename_columns=teamstats_rename_columns,
        format_columns=teamstats_format_columns,
    )
    # ここからgamechart dataframe作成開始
    game_chart_sort_columns = [
        "biggestLead",
        "biggestScoringRun",
        "leadChanges",
        "benchPoints",
        "timeLeading",
        "timesTied",
        "pointsFastBreak",
        "pointsFromTurnovers",
        "pointsInThePaint",
        "pointsSecondChance",
        "trueShootingPercentage",
        "reboundsTeamDefensive",
        "reboundsTeamOffensive",
        "reboundsTotal",
        "assists",
        "turnovers",
        "assistsTurnoverRatio",
    ]

    game_chart_rename_columns = {
        "biggestLead": "BIG LD",
        "biggestScoringRun": "BIG RUN",
        "leadChanges": "LeadChanges",
        "benchPoints": "BPTS",
        "timeLeading": "Time LD",
        "timesTied": "TimesTied",
        "pointsFastBreak": "FB PTS",
        "pointsInThePaint": "PITP",
        "pointsSecondChance": "SC PTS",
        "pointsFromTurnovers": "FTOV PTS",
        "trueShootingPercentage": "TS %",
        "reboundsTeamDefensive": "DREB",
        "reboundsTeamOffensive": "OREB",
        "reboundsTotal": "REB",
        "assists": "AST",
        "turnovers": "TOV",
        "assistsTurnoverRatio": "ATR",
    }

    game_chart_format_columns = {"TS %": "{:.3f}", "ATR": "{:.3f}"}

    game_chart_process_strings = "Time LD"

    df_game_chart = GameChart_DataFrame_Transform(
        df=df_teamstats,
        sort_columns=game_chart_sort_columns,
        rename_columns=game_chart_rename_columns,
        format_columns=game_chart_format_columns,
        process_strings=game_chart_process_strings,
    )
    # スコアテーブル作成

    if (
        gameStatus == "Final/OT"
        or gameStatus == "OT"
        or gameStatus == "Final/OT2"
        or gameStatus == "OT2"
    ):
        score_table = pd.DataFrame(
            data={
                "1": [away_Team_q1point, home_Team_q1point],
                "2": [away_Team_q2point, home_Team_q2point],
                "3": [away_Team_q3point, home_Team_q3point],
                "4": [away_Team_q4point, home_Team_q4point],
                "OT": [away_Team_OTpoint, home_Team_OTpoint],
                "TOTAL": [awayTeam_score, homeTeam_score],
            },
            index=[awayTeam_full_name, homeTeam_full_name],
        )

    else:
        score_table = pd.DataFrame(
            data={
                "1": [away_Team_q1point, home_Team_q1point],
                "2": [away_Team_q2point, home_Team_q2point],
                "3": [away_Team_q3point, home_Team_q3point],
                "4": [away_Team_q4point, home_Team_q4point],
                "TOTAL": [awayTeam_score, homeTeam_score],
            },
            index=[awayTeam_full_name, homeTeam_full_name],
        )

    # inactive player dataframe

    df_away_inactive = Inactive_Player(df=awayteam_boxscore_df)
    df_home_inactive = Inactive_Player(df=hometeam_boxscore_df)

    usage_drop_columns = [
        "GAME_ID",
        "TEAM_ID",
        "TEAM_ABBREVIATION",
        "TEAM_CITY",
        "PLAYER_ID",
        "PLAYER_NAME",
        "NICKNAME",
    ]
    boxscore_usage = boxscoreusagev2.BoxScoreUsageV2(game_id=game_id)
    df_boxscore_usage = boxscore_usage.sql_players_usage.get_data_frame()

    df_away_usage = Usage_dataframe_transform(
        df=df_boxscore_usage, teamname=awayTeam, drop_columns=usage_drop_columns
    )

    df_home_usage = Usage_dataframe_transform(
        df=df_boxscore_usage, teamname=homeTeam, drop_columns=usage_drop_columns
    )

    row3_spacer1, row3_1, row3_2, row3_3, row3_spacer2 = st.columns(
        (1.5, 2, 1.5, 2, 0.5)
    )

    with row3_1:
        if awayTeam_score > homeTeam_score:
            st.subheader(
                f"{awayTeam}  {awayTeam_score} ◀︎ \n ({awayTeam_win_count}-{awayTeam_lose_count})"
            )

        else:
            st.subheader(
                f"{awayTeam}  {awayTeam_score} \n ({awayTeam_win_count}-{awayTeam_lose_count})"
            )

    with row3_2:
        st.text(f"{gameStatus}")

    with row3_3:
        if awayTeam_score < homeTeam_score:
            st.subheader(
                f" ▶︎ {homeTeam_score}  {homeTeam} \n ({homeTeam_win_count}-{homeTeam_lose_count})"
            )
        else:
            st.subheader(
                f" {homeTeam_score}  {homeTeam} \n ({homeTeam_win_count}-{homeTeam_lose_count})"
            )

    st.table(score_table)

    st.text(
        f"{leader_away_player} ({awayTeam})  {leader_away_point} PTS  {leader_away_rebounds} REB  {leader_away_assist} AST     {leader_home_player} ({homeTeam})  {leader_home_point} PTS  {leader_home_rebounds} REB  {leader_home_assist} AST"
    )

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Game Information",
            "Inactive Player",
            "Team Stats",
            "Game Chart",
            "Box Score",
            "Usage",
        ]
    )

    with tab1:
        st.text(f"Location : {arena}  {arena_city}  {arenaState}  ")
        st.text(f"Attendance :  {attendance}")
        st.text(f"Officials :  {official_1} , {official_2} , {official_3}")

    with tab2:
        st.text(f"{awayTeam_full_name}")
        st.table(df_away_inactive)
        st.text(f"{homeTeam_full_name}")
        st.table(df_home_inactive)

    with tab3:
        st.dataframe(df_team_stats)

    with tab4:
        st.dataframe(df_game_chart)

    with tab5:
        st.text(f"{awayTeam_full_name}")
        st.dataframe(df_Boxscore_away)

        st.text(f"{homeTeam_full_name}")
        st.dataframe(df_Boxscore_home)

    with tab6:
        st.text(f"{awayTeam_full_name}")
        st.dataframe(df_away_usage)
        st.text(f"{homeTeam_full_name}")
        st.dataframe(df_home_usage)

    st.markdown("---")
