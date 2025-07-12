import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

DB_NAME = "generation_data.db"
TABLE_NAME = "wind_solar_data"

def load_data():
    with sqlite3.connect(DB_NAME) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)

    df['startTime'] = pd.to_datetime(df['startTime'], utc=True)
    df['date'] = df['startTime'].dt.date
    return df

def plot_heatmaps_separately(df):
    """Plot separate heatmaps for Wind Onshore, Wind Offshore, and Solar."""
    daily = df.groupby(['date', 'psrType'])['quantity'].sum().unstack(fill_value=0)

    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    for i, psr in enumerate(['Wind Offshore', 'Wind Onshore', 'Solar']):
        if psr in daily.columns:
            sns.heatmap(
                pd.DataFrame(daily[psr]).T,
                ax=axes[i],
                cmap="YlGnBu",
                cbar_kws={'label': 'MW'},
                linewidths=0.1
            )
            axes[i].set_title(f"{psr} - Daily Generation")
            axes[i].set_ylabel("Type")

    plt.tight_layout()
    plt.show()

def plot_interactive_separately(df):
    """Plot separate interactive charts for each psrType."""
    grouped = df.groupby(['startTime', 'psrType'])['quantity'].sum().reset_index()

    for psr in ['Wind Offshore', 'Wind Onshore', 'Solar']:
        df_psr = grouped[grouped['psrType'] == psr]
        if not df_psr.empty:
            fig = px.line(
                df_psr,
                x="startTime",
                y="quantity",
                title=f"📊 Interactive Line Chart - {psr}",
                labels={"startTime": "Time", "quantity": "MW"},
            )
            fig.update_layout(height=400)
            fig.show()

if __name__ == "__main__":
    df = load_data()

    print("🧊 Plotting separate heatmaps...")
    plot_heatmaps_separately(df)

    print("🚀 Plotting separate interactive charts...")
    plot_interactive_separately(df)
