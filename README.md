🍽️ Norovirus Restaurant Outbreak Modeling
Simulating real outbreaks, validating with data, and testing what actually works.

This project explores how norovirus spreads inside a restaurant using a stochastic simulation model built to feel as close to real life as possible. We use real outbreak sizes from the CDC’s NORS database and validate our model through K-fold cross-validation and full-dataset calibration. This helps us make sure our simulated outbreaks truly reflect ground-truth behavior before testing any interventions.

Once the model is calibrated, we evaluate three major public-health strategies:
✨ Excluding symptomatic food handlers
✨ Improving hygiene to lower transmission
✨ Combining exclusion + hygiene

Each policy is tested across different compliance levels to see how much it can reduce outbreak size. The result is a clear picture of which interventions make the biggest impact in controlling norovirus in restaurant settings.
