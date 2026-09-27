
import streamlit as st
import requests

st.title("Lead Conversion Prediction App")

st.write(
    "This app predicts whether a lead is likely to be converted "
    "based on the lead's demographic and interaction details."
)

st.write(
    "Enter the lead details below and click Predict "
    "to get the prediction."
)

# Numerical Features
age = st.slider("Age", 18, 63, 45, 1)

website_visits = st.slider(
    "Website Visits", 0, 30, 3, 1
)

time_spent_on_website = st.slider(
    "Time Spent on Website (seconds)",
    0, 2537, 376, 1
)

page_views_per_visit = st.slider(
    "Page Views per Visit",
    0.0, 18.5, 2.8, 0.1
)

# Categorical Features
current_occupation = st.selectbox(
    "Current Occupation",
    ["Professional", "Unemployed", "Student"]
)

first_interaction = st.selectbox(
    "First Interaction",
    ["Website", "Mobile App"]
)

profile_completed = st.selectbox(
    "Profile Completed",
    ["High", "Medium", "Low"]
)

last_activity = st.selectbox(
    "Last Activity",
    ["Email Activity", "Phone Activity", "Website Activity"]
)

print_media_type1 = st.selectbox(
    "Print Media Type 1",
    ["No", "Yes"]
)

print_media_type2 = st.selectbox(
    "Print Media Type 2",
    ["No", "Yes"]
)

digital_media = st.selectbox(
    "Digital Media",
    ["No", "Yes"]
)

educational_channels = st.selectbox(
    "Educational Channels",
    ["No", "Yes"]
)

referral = st.selectbox(
    "Referral",
    ["No", "Yes"]
)

# Create input data
input_data = {
    "age": age,
    "website_visits": website_visits,
    "time_spent_on_website": time_spent_on_website,
    "page_views_per_visit": page_views_per_visit,
    "current_occupation": current_occupation,
    "first_interaction": first_interaction,
    "profile_completed": profile_completed,
    "last_activity": last_activity,
    "print_media_type1": print_media_type1,
    "print_media_type2": print_media_type2,
    "digital_media": digital_media,
    "educational_channels": educational_channels,
    "referral": referral
}

# Prediction
if st.button("Predict Lead Conversion", type="primary"):

    try:

        api_url = "https://<your-space-name>.hf.space/v1/predict"

        response = requests.post(
            api_url,
            json=input_data
        )

        if response.status_code == 200:

            result = response.json()

            if result["prediction"] == 1:

                st.success(
                    "Lead Conversion Prediction: Converted"
                )

            else:

                st.info(
                    "Lead Conversion Prediction: Not Converted"
                )

        else:

            st.error(
                f"Error in API request: {response.text}"
            )

    except Exception as e:

        st.error(
            f"Unable to connect to API: {str(e)}"
        )
