import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
st.set_page_config(page_title="🚨 Police Insights Dashboard", layout="wide")

#Setting background iamge
def set_bg_hack_url():
    
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://www.shutterstock.com/image-photo/red-beacon-isolated-on-white-260nw-2361953095.jpg");
             background-size: cover;
             background-repeat: no-repeat;
              background-color: rgba(255,255,255,0.7);
             background-blend-mode: lighten; 
                      }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_bg_hack_url()

# Header
st.markdown("""
    <h1 style='color:RED; font-size: 28px; font-family:Arial, sans-serif;white-space: nowrap;'>
        🔒 SECURE CHECK: DIGITAL LEDGER FOR POLICE CHECK POST👮
    </h1>
""", unsafe_allow_html=True)

#Sub headers

st.markdown("""
    <h3 style='color:navy; font-size: 16px; font-family:Georgia, serif;'>
        An interactive dashboard for analyzing police stop data using MySQL and Python
    </h3>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display: flex; align-items: center;">
    <img src="data:image/png;base64,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" width=60px;style="margin-right: 10px;"/>
    <h5 style="color:green; font-size:15px;font-family:Georgia, serif;">
        Law Enforcement & Public Safety Real-time Monitoring Systems
    </h5>
</div>
""", unsafe_allow_html=True)


# Database connection function(Creates and returns a connection to my local MySQL database named secure_check.)
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="secure_check"
    )

