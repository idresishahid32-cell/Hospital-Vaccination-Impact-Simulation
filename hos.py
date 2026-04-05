import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🏥 Hospital Vaccination Impact Simulation")

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("Simulation Parameters")

N = st.sidebar.slider("Population", 500, 5000, 2000)
beta = st.sidebar.slider("Infection Rate (β)", 0.1, 1.0, 0.35)
gamma = st.sidebar.slider("Recovery Rate (γ)", 0.05, 0.5, 0.1)
nu = st.sidebar.slider("Vaccination Rate (ν)", 0.0, 0.2, 0.02)
epsilon = st.sidebar.slider("Vaccine Effectiveness (ε)", 0.0, 1.0, 0.85)
days = st.sidebar.slider("Days", 30, 200, 120)

hospital_capacity = st.sidebar.slider("Hospital Capacity", 50, 500, 150)

# -----------------------------
# INITIAL VALUES
# -----------------------------
S = [N - 100]
I = [100]
R = [0]
V = [0]

# -----------------------------
# SIMULATION
# -----------------------------
for t in range(days):
    s, i, r, v = S[-1], I[-1], R[-1], V[-1]
    
    # Dynamic intervention
    if i > hospital_capacity:
        beta_eff = beta * 0.6
        nu_eff = nu + 0.05
    else:
        beta_eff = beta
        nu_eff = nu

    new_vaccinated = nu_eff * s
    new_infected_S = beta_eff * s * i / N
    new_infected_V = beta_eff * (1 - epsilon) * v * i / N
    new_recovered = gamma * i

    S.append(s - new_infected_S - new_vaccinated)
    I.append(i + new_infected_S + new_infected_V - new_recovered)
    R.append(r + new_recovered)
    V.append(v + new_vaccinated - new_infected_V)

# -----------------------------
# HERD IMMUNITY
# -----------------------------
R0 = beta / gamma
herd_threshold = 1 - (1 / R0)

st.subheader(f"📊 R₀: {R0:.2f}")
st.subheader(f"🛡️ Herd Immunity Threshold: {herd_threshold*100:.2f}%")

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots()

ax.plot(S, label="Susceptible")
ax.plot(I, label="Infected")
ax.plot(R, label="Recovered")
ax.plot(V, label="Vaccinated")

ax.axhline(y=hospital_capacity, linestyle='--', label="Hospital Capacity")

ax.set_xlabel("Days")
ax.set_ylabel("Population")
ax.set_title("Simulation Graph")
ax.legend()

st.pyplot(fig)

# -----------------------------
# WARNING
# -----------------------------
if max(I) > hospital_capacity:
    st.error("⚠️ Hospital Overloaded during simulation!")
else:
    st.success("✅ Hospital capacity maintained.")