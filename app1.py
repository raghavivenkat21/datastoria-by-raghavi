import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DataStoria by Raghavi",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- HEADER ----------------
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>
        DataStoria Pro - by Raghavi
    </h1>
    <hr>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Controls")
st.sidebar.write("Upload dataset to generate insights")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# ---------------- MAIN APP ----------------
if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # ---------------- TABS ----------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "📌 Overview",
        "📈 Visualizations",
        "🧠 Insights",
        "🔍 Data Quality"
    ])

    numeric_cols = df.select_dtypes(include="number").columns

    # ---------------- TAB 1 ----------------
    with tab1:

        st.subheader("Dataset Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())

        st.dataframe(df.head())

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Dataset",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    # ---------------- TAB 2 ----------------
    with tab2:

        st.subheader("📊 Automatic Visualizations")

        if len(numeric_cols) > 0:

            selected_col = st.selectbox("Select Column", numeric_cols)

            fig = px.histogram(
                df,
                x=selected_col,
                title=f"Distribution of {selected_col}",
                color_discrete_sequence=["#4CAF50"]
            )

            st.plotly_chart(fig, use_container_width=True)

            # SAFE DOWNLOAD (no kaleido issue)
            st.download_button(
                "📊 Download Dataset (CSV)",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="chart_data.csv",
                mime="text/csv"
            )

            st.subheader("🔗 Correlation Heatmap")

            corr = df[numeric_cols].corr()

            heatmap = px.imshow(
                corr,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="Viridis"
            )

            st.plotly_chart(heatmap, use_container_width=True)

    # ---------------- TAB 3 ----------------
    with tab3:

        st.subheader("🧠 Smart Insights")

        if len(numeric_cols) > 0:

            for col in numeric_cols:

                mean_val = df[col].mean()
                max_val = df[col].max()
                min_val = df[col].min()

                st.markdown(f"""
                ### 📌 {col}
                - 📊 Mean: **{mean_val:.2f}**
                - 🔼 Max: **{max_val:.2f}**
                - 🔽 Min: **{min_val:.2f}**
                """)

                if max_val > mean_val * 2:
                    st.warning(f"⚠️ {col} shows high variation (possible outliers)")

        st.subheader("🔍 Column Types")

        for col in df.columns:

            if df[col].dtype == "object":
                st.write(f"🟡 {col} → Categorical")
            else:
                st.write(f"🔵 {col} → Numerical / Other")

    # ---------------- TAB 4 ----------------
    with tab4:

        st.subheader("📊 Data Quality Score")

        missing_ratio = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        quality_score = 100 - (missing_ratio * 100)

        st.metric("Dataset Quality Score", f"{quality_score:.2f} / 100")

        st.progress(int(quality_score))

        st.subheader("📌 Missing Values Per Column")
        st.dataframe(df.isnull().sum())

        st.success("Dataset analysis completed successfully 🚀")

else:

    st.info("👈 Upload a CSV file from sidebar to start analysis")
