import streamlit as st
import pandas as pd
import numpy as np
import math as m
import matplotlib.pyplot as plt
from PIL import Image

# Set matplotlib backend
plt.switch_backend('Agg')

st.header("Advanced corrodeD pipe structurAl integrity systeM (ADAM)")

st.subheader('Dimensional Parameters')
htp = "https://www.researchgate.net/profile/Changqing-Gong/publication/313456917/figure/fig1/AS:573308992266241@1513698923813/Schematic-illustration-of-the-geometry-of-a-typical-corrosion-defect.png"
st.image(htp, caption="Fig. 1: Schematic illustration of the geometry of a typical corrosion defect.")

st.sidebar.header('User Input Parameters')

def user_input_features():
    pipe_thickness = st.sidebar.number_input('Pipe Thickness, t (mm)', value=10.0)
    pipe_diameter = st.sidebar.number_input('Pipe Diameter, D (mm)', value=500.0)
    pipe_length = st.sidebar.number_input('Pipe Length, L (mm)', value=1000.0)
    corrosion_length = st.sidebar.number_input('Corrosion Length, Lc (mm)', value=50.0)
    corrosion_depth = st.sidebar.number_input('Corrosion Depth, Dc (mm)', value=2.0)
    Sy = st.sidebar.number_input('Yield Stress, Sy (MPa)', value=358.0)
    UTS = st.sidebar.number_input('Ultimate Tensile Strength, UTS (MPa)', value=455.0)
    Maximum_Operating_Pressure = st.sidebar.slider('Maximum Operating Pressure, Pop, Max (MPa)', min_value=0, max_value=50, value=10)
    Minimum_Operating_Pressure = st.sidebar.slider('Minimum Operating Pressure, Pop, Min (MPa)', min_value=0, max_value=50, value=5)

    data = {'t (mm)': pipe_thickness,
            'D (mm)': pipe_diameter,
            'L (mm)': pipe_length,
            'Lc (mm)': corrosion_length,
            'Dc (mm)': corrosion_depth,           
            'UTS (MPa)': UTS,
            'Sy (MPa)': Sy,
            'Pop_Max (MPa)': Maximum_Operating_Pressure,
            'Pop_Min (MPa)': Minimum_Operating_Pressure}
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

t = df['t (mm)'].values.item()
D = df['D (mm)'].values.item()
L = df['L (mm)'].values.item()
Lc = df['Lc (mm)'].values.item()
Dc = df['Dc (mm)'].values.item()
UTS = df['UTS (MPa)'].values.item()
Sy = df['Sy (MPa)'].values.item()
Pop_Max = df['Pop_Max (MPa)'].values.item()
Pop_Min = df['Pop_Min (MPa)'].values.item()

st.subheader('Nomenclature')
st.write('t is the pipe thickness; D is the pipe diameter; L is the pipe length; Lc is the corrosion length; Dc is the corrosion depth; Sy is the pipe material yield stress; UTS is the pipe material Ultimate Tensile Strength.')

# Calculate burst pressures
Pvm = 4 * t * UTS / (m.sqrt(3) * D)
PTresca = 2 * t * UTS / D
M = m.sqrt(1 + 0.8 * (L / (m.sqrt(D * t))))

