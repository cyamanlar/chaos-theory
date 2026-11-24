"""
Chaos, Sensitive Dependence on Initial Conditions and Noise Reduction
Author: Cansu Yamanlar

1) Logistic map: sensitive dependence on initial conditions + Lyapunov exponent
2) Lorenz (1963) system: two runs with initial conditions differing by 1e-6
3) Noise reduction in the frequency domain: harmonic analysis of a noisy
   monthly temperature series (keep first k harmonics, drop the rest)

Run:  python chaos_noise_demo.py      -> prints results, saves figures/ *.png
Requires: numpy, matplotlib, scipy
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

os.makedirs("figures", exist_ok=True)

# ---------------------------------------------------------------- 1. Logistic map
def logistic(x0, r=4.0, n=25):
    x = np.empty(n + 1)
    x[0] = x0
    for i in range(n):
        x[i + 1] = r * x[i] * (1 - x[i])
    return x

x = logistic(0.3)
y = logistic(0.3001)
diff = np.abs(x - y)

print("n    x_n        y_n        |x_n - y_n|")
for n in range(16):
    print(f"{n:<4d} {x[n]:.6f}   {y[n]:.6f}   {diff[n]:.6f}")

# Lyapunov exponent: lambda = mean(ln|f'(x_n)|), f'(x) = r(1 - 2x)
xl = logistic(0.3, n=100_000)[1000:]          # discard transient
lam = np.mean(np.log(np.abs(4 * (1 - 2 * xl))))
print(f"\nEstimated Lyapunov exponent = {lam:.4f}  (theory: ln 2 = {np.log(2):.4f})")

d0, Delta = 1e-4, 0.5
T = np.log(Delta / d0) / np.log(2)
print(f"Predictability horizon T = ln(Delta/d0)/lambda = {T:.2f} iterations")

plt.figure(figsize=(8, 4))
plt.semilogy(diff[:21], "o-", label="|x_n - y_n|")
plt.semilogy(np.minimum(d0 * 2.0 ** np.arange(21), 1), "--", label=r"$\delta_0 2^n$")
plt.axhline(Delta, ls=":", c="gray")
plt.xlabel("iteration n"); plt.ylabel("absolute difference")
plt.title("Logistic map (r = 4): sensitive dependence on initial conditions")
plt.legend(); plt.tight_layout(); plt.savefig("figures/logistic_error_growth.png", dpi=150)

# ---------------------------------------------------------------- 2. Lorenz system
def lorenz(t, s, sigma=10.0, rho=28.0, beta=8 / 3):
    X, Y, Z = s
    return [sigma * (Y - X), X * (rho - Z) - Y, X * Y - beta * Z]

t = np.linspace(0, 40, 8000)
a = solve_ivp(lorenz, (0, 40), [1.0, 1.0, 1.0], t_eval=t, rtol=1e-10, atol=1e-12)
b = solve_ivp(lorenz, (0, 40), [1.0 + 1e-6, 1.0, 1.0], t_eval=t, rtol=1e-10, atol=1e-12)
sep = np.linalg.norm(a.y - b.y, axis=0)
i_div = np.argmax(sep > 1.0)
print(f"\nLorenz: runs differing by 1e-6 separate by > 1 unit at t = {t[i_div]:.1f}")

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(t, a.y[0], lw=0.8, label="x0 = 1")
ax[0].plot(t, b.y[0], lw=0.8, label="x0 = 1 + 1e-6")
ax[0].set_xlabel("time"); ax[0].set_ylabel("x"); ax[0].legend(); ax[0].set_title("Butterfly effect")
ax[1].plot(a.y[0], a.y[2], lw=0.4)
ax[1].set_xlabel("x"); ax[1].set_ylabel("z"); ax[1].set_title("Lorenz attractor (x-z plane)")
plt.tight_layout(); plt.savefig("figures/lorenz_butterfly.png", dpi=150)

# ---------------------------------------------------------------- 3. Harmonic noise reduction
rng = np.random.default_rng(42)
N = 120                                            # 10 years of monthly data
tt = np.arange(N)
signal = 15 + 9 * np.cos(2 * np.pi * (tt - 6.5) / 12)   # annual cycle, deg C
noisy = signal + rng.normal(0, 2.0, N)                   # white noise, sigma = 2 deg C

# Harmonic coefficients a_k, b_k (course notation)
k_all = np.arange(1, N // 2 + 1)
a_k = np.array([2 / N * np.sum(noisy * np.cos(2 * np.pi * k * tt / N)) for k in k_all])
b_k = np.array([2 / N * np.sum(noisy * np.sin(2 * np.pi * k * tt / N)) for k in k_all])
a_k[-1] /= 2; b_k[-1] = 0                           # Nyquist harmonic
var_k = (a_k ** 2 + b_k ** 2) / 2
var_k[-1] = a_k[-1] ** 2
R2 = var_k / np.var(noisy)
k_annual = N // 12                                  # 10 cycles in 120 months
print(f"\nHarmonic k = {k_annual} (annual cycle) explains {100 * R2[k_annual - 1]:.1f}% of variance")

# Keep only the annual harmonic (and its first overtone) -> denoised series
keep = [k_annual, 2 * k_annual]
recon = np.full(N, noisy.mean())
for k in keep:
    recon += a_k[k - 1] * np.cos(2 * np.pi * k * tt / N) + b_k[k - 1] * np.sin(2 * np.pi * k * tt / N)

snr_before = np.var(signal) / np.var(noisy - signal)
snr_after = np.var(signal) / np.var(recon - signal)
print(f"SNR before = {snr_before:.1f}, after harmonic filtering = {snr_after:.1f}")

plt.figure(figsize=(9, 4))
plt.plot(tt, noisy, ".", c="gray", label="noisy observations")
plt.plot(tt, signal, lw=2, label="true signal")
plt.plot(tt, recon, "--", lw=2, label="harmonic reconstruction")
plt.xlabel("month"); plt.ylabel("temperature (deg C)"); plt.legend()
plt.title("Noise reduction in the frequency domain")
plt.tight_layout(); plt.savefig("figures/harmonic_denoising.png", dpi=150)
print("\nFigures saved to ./figures/")
