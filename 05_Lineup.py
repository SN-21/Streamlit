import streamlit as st
import pandas as pd

from nba_api.stats.endpoints import leaguelineupviz


def Lineup_DataFrame_Transform(df, rename_columns, format_columns):
    df_lineup_rename = df.rename(columns=rename_columns)
    df_lineup_style = df_lineup_rename.style.format(format_columns)

    return df_lineup_style


lineup = leaguelineupviz.LeagueLineupViz(minutes_min=50)
df = lineup.league_lineup_viz.get_data_frame()
df_lineup = pd.DataFrame(df)

df_lineup_index_drop = df_lineup.drop(["GROUP_ID", "TEAM_ID"], axis=1)

lineup_rename_columns = {
    "TEAM_ABBREVIATION": "TEAM",
    "OFF_RATING": "OFF RATING",
    "DEF_RATING": "DEF RATING",
    "NET_RATING": "NET RATTING",
    "TS_PCT": "TS %",
    "FTA_RATE": "FTA RATE",
    "TM_AST_PCT": "TM AST %",
    "PCT_FGA_2PT": "FGA 2PT %",
    "PCT_FGA_3PT": "FGA 3PT %",
    "PCT_PTS_2PT_MR": "PTS 2PT MR %",
    "PCT_PTS_3PT": "PTS 3PT %",
    "PCT_PTS_FB": "PTS FB %",
    "PCT_PTS_FT": "PTS FT %",
    "PCT_PTS_PAINT": "PTS PAINT %",
    "PCT_AST_FGM": "AST FGM %",
    "PCT_UAST_FGM": "UAST FGM %",
    "OPP_FG3_PCT": "OPP FG3 %",
    "OPP_EFG_PCT": "OPP EFG %",
    "OPP_FTA_RATE": "OPP FTA RATE",
    "OPP_TOV_PCT": "OPP TOV %",
}


lineup_format_columns = {
    "OFF RATING": "{:.1f}",
    "DEF RATING": "{:.1f}",
    "NET RATTING": "{:.1f}",
    "TS %": "{:.3f}",
    "MIN": "{:.1f}",
    "PACE": "{:.2f}",
    "FTA RATE": "{:.3f}",
    "TS %": "{:.3f}",
    "TM AST %": "{:.3f}",
    "FGA 2PT %": "{:.3f}",
    "FGA 3PT %": "{:.3f}",
    "PTS 2PT MR %": "{:.3f}",
    "PTS 3PT %": "{:.3f}",
    "PTS FB %": "{:.3f}",
    "PTS FT %": "{:.3f}",
    "PTS PAINT %": "{:.3f}",
    "AST FGM %": "{:.3f}",
    "UAST FGM %": "{:.3f}",
    "OPP FG3 %": "{:.3f}",
    "OPP EFG %": "{:.3f}",
    "OPP FTA RATE": "{:.3f}",
    "OPP TOV %": "{:.3f}",
}

df_lineup_group_name_change = df_lineup_index_drop.rename(
    columns={"GROUP_NAME": "LINEUP"}
)

df_lineup_set_index = df_lineup_group_name_change.set_index("LINEUP")


df_lineup_style = Lineup_DataFrame_Transform(
    df_lineup_set_index, lineup_rename_columns, lineup_format_columns
)

st.dataframe(df_lineup_style, use_container_width=True)
