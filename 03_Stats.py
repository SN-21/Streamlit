import streamlit as st
import pandas as pd

from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.library.parameters import MeasureTypeDetailedDefense


def DfIndexNameToTeamname(df):
    df_new_index = df.set_axis(
        [
            "Atlanta Hawks",
            "Boston Celtics",
            "Brooklyn Nets",
            "Charlotte Hornets",
            "Chicago Bulls",
            "Cleveland Cavaliers",
            "Dallas Mavericks",
            "Denver Nuggets",
            "Detroit Pistons",
            "Golden State Warriors",
            "Houston Rockets",
            "Indiana Pacers",
            "LA Clippers",
            "Los Angeles Lakers",
            "Memphis Grizzlies",
            "Miami Heat",
            "Milwaukee Bucks",
            "Minnesota Timberwolves",
            "New Orleans Pelicans",
            "New York Knicks",
            "Oklahoma City Thunder",
            "Orlando Magic",
            "Philadelphia 76ers",
            "Phoenix Suns",
            "Portland Trail Blazers",
            "Sacramento Kings",
            "San Antonio Spurs",
            "Toronto Raptors",
            "Utah Jazz",
            "Washington Wizards",
        ]
    )

    return df_new_index


def DfDropUnnecessaryColumns(df):
    # df_drop = df.drop(["TEAM_ID", "MIN", "TEAM_NAME", "CFID", "CFPARAMS"], axis=1)
    # "CFID", "CFPARAMS" のカラムは、APIの仕様からなくなっていたので、削除
    df_drop = df.drop(["TEAM_ID", "MIN", "TEAM_NAME"], axis=1)
    

    return df_drop


teamstats_a = leaguedashteamstats.LeagueDashTeamStats(
    last_n_games=82, measure_type_detailed_defense="Advanced"
)
df_adovenced = teamstats_a.league_dash_team_stats.get_data_frame()

df_adovenced_new_index = DfIndexNameToTeamname(df_adovenced)


df_adovenced_new_index_drop = DfDropUnnecessaryColumns(df_adovenced_new_index)

df_adovenced_fin = df_adovenced_new_index_drop.style.format(
    {
        "W_PCT": "{:.3f}",
        "E_OFF_RATING": "{:.1f}",
        "OFF_RATING": "{:.1f}",
        "E_DEF_RATING": "{:.1f}",
        "DEF_RATING": "{:.1f}",
        "E_NET_RATING": "{:.1f}",
        "NET_RATING": "{:.1f}",
        "E_PACE": "{:.1f}",
        "AST_RATIO": "{:.1f}",
        "PACE": "{:.2f}",
        "PACE_PER40": " {:.1f}",
        "AST_TO": "{:.1f}",
        "AST_PCT": "{:.3f}",
        "OREB_PCT": "{:.3f}",
        "DREB_PCT": "{:.3f}",
        "REB_PCT": "{:.3f}",
        "TM_TOV_PCT": "{:.3f}",
        "EFG_PCT": "{:.3f}",
        "TS_PCT": "{:.3f}",
    }
)

teamstats_scoring = leaguedashteamstats.LeagueDashTeamStats(
    last_n_games=30, measure_type_detailed_defense="Scoring"
)

df_scoring = teamstats_scoring.league_dash_team_stats.get_data_frame()

df_scoring_new_index = DfIndexNameToTeamname(df_scoring)

df_scoring_new_index_drop = DfDropUnnecessaryColumns(df_scoring_new_index)

df_scoring_style = df_scoring_new_index_drop.style.format(
    {
        "W_PCT": "{:.3f}",
        "PCT_FGA_2PT": "{:.3f}",
        "PCT_FGA_3PT": "{:.3f}",
        "PCT_PTS_2PT": "{:.3f}",
        "PCT_PTS_2PT_MR": "{:.3f}",
        "PCT_PTS_3PT": "{:.3f}",
        "PCT_PTS_FB": "{:.3f}",
        "PCT_PTS_FT": "{:.3f}",
        "PCT_PTS_OFF_TOV": "{:.3f}",
        "PCT_PTS_PAINT": "{:.3f}",
        "PCT_AST_2PM": " {:.3f}",
        "PCT_UAST_2PM": "{:.3f}",
        "PCT_AST_3PM": "{:.3f}",
        "PCT_UAST_3PM": "{:.3f}",
        "PCT_AST_FGM": "{:.3f}",
        "PCT_UAST_FGM": "{:.3f}",
    }
)


teamstats_defense = leaguedashteamstats.LeagueDashTeamStats(
    last_n_games=82, measure_type_detailed_defense="Defense"
)

df_defense = teamstats_defense.league_dash_team_stats.get_data_frame()

df_defense_new_index = DfIndexNameToTeamname(df_defense)

df_defense_new_index_drop = DfDropUnnecessaryColumns(df_defense_new_index)

df_defense_style = df_defense_new_index_drop.style.format(
    {
        "W_PCT": "{:.3f}",
        "DEF_RATING": "{:.1f}",
        "DREB_PCT": "{:.3f}",
        "OPP_PTS_OFF_TOV": "{:.0f}",
        "OPP_PTS_2ND_CHANCE": "{:.0f}",
        "OPP_PTS_FB": "{:.0f}",
        "OPP_PTS_PAINT": "{:.0f}",
    }
)


tab1, tab2, tab3 = st.tabs(["Adovenced Stats", "Scoring Stats", "Defence Stats"])
with tab1:
    st.dataframe(df_adovenced_fin, use_container_width=True)

with tab2:
    st.dataframe(df_scoring_style, use_container_width=True)

with tab3:
    st.dataframe(df_defense_style, use_container_width=True)
