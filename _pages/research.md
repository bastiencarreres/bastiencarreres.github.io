---
layout: page
permalink: /research/
title: Research
nav: false
---

My research focuses on measuring the growth rate of cosmic structures (\\(f\sigma_8\\)) with type Ia supernovae (SNe Ia). Galaxies are not perfectly carried along by the expansion of the Universe: they also fall toward overdense regions, acquiring so-called peculiar velocities. Because SNe Ia are excellent distance indicators, comparing their distances with their observed redshifts reveals these motions, turning supernova surveys into maps of the large-scale velocity field. The statistics of that field directly constrain \\(f\sigma_8\\), a key quantity for testing general relativity on cosmological scales.

<div class="row justify-content-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/research/pv-hubble-diagram-toy-model.png" class="img-fluid rounded z-depth-1" zoomable=true caption="How the peculiar velocity of a single supernova's host galaxy displaces it on the Hubble diagram (from Carreres et al. 2023)." %}
  </div>
</div>

## Intrinsic scatter systematics in LSST growth-rate measurements

_Carreres et al. 2025, ApJ 994, 178_

The Vera C. Rubin Observatory's LSST will observe an unprecedented number of nearby SNe Ia, making it a prime dataset for growth-rate measurements. But SNe Ia are only standardizable candles: after standardization, their brightnesses still scatter by an amount and in a way that depends on their intrinsic properties and on the dust in their host galaxies. In this work I simulated the full 10-year LSST supernova sample — including correlated peculiar velocities drawn from an N-body simulation and realistic correlations between supernovae and their host galaxies — for four different models of this intrinsic scatter.

For most scatter models, \\(f\sigma_8\\) is recovered without bias and with a precision of about 13–14%. For the most realistic, dust-based model, however, the non-Gaussian distribution of Hubble diagram residuals biases \\(f\sigma_8\\) low by about 20% — a systematic that standard bias-correction methods (BBC) do not remove. The error budget is dominated by statistical uncertainty (over 75% of the total), with the leading systematic coming from the damping parameter \\(\sigma_u\\), an empirical description of redshift-space distortions in the velocity power spectrum. These results motivate new methods to handle non-Gaussian Hubble residuals and better modeling of the velocity power spectrum damping.

<div class="row justify-content-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/research/lsst-scatter-fs8-results.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Recovered growth rate for four intrinsic scatter models, averaged over eight LSST mock catalogs: most models are unbiased, but the realistic dust-based model (P23) biases the measurement low by about 20%." %}
  </div>
</div>

_[Read the paper](https://arxiv.org/abs/2505.13290)_

## Peculiar velocities in the ZTF SN Ia DR2 Hubble diagram

_Carreres, Rosselli, et al. 2025, A&A 694, A8_

The Zwicky Transient Facility (ZTF) has assembled by far the largest homogeneous sample of low-redshift (\\(z < 0.1\\)) SNe Ia to date. At such low redshifts, the peculiar velocities of the host galaxies are not negligible compared to the expansion redshift, and — crucially — they are correlated between nearby galaxies, since neighboring galaxies fall toward the same large-scale structures. Using realistic simulations of the ZTF survey, we compared three ways of treating peculiar velocities in the Hubble diagram fit: ignoring them, treating them as independent noise (a diagonal error term), and modeling their full covariance from the velocity power spectrum.

Only the full covariance matrix correctly accounts for the sample variance induced by correlated velocities. Applied to the ZTF SN Ia DR2 data, neglecting peculiar velocity correlations shifts the intercept of the Hubble diagram by an amount equivalent to about \\(1\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\\) on \\(H_0\\), and underestimates the \\(H_0\\) uncertainty. As calibration systematics improve, properly accounting for this effect becomes increasingly important for local measurements of \\(H_0\\) — and for the Hubble tension debate.

<div class="row justify-content-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/research/ztf-dr2-hubble-fit-pv-covariance.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Hubble diagram fit of the ZTF SN Ia DR2 sample under three treatments of peculiar velocities: none (blue), diagonal error term (yellow), and full velocity covariance (red). The contours shift and widen when velocity correlations are properly included." %}
  </div>
</div>

_[Read the paper](https://arxiv.org/abs/2405.20409)_

## Forecasting growth-rate measurements with ZTF simulations

_Carreres et al. 2023, A&A 674, A197_

In this first paper of the series, I built detailed end-to-end simulations of the ZTF SN Ia survey — from host galaxies and peculiar velocities drawn from an N-body simulation, through realistic light-curve sampling using actual ZTF observing logs, to the selection effects imposed by photometric detection and spectroscopic typing. These simulations were used to develop and validate a maximum-likelihood pipeline that measures \\(f\sigma_8\\) directly from supernova peculiar velocities.

A key finding is that selection effects — chiefly the spectroscopic typing of candidates — bias the distance (and hence velocity) estimates above \\(z \simeq 0.06\\). Restricting to the unbiased sample at \\(z < 0.06\\), the equivalent of 6 years of ZTF data yields an unbiased measurement of \\(f\sigma_8\\) with 19% precision, competitive with existing peculiar-velocity measurements based on the Tully-Fisher relation or the Fundamental Plane. This work established the framework for the growth-rate measurement with real ZTF data, and its methodology carries over to the much larger photometric samples expected from the Rubin Observatory.

<div class="row justify-content-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/research/ztf-forecast-fs8-precision.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Forecast growth-rate constraints from 27 mock realizations of 6 years of ZTF data (redshift range 0.02–0.06): unbiased, with an average precision of 19%." %}
  </div>
</div>

_[Read the paper](https://arxiv.org/abs/2303.01198)_
