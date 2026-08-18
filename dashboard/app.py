import streamlit as st
import pandas as st_pandas
import pandas as pd
import altair as alt

st.set_page_config(page_title="Engineering Workflow Audit Dashboard", layout="wide")

st.title("🚀 Engineering Tooling Adoption & ROI Dashboard")
st.markdown("""
This dashboard visualizes the results of our **Engineering Tooling Baseline Audit**.
It compares manual task execution times (Baseline) against automation-assisted execution times across 15 standard sprint tasks.
""")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("../data/audit_results.csv")
    df['Time Saved (mins)'] = df['Baseline Time (mins)'] - df['Tool-Assisted Time (mins)']
    df['Time Saved (%)'] = (df['Time Saved (mins)'] / df['Baseline Time (mins)']) * 100
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file not found. Ensure `audit_results.csv` exists in the `data/` directory.")
    st.stop()

# --- Top Level Metrics ---
st.header("Executive Scorecard")
col1, col2, col3, col4 = st.columns(4)

total_baseline = df['Baseline Time (mins)'].sum()
total_assisted = df['Tool-Assisted Time (mins)'].sum()
total_saved = total_baseline - total_assisted
avg_rework = df['Rework Rate (%)'].mean()
net_negative_count = df['Net-Negative Flag'].sum()

col1.metric("Total Baseline Time", f"{total_baseline} mins")
col2.metric("Total Tool-Assisted Time", f"{total_assisted} mins", f"{-total_saved} mins", delta_color="inverse")
col3.metric("Avg Rework Rate", f"{avg_rework:.1f}%")
col4.metric("Net-Negative Tasks", f"{net_negative_count} / {len(df)}")

st.divider()

# --- Time Savings by Category ---
st.header("Time Savings by Task Category")

category_df = df.groupby('Task Category')[['Baseline Time (mins)', 'Tool-Assisted Time (mins)']].mean().reset_index()

# Melt for Altair
melted_df = pd.melt(category_df, id_vars=['Task Category'], value_vars=['Baseline Time (mins)', 'Tool-Assisted Time (mins)'],
                    var_name='Method', value_name='Time (mins)')

chart = alt.Chart(melted_df).mark_bar().encode(
    x=alt.X('Task Category:N', title='Task Category', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('Time (mins):Q', title='Average Time (minutes)'),
    color=alt.Color('Method:N', scale=alt.Scale(domain=['Baseline Time (mins)', 'Tool-Assisted Time (mins)'], range=['#1f77b4', '#ff7f0e'])),
    xOffset='Method:N'
).properties(height=400)

st.altair_chart(chart, use_container_width=True)


# --- Rework & Quality ---
st.header("Quality & Rework Analysis")
col_q1, col_q2 = st.columns(2)

with col_q1:
    st.subheader("Rework Rate vs Quality Score")
    scatter = alt.Chart(df).mark_circle(size=100).encode(
        x=alt.X('Rework Rate (%):Q', title='Rework Rate (%)'),
        y=alt.Y('Quality Score (1-5):Q', scale=alt.Scale(domain=[1, 5])),
        color='Task Category:N',
        tooltip=['Task Description', 'Rework Rate (%)', 'Quality Score (1-5)', 'Net-Negative Flag']
    ).interactive()
    st.altair_chart(scatter, use_container_width=True)

with col_q2:
    st.subheader("Net-Negative Tasks (Where Automation Hurt)")
    net_neg_df = df[df['Net-Negative Flag'] == True]
    if not net_neg_df.empty:
        st.dataframe(net_neg_df[['Task Category', 'Task Description', 'Baseline Time (mins)', 'Tool-Assisted Time (mins)', 'Rework Rate (%)']], hide_index=True)
        st.markdown("**Insight:** Refactoring and Triaging without an MCP Server connecting to context leads to hallucination and high rework rates, taking longer than manual execution.")
    else:
        st.success("No net-negative tasks found!")

# --- Raw Data ---
with st.expander("View Raw Audit Data"):
    st.dataframe(df, use_container_width=True)

st.markdown("---")
st.caption("Toolkit powered by the Engineering Workflow Audit framework.")
