# Chaos Theory, the Butterfly Effect, Fractals and Noise — An Atmospheric Science and Machine Learning Perspective

**Cansu Yamanlar** · İTÜ MTO 311E Data Analysis · November 2026

**▶ Interactive dashboard:** [Lorenz's desk, MIT, 1961](https://cyamanlar.github.io/chaos-theory/) — play Edward Lorenz, type in two nearby initial values and watch the two weathers split (`index.html`).

## 1. Introduction: what the lecture notes say

The core message of the lecture is this: **in nonlinear systems such as the atmosphere, a small error or noise grows over iterative steps; therefore we must both remove noise from the data and think in terms of probabilities rather than a single forecast.**

The points in the lecture notes, unpacked:

| Note | Meaning | Section |
| --- | --- | --- |
| "The model blows up, noise grows, the model cannot handle it; over iterative steps" | A model uses its previous output as the next input; the error is multiplied at every step (noise amplification) | 3, 4 |
| "Noise / noise reduction → in harmonic analysis" | Noise can be separated in the frequency domain (Fourier/harmonic analysis, smoothing) | 4 |
| "Sensitive dependence on initial conditions (chaos theory)" | A tiny difference in the initial condition becomes a huge difference over time | 2, 3 |
| "Fractal geometry → time series, stock market movement, weather" | Irregular shapes and series in nature look similar at every scale | 5 |
| "Chaos theory: the film, Edward Lorenz" | Lorenz, the father of chaos theory, and the documentary about him | 2 |
| "Noise is always present in important signals… electromagnetic… noise can be filtered in the frequency domain" | Every measurement contains noise; signal and noise live at different frequencies, so they can be separated | 4 |

Outline: first we define chaos, then show mathematically why it depends on initial conditions. Then we cover noise, fractals, applications in atmospheric science and sustainability, and the link to machine learning (ML).

## 2. What is chaos? The Lorenz story

**Chaos = deterministic but unpredictable behaviour.** The equations governing the system are fully known and contain no randomness. Yet its long-term future cannot be computed in practice.

### The story: 0.506 instead of 0.506127

In 1961 at MIT, meteorologist Edward Lorenz was running a simple 12-variable weather model. To look at a simulation again, he restarted it halfway and typed in an intermediate value by hand from the printout. The computer stored 0.506127, but the printout showed 0.506. The difference was smaller than one part in a thousand, about the size of a measurement error.

When he came back from a coffee break, the two simulations had produced completely different weather after a few "months". The computer was not broken: **the system was extremely sensitive to the tiny initial difference.** This is the concept of *sensitive dependence on initial conditions* in the lecture notes.

### The Lorenz (1963) equations

Lorenz later reduced the model to three equations describing convection in a fluid layer heated from below (Rayleigh–Bénard convection):

$$
\frac{dx}{dt} = \sigma (y - x), \qquad \frac{dy}{dt} = x(\rho - z) - y, \qquad \frac{dz}{dt} = xy - \beta z
$$

The classic values are σ = 10, ρ = 28, β = 8/3. Physical meaning of the variables and parameters:

| Symbol | Physical meaning |
| --- | --- |
| x | Intensity of the convective circulation (rotation speed and direction of the cell) |
| y | Horizontal temperature difference between the rising and sinking branches |
| z | Deviation of the vertical temperature profile from a linear profile |
| σ (Prandtl number) | Ratio of viscosity to thermal diffusivity |
| ρ (Rayleigh number) | Strength of heating from below; chaos begins above ρ ≈ 24.74 |
| β | Geometry of the convection cell (aspect ratio) |

The key point is that **the xz and xy terms are nonlinear.** In a linear system, an input error passes to the output proportionally. In a nonlinear system, the error multiplies itself and grows exponentially.

### The butterfly effect and the strange attractor

Plotted in phase space, the solution forms a shape resembling butterfly wings: **the Lorenz attractor.** The trajectory switches irregularly between the two wings, never repeats itself, yet never leaves the wings.

- **Weather** = which wing the trajectory is on right now. This is unpredictable in the long run.
- **Climate** = the shape of the wings, i.e. the statistics. This is predictable.

Lorenz titled his 1972 talk "Does the flap of a butterfly's wings in Brazil set off a tornado in Texas?". This is why the concept is known as the **butterfly effect**. A butterfly does not literally create a tornado. The idea is that a small-scale difference we cannot observe can grow enough to completely change our forecast.

### The film mentioned in the lecture

The notes do not name the film. Two well-known documentaries cover Lorenz and these topics:

- **BBC – *The Secret Life of Chaos* (2010, presented by Jim Al-Khalili).** Covers Turing's pattern formation, Lorenz's weather model, Mandelbrot's fractals and the emergence of order from disorder. This best matches the chaos + fractals pairing in the notes.
- ***Chaos: A Mathematical Adventure* (2013, Ghys, Leys and Alvarez).** A nine-chapter animation that explains the Lorenz attractor and the butterfly effect very visually.

It is worth confirming in class which one was meant.

## 3. Why does it depend on initial conditions? Mathematics and physics

**Answer: in nonlinear systems, the distance between two nearby starting points is multiplied by a factor at every step. The error therefore grows exponentially rather than additively.**

### Step 1 — The simplest chaotic system: the logistic map

This is exactly what the lecture calls "iterative steps". Each value is computed from the previous one:

$$
x_{n+1} = r \, x_n \, (1 - x_n), \qquad r = 4
$$

Let us run the same equation twice, starting from x₀ = 0.3 and x₀ = 0.3001. The difference is only 0.0001, the size of a thermometer's rounding error. The figure below shows that the difference reaches 0.034 at step 10 and 0.94 at step 20. At that point the two series are completely unrelated; since the values lie between 0 and 1, the error has "saturated".

![Logistic map error growth](figures/logistic_error_growth.png)

Although the difference fluctuates in the first steps, on average it follows the theoretical line that doubles every step, and it saturates once it reaches the 0–1 range.

### Step 2 — Why is it multiplied? (Mathematics)

For a small error δₙ, a Taylor expansion gives δₙ₊₁ ≈ f′(xₙ) · δₙ. At every step, the error is multiplied by the slope of the function at that point. The average logarithm of these slopes is the **Lyapunov exponent λ**:

$$
\lambda = \lim_{N\to\infty} \frac{1}{N} \sum_{n=0}^{N-1} \ln \lvert f'(x_n) \rvert, \qquad \delta(t) \approx \delta_0 \, e^{\lambda t}
$$

- **λ < 0:** The error decays; the system is stable (a pendulum with friction).
- **λ = 0:** The error stays constant (periodic motion, e.g. a planetary orbit).
- **λ > 0:** The error grows exponentially, i.e. **chaos.** For r = 4, λ = ln 2 ≈ 0.693: on average the error doubles at every step.

### Step 3 — The predictability horizon

The forecast becomes worthless once the error reaches an acceptable limit Δ. This time is:

$$
T \approx \frac{1}{\lambda} \ln \frac{\Delta}{\delta_0}
$$

**Key result:** Reducing the initial error (δ₀) tenfold adds only ln 10 / λ to the forecast horizon. For the logistic map, that is just 3.3 steps. However much you improve the measurements, the gain remains logarithmic.

### Step 4 — The atmospheric counterpart (Physics)

In the atmosphere, the nonlinear term is the **advection term (u·∇)u** in the Navier–Stokes equations: the wind transports itself. This term **stretches and folds** air parcels: two nearby parcels first move apart, then fold back into a bounded region. The error therefore does not grow without bound, but information is lost.

The atmosphere in numbers:

- At the synoptic scale (fronts, low-pressure systems), the error doubling time in today's models is about 1.5–2 days.
- At the convective scale (thunderstorms), it is of the order of hours.
- Small-scale errors propagate to larger scales over time (upscale error growth, Lorenz 1969). This is why the practical limit of deterministic weather forecasting is about 10 days and the theoretical upper limit about 2 weeks.

**Worked example:** Suppose today's temperature analysis over Istanbul has a 0.5 °C error and the error doubles every 2 days. The error is then 1 °C on day 2, 2 °C on day 4, 4 °C on day 6 and 8 °C on day 8. An 8 °C error is no better than quoting the climatological mean: the forecast no longer carries information. This is a simplified calculation; in reality the error saturates at some level.

## 4. What is noise? Are error and noise the same thing?

**Noise is the random part of a measured value that does not belong to the physical signal we are interested in.** Every measurement can be written as:

$$
x_t = s_t + b + \varepsilon_t \qquad \text{(observation = true signal + bias + random noise)}
$$

### Error, bias and noise

| Term | Definition | Atmospheric example | How to remove it |
| --- | --- | --- | --- |
| Error | Observation − true value; the total difference | Thermometer reads 21.7 °C, true value is 21.0 °C | By splitting it into its components |
| Bias (systematic error) | Always shifted in the same direction; non-zero mean | A sun-exposed sensor always reads +0.5 °C too high | Calibration, homogeneity test, bias correction |
| Noise (random error, ε) | Zero-mean, unpredictable fluctuation | Sensor resolution, electronic noise, electromagnetic interference | Averaging, smoothing, filtering |
| Representativeness error | A point measurement cannot represent a model grid box | A single station is not the average of a 9 km model cell | Error covariances in data assimilation |

So **noise is the random part of the error.** Once you find the bias, you can subtract it. Noise cannot be removed from a single measurement; it can only be suppressed statistically (many measurements, frequency analysis).

**Chaos is not noise.** A chaotic series *looks* random but is deterministic. Noise is genuinely random. This distinction may come up in the exam.

### The lecture's example: radio and electromagnetic interference

When listening to the radio, the music is the signal and the crackle is noise. The same applies to an automatic weather station. The sensor cable picks up electromagnetic interference from a nearby power line or radio transmitter, which adds fast, irregular spikes on top of the data. This is what the lecture means by "noise is always present in important signals": there is no noise-free measurement.

### "The model blows up": why does noise grow in an iterative model?

A numerical weather prediction model uses the output of one time step as the input to the next. Noise in the initial data is multiplied by e^λ at every step, as in Section 3. This noise does a second kind of damage: short-wavelength noise that the grid cannot resolve can trigger numerically unstable modes. The model then genuinely "blows up" and the values go to infinity. This is what the lecture means by "the model cannot handle it". For this reason, models balance the initial data (initialization) and damp short waves with numerical diffusion or filters.

### Noise reduction: filtering in the frequency domain (harmonic analysis)

The lecture's last note, "noise can be filtered in the frequency domain", connects directly to the **Harmonic Analysis** topic of the course. The logic:

1. Write the series as a sum of harmonics: x_t = x̄ + Σ [a_k cos(2πkt/N) + b_k sin(2πkt/N)].
2. Compute the variance carried by each harmonic: C_k²/2, where C_k² = a_k² + b_k².
3. **The physical signal is concentrated in a few low frequencies.** For example, in monthly temperature the 1st harmonic (the annual cycle) can explain more than 90% of the total variance.
4. **White noise, by contrast, is spread evenly across all frequencies.** Most high-frequency harmonics are noise.
5. Keep the first few harmonics, discard the rest, and reconstruct the series. The result is the denoised signal.

The **moving average, binomial/Gaussian smoothing and LOWESS** covered in the course do the same job in the time domain. They are low-pass filters: they keep the slowly varying signal and suppress fast-oscillating noise. Success is measured by the **signal-to-noise ratio (SNR)**: SNR = Var(signal) / Var(noise).

## 5. Fractal geometry: weather, time series and the stock market

**A fractal is a shape that looks similar to itself as you zoom in (self-similar) and whose dimension is not an integer.** Euclidean geometry describes smooth shapes such as lines, circles and cubes. Clouds, coastlines, lightning and mountain ranges in nature, however, are rough. Mandelbrot developed fractal geometry to describe them. The lecture note "important for how we look at events, the geometry of shapes" refers to this.

### How is the fractal dimension computed?

Suppose we cover a shape with boxes of size ε and need N(ε) boxes. The box-counting dimension is defined as:

$$
D = \lim_{\varepsilon \to 0} \frac{\log N(\varepsilon)}{\log (1/\varepsilon)}
$$

- **Line:** D = 1. **Plane:** D = 2.
- **Koch curve:** At each step a segment is divided into 3 and replaced by 4 segments, so D = log 4 / log 3 ≈ 1.26. More than a line, less than a plane.
- **Coastline paradox:** Mandelbrot (1967) showed that the measured length of the coast of Britain keeps increasing as the ruler gets shorter. For the west coast, D ≈ 1.25.
- **Lorenz attractor:** D ≈ 2.06. The butterfly shape in Section 2 is itself a fractal. Chaos and fractals are therefore two sides of the same coin: chaos describes the dynamics, and the fractal describes the geometry of those dynamics.

### Fractals in the atmosphere

- **Clouds:** Lovejoy (1982) showed in satellite and radar images that the perimeter–area relation of cloud and rain areas follows the same fractal dimension (D ≈ 1.35) from a few kilometres to thousands of kilometres. You cannot tell the scale of a cloud by looking at a photograph of it.
- **Turbulence:** Richardson's famous 1922 rhyme reads: "Big whirls have little whirls that feed on their velocity, and little whirls have lesser whirls and so on to viscosity." Large eddies pass energy down to smaller ones (the energy cascade). Kolmogorov (1941) showed that the energy spectrum follows E(k) ∝ k^(−5/3). This is a scale-invariant, i.e. fractal, structure.
- **Precipitation and lightning:** Rain areas and lightning channels also show fractal and multifractal behaviour.

### Fractals in time series: the Hurst exponent

A time series can also be fractal: plot a temperature or river-discharge series over a 10-year or a 100-year window and you see similar irregularity. This is measured by the **Hurst exponent H**:

- **H = 0.5:** Random walk, no memory.
- **H > 0.5:** Persistence. A dry year tends to be followed by another dry year, i.e. long-range dependence.
- **H < 0.5:** Anti-persistence (a tendency to reverse).
- The fractal dimension of the series' graph is D = 2 − H.

Hurst found H ≈ 0.7 in the annual flood records of the Nile while working on dam design. **This is a crucial warning for trend analysis:** in a persistent series, tests such as Mann–Kendall can flag a trend as significant when there is none. This is why the course topics of autocorrelation and homogeneity matter.

### The link to the stock market

In 1963 Mandelbrot studied cotton prices. He found that price changes did not follow a normal distribution: large crashes were far more frequent than expected (fat tails), and the chart looked similar at daily, monthly and yearly scales.

| | Atmosphere | Stock market |
| --- | --- | --- |
| In common | Multi-scale, fat-tailed (extreme events), volatility clustering | Same features |
| Governing law | Physics (Navier–Stokes, thermodynamics); deterministic chaos | No physical law; human behaviour |
| Effect of the forecast | A forecast does not change the weather | A forecast changes the price (reflexivity) |
| Predictability | ~10 days for weather; climate statistically | Mostly close to a random walk |

So the lecture uses the stock market as an example in the sense that "the same mathematical language is used". It has not been shown that markets contain low-dimensional deterministic chaos as the atmosphere does.

## 6. Where is this used in atmospheric science and sustainability?

**The biggest practical consequence of chaos theory is this: modern meteorology and climate science do not issue a single forecast; they issue a probability distribution.**

### 6.1 Ensemble forecasting

Since we cannot know the initial condition exactly, we run the same model many times from slightly different initial conditions. ECMWF's ensemble system (ENS) runs with 1 control and 50 perturbed members.

- If the members stay close together (low spread), the forecast can be trusted.
- If the members diverge (high spread), the atmosphere is in a "chaotic" regime that day and uncertainty is high.
- "70% chance of rain tomorrow" means that about 36 of the 51 members produce rain.
- The lecture note "the initial conditions are changed" describes these perturbations.

### 6.2 Data assimilation

The model's initial state is obtained by optimally combining noisy observations with the previous forecast (the background). The Kalman filter and 4D-Var are the best-known methods. Each source of information is weighted by the inverse of its noise variance: trust noisy observations less and reliable ones more. The definition of noise in Section 4 becomes a direct mathematical tool here.

### 6.3 Weather vs. climate: Lorenz's two kinds of predictability

| | Weather forecast | Climate projection |
| --- | --- | --- |
| Problem type | Initial-value problem (1st kind) | Boundary-value problem (2nd kind) |
| What it predicts | Will it rain in Istanbul tomorrow? | How many hot days will Istanbul have in 2050? |
| Determined by | Today's state of the atmosphere | External forcings such as CO₂ |
| Role of chaos | Information is lost after ~10 days | We predict the statistics, not the value for a single year |

This answers the question "if we cannot forecast the weather beyond 10 days, how can we know the climate?". In climate change, the shape of the attractor changes, and we predict that shape.

### 6.4 Noise in climate = internal variability

In climate projections, the **signal** is human-induced warming. The **noise** is chaotic natural fluctuation such as ENSO and the NAO. To separate them, the same climate model is run dozens of times, changing only the initial condition (initial-condition large ensembles). Examples are the CESM Large Ensemble (40 members) and the MPI Grand Ensemble (100 members).

- **The ensemble mean** gives the forced signal.
- **The spread across members** gives the natural variability.
- **Time of emergence:** the year when the signal exceeds the noise (SNR > 1 or 2). For temperature, it emerges early in the tropics and later in the mid-latitudes. Precipitation is noisier, so it emerges much later.

### 6.5 What to know for sustainability and climate risk

1. **Never make decisions from a single model run.** Computing a city's flood risk from a single climate model simulation ignores the butterfly effect. Use ensembles and probabilities.
2. **Extreme events are fat-tailed.** Assuming a normal distribution underestimates the 100-year flood. Return-period analysis needs an appropriate distribution (e.g. GEV).
3. **Persistence (Hurst) amplifies drought risk.** Dry years cluster; water-resource and agricultural planning must account for this.
4. **Renewable energy forecasts are probabilistic.** Uncertainty in wind and solar power forecasts grows with lead time. Grid operators use ensemble forecasts for reserve capacity planning.
5. **Seasonal forecasting is possible despite chaos.** Thanks to slowly varying boundary conditions such as ocean temperature and ENSO, the "probability of a warmer-than-normal season" 1–3 months ahead can be forecast. Agriculture and early-warning systems rely on this.

## 7. Why it matters for machine learning

**ML models are also subject to the rules of chaos and noise. An AI weather model cannot remove the butterfly effect; it can only deal with it more intelligently.**

### 7.1 Noise in ML: what a model must not memorize

In ML, data are modelled as y = f(x) + ε, where f is the physical relationship to be learned and ε is noise. The expected error splits into three parts:

$$
E\big[(y - \hat{y})^2\big] = \text{Bias}^2 + \text{Variance} + \sigma_\varepsilon^2
$$

- **σε² (irreducible error):** However good the model, an error as large as the measurement noise remains.
- **Overfitting = memorizing noise.** Training error drops to zero but the model fails on new data. This is why regularization, dropout and early stopping exist.
- **Noise is sometimes useful:** Deliberately adding noise to the inputs during training (noise injection) makes the model robust to measurement errors.

### 7.2 The ML version of "the model blows up": rollout

GraphCast (Google DeepMind), Pangu-Weather (Huawei), FourCastNet (NVIDIA) and ECMWF's operational AIFS forecast in 6-hour steps. For a 10-day forecast, the model feeds its own output back in as input 40 times (autoregressive rollout). This is the exact counterpart of the lecture note "noise grows over iterative steps".

- A model trained for a single step has never seen its own erroneous output; errors accumulate and the forecast drifts away from reality.
- **Solution:** fine-tuning with multi-step rollouts. Trained on its own outputs over several steps, the model learns to correct its own errors.

### 7.3 Why does chaos blur ML forecasts?

If a model is trained with mean squared error (MSE), the following happens: because the long-range future is uncertain, the forecast that minimizes MSE is **the average of all possible futures.** That average is a smooth, blurry field. As a result, storms weaken and extreme events disappear, which is dangerous for climate risk.

**The solution is probabilistic ML.** GenCast (DeepMind, 2024) produces an ensemble with a diffusion model. ECMWF's AIFS ENS is trained with the CRPS (Continuous Ranked Probability Score) loss function. In other words, ML has adopted meteorology's answer to chaos: a distribution instead of a single forecast.

### 7.4 The frequency domain and neural networks

- The **Fourier Neural Operator (FNO)** is the basis of FourCastNet. It moves the input to the frequency domain with a Fourier transform and **keeps only the first few (low-frequency) modes.** This is the same idea as keeping the first harmonics and discarding the rest in harmonic analysis.
- **Spectral bias:** Neural networks learn low frequencies first and high-frequency detail (and noise) later. Early stopping therefore acts as a natural noise filter.

### 7.5 Best practices for ML with atmospheric data

1. **Do not use a random train/test split.** Atmospheric data are autocorrelated (Hurst > 0.5). A random split lets the model "predict" today from yesterday, causing data leakage. Use blocked splits by year.
2. **Measure skill in Lyapunov times.** Models that learn chaotic systems (e.g. Pathak et al. 2018, reservoir computing) report skill as "how many Lyapunov times (1/λ) the forecast stays accurate".
3. **Clean the data first.** Homogeneity testing, bias correction and smoothing come before ML. A model trained on noisy data mistakes noise for physics.
4. **Use probabilistic metrics alongside deterministic ones:** CRPS and the spread–skill ratio in addition to RMSE.

## 8. Worked exam question and summary

### Question

The logistic map xₙ₊₁ = 4xₙ(1 − xₙ) is iterated from two initial conditions, x₀ = 0.3000 and y₀ = 0.3001.

(a) Compute x₁, x₂, x₃, y₁, y₂, y₃ and the absolute differences |xₙ − yₙ|.
(b) The Lyapunov exponent of this map is λ = ln 2. Estimate the number of iterations after which the difference reaches 0.5.
(c) Explain the result in terms of sensitive dependence on initial conditions and noise.

### Solution

**(a)** x₁ = 4(0.3)(0.7) = 0.840000 and y₁ = 4(0.3001)(0.6999) = 0.840160.

| n | xₙ | yₙ | \|xₙ − yₙ\| |
| --- | --- | --- | --- |
| 0 | 0.300000 | 0.300100 | 0.000100 |
| 1 | 0.840000 | 0.840160 | 0.000160 |
| 2 | 0.537600 | 0.537165 | 0.000435 |
| 3 | 0.994345 | 0.994475 | 0.000130 |

The difference does not grow monotonically; it shrinks at step 3 because the slope |f′(x)| = |4 − 8x| is small near x ≈ 1. Growth over the first steps is exponential only on average.

**(b)** With δ₀ = 0.0001, Δ = 0.5 and λ = ln 2 ≈ 0.693:

$$
T \approx \frac{1}{\lambda}\ln\frac{\Delta}{\delta_0} = \frac{\ln(0.5/0.0001)}{\ln 2} = \frac{\ln 5000}{0.693} = \frac{8.517}{0.693} \approx 12.3 \text{ iterations}
$$

Numerical check: the difference is 0.408 at step 12, 0.488 at step 13 and 0.954 at step 14. The 0.5 threshold is crossed at step 13–14, consistent with the average-based estimate.

**(c)** An initial difference of 0.0001, i.e. a measurement noise, grows within about 13 iterations into a difference half the size of the whole 0–1 range. The system is deterministic but chaotic because λ > 0. Reducing the initial error tenfold adds only ln 10 / ln 2 ≈ 3.3 iterations to T. This is why ensembles are used instead of a single forecast.

### One-page summary

| Concept | In one sentence | In the atmosphere | In ML |
| --- | --- | --- | --- |
| Chaos | Deterministic but unpredictable | Weather cannot be forecast beyond ~10 days | Error accumulation in rollout |
| Sensitive dependence on initial conditions | If λ > 0, the error grows as e^(λt) | Ensemble forecasting, data assimilation | Probabilistic models (GenCast, AIFS ENS) |
| Fractal | Scale-invariant, self-similar structure | Clouds, turbulence, Hurst persistence | Blocked train/test splits |
| Noise | The random, zero-mean part of the error | Sensor and electromagnetic interference; internal variability in climate | Overfitting, irreducible error |
| Noise reduction | Keep the signal at low frequencies, discard the rest | Harmonic analysis, MA, LOWESS | Fourier Neural Operator, early stopping |

## Code and figures

`index.html` is a self-contained interactive version of the Lorenz experiment: open it in any browser, no installation needed.

`chaos_noise_demo.py` demonstrates the three ideas of this report numerically. To run it:

```bash
pip install -r requirements.txt
python chaos_noise_demo.py
```

| Part | Printed result | Saved figure |
| --- | --- | --- |
| Logistic map | Step-by-step difference table; λ = 0.6932 (theory ln 2); T ≈ 12.3 steps | `figures/logistic_error_growth.png` |
| Lorenz system | Two solutions starting 1e-6 apart diverge at t ≈ 25 | `figures/lorenz_butterfly.png` |
| Harmonic noise reduction | The annual harmonic explains 94.5% of the variance; SNR 16.6 → 1154 | `figures/harmonic_denoising.png` |

![Lorenz butterfly effect](figures/lorenz_butterfly.png)

![Noise reduction with harmonic analysis](figures/harmonic_denoising.png)
