import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.set_page_config(page_title="Universal Excel Data Explorer", page_icon="📊", layout="wide")

st.title("📊 Universal Excel Data Explorer")
st.markdown("Upload **any Excel file** — the app will automatically summarize and visualize it.")

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("📁 Upload Excel file", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ File loaded successfully!")

        st.subheader("🧾 Preview of Data")
        st.dataframe(df.head())

        # -------------------------------
        # BASIC INFORMATION
        # -------------------------------
        st.subheader("📌 Basic Information")
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        st.text(info_str)

        # -------------------------------
        # STATISTICAL SUMMARY
        # -------------------------------
        st.subheader("📈 Statistical Summary (.describe())")
        st.dataframe(df.describe(include='all').T)

        # -------------------------------
        # AUTO-DETECT COLUMNS
        # -------------------------------
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        categorical_cols = df.select_dtypes(exclude='number').columns.tolist()

        # -------------------------------
        # NUMERIC ANALYSIS
        # -------------------------------
        if len(numeric_cols) > 0:
            st.subheader("🔢 Numeric Columns Overview")
            st.write(f"Detected {len(numeric_cols)} numeric column(s): {', '.join(numeric_cols)}")

            # Histogram for each numeric column
            for col in numeric_cols:
                st.markdown(f"**Histogram for {col}**")
                fig, ax = plt.subplots()
                sns.histplot(df[col].dropna(), kde=True, ax=ax)
                st.pyplot(fig)

            # Pairplot (correlation overview)
            if len(numeric_cols) >= 2:
                st.markdown("### 🔗 Pairwise Correlations (Pairplot)")
                fig_pair = sns.pairplot(df[numeric_cols].dropna())
                st.pyplot(fig_pair)

                # Correlation heatmap
                st.markdown("### 🧮 Correlation Heatmap")
                fig_corr, ax_corr = plt.subplots()
                sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax_corr)
                st.pyplot(fig_corr)

        else:
            st.info("⚠️ No numeric columns detected.")

        # -------------------------------
        # CATEGORICAL ANALYSIS
        # -------------------------------
        if len(categorical_cols) > 0:
            st.subheader("🔠 Categorical Columns Overview")
            st.write(f"Detected {len(categorical_cols)} categorical column(s): {', '.join(categorical_cols)}")

            for col in categorical_cols:
                value_counts = df[col].value_counts().head(15)
                st.markdown(f"**Top values in {col}**")
                fig, ax = plt.subplots()
                sns.barplot(x=value_counts.values, y=value_counts.index, ax=ax)
                ax.set_xlabel("Count")
                ax.set_ylabel(col)
                st.pyplot(fig)
        else:
            st.info("⚠️ No categorical columns detected.")

        # -------------------------------
        # DOWNLOAD CLEAN DATA
        # -------------------------------
        st.subheader("💾 Download Combined / Cleaned Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

else:
    st.info("⬆️ Please upload an Excel file to explore.")