if L < m.sqrt(20 * D * t):
    P_ASME_B31G = (2 * t * UTS / D) * (1 - (2/3) * (Dc / t) / (1 - (2/3) * (Dc / t) / M)
else:
    P_ASME_B31G = (2 * t * UTS / D) * (1 - (Dc / t))

Q = m.sqrt(1 + 0.31 * (Lc)**2 / (D * t))
P_DnV = (2 * UTS * t / (D - t)) * ((1 - (Dc / t)) / (1 - (Dc / (t * Q))))
P_PCORRC = (2 * t * UTS / D) * (1 - Dc / t)

# Display user inputs
user_input = {
    't (mm)': f"{t:.2f}",
    'D (mm)': f"{D:.2f}",
    'L (mm)': f"{L:.2f}",
    'Lc (mm)': f"{Lc:.2f}",
    'Dc (mm)': f"{Dc:.2f}",
    'UTS (MPa)': f"{UTS:.2f}",
    'Sy (MPa)': f"{Sy:.2f}",
    'Pop_Max (MPa)': f"{Pop_Max:.2f}",
    'Pop_Min (MPa)': f"{Pop_Min:.2f}"
}
user_input_df = pd.DataFrame(user_input, index=[0])
st.subheader('User Input Parameters')
st.write(user_input_df)

# Display burst pressures
st.subheader('Calculated Intact Pipe Burst Pressure via Von Mises')
st.write(pd.DataFrame({'Pvm (MPa)': [f"{Pvm:.2f}"]}))

st.subheader('Calculated Corroded Pipe Burst Pressure via ASME_B31G')
st.write(pd.DataFrame({'P_ASME_B31G (MPa)': [f"{P_ASME_B31G:.2f}"]}))

st.subheader('Calculated Corroded Pipe Burst Pressure via DnV')
st.write(pd.DataFrame({'P_DnV (MPa)': [f"{P_DnV:.2f}"]}))

st.subheader('Calculated Corroded Pipe Burst Pressure via PCORRC')
st.write(pd.DataFrame({'P_PCORRC (MPa)': [f"{P_PCORRC:.2f}"]}))

# Stress calculations
P1max = Pop_Max * D / (2 * t)
P2max = Pop_Max * D / (4 * t)
P3max = 0

P1min = Pop_Min * D / (2 * t)
P2min = Pop_Min * D / (4 * t)
P3min = 0

Sigma_VM_Pipe_Max_Operating_Pressure = (1/m.sqrt(2)) * m.sqrt((P1max-P2max)**2 + (P2max-P3max)**2 + (P3max-P1max)**2)
Sigma_VM_Pipe_Min_Operating_Pressure = (1/m.sqrt(2)) * m.sqrt((P1min-P2min)**2 + (P2min-P3min)**2 + (P3min-P1min)**2)

sigma_a = (Sigma_VM_Pipe_Max_Operating_Pressure - Sigma_VM_Pipe_Min_Operating_Pressure) / 2
sigma_m = (Sigma_VM_Pipe_Max_Operating_Pressure + Sigma_VM_Pipe_Min_Operating_Pressure) / 2
Se = 0.5 * UTS
sigma_f = UTS + 345

# Fatigue criteria calculations
Goodman_Value = (sigma_a / Se) + (sigma_m / UTS)
Soderberg_Value = (sigma_a / Se) + (sigma_m / Sy)
Gerber_Value = (sigma_a / Se) + ((sigma_m / UTS) ** 2)
Morrow_sigma_a_allow = Se * (1 - sigma_m / sigma_f)
Morrow_Value = (sigma_a / Se) + (sigma_m / sigma_f)

# Display stress parameters
st.subheader('Fatigue Stress Parameters')
st.write(pd.DataFrame({
    'Alternating Stress, σa (MPa)': [f"{sigma_a:.2f}"],
    'Mean Stress, σm (MPa)': [f"{sigma_m:.2f}"],
    'Endurance Limit, Se (MPa)': [f"{Se:.2f}"]
}))

# Display fatigue criteria
st.subheader('Fatigue Failure Assessment')
st.write(pd.DataFrame({
    'Goodman Value': [f"{Goodman_Value:.3f}"],
    'Soderberg Value': [f"{Soderberg_Value:.3f}"],
    'Gerber Value': [f"{Gerber_Value:.3f}"],
    'Allowable σₐ (Morrow) (MPa)': [f"{Morrow_sigma_a_allow:.2f}"]
}))

# Goodman Diagram
plt.close('all')
fig, ax = plt.subplots(figsize=(10, 6))

sigma_m_values = np.linspace(0, UTS, 100)
goodman_line = Se * (1 - sigma_m_values / UTS)
soderberg_line = Se * (1 - sigma_m_values / Sy)
gerber_line = Se * (1 - (sigma_m_values / UTS) ** 2)

ax.plot(sigma_m_values, goodman_line, label='Goodman Line', color='blue')
ax.plot(sigma_m_values, soderberg_line, label='Soderberg Line', color='green')
ax.plot(sigma_m_values, gerber_line, label='Gerber Parabola', color='red')

ax.scatter(sigma_m, sigma_a, color='red', s=100, label='Current Operating Point', zorder=5)

ax.axhline(y=Se, color='gray', linestyle='--', label='Endurance Limit (Se)')
ax.axvline(x=UTS, color='orange', linestyle='--', label='Ultimate Strength (UTS)')
ax.axvline(x=Sy, color='purple', linestyle='--', label='Yield Strength (Sy)')

ax.set_xlim(0, UTS * 1.1)
ax.set_ylim(0, Se * 1.2)
ax.set_xlabel('Mean Stress (σm) [MPa]')
ax.set_ylabel('Alternating Stress (σa) [MPa]')
ax.set_title('Modified Goodman Diagram')
ax.grid(True)
ax.legend()

st.subheader('Modified Goodman Diagram')
st.pyplot(fig)

# Display diagram data
st.subheader('Diagram Data Points')
diagram_data = pd.DataFrame({
    'Mean Stress (MPa)': sigma_m_values,
    'Goodman Line (MPa)': goodman_line,
    'Soderberg Line (MPa)': soderberg_line,
    'Gerber Parabola (MPa)': gerber_line
})
st.write(diagram_data)

# References
st.subheader('Reference')
st.write('Xian-Kui Zhu, A comparative study of burst failure models for assessing remaining strength of corroded pipelines, Journal of Pipeline Science and Engineering 1 (2021) 36 - 50, https://doi.org/10.1016/j.jpse.2021.01.008')

st.subheader('Assessment')
st.markdown('[Case Study](https://drive.google.com/file/d/1Ako5uVRPYL5k5JeEQ_Xhl9f3pMRBjCJv/view?usp=sharing)', unsafe_allow_html=True)
st.markdown('[Corroded Pipe Burst Data](https://docs.google.com/spreadsheets/d/1YJ7ziuc_IhU7-MMZOnRmh4h21_gf6h5Z/edit?gid=56754844#gid=56754844)', unsafe_allow_html=True)
st.markdown('[Pre-Test](https://forms.gle/wPvcgnZAC57MkCxN8)', unsafe_allow_html=True)
st.markdown('[Post-Test](https://forms.gle/FdiKqpMLzw9ENscA9)', unsafe_allow_html=True)