# Function to fetch data from database
def get_data(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    conn.close()
    return pd.DataFrame(rows, columns=cols)

# Display full table in dashboard
st.header("🧾Police Log Records")
query = "SELECT * FROM police_logs"
data = get_data(query)
st.dataframe(data)# displays result in an interactive table




# Key Metrics
     
total_stops = len(data)
total_arrests = data['is_arrested'].sum()
drug_related_stops = data['Drugs_related_stop'].sum()


st.header("📌 Key Metrics")
col1, col2, col3= st.columns(3)

col1.metric("🚓 Total Stops", total_stops)
col2.metric("🔒 Arrests", total_arrests)
col3.metric("💊 Drug-Related Stops", drug_related_stops)


# choropleth

st.subheader("🌍 Choropleth: Arrest Rate by Country")

query = """
SELECT Country_name, 
       ROUND(AVG(is_arrested) * 100, 2) as arrest_rate
FROM police_logs
GROUP BY Country_name
"""
df_choropleth = get_data(query)

if not df_choropleth.empty:
    fig = px.choropleth(
        df_choropleth,
        locations="Country_name",
        locationmode="country names",
        color="arrest_rate",
        hover_name="Country_name",
        color_continuous_scale="Reds",
        title="🌍 Arrest Rate by Country (%)"
    )
    st.plotly_chart(fig)
else:
    st.warning("No data available for choropleth.")

#MEDIUM QUERIES

medium_query_map={"Top 10 vehicles involved in drug-related stops":"""SELECT Vehicle_Number, COUNT(*) AS drug_stop_count
                FROM police_logs WHERE drugs_related_stop = TRUE GROUP BY Vehicle_Number
                ORDER BY drug_stop_count DESC LIMIT 10""",
                "Most frequently searched Vehicles":"""SELECT Vehicle_Number,count(*) as search_count
                 FROM police_logs WHERE search_conducted = TRUE GROUP BY Vehicle_Number ORDER BY search_count DESC""",
                 "Driver age group with highest arrest rate":"""SELECT CASE WHEN driver_age < 18 THEN '<18'
                  WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
                    WHEN driver_age BETWEEN 36 AND 45 THEN '36-45'
                    WHEN driver_age BETWEEN 46 AND 55 THEN '46-55'
                    WHEN driver_age BETWEEN 56 AND 65 THEN '56-65'
                    ELSE '65+'
                    END AS driver_age_group,
                    count(*) as total_stops,
                    sum(CASE when is_arrested= TRUE then 1 else 0 END) AS TOTAL_ARREST,
                    Round(sum(CASE when is_arrested= TRUE then 1 else 0 END)*100/count(*),4) AS ARREST_RATE
                    FROM police_logs
                    group by driver_age_group
                    order by arrest_rate desc
                    limit 1""",
                    "Gender distribution of drivers stopped in each country":"""SELECT country_name, driver_gender, COUNT(*) AS total_stop_count
                     FROM police_logs GROUP BY country_name, driver_gender ORDER BY country_name, driver_gender""",
                     "Highest search rate for race and gender combination":"""SELECT driver_race, driver_gender,COUNT(*) AS stop_count,SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS total_searches,
                      round(100*(SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END)/ COUNT(*)),2) AS search_rate
                      FROM police_logs GROUP BY driver_race, driver_gender ORDER BY search_rate DESC LIMIT 1 """,
                      "Time of day with most traffic stops": """SELECT hour(stop_time) as Hour_of_the_day, count(*) as total_stops,
                        CASE WHEN HOUR(Stop_time) BETWEEN 5 AND 11 THEN 'Morning'
                        WHEN HOUR(Stop_time) BETWEEN 12 AND 15 THEN 'Afternoon'
                        WHEN HOUR(Stop_time) BETWEEN 16 AND 19 THEN 'Evening'
                        ELSE 'Night' END AS time_of_day from police_logs
                        GROUP BY hour(stop_time),time_of_day
                        ORDER BY hour(stop_time) desc LIMIT 1""",
                        "Average stop duration for different violations":"""SELECT VIOLATION,
                        avg(CASE WHEN STOP_DURATION="0-15 Min" THEN 7.5 
                        WHEN STOP_DURATION="16-30 Min" THEN 23
                        WHEN STOP_DURATION="30+ Min" THEN 35
                        END) AS avg_duration,COUNT(*) AS TOTAL_STOPS
                        FROM POLICE_LOGS
                        GROUP BY VIOLATION
                        ORDER BY violation
                        """,
                        "Are stops during the night more likely to lead to arrests":"""SELECT CASE 
                        WHEN HOUR(STOP_TIME) BETWEEN 5 AND 11 THEN 'MORNING'
                        WHEN HOUR(STOP_TIME) BETWEEN 12 AND 3 THEN 'AFTERNOON'
                        WHEN HOUR(STOP_TIME) BETWEEN 4 AND 7 THEN 'EVENING'
                        ELSE 'NIGHT' END AS TIME_OF_THE_DAY,
                        COUNT(*) AS TOTAL_STOPS,
                        SUM(CASE WHEN IS_ARRESTED=TRUE THEN 1 ELSE 0 END) AS TOTAL_ARREST,
                        ROUND(SUM(CASE WHEN IS_ARRESTED=TRUE THEN 1 ELSE 0 END)*100/COUNT(*),2) AS ARREST_RATE
                        FROM POLICE_LOGS
                        GROUP BY TIME_OF_THE_DAY
                        ORDER BY ARREST_RATE DESC""",
                        "Violations most associated with searches or arrests":"""SELECT VIOLATION,COUNT(*) AS TOTAL_STOPS,
                        SUM(CASE WHEN SEARCH_CONDUCTED= TRUE THEN 1 ELSE 0 END) AS TOTAL_SEARCH,
                        SUM(CASE WHEN IS_ARRESTED= TRUE THEN 1 ELSE 0 END) AS TOTAL_ARREST
                        FROM POLICE_LOGS
                        GROUP BY VIOLATION
                        ORDER BY TOTAL_SEARCH DESC,TOTAL_ARREST DESC""",
                        "Violations most common among younger drivers (<25)":"""SELECT VIOLATION,COUNT(*) AS YOUNG_DRIVERS_COUNT
                        FROM POLICE_LOGS
                        WHERE DRIVER_AGE<25
                        GROUP BY VIOLATION
                        ORDER BY YOUNG_DRIVERS_COUNT DESC
                        LIMIT 1""",
                        "Violation that rarely results in search or arrest":"""SELECT violation,COUNT(*) AS total_stops,
                        SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS total_searches,
                        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests,
                        ROUND(100.0 * (SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) + 
                                        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END)) / COUNT(*), 2) AS combined_rate_percent
                        FROM police_logs
                        GROUP BY violation
                        ORDER BY combined_rate_percent ASC
                        LIMIT 1""",
                        "Countries that report the highest rate of drug-related stops":"""select country_name,count(*) as total_stops,
                        Round(100*sum(case when drugs_related_stop=TRUE then 1 else 0 end)/count(*),2) as drugs_stop_percentage
                        from police_logs
                        group by country_name
                        order by drugs_stop_percentage desc
                        limit 1""",
                        "Arrest rate by country and violation":"""SELECT
                        ROUND(SUM(CASE WHEN IS_ARRESTED= TRUE THEN 1 ELSE 0 END)*100/COUNT(*),2) AS ARREST_RATE,
                        COUNTRY_NAME,VIOLATION,COUNT(*) AS TOTAL_STOPS
                        FROM POLICE_LOGS
                        GROUP BY COUNTRY_NAME,VIOLATION
                        ORDER BY ARREST_RATE DESC""",
                        "Country that has the most stops with search conducted":"""SELECT 
                        COUNTRY_NAME,COUNT(*) AS TOTAL_SEARCH_CONDUCTED_STOPS
                        FROM POLICE_LOGS
                        WHERE SEARCH_CONDUCTED=TRUE
                        GROUP BY COUNTRY_NAME
                        ORDER BY TOTAL_SEARCH_CONDUCTED_STOPS DESC
                        LIMIT 1"""}

# COMPLEX QUERIES

complex_query_map={"Yearly Breakdown of Stops and Arrests by Country":"""SELECT COUNTRY_NAME,YEAR,TOTAL_STOPS,TOTAL_ARREST,
ROUND(100*TOTAL_ARREST/TOTAL_STOPS,2) AS ARREST_RATE,
RANK() OVER(PARTITION BY COUNTRY_NAME ORDER BY YEAR) AS YEAR_RANK
FROM
(SELECT COUNTRY_NAME,YEAR(STOP_DATE) AS YEAR,
COUNT(*) AS TOTAL_STOPS,
SUM(CASE WHEN IS_ARRESTED= TRUE THEN 1 ELSE 0 END) AS TOTAL_ARREST
FROM POLICE_LOGS 
GROUP BY COUNTRY_NAME,YEAR) AS YEAR_DATA
""",
"Driver Violation Trends Based on Age and Race": """
WITH age_grouped AS (
SELECT violation,driver_race,
CASE WHEN driver_age < 18 THEN 'Under 18'
WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
ELSE '60+' 
END AS age_group
FROM police_logs
)
SELECT 
ag.age_group,
ag.driver_race,
ag.violation,
COUNT(*) AS total_violations
FROM age_grouped ag
GROUP BY ag.age_group, ag.driver_race, ag.violation
ORDER BY ag.age_group, total_violations DESC;
""",
"Time Period Analysis of Stops":"""SELECT YEAR(STOP_DATE) AS YEAR, MONTH(STOP_DATE) AS MONTH, HOUR(STOP_TIME) AS HOUR,
COUNT(*) AS TOTAL_STOPS
FROM POLICE_LOGS
GROUP BY YEAR,MONTH,HOUR
ORDER BY YEAR,MONTH,HOUR
""",
"Violations with High Search and Arrest Rates":"""SELECT VIOLATION, COUNT(*) AS TOTAL_STOP,
SUM(CASE WHEN SEARCH_CONDUCTED=TRUE THEN 1 ELSE 0 END) AS TOTAL_SEARCH,
ROUND(SUM(CASE WHEN SEARCH_CONDUCTED=TRUE THEN 1 ELSE 0 END)*100/COUNT(*),2) AS TOTAL_SEARCH_RATE,
RANK() OVER (ORDER BY 1.0 * SUM(CASE WHEN SEARCH_CONDUCTED=TRUE THEN 1 ELSE 0 END)/COUNT(*) DESC) AS search_rank,
SUM(CASE WHEN IS_ARRESTED=TRUE THEN 1 ELSE 0 END) AS TOTAL_ARREST,
ROUND(SUM(CASE WHEN IS_ARRESTED=TRUE THEN 1 ELSE 0 END)*100/COUNT(*),2) AS TOTAL_ARREST_RATE,
RANK() OVER (ORDER BY 1.0 * SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) / COUNT(*) DESC) AS arrest_rank
FROM POLICE_LOGS
GROUP BY VIOLATION
ORDER BY TOTAL_SEARCH_RATE DESC,TOTAL_ARREST_RATE DESC
""",
"Driver Demographics by Country":"""SELECT 
    country_name,
    ROUND(AVG(driver_age), 1) AS avg_age,
    SUM(CASE WHEN driver_gender = 'M' THEN 1 ELSE 0 END) AS male_drivers,
    SUM(CASE WHEN driver_gender = 'F' THEN 1 ELSE 0 END) AS female_drivers,
    COUNT(*) AS total_drivers,
    SUM(CASE WHEN driver_race = 'White' THEN 1 ELSE 0 END) AS white_drivers,
    SUM(CASE WHEN driver_race = 'Black' THEN 1 ELSE 0 END) AS black_drivers,
    SUM(CASE WHEN driver_race = 'Hispanic' THEN 1 ELSE 0 END) AS hispanic_drivers,
    SUM(CASE WHEN driver_race = 'Asian' THEN 1 ELSE 0 END) AS asian_drivers,
    SUM(CASE WHEN driver_race NOT IN ('White','Black','Hispanic','Asian') THEN 1 ELSE 0 END) AS other_race
FROM police_logs
GROUP BY country_name
ORDER BY country_name
""",
"Top 5 Violations with Highest Arrest Rates":"""SELECT VIOLATION,COUNT(*) AS TOTAL_STOPS,
round(100*sum(case when IS_ARRESTED=TRUE then 1 else 0 end)/COUNT(*),2) AS ARREST_RATE
FROM POLICE_LOGS
GROUP BY VIOLATION
ORDER BY ARREST_RATE DESC
LIMIT 5
"""
}


st.header("📊 Advanced Police Stop Data Insights")

left_col, right_col = st.columns(2)

# Medium-Level Query Panel
with left_col:
    st.subheader("📘 Medium-Level Queries")
    medium_selected = st.selectbox("Select a Medium Query", list(medium_query_map.keys()))
    if st.button("Run Medium Query"):
        df = get_data(medium_query_map[medium_selected])
        st.dataframe(df, use_container_width=True)

        if "Vehicle_Number" in df.columns and "drug_stop_count" in df.columns:
            fig = px.bar(df, x='Vehicle_Number', y='drug_stop_count', title='Top 10 Vehicles in Drug-Related Stops')
            st.plotly_chart(fig, use_container_width=True,key=fig.layout.title.text)
        elif "Vehicle_Number" in df.columns and "search_count" in df.columns:
           fig = px.bar(df, x='Vehicle_Number', y='search_count', title='Most Frequently Searched Vehicles')
           st.plotly_chart(fig, use_container_width=True,key=fig.layout.title.text)
        elif "driver_age_group" in df.columns:
           st.metric(
            label="Highest Arrest Rate Age Group",
            value=df["driver_age_group"].iloc[0],
            delta=f"{df['ARREST_RATE'].iloc[0]:.2f}%"
            )
        elif "driver_gender" in df.columns and "country_name"in df.columns:
            fig = px.bar(df, x='country_name', y='total_stop_count', color='driver_gender',barmode='group', title='Gender Distribution of Drivers by Country')
            st.plotly_chart(fig, use_container_width=True,key=fig.layout.title.text)
        elif "driver_race" in df.columns and "driver_gender" in df.columns and "search_rate" in df.columns:
             st.metric(
                  label="Highest search rate for Race and gender combination",
                  value=f"{df["driver_race"].iloc[0]} - {df["driver_gender"].iloc[0]}",
                  delta=f"{float(df["search_rate"].iloc[0])}%"
             )
        elif "time_of_day" in df.columns and "total_stops" in df.columns:
             st.metric(
                  label="Time of day with most traffic stops",
                  value=df["time_of_day"].iloc[0],
                  delta=int(df["total_stops"].iloc[0])
             )
        elif "violation" in df.columns and "avg_duration" in df.columns:
             fig=px.bar(df,x='violation',y='avg_duration',title='Average stop duration for each violation(Minutes)')
             st.plotly_chart(fig,use_container_width=True,key=fig.layout.title.text)
        elif "TIME_OF_THE_DAY" in df.columns and "ARREST_RATE" in df.columns and "TOTAL_ARREST" in df.columns:
            fig = px.bar(df, x='TIME_OF_THE_DAY', y='ARREST_RATE',title='Arrest Rate by Time of Day (%)', color='TIME_OF_THE_DAY')
            st.plotly_chart(fig,use_container_width=True,key=fig.layout.title.text)
        elif "VIOLATION" in df.columns and "TOTAL_SEARCH" in df.columns and "TOTAL_ARREST" in df.columns:
           fig = px.bar(df, x='VIOLATION', y=['TOTAL_SEARCH', 'TOTAL_ARREST'],title='Search and Arrest Counts per Violation', barmode='group')
           st.plotly_chart(fig)
        elif "YOUNG_DRIVERS_COUNT" in df.columns:
             st.metric(
                  label="Violations most common among younger drivers (<25)",
                  value=df["VIOLATION"].iloc[0],
                  delta=int(df["YOUNG_DRIVERS_COUNT"].iloc[0])
             )
             
        elif "combined_rate_percent" in df.columns:
            st.metric(
                  label="Violations that rarely results in search or arrest",
                  value=df["violation"].iloc[0],
                  delta=f"{(df["combined_rate_percent"].iloc[0]):.2f}%"
             )
        elif "country_name" in df.columns and  "drugs_stop_percentage" in df.columns and "total_stops" in df.columns:
             st.metric(
                  label="Country reporting the highest rate of drug-related stops",
                  value=df["country_name"].iloc[0],
                  delta=f"{(df["drugs_stop_percentage"].iloc[0]):.2f}%"
             )
        elif "COUNTRY_NAME" in df.columns and  "VIOLATION" in df.columns and "ARREST_RATE" in df.columns:
                fig = px.bar(df, x='COUNTRY_NAME', y='ARREST_RATE',color='VIOLATION', title='Arrest Rate by Country and Violation')
                st.plotly_chart(fig,key=fig.layout.title.text)
        elif "TOTAL_SEARCH_CONDUCTED_STOPS" in df.columns:
             st.metric(
                  label="Country having most stops with search conducted",
                  value=df["COUNTRY_NAME"].iloc[0],
                  delta=int(df["TOTAL_SEARCH_CONDUCTED_STOPS"].iloc[0])
             )
        

  # Complex-Level Query Panel
with right_col:
    st.subheader("📙 Complex-Level Queries")
    complex_selected = st.selectbox("Select a Complex Query", list(complex_query_map.keys()))
    if st.button("Run Complex Query"):
        df = get_data(complex_query_map[complex_selected])
        st.dataframe(df, use_container_width=True)

        if "YEAR" in df.columns and "TOTAL_STOPS" in df.columns and "TOTAL_ARREST" in df.columns:
                fig = px.line(df, x="YEAR", y="TOTAL_STOPS", color="COUNTRY_NAME",
                              title="Stops Over Time by Country")
                st.plotly_chart(fig, use_container_width=True,key=fig.layout.title.text)
        elif "age_group" in df.columns:
                fig = px.bar(df, x="violation", y="total_violations", color="age_group",
                             title="Violations by Age Group")
                st.plotly_chart(fig, use_container_width=True,key=fig.layout.title.text)
                fig = px.bar(df, x="violation", y="total_violations", color="driver_race",
                             title="Violations by Race")
                st.plotly_chart(fig, use_container_width=True,key=fig.layout.title.text)
        elif "MONTH" in df.columns:
                fig = px.line(df, x="MONTH", y="TOTAL_STOPS", color="YEAR",
                              title="Monthly Stop Trends")
                st.plotly_chart(fig, use_container_width=True,key=fig.layout.title.text)
        elif "VIOLATION" in df.columns and "TOTAL_SEARCH_RATE" in df.columns:
                fig = px.bar(df, x="VIOLATION", y="TOTAL_ARREST_RATE",color="TOTAL_SEARCH_RATE",
                             title="Violations with High Arrest/Search Rates")
                st.plotly_chart(fig, use_container_width=True,key=fig.layout.title.text)
        elif "country_name" in df.columns and "avg_age" in df.columns:
                fig = px.bar(df, x="country_name", y="total_drivers", title="Total drivers per Country")
                st.plotly_chart(fig, use_container_width=True,key=fig.layout.title.text)
            
        else:
                fig = px.bar(df, x=df.columns[0], y=df.columns[2])
                st.plotly_chart(fig, use_container_width=True,key=fig.layout.title.text)

      


    
#User Form to input information for prediction
st.header("🚓 SecureCheck: Stop Outcome & Violation Predictor")
with st.form("📝checkpost_form"):
     st.subheader("🚦Enter Stop Details")

     Stop_Date = st.date_input("Stop Date")
     Stop_time = st.time_input("Stop Time")
     formatted_time = Stop_time.strftime("%H:%M:%S")
     Country_name = st.text_input("Country Name")
     Driver_gender = st.selectbox("Driver Gender", ["M", "F"])
     Driver_age = st.number_input("Driver Age", min_value=18, max_value=100, value=25)
     Driver_race = st.text_input("Driver Race")
     Search_conducted = st.selectbox("Search Conducted", ["0", "1"])
     Search_type = st.text_input("Search Type")
     is_arrested = st.selectbox("Is Arrested", ["0", "1"])
     
    
    #To Make sure stop_duration values are available and valid
     if not data['Stop_duration'].dropna().empty:
        Stop_duration = st.selectbox("Stop_duration", sorted(data['Stop_duration'].dropna().unique()))
     else:
        Stop_duration = ""

     Drugs_related_stop = st.selectbox("Drugs Related Stop", ["0", "1"])
     Vehicle_Number = st.text_input("Vehicle Number")

     submitted = st.form_submit_button("Predict Stop Outcome and Violation")

    # Prediction Logic After Form Submission
     filtered_data = pd.DataFrame()
     if submitted:
      
    # Filter matching or similar data
      filtered_data = data[
        (data['Search_conducted'] == int(Search_conducted)) &
        (data['Driver_age'] == int(Driver_age)) &
        (data['Driver_gender'] == Driver_gender) &
        (data['Stop_duration'] == Stop_duration) &
        (data['Drugs_related_stop'] == int(Drugs_related_stop))
    ]
      

    # Get predicted values
     if not filtered_data.empty:
        predicted_outcome = filtered_data['Stop_outcome'].mode()[0]
        predicted_violation = filtered_data['Violation'].mode()[0]
     else:
        predicted_outcome = "Warning"
        predicted_violation = "Speeding"
     st.subheader("Filtered-data for prediction:")
     st.write(filtered_data)
    

    #Interpret Other Flags

     search_result = "A search was conducted" if int(Search_conducted) else "No search was conducted"
     drug_result = "was drug related." if int(Drugs_related_stop) else "was not drug related."
     if Driver_gender=="M":
          Driver_gender="Male"
     else:
          Driver_gender="Female"
        

    #Prediction Summary
     st.markdown(f"""
    ### 🔍 Prediction Summary

    🚗 A **{Driver_age}-year-old {Driver_gender.lower()}** driver was stopped for **{predicted_violation}** at **{Stop_time}**.  
    {search_result},and he received a **{predicted_outcome}**. 
    The stop lasted for **{Stop_duration}**  and **{drug_result}**  
    **Predicted violation:** {predicted_violation}  
    **Vehicle Number:** {Vehicle_Number}  
    **Predicted Outcome:** {predicted_outcome}  
""")
  