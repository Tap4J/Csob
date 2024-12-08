# Csob
Assignment for CSOB exploratory analysis (data science position)
Dashboard deployed on following address: https://dashboardteam.streamlit.app/


## Guidelines
**Install Libraries from Requirements Using pip**
1. Open your terminal (macOS/Linux) or command prompt (Windows).
2. Navigate to the directory where you have downloaded/cloned the repository.
    ```sh
    cd path/to/your/project
    ```
3. (Optional) Create and activate a virtual environment:
      ```sh
      python3 -m venv env
      source venv/bin/activate
      ```
4. Install the required libraries using `pip`:

    ```sh
    pip install -r requirements.txt
    ```
**Run Jupyter Lab with the Notebook and Data**

To run the Jupyter Notebook with all the data in the GitHub repository, follow these steps:

1. Ensure you are still in the project directory.
2. Start Jupyter Lab:

    ```sh
    jupyter lab
    ```
3. A new tab will open in your default web browser, displaying the Jupyter Lab interface.
4. In Jupyter Lab, navigate to the directory where the notebook file (`.ipynb`) is located.
5. Open the notebook file to begin working with it.

## Run Dashboard
**Finish prerequisites from the previous step**
1. Open your terminal (macOS/Linux) or command prompt (Windows).
2. Navigate to the directory where you have downloaded/cloned the repository.
    ```sh
    cd path/to/your/project
    ```
3. Activate a virtual environment and run:
      ```sh
      streamlit run dashboard_team.py
      ```
**Run your dashboard in browser**

## Questions

1. **Actual value in total for each season start**
- How much money was spent every year in total for players?
- Is the amount increasing every year? What is the trend?
2. **Most transferred league/team**
- Which leagues are the most valued in terms of the value of players?
- Which team purchased the most players or spent the most?
- Which team is a farm (selling players)?
3. **Value of players**
- What are the top highest-valued players?
- How much does the estimated value differ from the actual value?
- Which players were traded the most?
- What is their total price after trading multiple times?
4. **Position**
- Which positions are most valued?
5. **Characteristics**
- What influences player value?
- Age and value?

## Results
1. **folder data contains:**
- original data "fotbal_prestupy_2000_2019"
- cleaned data "df_cleaned"
- cleaned data with the imputed value of 0 instead of NaN  "df_cleaned_non_na"
2. **jupyter notebooks:**
  - **"cleaning_dataset":**
    - cleaning of data
    - transformation of data, removing spaces
    - adding columns
    - changing data types
    - creating a dataset with the imputed value
  - **"exploratory_analysis":**
    - analysis of the dataset
    - prototyping questions
    - providing insights
    - providing visualisations
    - justification of results
    - searching relationships 
  - **"EDA_results":**
    - questions and their respective answers
    - visualizations and tables
3. **html file**
  - same as EDA_results jupyter notebook in format of HTML
4. **general_functions**
  - file with general reusable Python functions
5. **uloha_zadani:**
  - assignment task
