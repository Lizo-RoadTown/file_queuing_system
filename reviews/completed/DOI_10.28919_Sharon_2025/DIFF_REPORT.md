# Diff report — STOCHASTIC DIFFERENTIAL EQUATIONS FOR SIR MALARIA MODEL

**Curator:** @Jamaal Porchia  
**Reviewer:** @lmmaganto  
**DOI:** https://doi.org/10.28919/cmbn/9452  
**Figure:** 2  
**Generated:** 2026-04-23 00:41 UTC  

---

## Summary

| | Count |
|---|---|
| Cells compared | 4 |
| Cells agreed | 3 |
| Cells with differences | 1 |
| Total individual changes | 2 |

## Agreements (3 cells)

The following cells matched exactly between curator and reviewer.

---

## Differences (2 individual changes across 1 cells)

### Cell 1 — no citation

**Curator:**
```python
variable_names = [
    'Sh',
    'Ih',
    'Rh',
    'Sm',
    'Im',
    
]
"""Names of the variables in the SDE model. The order of the variables should be the same as the order of the drift and diffusion terms returned by the drift_term and diffusion_term functions."""

parameter_names = [
    'alpha_h',
    'alpha_m',
    'beta_h',
    'beta_m',
    'gamma_h',
    'rho_h',
    'delta_h',
    'pi_h',
    'pi_m',
    'sigma1',
    'sigma2',
    'sigma3',
    'sigma4',
    'sigma5'
]
"""Names of the parameters in the SDE model. The order of the parameters should be the same as the order of the values returned by the drift_term and diffusion_term functions."""

initial_values = dict(
    Sh=100.0,
    Ih=5.0,
    Rh=0.0,
    Sm=200.0,
    Im=10.0
   
)
"""Dictionary of initial values for the variables in the SDE model. The keys should be the variable names in variable_names and the values should be the initial values for those variables."""

parameter_values = dict(
    alpha_h=0.05,
    alpha_m=0.06,
    beta_h=0.01,
    beta_m=0.05,
    gamma_h=0.09,
    rho_h=0.0001,
    delta_h=0.1,
    pi_h=2.5,
    pi_m=125,
    sigma1=0.05,
    sigma2=0.05,
    sigma3=0.05,
    sigma4=0.05,
    sigma5=0.05
)
"""Dictionary of values for the parameters in the SDE model. The keys should be the parameter names in parameter_names and the values should be the values for those parameters."""

initial_time = 0.0
"""Initial time to simulate during testing and curation of the SDE model."""

final_time = 100.0
"""Final time to simulate during testing and curation of the SDE model."""


def drift_term(t, y, p):
    """The drift term(s) of the SDE model

    Args:
        t: current time
        y: current values of the variables in the same order as variable_names
        p: current values of the parameters in the same order as parameter_names
    Returns:
        list: The drift term(s) of the SDE model in the same order as variable_names
    """
    Sh, Ih, Rh, Sm, Im = y

    alpha_h, alpha_m, beta_h, beta_m, gamma_h, rho_h, delta_h, pi_h, pi_m, sigma1, sigma2, sigma3, sigma4, sigma5 = p

    dSh = (-alpha_h * Sh - beta_h * Sh * Im + pi_h)
    dIh = -(alpha_h + gamma_h + rho_h - delta_h) * Ih + beta_h * Sh * Im
    dRh = (-alpha_h * Rh + gamma_h * Ih)
    dSm = (-alpha_m * Sm - beta_m * Sm * Ih + pi_m)
    dIm = (-alpha_m * Im + beta_m * Sm * Ih)

    return[dSh, dIh, dRh, dSm, dIm]


def diffusion_term(t, y, p):
    """The diffusion term(s) of the SDE model

    Args:
        t: current time
        y: current values of the variables in the same order as variable_names
        p: current values of the parameters in the same order as parameter_names
    Returns:
        list: The diffusion term(s) of the SDE model in the same order as variable_names
    """
    Sh, Ih, Rh, Sm, Im = y

    alpha_h, alpha_m, beta_h, beta_m, gamma_h, rho_h, delta_h, pi_h, pi_m, sigma1, sigma2, sigma3, sigma4, sigma5 = p
    
    diff_Sh = -sigma1 * Sh * Im
    diff_Ih = sigma2 * Sh * Im
    diff_Rh = -sigma3 * Rh
    diff_Sm = -sigma4 * Sm * Ih
    diff_Im = sigma5 *Sm * Ih

    return[diff_Sh, diff_Ih, diff_Rh, diff_Sm, diff_Im]
```

