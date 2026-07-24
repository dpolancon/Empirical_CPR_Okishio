---
schema_version: 2
id: "i2-trap-validation-walkthrough"
title: "I(2) Trap Validation Walkthrough"
type: "validation-report"
status: "under-review"
aliases: ["I2 Trap Validation Walkthrough", "I(2) Trap Audit Walkthrough"]
tags: ["econometrics", "i2-trap", "validation-report"]
created: "2026-07-24"
updated: "2026-07-24"
last_reviewed: "2026-07-24"
source_snapshots: ["e-00-i2-trap", "e-01-i2-trap"]
audit_questions: ["1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "3.1", "3.2", "3.3", "4.1", "4.2", "4.3", "5.1", "5.2", "5.3", "6.1", "6.2", "6.3"]
theory_tasks: ["t01-cross-product-limit", "t02-normalized-design-and-rates", "t03-estimator-extension", "t04-transformed-fwl", "t05-cpr-residual-testing", "t06-state-dependent-inference"]
concepts: ["i2-trap", "polynomial-cointegration", "im-ols-framework", "fwl-orthogonalization", "cpr-cointegration-testing", "state-dependent-inference"]
---
# I(2) Trap Validation Walkthrough

## Current bottom line

This report examines whether the model

$$
y_t=a+b k_t+f\omega_t+d(k_t\omega_{t-1})+u_t
$$

can be estimated and tested by treating $k_t\omega_{t-1}$ as an ordinary
$I(2)$ regressor. The answer is no. The product has degree-two polynomial
scaling when $k_t$ and $\omega_t$ are $I(1)$, but that fact does not make
its second difference generically stationary. Calling the product
“classically $I(2)$” hides the distinction that drives the normalization,
rank conditions, estimator transformation, and critical values.

The local work supports three corrections. T01 establishes the product and
partial-sum limits; T02 establishes the mixed-rate normalization conditional
on a full-rank stochastic design; and T04 proves that Frisch–Waugh–Lovell
(FWL) residualization must occur inside the transformed design. T03, T05, and
T06 remain open. Their proposed IM-OLS extension, residual test, and
state-dependent inference are coherent research procedures, but the current
smoke simulations do not satisfy the predeclared agreement and calibration
gates. No result in this report upgrades the method to peer-reviewed or
empirically production-ready status.

## What is being validated

The disputed term is $q_t=k_t\omega_{t-1}$, where $k_t$ is capital and
$\omega_t$ is the wage share. The coefficient $d$ measures how the wage
share conditions the long-run capital effect. At a fixed state $s$, the
capital elasticity is

$$
\theta(s)=b+ds,
$$

and the inefficiency gap is

$$
\Gamma(s)=1-s-\theta(s)=1-b-(1+d)s.
$$

The original notes made linked claims about the integration order of $q_t$,
the applicability of DOLS, FM-OLS, and IM-OLS, the order of FWL operations,
the scaling of a residual partial-sum test, and inference for $\theta(s)$
and $\Gamma(s)$. Validation therefore cannot stop at a unit-root label. It
must follow the complete chain from stochastic order to design rank,
estimator limit, test calibration, and economic interpretation.

The integration-order gate is binding. A theoretically meaningful
distributional interaction does not enter the long-run model until the data
support its stochastic specification. In an empirical application, the
researcher must test $k_t$, $\omega_t$, and $q_t$ directly, report the
deterministic terms and lag choices, and block designs with correlations above
0.99 or condition numbers above 30 pending a specific rank analysis. The
current simulations study the mathematical design; they do not replace those
data diagnostics.

## Evidence ladder

The validation uses four levels of evidence, in descending order of authority:

1. Peer-reviewed linear IM-OLS and cointegrating-polynomial results define the
   available foundation. They do not automatically prove the new
   cross-product extension.
2. Independent local derivations check the functional limits, normalization,
   FWL algebra, residual statistic, and state contrasts.
3. Reproducible simulations expose finite-sample behavior at
   $T=\{40,50,60,80,100,120,200,500,1000\}$.
4. The historical NotebookLM ledger supplies a structured source audit. It is
   evidence to inspect, not authority to copy into a canonical claim.

The audit asked 18 questions in six phases. Every proposed validation metric
failed. That historical result identifies where the notes require correction;
it does not by itself constitute a theorem. A claim changes status only when
the local derivation and simulation record support the same conclusion.

## Step-by-step validation

### Step 0 — Freeze the object under review

The two source snapshots remain byte-for-byte immutable. Their manifest stores
the original paths, NotebookLM identifiers, and SHA-256 hashes. The
NotebookLM master ledger is also append-only and separately hashed. This
prevents a corrected concept note from silently replacing the claim that the
audit actually tested.

**Decision:** provenance passes. The validation can distinguish original
claims, machine-generated criticism, and later human-reviewed corrections.

### Step 1 — Classify the cross-product before choosing an estimator

For jointly $I(1)$ regressors with a functional central limit theorem,

$$
T^{-1}k_{\lfloor Tr\rfloor}\omega_{\lfloor Tr\rfloor-1}
\Rightarrow B_k(r)B_\omega(r),
$$

while the accumulated product satisfies

$$
T^{-2}\sum_{t=1}^{\lfloor Tr\rfloor}k_t\omega_{t-1}
\Rightarrow\int_0^r B_k(s)B_\omega(s)\,ds.
$$

Thus $q_t=O_p(T)$ and its partial sum is $O_p(T^2)$. The original
$O_p(T^{3/2})$ partial-sum claim is incorrect. The safe description is a
degree-two polynomial transform of integrated regressors, not an unqualified
classical $I(2)$ process. Questions 1.1–1.3 correctly exposed the
conflation, but T01 supplies the local derivation that resolves it.

This result is conditional. A stationary $\omega_t$, cointegration between
$k_t$ and $\omega_t$, or singular common-trend innovations changes the
effective dimension and can invalidate the stated design.

**Decision:** T01 is locally resolved as qualified. Rewrite the integration
claim; do not delete the exceptional cases.

### Step 2 — Normalize the complete design and test rank

For

$$
z_t=(1,k_t,\omega_t,k_t\omega_{t-1})',
$$

the appropriate column normalization is

$$
D_T=\operatorname{diag}(1,T^{1/2},T^{1/2},T).
$$

The resulting coefficient-error rates are $T^{-1/2}$ for the intercept,
$T^{-1}$ for the two level coefficients, and $T^{-3/2}$ for the
interaction coefficient. This mixed-rate structure rejects any calculation
that assigns the same $\sqrt T$ rate to all coefficients.

Normalization does not create rank. The limit Gram matrix must be positive
definite after accounting for deterministic terms and the stochastic-trend
dimension. Cointegrated regressors, a single common trend, stationary
$\omega_t$, or weak interaction variation require a different model or an
explicit unsupported-design verdict. A generalized inverse is not a
substitute for identified inference.

**Decision:** T02 is locally resolved as qualified. The derived rates are
usable only after the full-rank gate passes.

### Step 3 — Evaluate the proposed cross-product IM-OLS estimator

The local extension accumulates the dependent variable and regressors while
leaving the innovation projection terms unaccumulated:

$$
Y_t=at+bK_t+fW_t+dZ_t
    +\lambda_k k_t+\lambda_\omega\omega_t+\varepsilon_t,
$$

where $K_t=\sum_{j\le t}k_j$, $W_t=\sum_{j\le t}\omega_j$, and
$Z_t=\sum_{j\le t}k_j\omega_{j-1}$. The product stays inside the full
transformed design. The working coefficient normalization for
$(a,b,f,d)$ is

$$
R_T=\operatorname{diag}(T^{1/2},T,T,T^{3/2}).
$$

This construction corrects the notes’ description of linear IM-OLS:
augmentation terms absorb long-run correlation; the method does not work
because endogeneity “vanishes” after cumulation. It also leaves the stationary
wage-share branch outside the theorem. That branch remains diagnostic-only.

The smoke profile used 250 outer replications and 99 bootstrap draws per
replication. In the regular $\rho=0.5$, AR(1) $=0.5$ design, fixed-$b$
95% coverage across the four coefficients ranged from 90.4% to 95.2% at
$T=50$, with Monte Carlo standard errors (MCSEs) of 1.35–1.86 percentage
points, and from 92.0% to 95.2% at $T=100$, with MCSEs of 1.35–1.72 points.
Moving-block bootstrap coverage ranged from 82.0% to 94.0% at $T=50$
(MCSE 1.50–2.43 points) and from 81.2% to 90.8% at $T=100$ (MCSE
1.83–2.47 points). The two procedures therefore disagree by more than the
predeclared five-percentage-point small-sample tolerance. Smoke results are
diagnostic and cannot promote a task even when an individual number falls
inside a target interval.

**Decision:** T03 remains open. The estimator is a locally specified research
extension, not a validated replacement for standard IM-OLS.

### Step 4 — Apply FWL in the correct order

Let $S$ denote the partial-sum transformation and $M_X$ the residual-maker
for nuisance regressors $X$. In general,

$$
SM_X\neq M_{SX}S.
$$

Residualizing $q_t$ in levels and then accumulating the residual does not
produce the same transformed regressor as accumulating the complete design
and applying FWL there. Questions 4.1–4.3 identified this noncommutation. The
local algebra and numerical identity checks confirm that FWL itself still
holds when both regressions use exactly the same transformed design.

**Decision:** T04 is locally proved. Orthogonalization may improve numerical
presentation, but it cannot change the estimator or rescue a rank-deficient
design.

### Step 5 — Calibrate the residual cointegration test

Using level residuals from T03,

$$
\widehat u_t
=y_t-\widehat a-\widehat b k_t-\widehat f\omega_t
 -\widehat d k_t\omega_{t-1},
$$

the candidate statistic is

$$
J_T=
\frac{T^{-2}\sum_{t=1}^T
\left(\sum_{j=1}^t\widehat u_j\right)^2}
{\widehat\Omega_{u\cdot v}}.
$$

The $T^{-2}$ numerator scaling follows the cointegration-null residual
partial-sum order; the notes’ $T^{-4}$ alternative is not supported.
Critical values cannot be imported from a standard residual test because
estimating the mixed-rate polynomial design changes the limiting projection.

The smoke null rejection rates show the practical problem. At nominal 5%,
fixed-$b$ and bootstrap rejection rates were 11.2% (MCSE 1.99 points) and
2.4% (0.97) at $T=50$, 8.4% (1.75) and 5.2% (1.40) at $T=100$, and
8.4% (1.75) and 6.0% (1.50) at $T=500$. Only some cells fall inside the
prescribed size interval, and the two methods do not agree uniformly.

**Decision:** T05 remains open. Report both calibrations; do not select the
more favorable method after observing the result.

### Step 6 — Separate fixed-state and stochastic-state inference

At a fixed policy state $s_0$, inference for $\theta(s_0)=b+ds_0$ uses the
linear contrast $(0,1,0,s_0)$. The fixed-state gap is also linear. It is not
a nonlinear delta-method problem. When $s_t=\omega_{t-1}$ is integrated,
the state is stochastic and must enter the joint limit with all estimator–state
cross-covariances. The derivative

$$
\frac{\partial\Gamma(s)}{\partial s}=-(1+d)
$$

cannot be omitted. A uniform zero-gap path implies the joint restriction
$b=1$ and $d=-1$ when the state varies.

At $s_0=0.5$, fixed-$b$ versus bootstrap coverage for
$\theta(s_0)$ was 94.8% (MCSE 1.40 points) versus 83.2% (2.36) at
$T=50$, 91.6% (1.75) versus 86.8% (2.14) at $T=100$, and 96.4% (1.18)
versus 89.6% (1.93) at $T=500$. Conditional path-band coverage was 92.8%
(MCSE 1.63), 96.0% (1.24), and 94.8% (1.40) at those sample sizes, while
unconditional coverage was 98.8% (0.69), 100% (0), and 100% (0). The
unconditional band is strongly conservative in this smoke design.

**Decision:** T06 remains open. Fixed-state formulas are corrected, but
stochastic-state and pathwise inference are not locally calibrated.

## Claim disposition

| Original or implied claim | Forensic finding | Current disposition |
|---|---|---|
| The product of two $I(1)$ series is automatically classical $I(2)$. | It has degree-two polynomial scaling, but its second difference is not generically stationary. | Refuted as stated; replace with the qualified T01 result. |
| $\sum k_t\omega_{t-1}=O_p(T^{3/2})$. | The functional limit uses $T^{-2}$, so the partial sum is $O_p(T^2)$. | Refuted. |
| Additive CPR or linear IM-OLS theory automatically covers the product. | The cross-product changes rates, rank conditions, projection terms, and critical values. | Unsupported without T03–T06. |
| DOLS necessarily becomes asymptotically singular. | Regressor proliferation is a finite-sample degrees-of-freedom problem, not a general asymptotic rank theorem. | Refuted as a general claim. |
| FM-OLS long-run covariance should contain the nonstationary interaction level. | Long-run covariance corrections use stationary innovations or differences, not nonstationary levels. | Refuted. |
| Residualize the interaction first, then cumulate it. | Partial summation and residualization do not commute. | Refuted; use the complete transformed design. |
| The same IM-OLS transform is valid whether $\omega_t$ is $I(0)$ or $I(1)$. | The current theorem targets the $I(1)$ branch; the $I(0)$ branch has different scaling. | Unsupported; retain as diagnostic-only. |
| Standard residual-test critical values are adequate. | The estimated mixed-rate design changes the null projection and finite-sample calibration. | Refuted. |
| The residual partial-sum-square numerator needs $T^{-4}$ scaling. | Under cointegration, the locally derived statistic uses $T^{-2}$. | Refuted; T05 calibration remains open. |
| $\theta(s)$ always has a $\sqrt T$ limit. | Its rate follows the mixed-rate covariance of $b$ and $d$, and an integrated $s_t$ adds state uncertainty. | Refuted. |
| $\operatorname{Var}\{\Gamma(s)\}=\operatorname{Var}\{\theta(s)\}$. | This holds only when $s$ is fixed and treated as known. | Qualified. |

The table maps the specification space rather than hiding failed branches.
It preserves theoretically meaningful distributional conditioning while
letting stochastic evidence determine whether its observable proxy is
admissible in a long-run regression.

## Operational decision sequence

Use the following sequence before estimating the empirical model:

1. Plot $k_t$, $\omega_t$, $q_t=k_t\omega_{t-1}$, and their first
   differences. Mark institutional breaks and explain missing observations or
   exclusions before fitting a long-run model.
2. Test levels and first differences with at least two complementary
   procedures, such as ADF and KPSS. Test $q_t$ directly rather than
   inferring its order only from its components.
3. Map alternative deterministic terms, break treatments, and lag choices.
   Retain failed specifications in the record.
4. Compute pairwise correlations, the normalized Gram eigenvalues, and the
   condition number. A correlation above 0.99 or condition number above 30
   blocks automatic promotion and triggers a specific rank investigation.
5. If the $I(1)$, full-rank branch survives, estimate the complete
   transformed design. Do not residualize the product before transformation.
6. Report fixed-$b$ and re-estimated block-bootstrap inference side by side.
   If their difference exceeds five percentage points near $T=50$ or
   $T=100$, classify the empirical conclusion as inconclusive.
7. Treat $\theta(s)$ and $\Gamma(s)$ as fixed-state contrasts only when
   $s$ is genuinely fixed. Otherwise use joint state–estimator inference.
8. Interpret $d$ as a distribution-conditioned capital effect, not as a
   neutral interaction coefficient. A regime change in $d$ may reflect a
   change in the institutional relation between distribution, utilization,
   and accumulation; it does not by itself identify a causal mechanism.

The current stop rules are simple: do not use the extension after a rank
failure; do not claim validity for the stationary wage-share branch; do not
use standard CPR critical values; and do not promote T03, T05, or T06 while
their calibration gates remain unmet.

## Reproducing the validation

Run the repository checks from the project root:

```powershell
python -m pytest -q
python code\validate_note_repository.py
```

Reproduce the non-promotional T03–T06 smoke evidence with:

```powershell
python -m code.theory.run --task t03 t05 t06 --profile smoke --sample-grid all --workers 3
```

The committed compact evidence consists of the run manifest, estimator and
rate summaries, rank diagnostics, residual-test critical values and
size–power tables, fixed-state results, and path-band results. Raw Monte Carlo
draws remain ignored. The preregistered full profile requires 10,000
replications, 200,000 Brownian limit draws, and the prescribed nested
bootstraps. It has not passed, so this walkthrough must not quote the smoke
tables as final calibration.

## Review checklist

- [ ] Verify the snapshot and ledger hashes before changing a verdict.
- [ ] Define every symbol when it first appears in the empirical chapter.
- [ ] Show raw paths and historical discontinuities before the parametric
      results.
- [ ] Report direct integration-order evidence for the product.
- [ ] Report the full normalized-design rank diagnostics.
- [ ] Keep all estimation and FWL operations inside the same transformed
      design.
- [ ] Display fixed-$b$ and bootstrap results together, including Monte Carlo
      standard errors.
- [ ] Separate fixed-state, observed-path, and unconditional inference.
- [ ] Record failed specifications and disputed claims rather than deleting
      them.
- [ ] Keep T03, T05, and T06 open until the full simulation gates and the
      scholarly closure rule are met.

## Related notes

- [E_00 I(2) Trap](../sources/snapshots/i2-trap/e-00-i2-trap.md) · [[e-00-i2-trap|E_00 I(2) Trap]]
- [E_01 I(2) Trap](../sources/snapshots/i2-trap/e-01-i2-trap.md) · [[e-01-i2-trap|E_01 I(2) Trap]]
- [I(2) Trap](../concepts/i2-trap.md) · [[i2-trap|I(2) Trap]]
- [Polynomial Cointegration](../concepts/polynomial-cointegration.md) · [[polynomial-cointegration|Polynomial Cointegration]]
- [IM-OLS Framework](../concepts/im-ols-framework.md) · [[im-ols-framework|IM-OLS Framework]]
- [FWL Orthogonalization](../concepts/fwl-orthogonalization.md) · [[fwl-orthogonalization|FWL Orthogonalization]]
- [CPR Cointegration Testing](../concepts/cpr-cointegration-testing.md) · [[cpr-cointegration-testing|CPR Cointegration Testing]]
- [State-Dependent Inference](../concepts/state-dependent-inference.md) · [[state-dependent-inference|State-Dependent Inference]]
- [T01 Cross-Product Limit](../theory/tasks/t01-cross-product-limit.md) · [[t01-cross-product-limit|T01 Cross-Product Limit]]
- [T02 Normalized Design and Rates](../theory/tasks/t02-normalized-design-and-rates.md) · [[t02-normalized-design-and-rates|T02 Normalized Design and Rates]]
- [T03 Estimator Extension](../theory/tasks/t03-estimator-extension.md) · [[t03-estimator-extension|T03 Estimator Extension]]
- [T04 Transformed FWL](../theory/tasks/t04-transformed-fwl.md) · [[t04-transformed-fwl|T04 Transformed FWL]]
- [T05 CPR Residual Testing](../theory/tasks/t05-cpr-residual-testing.md) · [[t05-cpr-residual-testing|T05 CPR Residual Testing]]
- [T06 State-Dependent Inference](../theory/tasks/t06-state-dependent-inference.md) · [[t06-state-dependent-inference|T06 State-Dependent Inference]]
- [Canonical NotebookLM audit](../evidence/notebooklm/econometric-audit-master.md)
- [Simulation run manifest](../theory/results/run-manifest.json)
- [T03 estimator summary](../theory/results/t03-imols-summary.csv)
- [T05 size and power](../theory/results/t05-size-power.csv)
- [T06 fixed-state inference](../theory/results/t06-fixed-state-inference.csv)
- [T06 path-band coverage](../theory/results/t06-path-band-coverage.csv)
