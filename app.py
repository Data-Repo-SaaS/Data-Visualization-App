import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Set Streamlit layout to wide
st.set_page_config(layout="wide", page_title="Data Visualization", page_icon="🫧")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main { background-color: white; }
    .stButton > button { background-color: #178e79; color: white; border-radius: 5px; padding: 10px; border: none; }
    .stDownloadButton > button { background-color: #178e79; color: white; border-radius: 5px; padding: 10px; border: none; }
    .stTextInput > div > input, .stTextArea > div > textarea {
        background-color: #F5F5F5; border: 1px solid #DADADA; border-radius: 5px; padding: 5px;
    }
    .stSelectbox > div > div > div {
        background-color: #F5F5F5; border: 1px solid #DADADA; border-radius: 5px; padding: 5px;
    }
    h1, h2, h3, h4, h5, h6 { color: #333333; }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the app with emoji
st.title("🫧Data Visualization")

# File uploader for user data
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Reading the uploaded file
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")

        # Dataset Preview
        st.write("## Dataset Preview")

        # Allow users to select rows and columns to preview
        preview_rows = st.slider("Number of rows to preview", min_value=1, max_value=len(data), value=5)
        preview_columns = st.multiselect("Select columns to preview", data.columns.tolist(), default=data.columns.tolist())

        if preview_columns:
            st.write(data[preview_columns].head(preview_rows))

        # Display basic dataset information
        st.write("## Dataset Information")
        st.write("### Shape of the dataset:", data.shape)
        st.write("### Column names:", data.columns.tolist())
        st.write("### Summary Statistics:")
        st.dataframe(data.describe(), use_container_width=True)

        # Graph Visualization
        st.write("## Graph Visualization")

        # Select graph type
        graph_type = st.selectbox("Choose the graph type", [
            "Bar Plot", "Line Plot", "Scatter Plot", "Histogram", "Box Plot", "Heatmap", "Pie Chart", "Pair Plot"])

        # Select columns for visualization
        columns = data.columns.tolist()

        if graph_type in ["Bar Plot", "Line Plot", "Scatter Plot"]:
            x_axis = st.selectbox("Select X-axis", columns)
            y_axis = st.selectbox("Select Y-axis", columns)

            if st.button("Generate Graph"):
                plt.figure(figsize=(10, 6))
                if graph_type == "Bar Plot":
                    sns.barplot(x=data[x_axis], y=data[y_axis])
                elif graph_type == "Line Plot":
                    plt.plot(data[x_axis], data[y_axis])
                    plt.xlabel(x_axis)
                    plt.ylabel(y_axis)
                elif graph_type == "Scatter Plot":
                    sns.scatterplot(x=data[x_axis], y=data[y_axis])
                plt.title(f"{graph_type} of {y_axis} vs {x_axis}")
                st.pyplot(plt)

        elif graph_type == "Histogram":
            column = st.selectbox("Select Column", columns)

            if st.button("Generate Graph"):
                plt.figure(figsize=(10, 6))
                sns.histplot(data[column], kde=True, bins=30)
                plt.title(f"Histogram of {column}")
                st.pyplot(plt)

        elif graph_type == "Box Plot":
            column = st.selectbox("Select Column", columns)

            if st.button("Generate Graph"):
                plt.figure(figsize=(10, 6))
                sns.boxplot(y=data[column])
                plt.title(f"Box Plot of {column}")
                st.pyplot(plt)

        elif graph_type == "Heatmap":
            if st.button("Generate Graph"):
                plt.figure(figsize=(10, 6))
                sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
                plt.title("Heatmap of Correlation")
                st.pyplot(plt)

        elif graph_type == "Pie Chart":
            column = st.selectbox("Select Column for Pie Chart", columns)
            if st.button("Generate Graph"):
                pie_data = data[column].value_counts()
                plt.figure(figsize=(8, 8))
                plt.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=90)
                plt.title(f"Pie Chart of {column}")
                st.pyplot(plt)

        elif graph_type == "Pair Plot":
            if st.button("Generate Graph"):
                sns.pairplot(data)
                st.pyplot()

        # Notes Section
        st.write("## Take Notes")

        # Note-taking feature
        notes = st.text_area("Write your notes here")

        # Options for formatting notes
        note_title = st.text_input("Title for your notes")
        st.write("### Note Options")
        highlight_important = st.checkbox("Highlight important notes")
        add_timestamp = st.checkbox("Add timestamp to notes")

        if st.button("Download Notes"):
            formatted_notes = f"# {note_title}\n\n" if note_title else ""
            if add_timestamp:
                from datetime import datetime
                formatted_notes += f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            formatted_notes += notes
            if highlight_important:
                formatted_notes = f"**Important:**\n{formatted_notes}"

            notes_file = BytesIO()
            notes_file.write(formatted_notes.encode("utf-8"))
            notes_file.seek(0)
            st.download_button(
                label="Download Notes",
                data=notes_file,
                file_name="notes.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a file to start visualization.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #333333;'>"
    "<b>Data Visualization</b> | Developed by datarepo.in</a>"
    "</div>",
    unsafe_allow_html=True
)
