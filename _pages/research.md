---
layout: page
permalink: /research/
title: Research
nav: false
---

My research is centered on the use of Type Ia supernovae (SNe Ia) to constrain cosmological parameters, with a particular focus on large-scale structure. Most of my work is dedicated to the measurement of the growth of structure, \\(f\sigma_8\\), with SNe Ia, and to the effect of host-galaxy peculiar velocities as a systematic in SN Ia cosmology. I am a member of the Zwicky Transient Facility (ZTF) SN Ia cosmology group, of the LSST Dark Energy Science Collaboration (DESC), and of the Dark Energy Bedrock All-Sky Supernova (DEBASS) program.

## Growth of structure with SNe Ia

The growth of structure, \\(f\sigma_8\\), quantifies how matter overdensities evolve in our Universe. Since this evolution is governed by the balance between gravity and cosmic expansion, measuring \\(f\sigma_8\\) not only tests the standard cosmological model, but also helps to discriminate between the main candidates for new physics: dynamical dark energy and modified gravity.

At low redshift, \\(f\sigma_8\\) can be measured from the peculiar velocities (PVs) of galaxies, which are their own motions with respect to the Hubble flow. These velocities can be estimated by combining the spectroscopic redshift of a galaxy with a precise distance, such as the one given by a SN Ia on the Hubble diagram.

<div class="row justify-content-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/research/pv-hubble-diagram-toy-model.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Effect of the peculiar velocity of the host galaxy on the position of a SN Ia in the Hubble diagram (from Carreres et al. 2023)." %}
  </div>
</div>

Until recently, this measurement was not possible with SNe Ia because of the small number of low-redshift SNe Ia, with only ~200 of them in the DES 5-year cosmology analysis. The new generation of all-sky surveys, ZTF and the Rubin Observatory Legacy Survey of Space and Time (Rubin-LSST), will deliver tens of thousands of low-redshift SNe Ia and allow precise constraints on \\(f\sigma_8\\) with SNe Ia for the first time.

### Forecasts for ZTF

During my PhD, I adapted the maximum likelihood method, previously used with galaxy surveys, to SN Ia data, and I developed an end-to-end pipeline from the simulation of the ZTF sample to the measurement of \\(f\sigma_8\\). For this purpose, I wrote the [`snsim`](https://github.com/bastiencarreres/snsim) library, which simulates SN Ia surveys on top of an N-body simulation to include realistic clustering and velocities, along with the observing conditions and the spectroscopic selection of ZTF. Using 27 realizations of 6 years of the ZTF survey, I showed that the spectroscopic selection biases \\(f\sigma_8\\) when including SNe Ia above \\(z \sim 0.06\\), and that below this cut ZTF can constrain \\(f\sigma_8\\) at the 19% level ([Carreres et al. 2023](https://arxiv.org/abs/2303.01198)).

<div class="row justify-content-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/research/ztf-forecast-fs8-precision.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Constraints on the growth rate from 27 realizations of 6 years of ZTF data (0.02 < z < 0.06)." %}
  </div>
</div>

### Systematics for Rubin-LSST

At Duke, I studied the impact of SN Ia intrinsic scatter on the \\(f\sigma_8\\) measurement, and the use of the BEAMS with Bias Corrections (BBC) framework employed in the DES 5-year analysis. I simulated the 10 years of the Rubin-LSST survey at low redshift, with a realistic velocity field and correlations between SN Ia and host-galaxy properties. I found that, for the most realistic dust-based model, the non-Gaussian distribution of the Hubble diagram residuals causes a bias of ~20% on \\(f\sigma_8\\). The error budget is dominated by the statistical error (~75% of the total), while the systematics are currently dominated by the modeling of redshift-space distortions in the velocity field ([Carreres et al. 2025b](https://arxiv.org/abs/2505.13290)).

<div class="row justify-content-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/research/lsst-scatter-fs8-results.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Recovered growth rate for four intrinsic scatter models, averaged over eight LSST realizations. The dust-based model (P23) is biased by about −20%." %}
  </div>
</div>

With colleagues, I also forecasted that Rubin-LSST will measure \\(f\sigma_8\\) at the ~10% level, with the first competitive constraints after ~3 years of the survey ([Rosselli, Carreres et al. 2025](https://doi.org/10.1051/0004-6361/202556181)). These analyses rely on [`flip`](https://github.com/corentinravoux/flip), a Python package that I co-develop, which provides a modular framework to constrain \\(f\sigma_8\\) from velocity and density data ([Ravoux, Carreres et al. 2025](https://doi.org/10.1051/0004-6361/202554319)).

### Towards a measurement with real data

Although forecasts show a great potential, no robust measurement of \\(f\sigma_8\\) with SNe Ia has yet been achieved with the complexities of real data. I am currently working on the TITAN SN Ia sample from the Asteroid Terrestrial-impact Last Alert System (ATLAS), one of the largest low-redshift SN Ia samples to date, for which I will perform the \\(f\sigma_8\\) measurement. I forecasted that ATLAS could constrain \\(f\sigma_8\\) at the ~20–25% level, already competitive with galaxy surveys. This measurement will also provide a first data-driven systematic error budget for \\(f\sigma_8\\) before Rubin-LSST. I am also leading the \\(f\sigma_8\\) measurement with the DEBASS sample.

## Peculiar velocities as a systematic

PVs are also a source of systematic uncertainty in the Hubble diagram, and the smaller the redshift, the larger the effect is. Using simulations of ZTF, I showed that PVs need to be described by their full covariance matrix rather than by a diagonal term, as was done in previous analyses. For the ZTF SN Ia DR2 sample, neglecting PV correlations shifts \\(H_0\\) by ~1 km s<sup>−1</sup> Mpc<sup>−1</sup> and underestimates its uncertainty ([Carreres et al. 2025a](https://arxiv.org/abs/2405.20409)).

<div class="row justify-content-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/research/ztf-dr2-hubble-fit-pv-covariance.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Hubble diagram fit of the ZTF SN Ia DR2 sample without PVs (blue), with a diagonal PV error term (yellow), and with the full PV covariance (red)." %}
  </div>
</div>

The complete list of my publications is available on the [publications page]({{ '/publications/' | relative_url }}).
