import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go

st.set_page_config(
    page_title="Player Stats Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
alt.themes.enable("dark")

df = pd.read_csv("data/df_cleaned.csv")

st.title("Player Stats Dashboard")

season_list = list(df["Season Start"].unique())
selected_season = st.selectbox("Select a Season", season_list, index=len(season_list) - 1)
df_selected_season = df[df["Season Start"] == selected_season]
df_selected_season_sorted = df_selected_season.sort_values(by="Actual Value (mil)", ascending=False)

teams_list = pd.concat([df["New Team"], df["Original Team"]]).unique().tolist()
selected_team = st.selectbox("Select a Team", teams_list, index=len(teams_list) - 1)

def make_scatter_plot(input_df, season_list, y_input, group_by_team, color_by):
    all_seasons = pd.DataFrame({"Season Start": season_list})
    filtered_df = input_df[(input_df["New Team"] == group_by_team) | (input_df["Original Team"] == group_by_team)]

    if filtered_df.empty:
        raise ValueError(f"No data available for team '{group_by_team}'.")

    aggregated_df = filtered_df.groupby(["Season Start", color_by])[y_input].sum().reset_index()
    aggregated_df = pd.merge(all_seasons, aggregated_df, on="Season Start", how="left").fillna(0)


    scatter_plot = alt.Chart(aggregated_df).mark_circle(size=100).encode(
        x=alt.X("Season Start:O", title="Season Start"),
        y=alt.Y(f"{y_input}:Q", title=y_input),
        color=alt.Color(f"{color_by}:N", title=color_by),
        tooltip=["Season Start", f"{y_input}", color_by]
    ).properties(
        width=900,
        height=500
    )
    
    return scatter_plot









# def calculate_value_diff(input_df, input_season):
#     selected_season_actual = input_df[input_df["Season Start"] == input_season].groupby("Player ID")["Actual Value (mil)"].sum().reset_index()
#     selected_season_estimated = input_df[input_df["Season Start"] == input_season].groupby("Player ID")["Estimated Value (mil)"].sum().fillna(0).reset_index()
    
#     merged = pd.merge(selected_season_actual, selected_season_estimated, on="Player ID", how="outer", suffixes=("_actual", "_estimated"))
    
#     merged["Difference Value"] = (merged["Actual Value (mil)"] - merged["Actual Value (mil)"])

#     return merged


# def make_donut(input_df):
#     difference_value = input_df["Difference Value"].iloc[0]
#     if difference_value >= 0:
#         chart_color = ['#27AE60', '#12783D']
#     else:
#         chart_color = ['#E74C3C', '#781F16']


#     source = pd.DataFrame({
#         "Value": [abs(difference_value), 100 - abs(difference_value)],
#         "Category": ["Difference", "Remaining"]
#     })

#     donut_chart = alt.Chart(source).mark_arc(innerRadius=45).encode(
#         theta=alt.Theta(field="Value", type="quantitative"),
#         color=alt.Color("Category:N", scale=alt.Scale(range=chart_color)),
#     ).properties(width=130, height=130)

#     return donut_chart


col = st.columns((1.5, 4.5, 2), gap='medium')


with col[0]:
    st.markdown('#### Total Players Bought/Total PLayers Sold in mil')

    if selected_season > 1999:
        actual_value = df.groupby("New Team")["Actual Value (mil)"].sum().reset_index()
    else:
        actual_value = 0
    if selected_season > 1999:
        estimated_value = df.groupby("Original Team")["Actual Value (mil)"].sum().reset_index()
    else:
        estimated_value = 0
    
    st.metric(label="Actual Value vs Estimated", value=f"{actual_value} vs {estimated_value}")

    st.markdown('#### Difference against estimation')

    # donut_chart = make_donut(df_player_difference)


    # migrations_col = st.columns((0.2, 1, 0.2))
    # with migrations_col[1]:
    #     st.write('Value')
    #     st.altair_chart(donut_chart)

with col[1]:
    st.markdown('#### Scatter Plot Chart')


    # zavolat ešte original team
    scatter_plot_new_team = make_scatter_plot(df, season_list, "Actual Value (mil)", selected_team, "Position")
    st.altair_chart(scatter_plot_new_team, use_container_width=True)

with col[2]:
    st.markdown('#### Players for Selected Season')

    st.dataframe(df_selected_season_sorted[["Name", "Age", "New Team", "Actual Value (mil)"]],
                column_order=("Name", "Age", "New Team", "Actual Value (mil)"),
                hide_index=True)

    with st.expander('About', expanded=True):
        st.write('''  
            - Data: Football Player Transfers
            - :orange[**Player Transfers**]: Players that changed teams during the selected season.
            - :orange[**Age and Teams**]: Details about the player’s age and new team for the given season.
        ''')



