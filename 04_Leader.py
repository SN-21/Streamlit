import streamlit as st
import pandas as pd

from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.library.parameters import PerModeDetailed

leaders_per_game = leagueleaders.LeagueLeaders(per_mode48="PerGame")
df_leaders_per_game = leaders_per_game.league_leaders.get_data_frame()

leaders_total = leagueleaders.LeagueLeaders(per_mode48="Totals")
df_leaders_total = leaders_total.league_leaders.get_data_frame()

df_leaders_per_game_drop = df_leaders_per_game.drop(
    ["PLAYER_ID", "PLAYER_ID", "TEAM_ID", "RANK"], axis=1
)

df_leaders_total_drop = df_leaders_total.drop(
    ["PLAYER_ID", "PLAYER_ID", "TEAM_ID", "RANK"], axis=1
)

df_leader_per_game_index_drop = df_leaders_per_game_drop.set_index("PLAYER")


df_leader_total_index_drop = df_leaders_total_drop.set_index("PLAYER")


df_leader_per_game_style = df_leader_per_game_index_drop.style.format(
    {
        "MIN": "{:.1f}",
        "FGM": "{:.1f}",
        "FGA": "{:.1f}",
        "FG_PCT": "{:.3f}",
        "FG3M": "{:.1f}",
        "FG3A": "{:.1f}",
        "FG3_PCT": "{:.3f}",
        "FTM": "{:.1f}",
        "FTA": "{:.1f}",
        "FT_PCT": "{:.3f}",
        "OREB": "{:.1f}",
        "DREB": "{:.1f}",
        "REB": "{:.1f}",
        "AST": "{:.1f}",
        "STL": "{:.1f}",
        "BLK": "{:.1f}",
        "TOV": "{:.1f}",
        "PTS": "{:.1f}",
        "EFF": "{:.1f}",
    }
)

df_leader_total_style = df_leader_total_index_drop.style.format(
    {
        "FG_PCT": "{:.3f}",
        "FG3_PCT": "{:.3f}",
        "FT_PCT": "{:.3f}",
        "AST_TOV": "{:.2f}",
        "STL_TOV": "{:.2f}",
    }
)

tab1, tab2 = st.tabs(["per game stats", "total stats"])

with tab1:
    st.dataframe(df_leader_per_game_style, use_container_width=True)

with tab2:
    st.dataframe(df_leader_total_style, use_container_width=True)
