---
layout: page
permalink: /research/
title: Research
nav: false
---

The expansion of the Universe is accelerating, and the origin of this acceleration remains unknown. It can be explained by a dark energy component, or by a modification of general relativity on cosmological scales. Measuring the growth rate of structures (\\(f\sigma_8\\)) is one way to distinguish between these scenarios, since the rate at which matter clusters depends directly on the theory of gravity. My research focuses on measuring \\(f\sigma_8\\) at low redshift with type Ia supernovae (SNe Ia).

Galaxies are not only carried along by the expansion of the Universe: they also fall toward overdense regions, which gives them peculiar velocities (PVs). The redshift of a galaxy includes both contributions. SNe Ia are standardizable candles, so they provide a measurement of the distance to their host galaxy that is independent of the redshift. Comparing the two gives an estimate of the PV of the host.

<div class="row justify-content-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/research/pv-hubble-diagram-toy-model.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Effect of the peculiar velocity of the host galaxy on the position of a SN Ia on the Hubble diagram (from Carreres et al. 2023)." %}
  </div>
</div>

A single PV measurement is dominated by the uncertainty on the distance. With several thousands of SNe Ia, however, the statistics of the velocity field can be measured and used to constrain \\(f\sigma_8\\). The Zwicky Transient Facility (ZTF) has observed by far the largest low-redshift (\\(z < 0.1\\)) SN Ia sample to date, and the Rubin Observatory Legacy Survey of Space and Time (LSST) will increase this number considerably. To obtain an unbiased measurement from these samples, the systematic effects that were negligible in previous analyses need to be understood and modeled.

## Growth-rate measurement with ZTF simulations

_Carreres et al. 2023, A&A 674, A197_

In this work, we built realistic simulations of the ZTF SN Ia survey. Host galaxies and their PVs are drawn from an N-body simulation, light curves are sampled using the ZTF observing logs, and the selection effects due to photometric detection and spectroscopic typing are included. We used these simulations to develop and test a maximum likelihood method that constrains \\(f\sigma_8\\) using only SN Ia PVs.

We find that the spectroscopic typing selection biases the distance estimates above \\(z \simeq 0.06\\). Using the unbiased sample at \\(z < 0.06\\), the equivalent of 6 years of ZTF data gives an unbiased estimate of \\(f\sigma_8\\) with an average precision of 19%. This validates the framework, which can be applied to the real ZTF data and extended to the Rubin-LSST sample.

<div class="row justify-content-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/research/ztf-forecast-fs8-precision.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Growth-rate constraints from 27 realizations of 6 years of ZTF data (0.02 < z < 0.06)." %}
  </div>
</div>

_[Read the paper](https://arxiv.org/abs/2303.01198)_

## Impact of peculiar velocities on the Hubble diagram

_Carreres, Rosselli, et al. 2025, A&A 694, A8_

PVs also affect the measurement of cosmological parameters from the Hubble diagram, and the smaller the redshift, the larger the effect is. PVs of nearby galaxies are correlated, since these galaxies fall toward the same structures. In this work, we used simulations of ZTF to compare three treatments of PVs in the Hubble diagram fit: neglecting them, adding a diagonal error term, and using the full covariance matrix computed from the velocity power spectrum.

We find that the full covariance matrix is necessary to take into account the sample variance. Applied to the ZTF DR2 SN Ia sample, neglecting PVs and their correlations results in a shift of the intercept of the Hubble diagram equivalent to about \\(1\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\\) on \\(H_0\\), and in a slight underestimation of the \\(H_0\\) error bar.

<div class="row justify-content-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/research/ztf-dr2-hubble-fit-pv-covariance.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Hubble diagram fit of the ZTF SN Ia DR2 sample without PVs (blue), with a diagonal PV error term (yellow), and with the full PV covariance (red)." %}
  </div>
</div>

_[Read the paper](https://arxiv.org/abs/2405.20409)_

## Intrinsic scatter systematics for Rubin-LSST

_Carreres et al. 2025, ApJ 994, 178_

With the Rubin-LSST sample, the statistical uncertainty on \\(f\sigma_8\\) will decrease and systematic effects will become more important. In this work, we simulated the 10-year LSST SN Ia sample, including a correlated velocity field from an N-body simulation and realistic correlations between SN Ia properties and their host galaxies, for four models of the intrinsic scatter of SNe Ia.

For most of the intrinsic scatter models, we recover \\(f\sigma_8\\) with a precision of about 13–14%. For the most realistic, dust-based model, we find that the non-Gaussian distribution of the Hubble diagram residuals leads to a bias on \\(f\sigma_8\\) of about −20%. The error budget is dominated by the statistical uncertainty (more than 75% of the total), and the systematic error budget is dominated by the uncertainty on the damping parameter \\(\sigma_u\\), which gives an empirical description of redshift-space distortions in the velocity power spectrum.

<div class="row justify-content-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/research/lsst-scatter-fs8-results.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Recovered growth rate for four intrinsic scatter models, averaged over eight LSST mock catalogs. The dust-based model (P23) is biased by about −20%." %}
  </div>
</div>

_[Read the paper](https://arxiv.org/abs/2505.13290)_

## Collaborations

I am a member of ZTF, of the Rubin-LSST Dark Energy Science Collaboration ([DESC](https://lsstdesc.org/)), and of the Dark Energy Bedrock All-Sky Supernova program (DEBASS). I am also working on the TITAN SN Ia sample from the Asteroid Terrestrial-impact Last Alert System (ATLAS), for which I will perform the \\(f\sigma_8\\) measurement. I have also worked on growth-rate forecasts for LSST, on field-level inference of the growth rate from velocity and density fields, on the determination of SN Ia redshifts using galaxy groups, and on the ZTF DR2 papers. The full list is on the [publications page]({{ '/publications/' | relative_url }}).

## Perspectives

These results motivate a search for new methods to correct for the non-Gaussian distribution of the Hubble diagram residuals, as well as an improved modeling of the velocity power spectrum on small scales. Both are needed to obtain a precise and unbiased measurement of \\(f\sigma_8\\) from the ZTF and Rubin-LSST SN Ia samples. In the near term, I am applying this framework to the TITAN/ATLAS sample to measure \\(f\sigma_8\\) from SN Ia peculiar velocities.
