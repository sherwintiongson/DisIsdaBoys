import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# PWM + System Parameters
# -------------------------------
PWM_PERIOD = 200              # Timer auto-reload value
SWITCHING_FREQ = 40000        # Desired PWM switching frequency (Hz)
SINE_FREQ = 50                # Output sine frequency (Hz)
MOD_INDEX = 0.8               # Amplitude control (0 to 1)
SIM_TIME = 0.1                # seconds

# For center-aligned PWM:
# f_switch = f_timer / (2 * PWM_PERIOD)
TIMER_CLOCK = 2 * PWM_PERIOD * SWITCHING_FREQ
dt = 1 / TIMER_CLOCK

# -------------------------------
# Center-aligned timer
# -------------------------------
class CenterAlignedTimer:
    def __init__(self, period):
        self.period = period
        self.counter = 0
        self.direction = 1

    def tick(self):
        value = self.counter
        self.counter += self.direction

        if self.counter >= self.period:
            self.direction = -1
        elif self.counter <= 0:
            self.direction = 1

        return value

timer = CenterAlignedTimer(PWM_PERIOD)

# -------------------------------
# 2nd Order Low-Pass Filter
# Cutoff ~ 1 kHz (well below 40kHz, well above 50Hz)
# -------------------------------
FC = 1000
RC = 1 / (2 * np.pi * FC)
alpha = dt / (RC + dt)

filter1 = 0
filter2 = 0

# -------------------------------
# Storage arrays
# -------------------------------
time_values = []
filtered_values = []
sine_reference = []

# -------------------------------
# Simulation loop
# -------------------------------
t = 0
num_steps = int(SIM_TIME * TIMER_CLOCK)

for _ in range(num_steps):

    # 1. Scaled sine reference (modulation index applied)
    sine = MOD_INDEX * np.sin(2 * np.pi * SINE_FREQ * t)
    sine_reference.append(sine)

    # Convert to 0..1 for PWM compare
    duty = 0.5 + 0.5 * sine

    compare = duty * PWM_PERIOD

    # 2. Timer tick
    counter = timer.tick()

    # 3. PWM output (single channel differential model)
    pwm = 1 if counter < compare else -1

    # 4. 2nd order low-pass filter
    filter1 += alpha * (pwm - filter1)
    filter2 += alpha * (filter1 - filter2)

    # 5. Store
    time_values.append(t)
    filtered_values.append(filter2)

    t += dt

# -------------------------------
# Plot result
# -------------------------------
plt.figure(figsize=(10, 6))
plt.plot(time_values, filtered_values, label="Filtered Output")
plt.plot(time_values, sine_reference, linestyle="--", label="Ideal Sine")
plt.title(f"SPWM Output (Modulation Index = {MOD_INDEX})")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()