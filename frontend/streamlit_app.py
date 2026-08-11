import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Genesis Disaster Response", layout="wide")
st.title("Genesis — Disaster Response Orchestrator")

for key in ["thread_id", "result", "final_result"]:
    if key not in st.session_state:
        st.session_state[key] = None

situation = st.text_area("Describe the situation", placeholder="e.g. Severe flooding reported in Assam, India")
image_file = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])

if st.button("Run Incident"):
    image_path = None
    if image_file:
        image_path = f"uploaded_{image_file.name}"
        with open(image_path, "wb") as f:
            f.write(image_file.getbuffer())

    response = requests.post(f"{API_URL}/incidents", json={"situation": situation, "image_path": image_path})
    if response.status_code == 200:
        st.session_state.result = response.json()
        st.session_state.final_result = None
    else:
        st.error(f"Error: {response.text}")

if st.session_state.result:
    result = st.session_state.result

    st.subheader("Alert Classification")
    st.json(result["alert_info"])

    st.subheader("Image Findings")
    st.json(result["image_findings"])

    st.subheader("Response Plan")
    plan = result["response_plan"]
    for phase in ["immediate", "short_term", "recovery"]:
        st.markdown(f"**{phase.replace('_', ' ').title()}**")
        st.write(plan.get(phase, ""))

    st.subheader("Quality Check")
    st.json(result["quality_result"])

    if result.get("location_coords"):
        st.subheader("Incident Location")
        st.map(pd.DataFrame([result["location_coords"]]))

    if st.session_state.final_result is None:
        st.subheader("Approval Required")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Approve & Dispatch"):
                resp = requests.post(f"{API_URL}/incidents/{result['thread_id']}/approve", json={"approved": True})
                st.session_state.final_result = resp.json()
        with col2:
            if st.button("Reject"):
                resp = requests.post(f"{API_URL}/incidents/{result['thread_id']}/approve", json={"approved": False})
                st.session_state.final_result = resp.json()

if st.session_state.final_result:
    st.subheader("Execution Result")
    exec_result = st.session_state.final_result["execution_result"]
    st.json(exec_result)

    hospital_coords = next(
        (e["nearest_hospital"] for e in exec_result.get("log", []) if e.get("nearest_hospital")), None
    )
    if hospital_coords and result.get("location_coords"):
        st.subheader("Route to Nearest Hospital")
        st.map(pd.DataFrame([
            {"lat": result["location_coords"]["lat"], "lon": result["location_coords"]["lon"]},
            {"lat": hospital_coords["lat"], "lon": hospital_coords["lon"]},
        ]))
        st.write(f"Nearest hospital: {hospital_coords.get('name')} — "
                 f"{hospital_coords.get('distance_km', 'N/A')} km, {hospital_coords.get('duration_min', 'N/A')} min")