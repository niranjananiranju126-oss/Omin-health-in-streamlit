# Omin-health-in-streamlit
import streamlit as st

# Set page title and layout
st.set_page_config(page_title="Simple Health Checker", layout="wide")
st.title("🌟 Personal Health Dashboard")
st.write("Answer these simple questions to get your personalized health tips!")

# Use a form to collect all inputs at once
with st.form("health_check_form"):
    st.header("📋 Daily Health Questions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💧 1. Hydration & Activity")
        u_water = st.number_input("How much water did you drink? (Liters)", 0.0, 10.0, 2.0)
        u_activity = st.selectbox("How active were you today?", ["Low", "Medium", "High"])
        temp_env = st.selectbox("How is the temperature around you?", ["Cool (AC/Pleasant)", "Warm (Room Temp)", "Hot (Outdoors)"])
        
        st.subheader("🏥 3. Daily Vitality")
        u_sleep = st.number_input("How many hours did you sleep last night?", 0.0, 15.0, 7.0)
        u_battery = st.select_slider("How does your 'Mental Battery' feel?", options=["Low", "Half", "Full"], value="Half")
        had_mistakes = st.checkbox("Have you been making 'silly mistakes' or typos lately?")

    with col2:
        st.subheader("👀 2. Eye Stress")
        u_screen_time = st.slider("Total hours spent on phone or computer?", 0.0, 24.0, 6.0)
        u_strain = st.radio("Are your eyes feeling red or tired?", ["No", "Yes"])
        
        st.subheader("🌿 4. Stress Check-in")
        st.write("Check any that apply to you:")
        tight_muscles = st.checkbox("My shoulders or neck feel tight")
        long_work = st.checkbox("I've been working for more than 2 hours")
        overwhelmed = st.checkbox("I feel overwhelmed right now")

    # The submit button for the form
    submit_button = st.form_submit_button(label="Analyze My Health")

# --- ANALYSIS SECTION (Runs only after clicking the button) ---
if submit_button:
    st.divider()
    st.header("✅ Your Health Results")
    res_col1, res_col2 = st.columns(2)

    # 1. Hydration Analysis Logic
    base_target = 2.5
    if u_activity == 'High': base_target += 0.5
    if "Hot" in temp_env: base_target += 0.5
    elif "Warm" in temp_env: base_target += 0.2
    
    h_status = "Hydrated" if u_water >= base_target else "Mildly Dehydrated" if u_water >= (base_target - 0.5) else "Dehydrated"
    
    with res_col1:
        st.metric("Hydration Status", h_status, f"{round(u_water - base_target, 1)}L vs Goal")
        if h_status != "Hydrated":
            st.info(f"💡 Suggestion: Try to drink more to reach {round(base_target, 1)}L.")

    # 2. Eye Stress Analysis Logic
    with res_col2:
        if u_strain == "Yes" or u_screen_time > 6.0:
            st.error("👀 Eye Warning: Your eyes need a rest!")
            st.write("💡 Relief: Follow the **20-20-20 rule** (Look 20ft away every 20 mins).")
        else:
            st.success("👀 Eye Health: Your screen habits look good!")

    # 3. Vitality & Stress Logic
    st.write("---")
    vital_col, stress_col = st.columns(2)
    
    with vital_col:
        s_sleep = "Rested" if u_sleep >= 7 else "Sleep Deprived"
        st.write(f"**Sleep Status:** {s_sleep} ({u_sleep} hrs)")
        if u_battery == "Low" or had_mistakes:
            st.warning("⚠️ Battery Low: Take a break to recharge your focus.")

    with stress_col:
        stress_points = sum([tight_muscles, long_work, overwhelmed])
        s_stress = "High" if stress_points >= 2 else "Low"
        st.write(f"**Stress Level:** {s_stress}")
        if s_stress == "High":
            st.error("💡 Stress Tip: Close your eyes and take 3 deep breaths.")

    st.balloons()
    # --- PRINT HARD COPY SECTION ---
    st.write("---")
    if st.button("🖨️ Click Here to Print Your Hard Copy"):
        # This opens the browser's print window for the user
        st.components.v1.html("""
            <script>
                window.print();
            </script>
        """, height=0)