**Reviewer:**
```python
variable_names = [
    'Sh',
    'Ih',
    'Rh',
    'Sm',
    'Im',
    'X'
    
]
"""Names of the variables in the SDE model. The order of the variables should be the same as the order of the drift and diffusion terms returned by the drift_term and diffusion_term functions."""

parameter_names = [
    'alpha_h',
    'alpha_m',
    'beta_h',
    'beta_m',
    'gamma_h',
    'rho_h',
    'delta_h',
    'pi_h',
    'pi_m',
    'sigma1',
    'sigma2',
    'sigma3',
    'sigma4',
    'sigma5'
]
"""Names of the parameters in the SDE model. The order of the parameters should be the same as the order of the values returned by the drift_term and diffusion_term functions."""

initial_values = dict(
    Sh=100.0,
    Ih=5.0,
    Rh=0.0,
    Sm=200.0,
    Im=10.0
    X = 50
   
)
"""Dictionary of initial values for the variables in the SDE model. The keys should be the variable names in variable_names and the values should be the initial values for those variables."""

parameter_values = dict(
    alpha_h=0.05,
    alpha_m=0.06,
    beta_h=0.01,
    beta_m=0.05,
    gamma_h=0.09,
    rho_h=0.0001,
    delta_h=0.1,
    pi_h=2.5,
    pi_m=125,
    sigma1=0.05,
    sigma2=0.05,
    sigma3=0.05,
    sigma4=0.05,
    sigma5=0.05
)
"""Dictionary of values for the parameters in the SDE model. The keys should be the parameter names in parameter_names and the values should be the values for those parameters."""

initial_time = 0.0
"""Initial time to simulate during testing and curation of the SDE model."""

final_time = 100.0
"""Final time to simulate during testing and curation of the SDE model."""


def drift_term(t, y, p):
    """The drift term(s) of the SDE model

    Args:
        t: current time
        y: current values of the variables in the same order as variable_names
        p: current values of the parameters in the same order as parameter_names
    Returns:
        list: The drift term(s) of the SDE model in the same order as variable_names
    """
    Sh, Ih, Rh, Sm, Im = y

    alpha_h, alpha_m, beta_h, beta_m, gamma_h, rho_h, delta_h, pi_h, pi_m, sigma1, sigma2, sigma3, sigma4, sigma5 = p

    dSh = (-alpha_h * Sh - beta_h * Sh * Im + pi_h)
    dIh = -(alpha_h + gamma_h + rho_h - delta_h) * Ih + beta_h * Sh * Im
    dRh = (-alpha_h * Rh + gamma_h * Ih)
    dSm = (-alpha_m * Sm - beta_m * Sm * Ih + pi_m)
    dIm = (-alpha_m * Im + beta_m * Sm * Ih)

    return[dSh, dIh, dRh, dSm, dIm]


def diffusion_term(t, y, p):
    """The diffusion term(s) of the SDE model

    Args:
        t: current time
        y: current values of the variables in the same order as variable_names
        p: current values of the parameters in the same order as parameter_names
    Returns:
        list: The diffusion term(s) of the SDE model in the same order as variable_names
    """
    Sh, Ih, Rh, Sm, Im = y

    alpha_h, alpha_m, beta_h, beta_m, gamma_h, rho_h, delta_h, pi_h, pi_m, sigma1, sigma2, sigma3, sigma4, sigma5 = p
    
    diff_Sh = -sigma1 * Sh * Im
    diff_Ih = sigma2 * Sh * Im
    diff_Rh = -sigma3 * Rh
    diff_Sm = -sigma4 * Sm * Ih
    diff_Im = sigma5 *Sm * Ih

    return[diff_Sh, diff_Ih, diff_Rh, diff_Sm, diff_Im]
```

**Changes (2):**

1. `'X'` - made up testing my script
2. `X = 50` - made up ignore

---

## Curator notification

@Jamaal Porchia - your submission has been second reviewed by @lmmaganto.

2 change(s) were made across 1 cell(s):

- `'X'` - made up testing my script
- `X = 50` - made up ignore
