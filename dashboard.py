import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="Player Stats Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
alt.themes.enable("dark")

df = pd.read_csv("data/df_cleaned.csv")

st.title("Player Stats Dashboard")

season_list = list(df["Season"].unique())

selected_season = st.selectbox("Select a Season", season_list, index=len(season_list))
df_selected_season = df[df["Season Start"] == selected_season]
df_selected_season_sorted = df_selected_season.sort_values(by="Actual Value (mil)", ascending=False)

def make_line_plot(input_df, x_input, y1_input, y2_input):
    actual_value_line = alt.Chart(input_df).mark_line(color="green").encode(
        x = alt.X(f'{x_input}:O', axis=alt.Axis(title=x_input, titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        y = alt.Y(f'{y1_input}:Q', axis=alt.Axis(title=y1_input, titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        tooltip=[x_input, y1_input]
    ).properties(
        width=900,
        height=500
    )
    estimated_value_line = alt.Chart(input_df).mark_line(color="red").encode(
        x = alt.X(f'{x_input}:O'),
        y = alt.Y(f'{y2_input}:Q'),
        tooltip=[x_input, y2_input]
    )
    combined_chart = alt.layer(
        actual_value_line, estimated_value_line
    ).resolve_scale(
        y="shared"
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )
    return combined_chart


def calculate_value_diff(input_df, input_season):
    selected_season_actual = input_df[input_df["Season Start"] == input_season].groupby("Player ID")["Actual Value (mil)"].sum().reset_index()
    selected_season_estimated = input_df[input_df["Season Start"] == input_season].groupby("Player ID")["Estimated Value (mil)"].sum().fillna(0).reset_index()
    
    merged = pd.merge(selected_season_actual, selected_season_estimated, on="Player ID", how="outer", suffixes=("_actual", "_estimated"))
    
    merged["Difference Value"] = (merged["Actual Value (mil)_actual"] - merged["Actual Value (mil)_estimated"])

    return merged


def make_donut(input_df):
    difference_value = input_df["Difference Value"].iloc[0]
    if difference_value >= 0:
        chart_color = ['#27AE60', '#12783D']
    else:
        chart_color = ['#E74C3C', '#781F16']


    source = pd.DataFrame({
        "Value": [abs(difference_value), 100 - abs(difference_value)],
        "Category": ["Difference", "Remaining"]
    })

    donut_chart = alt.Chart(source).mark_arc(innerRadius=45).encode(
        theta=alt.Theta(field="Value", type="quantitative"),
        color=alt.Color("Category:N", scale=alt.Scale(range=chart_color)),
    ).properties(width=130, height=130)

    return donut_chart


col = st.columns((1.5, 4.5, 2), gap='medium')


with col[0]:
    st.markdown('#### Actual Value/Estimated Value in mil')

    df_player_difference = calculate_value_diff(df, selected_season)

    if "Actual Value (mil)" in df.columns:
        actual_value = df.groupby("Player ID")["Actual Value (mil)"].sum().reset_index()
    else:
        actual_value = 0
    if "Estimated Value (mil)" in df.columns:
        estimated_value = df.groupby("Player ID")["Estimated Value (mil)"].sum().reset_index()
    else:
        estimated_value = 0
    
    st.metric(label="Actual Value vs Estimated", value=f"{actual_value} vs {estimated_value}")

    st.markdown('#### Difference against estimation')

    donut_chart = make_donut(df_player_difference)


    migrations_col = st.columns((0.2, 1, 0.2))
    with migrations_col[1]:
        st.write('Inbound')
        st.altair_chart(donut_chart)

with col[1]:
    st.markdown('#### Line Chart')

    line_plot = make_line_plot(df_selected_season, "Season", "Actual Value (mil)", "Estimated Value (mil)")
    st.plotly_chart(line_plot, use_container_width=True)

with col[2]:
    st.markdown('#### Players for Selected Season')

    st.dataframe(df_selected_season_sorted[["Name", "Age", "New Team", "Actual Value (mil)"]],
                 column_order=("Name", "Age", "New Team", "Actual Value (mil)"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Name": st.column_config.TextColumn("Player Name"),
                    "Age": st.column_config.IntColumn("Age"),
                    "New Team": st.column_config.TextColumn("Team"),
                    "Actual Value (mil)": st.column_config.TextColumn("Actual Value (mil)"),
                 })

    with st.expander('About', expanded=True):
        st.write('''  
            - Data: Football Player Transfers
            - :orange[**Player Transfers**]: Players that changed teams during the selected season.
            - :orange[**Age and Teams**]: Details about the player’s age and new team for the given season.
        ''')



