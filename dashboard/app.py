import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt

# set page congfit 
st.set_page_config(page_title="AdSmart Campaign Dashboard", layout="centered")

# title 
st.title("AdSmart Campaign Analytics")
st.markdown("""
### Welcome to **AdSmart**  
Where your *pretend* campaign works harder than some real ones.

We're talking simulated clicks, cooked-up conversions, and just enough data science to make it feel legit.

No real budgets harmed. Just vibes, metrics, and the occasional A/B test gone rogue.
""")

# load data 
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/interactions.csv")
    return df

df = load_data()

# show arw data toggle
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Interactions Data")
    st.dataframe(df.head())

# KPIs

st.subheader("Key Metrics")
ctr = (df["clicked"].sum() / len(df)) * 100
cvr = (df["converted"].sum() / df["clicked"].sum()) * 100
col1, col2 = st.columns(2)
col1.metric("Click-Through Rate (CTR)", f"{ctr:.2f}%")
col2.metric("Conversion Rate (CVR)", f"{cvr:.2f}%")

# funnel summay
st.subheader("Funnel Breakdown")
total_users = len(df)
clicks = df["clicked"].sum()
conversions = df["converted"].sum()
st.write(f"Total Users: **{total_users}** -> Clicked: **{clicks}** -> Converted: **{conversions}**")

# calculate percentages 
click_rate = (clicks / total_users) * 100
conversion_rate = (conversions / total_users) * 100
post_click_cvr = (conversions / clicks) * 100 if clicks > 0 else 0

# write text summary
st.markdown(f"""
**Total Users:** {total_users:,}  
**Clicked:** {clicks:,} ({click_rate:.2f}% of total)  
**Converted:** {conversions:,} ({conversion_rate:.2f}% of total, {post_click_cvr:.2f}% post-click)
""")

#funnel bar chart
funnel_data = pd.DataFrame({
    "Stage": ["Total Users", "Clicked", "Converted"],
    "Count": [total_users, clicks, conversions]
})

fig, ax = plt.subplots(figsize=(6,4))
bars = ax.barh(funnel_data["Stage"], funnel_data["Count"], color=["#6fa8dc", "#f6b26b", "#93c47d"])


# Annotate bars with numbers and percentages
for i, bar in enumerate(bars):
    count = funnel_data["Count"].iloc[i]
    pct = (count / total_users) * 100
    ax.text(count + total_users * 0.01, bar.get_y() + bar.get_height() / 2,
            f"{count:,} ({pct:.2f}%)", va='center', fontsize=10)

ax.set_xlabel("User Count")
ax.set_title("User Funnel: Who Clicked & Who Committed")
ax.invert_yaxis()  # top-down funnel style
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.grid(axis="x", linestyle="--", alpha=0.5)

st.pyplot(fig)

st.write(f"Total Users: {total_users}")
st.write(f"Clicked: {clicks} ({(clicks/total_users)*100:.2f}%)")
st.write(f"Converted: {conversions} ({(conversions/clicks)*100:.2f}% of clickers)")

# show visuals 
st.subheader("Visualizations")
st.image("visuals/funnel_chart.png", caption="Confusion Matrix", use_container_width=True)
st.image("visuals/roc_curve.png", caption="ROC Curve",  use_container_width=True)

# footer 
st.markdown("---")
st.caption("👩🏽‍💻 Built by Pearl Senza Sikepe| All data simulated.")