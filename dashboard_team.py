import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
print(alt.__version__)

st.set_page_config(
    page_title="Player Stats Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
            
[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 1rem;
    background-color: #ffffff; /* White background for the chart */
    border: 1px solid #000000; /* Black border for the box */
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #ffffff; /* White background for a card-like appearance */
    border: 1px solid #d9d9d9; /* Light grey border */
    border-radius: 10px;
    text-align: center;
    padding: 15px 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}

[data-testid="stMetricLabel"] {
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: "IBM Plex Mono", monospace; /* Match the Altair title font */
    color: #262730; /* Dark text color */
    font-weight: bold;
}
                 
[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 1rem;
    background-color: #ffffff; /* White background for the chart */
    border: 1px solid #000000; /* Black border for the box */
    margin-bottom: -7rem;
}
                       
</style>
""", unsafe_allow_html=True)

# Loading data - cleaned without NaN values
df = pd.read_csv("data/df_cleaned.csv")

# Sidebar definitions for season and players

with st.sidebar:

    st.title("Player Stats Dashboard")

    teams_list = pd.concat([df["New Team"], df["Original Team"]]).unique().tolist()
    selected_team = st.selectbox("Select a Team", teams_list, index=0 )

    season_list = list(df["Season Start"].unique())
    selected_season = st.selectbox("Select a Season", season_list, index=len(season_list) - 1)
    df_selected_season = df[df["Season Start"] == selected_season]
    df_selected_season_sorted = df_selected_season.sort_values(by="Actual Value (mil)", ascending=False)


# Main plots - scatter bought and sold players

def make_scatter_plot(input_df, season_list, y_input, selected_team, graph_type, color_by):
    all_seasons = pd.DataFrame({"Season Start": season_list})

    if graph_type == "bought":
        filtered_df = input_df[input_df["New Team"] == selected_team]
    elif graph_type == "sold":
        filtered_df = input_df[input_df["Original Team"] == selected_team]
    else:
        raise ValueError("graph_type must be either 'bought' or 'sold'")

    if filtered_df.empty:
        no_data_text = alt.Chart(all_seasons).mark_text(
        align='center',
        baseline='middle',
        fontSize=20
        ).encode(
            text=alt.value(f"No Data for Players {graph_type.capitalize()} by {selected_team}")
        ).properties(
            width=900,
            height=500,
            title=f"No Data for Players {graph_type.capitalize()} by {selected_team}"
        )
        return no_data_text
    
    aggregated_df = filtered_df.groupby(["Season Start", color_by, "Name"])[y_input].sum().reset_index()
    aggregated_df_with_all_seasons = pd.merge(all_seasons, aggregated_df, on="Season Start", how="left")
    filtered_chart_data = aggregated_df_with_all_seasons[aggregated_df_with_all_seasons[y_input] > 0]

    scatter_plot = alt.Chart(filtered_chart_data ).mark_circle(size=100).encode(
        x=alt.X("Season Start:O", title="Season", scale=alt.Scale(domain=season_list), axis=alt.Axis(labelAngle=-90)),
        y=alt.Y(f"{y_input}:Q", title=y_input),
        color=alt.Color(f"{color_by}:N", title=color_by),
        tooltip=["Name", "Season Start", f"{y_input}", color_by]
    ).properties(
        width=900,
        height=500,
        title=f"Players {graph_type.capitalize()} by {selected_team}"
    )
    
    return scatter_plot

# Site columns

col = st.columns((1.5, 4.5, 2), gap='medium')

# First column definition, calculating total values adn about table

with col[0]:
    st.markdown('#### Value of Players Bought vs Sold for Selected Season (in mil)')

    if selected_season not in [None, '']:
        season_df = df[df["Season Start"] == selected_season]
    else:
        season_df = df 

    new_team_value = season_df[season_df["New Team"] == selected_team]["Actual Value (mil)"].sum()
    original_team_value = season_df[season_df["Original Team"] == selected_team]["Actual Value (mil)"].sum()

    new_team_value_formatted = f"{new_team_value:.2f}"
    original_team_value_formatted = f"{original_team_value:.2f}"

    st.metric(label="Purchased Players Value", value=new_team_value_formatted)
    st.metric(label="Sold Players Value", value=original_team_value_formatted)

    with st.expander('About', expanded=True):
        st.write('''  
            - Data: Football Player Transfers
            - :orange[**Team Transfers of Players by Position**]: Players that were purchased and sold by the selected team with their position in the team.
            - :orange[**Value of Players**]: Value of purchased and sold players for particular season for the selected team.
            - :orange[**Highest Valued Players**]: Highest valeud players for selected season with info about their name, age, new team transfer and value.
        ''')

# Second column defintion with plots

with col[1]:
    st.markdown('#### Team Transfers of Players')

    scatter_plot_new_team = make_scatter_plot(df, season_list, "Actual Value (mil)", selected_team, "bought", "Position")
    st.altair_chart(scatter_plot_new_team, use_container_width=True)
    scatter_plot_original_team = make_scatter_plot(df, season_list, "Actual Value (mil)", selected_team, "sold", "Position")
    st.altair_chart(scatter_plot_original_team, use_container_width=True)

# Third column with table + TOdo donut charts

with col[2]:
    st.markdown(f'#### Highest Valued Players in Season {selected_season}')

    st.dataframe(df_selected_season_sorted[["Name", "Age", "New Team", "Actual Value (mil)"]],
                column_order=("Name", "Age", "New Team", "Actual Value (mil)"),
                hide_index=True, height=900 )




