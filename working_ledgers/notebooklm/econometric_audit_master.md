---
type: econometric_audit_master
status: complete
notebook_id: "b0c5603e-e34a-4c97-b436-8577da5280eb"
notebook_title: "CPR Co-integration IM-OLS"
notebook_source_count: 14
source_intelligence_count: 13
excluded_source_ids: ["e6c4625f-929b-4531-8256-9124deac419e"]
source_clusters: [1, 2, 3, 4, 5, 6]
partition_key: audit_phase
---
# Econometric Audit Master Ledger

| Field | Value |
|---|---|
| NotebookLM notebook ID | `b0c5603e-e34a-4c97-b436-8577da5280eb` |
| Generated | 2026-07-23T19:50:09-04:00 |
| Ready notebook sources | 14 |
| Source-intelligence threads | 13 |
| Excluded from every query | Bridging comparative and international political economy for the study of industrial policy beyond the hegemons  Introduction to special issue.pdf |
| Source clusters | `cluster_1.csv` through `cluster_6.csv` |
| Partition contract | Stable HTML boundary markers around every phase and question |

<!-- SOURCE_INTELLIGENCE_START -->
## Source Intelligence Baseline

Each source below was queried in a clean, source-restricted NotebookLM thread.

<!-- SOURCE_INTELLIGENCE_ITEM_START index="1" source_id="c96685a6-db4f-40f2-975b-fe53312d9e03" -->
### Source 01 — Dissertation_Grabarczyk.pdf

| Source field | Value |
|---|---|
| NotebookLM source ID | `c96685a6-db4f-40f2-975b-fe53312d9e03` |
| Source type | `SourceType.PDF` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

The provided sources do not contain information on validating Cointegrating Polynomial Regressions (CPR) with **$I(2)$ interactive terms**. The text explicitly models regressors strictly as **$I(1)$ processes**, noting that their integer powers are not integrated themselves, and explicitly excludes generic cross-product interactive terms unless required to resolve specific mathematical mappings [1-3]. 

Focusing instead on the paper's actual contributions to validating CPRs involving powers and required cross-products of **$I(1)$** processes, the 3 most critical mechanics are:

*   **Asymptotic Equivalence of "Standard" FM-OLS (FM-LIN) and FM-CPR Estimator Transformations:** The author demonstrates that naively applying linear cointegration transformations—incorrectly treating $I(1)$ polynomial terms as distinct standard integrated regressors—is actually asymptotically equivalent to the tailor-made FM-CPR estimator [4, 5]. The FM-LIN estimator utilizes the transformation $\hat{\theta}^{++} = (Z'Z)^{-1}(Z'y^{++} - A^{**})$, where the modified dependent variable $y^{++}_t$ and the bias-correction matrix $A^{**}$ are scaled using the long-run covariance of a pseudo-differenced process $w_t$ [6, 7]. Through these transformations, both estimators ultimately share the exact same zero-mean Gaussian mixture limiting distribution: $G^{-1}(\hat{\theta}^{++} - \theta) \Rightarrow (\int_0^1 J(r)J(r)'dr)^{-1} \int_0^1 J(r)dB_{u\cdot v}(r)$ [8].
*   **Rank Conditions for "Full Design" in IM-OLS Asymptotic Mechanics:** The paper establishes that validating Integrated Modified OLS (IM-OLS) inference in multivariate CPRs demands a strict **"full design" rank condition** to achieve a nuisance-parameter-free fixed-$b$ limit [9, 10]. Without interactive terms, the transformation matrix $F(\Omega_{vv})$ linking underlying standard Brownian motions $W_v(r)$ to the stacked polynomial Brownian motions $B_v(r)$ fails to be bijective if the long-run covariance $\lambda_{12} \neq 0$ [10, 11]. By explicitly introducing specific $I(1)$ interactive cross-products (e.g., $x_{1t}x_{2t}$) into the regression, $F(\Omega_{vv})$ achieves full rank, enabling the conditionally Gaussian limit: $A_{IM}^{-1}(\tilde{\theta} - \theta) \Rightarrow \omega_{u\cdot v}^{1/2} (\Pi')^{-1}(\int g(s)g(s)'ds)^{-1} \int [G(1)-G(s)]dw_{u\cdot v}(s)$ [10, 12].
*   **Estimator Transformations and Rank Conditions for Seemingly Unrelated CPRs (SUCPR):** To accommodate cross-sectional dependence and heterogeneous parameters across equations, the paper extends single-equation CPRs to SUCPR systems via long-run covariance-weighted transformations [13, 14]. The fully modified SUR (FM-SUR) estimator transforms the system as $\tilde{\theta} = (Z'(I_T \otimes \hat{\Omega}_{u\cdot v}^{-1})Z)^{-1}(Z'(I_T \otimes \hat{\Omega}_{u\cdot v}^{-1})y^+ - \tilde{A}^*)$ [15]. Because the polynomial parameters converge at differing rates, validating $\chi^2_s$-distributed Wald statistics for group-wise pooling requires a highly specific **asymptotic rank condition**: there must exist a scaling matrix $G_R$ such that the limit of the restriction matrix, $\lim_{T \to \infty} G_R R G = R^*$, ensures $R^*$ maintains a full row rank $s$ [16, 17].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="1" source_id="c96685a6-db4f-40f2-975b-fe53312d9e03" -->

<!-- SOURCE_INTELLIGENCE_ITEM_START index="2" source_id="99bc8d16-a831-403f-8ca9-f775523f4a38" -->
### Source 02 — E_00_I2_Trap.md

| Source field | Value |
|---|---|
| NotebookLM source ID | `99bc8d16-a831-403f-8ca9-f775523f4a38` |
| Source type | `SourceType.MARKDOWN` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

*   **Rank Conditions and Stochastic Trend Cancellation:** Validates the Cointegrating Polynomial Regression (CPR) framework by establishing the strict parameter conditions under which the distinct stochastic trends of the $I(1)$ constituent variables ($x_t$ and $y_{t-1}$) and the dominant stochastic trend of the $I(2)$ interaction term ($(x_t \cdot y_{t-1})$) perfectly cancel out in the long run [1]. This precise balancing of deterministic and stochastic components guarantees a stationary, mean-reverting residual process ($e_t$), effectively neutralizing the "I(2) trap" without requiring a full multi-equation Vector Autoregressive (VAR) framework [1-3].
*   **Estimator Transformations via Partial Sum Operators:** Details the mathematical adaptation of Integrated Modified OLS (IM-OLS) for non-linear interactive models through the application of a partial sum (integration) operator across the dependent variable and all regressors, explicitly including the $I(2)$ cross-product term [4-6]. This algebraic transformation implicitly absorbs serial correlation and endogeneity biases, providing a computationally elegant estimator that bypasses the necessity for explicit Long-Run Covariance (LRCV) matrix estimation or the severe multicollinearity induced by the explosion of leads and lags required in DOLS [4, 7, 8].
*   **Asymptotic Mechanics and Gaussian Mixture Limiting Distributions:** Formalizes the asymptotic validity of FM-OLS and DOLS by demonstrating how their criterion functions are modified to accommodate mixed-order regressors [9-11]. For FM-OLS, expanding the LRCV matrix to map the cross-covariances between the innovations of the $I(1)$ variables and the $I(2)$ interaction term ensures the estimator maintains a zero-mean Gaussian mixture limiting distribution, thereby securing the validity of standard asymptotic inference procedures [10]. For DOLS, the required asymptotic orthogonality to the error term is mechanically achieved by structurally augmenting the design matrix with leads and lags of the differenced interaction term, $\Delta(x_t \cdot y_{t-1})$, alongside $\Delta x_t$ and $\Delta y_{t-1}$ [5, 11].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="2" source_id="99bc8d16-a831-403f-8ca9-f775523f4a38" -->

<!-- SOURCE_INTELLIGENCE_ITEM_START index="3" source_id="0c9a6214-5241-4e81-bfab-2a1a343f702c" -->
### Source 03 — E_01_I2_Trap.md

| Source field | Value |
|---|---|
| NotebookLM source ID | `0c9a6214-5241-4e81-bfab-2a1a343f702c` |
| Source type | `SourceType.MARKDOWN` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

Here are the 3 most critical contributions from the sources for validating Cointegrating Polynomial Regressions (CPR) with $I(2)$ interactive terms:

*   **Rank Conditions for I(2) Cointegration within the CPR Framework:** The paper formally links the structural I(2) Vector Autoregressive (VAR) conditions to the polynomial cointegration space. For a system $\Delta^2 x_t = \Pi x_{t-1} - \Gamma \Delta x_{t-1} + \Psi(L)\Delta^2 x_{t-1} + \varepsilon_t$, the framework requires the cointegration rank to be $\text{rank}(\Pi) = r$ and the reduced rank condition $\text{rank}(\alpha'_\perp \Gamma \beta_\perp) = p - r - s$ (where $s$ denotes the number of I(2) trends) [1-3]. This validates that the structural product of $I(1)$ processes (e.g., $\tilde{k}_t \cdot \omega_{t-1}$) functions as an $I(2)$ quadratic trend, necessitating the expansion of the standard Johansen I(1) setup into a CPR representation where integrated variables can exhibit different integration orders ($I(1)$, $I(2)$, etc.) [3, 4].
*   **Estimator Transformations via IM-OLS and Orthogonalization (FWL):** To bypass the "I(2) trap"—which invalidates standard Fully Modified OLS (FM-OLS) through subjective Long-Run Covariance (LRCV) estimations and detonates Dynamic OLS (DOLS) via regressor explosion—the framework employs an Integrated Modified OLS (IM-OLS) estimator paired with residual centering [5-7]. The $I(2)$ interaction term is first orthogonalized against its linear components to extract the residual $\hat{u}_t$, eliminating multicollinearity while Frisch-Waugh-Lovell equivalence guarantees the coefficient $\hat{d}$ remains identical [6, 8-10]. The estimator then applies a partial sum operator $\tilde{x}_t = \sum_{s=1}^t x_s$, elevating the $I(2)$ regressor to $I(3)$ or $I(4)$, thus yielding a sparse design matrix devoid of nuisance parameters [11-13].
*   **Asymptotic Mechanics, FCLT, and Nuisance-Free Limit Theory:** The text establishes a rigorous Functional Central Limit Theorem (FCLT) mapping the partial sum of the $I(2)$ product $X_{1t} X_{2t}$ to an iterated stochastic integral $T^{-3/2} \sum X_{1t} X_{2t} \xrightarrow{w} \int_0^r W_{X1}(s) dW_{X2}(s) + \int_0^r W_{X2}(s) dW_{X1}(s)$ [14, 15]. Consequently, the IM-OLS estimator achieves extreme super-consistency, converging at a rate of $T^{-3/2}$ because the variance of the transformed integrated noise $\tilde{e}_t = O_p(T)$ is asymptotically negligible relative to the $O_p(T^7)$ growth of the transformed regressor $\tilde{\hat{u}}_t$ [12, 13, 16]. The resulting limiting distribution under fixed-$b$ asymptotics is nuisance-parameter-free: $T^{3/2} (\hat{d} - d) \xrightarrow{d} \left( \int_0^1 \tilde{W}_u(r)^2 dr \right)^{-1} \int_0^1 \tilde{W}_u(r) d\tilde{W}_e(r)$, guaranteeing the validity of standard $t$-statistics ($t_{\hat{d}} \xrightarrow{d} \mathcal{N}(0, 1)$) for hypothesis testing [17-19].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="3" source_id="0c9a6214-5241-4e81-bfab-2a1a343f702c" -->

<!-- SOURCE_INTELLIGENCE_ITEM_START index="4" source_id="a632dafd-0b06-4e54-a0a5-d1e61958e35f" -->
### Source 04 — EngleGranger-CoIntegrationErrorCorrection-1987.pdf

| Source field | Value |
|---|---|
| NotebookLM source ID | `a632dafd-0b06-4e54-a0a5-d1e61958e35f` |
| Source type | `SourceType.PDF` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

The provided source material does not contain information regarding Cointegrating Polynomial Regressions (CPR) or $I(2)$ interactive terms, as the authors explicitly restrict their analysis to linear combinations of $I(1)$ series and $I(0)$ equilibrium constraints [1]. 

However, regarding the foundational asymptotic mechanics, rank conditions, and estimator transformations relevant to co-integrated systems, the paper provides the following critical contributions:

*   **Rank Conditions in Moving Average Representations:** The Granger Representation Theorem establishes that if an $N \times 1$ vector $x_t \sim I(1)$ has a co-integrating rank of $r$, the matrix polynomial $C(1)$ in its Wold representation must have a reduced rank of $N - r$ [2]. For the equilibrium error $z_t = \alpha'x_t$ to achieve $I(0)$ stationarity, the co-integrating vector $\alpha$ must lie strictly in the null space of $C(1)$, requiring $\alpha'C(1) = 0$ [3]. 
*   **Asymptotic Mechanics of the Moment Matrix:** The sample moment matrix $M_T = T^{-2} \sum x_t x_t'$ converges to a finite, non-zero limiting matrix $M$ which asymptotically holds a rank of $N - r$ [4]. Because all linear combinations of $x_t$ exhibit infinite variance except those defined by co-integrating vectors, the relationship $\alpha'M = 0$ holds in the limit, allowing ordinary least squares to effectively isolate vectors with minimal residual variance [4-6].
*   **Two-Step Estimator Transformations and Convergence:** The paper introduces a transformation separating the long-run equilibrium estimation from short-run dynamics, proving that OLS estimators of the co-integrating vector $\hat{\alpha}$ converge highly rapidly to their probability limits with a finite sample bias of order $O(T^{-1})$ [7]. By treating $\hat{\alpha}$ as a known parameter, the resulting two-step estimator for the error correction model involves solely $I(0)$ terms and achieves the same limiting normal distribution as a maximum likelihood estimator that possesses true knowledge of $\alpha$ [8-12].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="4" source_id="a632dafd-0b06-4e54-a0a5-d1e61958e35f" -->

<!-- SOURCE_INTELLIGENCE_ITEM_START index="5" source_id="6f93d684-3ba3-4684-a95d-84d256c22c9b" -->
### Source 05 — Paurolo1996.pdf

| Source field | Value |
|---|---|
| NotebookLM source ID | `6f93d684-3ba3-4684-a95d-84d256c22c9b` |
| Source type | `SourceType.PDF` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

Here are the three most critical contributions from the provided text regarding the foundational mechanics, rank conditions, and transformations required for validating I(2) systems and polynomial cointegration:

*   **Rank Conditions for I(2) Integration Indices:** The paper establishes the precise reduced-rank conditions necessary for a vector autoregressive system to be integrated of order 2, which is foundational for defining polynomial cointegration spaces. It proves that the process $A(L)X_t = \mu + \varepsilon_t$ is I(2) if and only if the impact matrix $A(1)$ has reduced rank $p_0$ such that $A(1) = -\alpha\beta'$, and the transformed derivative matrix $\Gamma_{\alpha_\perp \beta_\perp} = \alpha_\perp' \dot{A}(1) \beta_\perp$ has reduced rank $p_1$ such that $\Gamma_{\alpha_\perp \beta_\perp} = \phi\eta'$ [1, 2]. This formally identifies the system's integration indices $p_0$, $p_1$, and $p_2 = p - p_0 - p_1$, partitioning the state space into orthogonal $I(0)$, $I(1)$, and $I(2)$ bases [1, 3].
*   **Two-Stage Estimator Transformations:** The study validates a sequential maximum likelihood procedure that transforms the complex I(2) interactions into nested reduced-rank regression (canonical correlation) problems [2, 4]. The first stage isolates the $I(0)$ parameters, yielding the estimators $\hat{\beta} = (v_1, \dots, v_{p_0})$ and $\hat{\alpha} = M_{02.1}\hat{\beta}(\hat{\beta}'M_{22.1}\hat{\beta})^{-1}$ [5, 6]. Conditional on $\hat{\alpha}$ and $\hat{\beta}$, the second stage isolates the $I(1)$ interaction parameters $\phi$ and $\eta'$ by solving a secondary generalized eigenvalue problem, specifically $|\rho M_{xx.\beta}^* - M_{x\bar{\alpha}_\perp.\beta}^* M_{\bar{\alpha}_\perp\bar{\alpha}_\perp.\beta}^{*-1} M_{\bar{\alpha}_\perp x.\beta}^*| = 0$, effectively decoupling the multicointegrating polynomial dependencies [7, 8].
*   **Asymptotic Mechanics of the Trace Statistics:** The paper proves that the likelihood ratio test statistics used to determine the I(2) ranks, specifically $_hQ(p_0)$ and $_hQ(p_1|p_0)$, converge weakly to nonstandard Limiting Gaussian Functional (LGF) distributions [9]. The asymptotic limits are represented by traces of stochastic integrals of Brownian motions, such as $\text{tr}\left\{\int_0^1 dBF' \left(\int_0^1 FF' du\right)^{-1} \int_0^1 FdB'\right\}$ [10]. Crucially, these limit distributions are completely free of nuisance parameters and depend exclusively on the I(1) and I(2) dimensions ($p_1$ and $p_2$), ensuring robust asymptotic validation of the selected rank conditions [9].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="5" source_id="6f93d684-3ba3-4684-a95d-84d256c22c9b" -->

<!-- SOURCE_INTELLIGENCE_ITEM_START index="6" source_id="9d86e85d-b9c0-4aec-b3a0-cbf9533b1155" -->
### Source 06 — Pedroni2000.pdf

| Source field | Value |
|---|---|
| NotebookLM source ID | `9d86e85d-b9c0-4aec-b3a0-cbf9533b1155` |
| Source type | `SourceType.PDF` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

The provided source, "Fully modified OLS for heterogeneous cointegrated panels" by Pedroni (2000), does not contain any information regarding Cointegrating Polynomial Regressions (CPR) or $I(2)$ interactive terms. The paper is exclusively focused on linear cointegrating systems for $I(1)$ nonstationary variables in dynamic, heterogeneous panels [1]. 

Because the source lacks material on $I(2)$ CPR, I cannot extract contributions validating that specific model. However, regarding your targeted sub-topics—asymptotic mechanics, estimator transformations, and rank conditions—here are the paper's 3 critical contributions mapped to the $I(1)$ framework it actually covers:

*   **Asymptotic Mechanics via Sequential Limits (Restricted to $I(1)$):** The paper derives the asymptotic distributions for panel estimators using sequential limit theory ($T \to \infty$ followed by $N \to \infty$) based on $I(1)$ multivariate functional central limit theorems [2]. The mechanics rely on the partial sum convergence $\frac{1}{\sqrt{T}}\sum_{t=1}^{[Tr]} \xi_{it} \to B_i(r, \Omega_i)$, where $B_i$ is a Brownian motion with asymptotic covariance $\Omega_i$ [3]. The paper does not address the distinct, higher-order asymptotic scaling or convergence rates required for $I(2)$ polynomial functionals.
*   **Semi-Parametric Estimator Transformations:** To correct for second-order endogeneity and serial correlation biases in heterogeneous panels, Pedroni develops a Fully Modified OLS (FMOLS) transformation [4]. The transformation relies on a Cholesky decomposition of the long-run covariance matrix, adjusting the dependent variable as $y_{it}^* = (y_{it} - \bar{y}_i) - \frac{\hat{L}_{21i}}{\hat{L}_{22i}}\Delta x_{it}$ alongside a serial correlation correction term $\hat{\gamma}_i$ [5, 6]. This transformation is strictly designed to purge nuisance parameters in linear $I(1)$ relationships and cannot process non-linear or polynomial $I(2)$ dynamics [6-8].
*   **Standard $I(1)$ Structural Assumptions (Absence of $I(2)$ Rank Conditions):** The study does not evaluate the reduced rank conditions necessary for $I(2)$ multi-cointegration or polynomial cointegration spaces. It fundamentally assumes a standard $I(1)$ cointegrating vector $\beta$ where $y_{it} = \alpha_i + \beta x_{it} + \mu_{it}$ directly yields a stationary error process $\mu_{it}$, bypassing the need to solve for the polynomial cointegrating ranks inherent to CPR [1].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="6" source_id="9d86e85d-b9c0-4aec-b3a0-cbf9533b1155" -->

<!-- SOURCE_INTELLIGENCE_ITEM_START index="7" source_id="3371fd51-9895-482e-b0be-60176877edd7" -->
### Source 07 — PhillipsHansen1990.pdf

| Source field | Value |
|---|---|
| NotebookLM source ID | `3371fd51-9895-482e-b0be-60176877edd7` |
| Source type | `SourceType.PDF` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

The provided text focuses exclusively on $I(1)$ and $I(0)$ time series processes and contains no information regarding Cointegrating Polynomial Regressions (CPR) or $I(2)$ interactive terms [1, 2]. However, applying your criteria to the paper's actual focus on $I(1)$ models, the 3 most critical contributions regarding asymptotic mechanics, rank conditions, and estimator transformations are:

*   **Estimator Transformations via Semi-Parametric Bias Correction:** The paper introduces "fully-modified" estimators to eliminate second-order asymptotic bias effects caused by contemporaneous and serial dependence (endogeneity) between regressors and instruments [3, 4]. By utilizing a nonparametric consistent estimate of the long-run covariance matrix $\Omega$, the dependent variable is transformed to $\hat{y}_{1t}^{+} = y_{1t} - \hat{\Omega}_{12}\hat{\Omega}_{22}^{-1}\Delta y_{2t}$ [5]. The final bias-corrected estimator takes the form $\hat{\Gamma}^{*+} = [\sum \hat{y}_{1t}^{+} x_t' - T(\hat{J}_{1b}\hat{\Delta}_{2b}, 0)](\sum x_t x_t')^{-1}$, establishing asymptotic median-unbiasedness without requiring full maximum likelihood estimation [5-7].
*   **Asymptotic Mechanics of Modified Wald Tests:** Traditional methods of inference fail in cointegrated systems because their limiting Gaussian functional (LGF) distributions are polluted by nuisance parameters, stemming from the dependence between limit Brownian motions $B_1$ and $B_2$ [8-10]. The critical mechanical contribution is that applying the fully-modified estimator transforms the asymptotic distribution of the Wald statistic ($G_R$) into a standard $\chi^2$ distribution under the null hypothesis ($G_R \Rightarrow \chi^2_g$) [11]. This entirely eliminates nuisance parameter dependencies and validates traditional hypothesis testing in $I(1)$ regressions [1, 11]. 
*   **Rank Conditions for Spurious $I(1)$ Instruments:** The paper proves that Instrumental Variable (IV) regressions yield consistent estimates even when instruments ($y_{3t}$) are strictly stochastically independent of the regressors ($y_{2t}$) [12, 13]. Because both processes are $I(1)$, the asymptotic relevance condition is naturally satisfied via stochastic trends. The crucial rank condition is demonstrated as $\text{rank}(\int_0^1 B_2 B_3') = n_2 \text{ a.s.}$ [14]. This establishes that the required rank condition for IV consistency is fulfilled as a beneficial artifact of spurious regression theory, maintaining relevance upon standardization by $T^{-2}$ [12, 14].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="7" source_id="3371fd51-9895-482e-b0be-60176877edd7" -->

<!-- SOURCE_INTELLIGENCE_ITEM_START index="8" source_id="d6a5173a-8bb2-41dd-8dfd-2d34c6ce8eb0" -->
### Source 08 — Saikkonen1991.pdf

| Source field | Value |
|---|---|
| NotebookLM source ID | `d6a5173a-8bb2-41dd-8dfd-2d34c6ce8eb0` |
| Source type | `SourceType.PDF` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

The provided source does not contain information regarding Cointegrating Polynomial Regressions (CPR) or I(2) interactive terms, as its mathematical framework is strictly restricted to systems of first-order integrated processes, I(1) [1, 2]. 

However, applying your requested focus areas to the I(1) framework presented in the paper yields the following critical theoretical contributions:

*   **Asymptotic Mechanics and the $\mathcal{S}_c$ Estimator Class:** The paper establishes an asymptotic optimality theory by defining a broad class of estimators, $\mathcal{S}_c$, whose limiting distributions are characterized by functionals of a vector Brownian motion, defined as $T(\tilde{A} - A) \Rightarrow \left(\int_0^1 L dB_1^c \right)' V + U$ [3]. Because asymptotic normality does not hold, efficiency is determined not by conventional minimum variance, but by the highest concentration (peakedness) of this non-standard limiting distribution, achieving optimality when the conditional joint distribution yields a mixed-normal limit [3-6].
*   **Covariance Conditions for Maximum Efficiency:** The paper evaluates optimality via conditional covariance matrices, demonstrating that efficiency is strictly bounded by $\Omega_{1\cdot c} \otimes \left(\int_0^1 B_2 B_2'\right)^{-1}$ [7]. It proves that maximum asymptotic efficiency requires the spectral density error matrix condition $\Omega_{1\cdot 2} = \Omega_{1\cdot c}$ to hold [8]. This mathematically proves that leveraging the stationary differences of strictly non-included, yet cointegrated, variables ($\Delta y_{3t}$) in addition to the primary regressors ($\Delta y_{2t}$) is necessary to minimize the error covariance bound and fully explain the short-run dynamics [9-11].
*   **Time-Domain Estimator Transformation:** To resolve the asymptotic inefficiency of standard OLS caused by endogeneity and serial correlation, the paper introduces a time-domain linear estimator transformation that augments the regression with $K$ leads and lags: $y_{1t} = A_c y_{2t} + \sum_{j=-K}^{K} \Pi_j \Delta y_{c, t-j} + \hat{v}_t$ [9, 12]. This transformation orthogonalizes the error process to approximately white noise without requiring initial consistent estimations (unlike frequency-domain corrections), structuring the nuisance parameters so that standard Wald testing with asymptotic $\chi^2$ distributions can be applied [11, 13-15].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="8" source_id="d6a5173a-8bb2-41dd-8dfd-2d34c6ce8eb0" -->

<!-- SOURCE_INTELLIGENCE_ITEM_START index="9" source_id="69357ef3-68cd-4c3d-9545-58bcac917835" -->
### Source 09 — StockWatson1993_DOLS.pdf

| Source field | Value |
|---|---|
| NotebookLM source ID | `69357ef3-68cd-4c3d-9545-58bcac917835` |
| Source type | `SourceType.PDF` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

*   **Canonical Regressor and Error Transformations:** To resolve the asymptotic multicollinearity inherent in regressions featuring mixed integration orders and deterministic polynomials, the authors introduce the transformation $z_t = Bx_t$, where an invertible matrix $B$ isolates distinct $I(0)$, $I(1)$, $I(2)$, and time trend components [1, 2]. The original parameter vector $\beta$ is subsequently recovered from the transformed regression $\Delta^{d-l+1} y_t^l = (z_t' \otimes I_{k_1})\delta + \nu_t$ via the mapping $\beta = (B' \otimes I_{k_1})\delta$ [3]. To validate the single-equation dynamic estimation of these terms, the estimator utilizes a two-sided lower-triangular spectral filter $D(L)$ mapping Wold errors $u_t = H(L)\epsilon_t$ into orthogonalized errors $\nu_t = C(L)\epsilon_t$, ensuring the regressors are strictly uncorrelated with the residual at all leads and lags [4-7]. 

*   **Sequential Rank Conditions for $I(d)$ Triangular Representations:** The derivation of the triangular representation for $I(d)$ systems requires recursive application of rank conditions to the matrix polynomial $F(L)$ in the representation $\Delta^d y_t = \mu + F(L)\epsilon_t$ [8]. Assuming $\text{rank}(F(1)) = k_1 < n$, the system inherently contains $k_1$ $I(d)$ stochastic trends and at least $n - k_1$ cointegrating vectors [8, 9]. Through Lemma A.1, the authors recursively partition the system by exploiting the full row rank of $F(1)$'s upper block, successively decomposing the variables into $k_1$ $I(d)$ trends, $k_2$ $I(d-1)$ trends, and lower-order components [10-13]. This explicitly maps the required rank conditions for sub-spaces in complex higher-order multicointegration frameworks (e.g., $CI(2,1)$ or $CI(2,2)$ systems) [6, 14].

*   **Asymptotic Mechanics and $\chi^2$ Inference for $I(2)$ Systems:** The asymptotic distribution is governed by the block-diagonal scaling matrix $\Upsilon_T = \text{diag}(T^{1/2}I_{g_1}, TI_{g_2}, T^2I_{g_3}, \dots)$ applied to the canonical regressors, which yields disparate convergence rates corresponding to the integration order (e.g., $T^2$ for $I(2)$ components, $T$ for $I(1)$ components) [15, 16]. Because the variables are filtered into strict exogeneity, the parameter estimates are conditionally Gaussian and unconditionally follow an asymptotic mixed normal distribution [17, 18]. As a result, the Wald statistic for testing general linear restrictions $R\delta = r$ (or equivalently $P\beta = r$) avoids non-standard Dickey-Fuller-type distributions and converges strictly to a standard $\chi^2$ distribution, fully validating standard hypothesis testing for systems with integrated polynomials and $I(2)$ variables [17, 19, 20].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="9" source_id="69357ef3-68cd-4c3d-9545-58bcac917835" -->

<!-- SOURCE_INTELLIGENCE_ITEM_START index="10" source_id="8c9b16c5-e8d2-4872-88ce-c427c4d4edfb" -->
### Source 10 — VogelsanWagner2014.pdf

| Source field | Value |
|---|---|
| NotebookLM source ID | `8c9b16c5-e8d2-4872-88ce-c427c4d4edfb` |
| Source type | `SourceType.PDF` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

The provided sources do not contain information specifically regarding Cointegrating Polynomial Regressions (CPR), $I(2)$ interactive terms, or rank conditions for validating such models. However, the text details critical asymptotic mechanics and estimator transformations related to $I(2)$ regression spaces via the introduction of the Integrated Modified OLS (IM-OLS) estimator. 

Here are the 3 most critical contributions regarding these underlying mechanics and estimator transformations:

*   **Partial Sum Transformation to an $I(2)$ Space:** To circumvent the need for estimating long-run variance matrices and selecting kernel/bandwidth parameters, the IM-OLS estimator takes the partial sums of a standard $I(1)$ cointegrating regression, inherently transforming the model into a regression with $I(2)$ regressors ($S x_t$) and $I(1)$ errors ($S u_t$) [1-3]. To correct for endogeneity, the estimator augments the model using the original regressors ($x_t$), formulated as $S y_t = S f'_t \delta + S x'_t \beta + x'_t \gamma + S u_t$ [4]. Because both $x_t$ and $S u_t$ are $I(1)$ processes, their correlation is naturally absorbed into the centering parameter $\gamma = \Omega_{vv}^{-1}\Omega_{vu}$ without requiring the addition of leads or lags [4, 5].
*   **Asymptotic Bias Eradication via Nuisance Parameter Annihilation:** In standard OLS and FM-OLS, sub-matrices taking the form $\sum x_t u_t$ produce the additive nuisance parameter $\Delta_{vu}$, which complicates inference and causes endogeneity bias [3, 6, 7]. The IM-OLS estimator transformation mechanically replaces these terms with sub-matrices of the form $\sum S x_t S u_t$ [3, 7]. The appropriately scaled limits of these transformed sums do not contain additive nuisance parameters, functioning similarly to the FM-OLS orthogonalization step but yielding an asymptotically bias-free estimator featuring a zero-mean Gaussian mixture limiting distribution denoted by $\Psi$ [7-9].
*   **Residual Orthogonalization for Pivotal Fixed-$b$ Inference:** The OLS parameter estimates of the transformed model ($\tilde{\delta}, \tilde{\beta}, \tilde{\gamma}$) remain asymptotically correlated with the regression residuals $\tilde{S}u_t$ due to unknown nuisance parameters [5, 10]. To enable pivotal fixed-$b$ hypothesis testing, an additional estimator transformation is introduced to adjust the residuals via orthogonal projection: $\tilde{S}u_t^* = \tilde{S}u_t - (z_t^\perp)'\hat{\pi}$ [11]. The projection relies on the space $z_t^\perp$, which is derived from $z_t = t \sum_{j=1}^T \xi_j - \sum_{j=1}^{t-1} \sum_{s=1}^j \xi_s$ (where $\xi_t = [Sf_t', Sx_t', x_t']'$) [10, 11]. This transformation guarantees that the limit process of the adjusted residuals, $\tilde{P}^*(r)$, is conditionally uncorrelated with (and thus independent of) the limiting distribution of the parameter estimates $\Psi$ [12].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="10" source_id="8c9b16c5-e8d2-4872-88ce-c427c4d4edfb" -->

<!-- SOURCE_INTELLIGENCE_ITEM_START index="11" source_id="86a8d87b-e96b-4fe5-9a58-7e354e8bfe4b" -->
### Source 11 — Wagner2023.pdf

| Source field | Value |
|---|---|
| NotebookLM source ID | `86a8d87b-e96b-4fe5-9a58-7e354e8bfe4b` |
| Source type | `SourceType.PDF` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

The provided source does not contain information specifically regarding Cointegrating Polynomial Regressions (CPR) with $I(2)$ interactive terms, nor does it discuss the IM-OLS (Integrated Modified OLS) estimator in detail. The paper focuses exclusively on nonlinear transformations of $I(1)$ unit root processes using Fully Modified OLS (FM-OLS) [1-3]. 

However, extracting the closest critical contributions regarding asymptotic mechanics, rank conditions, and estimator transformations for the $I(1)$ CPR framework yields the following:

*   **Full Design Asymptotic Mechanics:** The paper establishes that while general CPR testing suffers from nuisance parameter dependencies, a *full design* structure allows the limiting distribution to be resolved into a functional of standard Brownian motions [4, 5]. Specifically, if the regressor structure permits the transformation $J(r) = \begin{bmatrix} I & 0 \\ 0 & \Pi \end{bmatrix} \begin{bmatrix} D(r) \\ \mathbf{W}_v(r) \end{bmatrix}$ (where $\Pi$ is a regular matrix and $\mathbf{W}_v(r)$ represents standard Brownian motions), both the KPSS-type cointegration test ($C_T$) and the variance ratio spurious regression test ($\hat{P}_u$) can successfully scale out the scalar long-run variance. This guarantees asymptotically valid, nuisance-parameter-free tabulations for empirically relevant structures where only a single $I(1)$ process enters the regression with higher powers [6-8].
*   **Polynomial FM-OLS Estimator Transformations:** To correct for second-order bias and endogeneity in nonlinear settings, the paper utilizes an estimator transformation that modifies the dependent variable to $y_t^+ := y_t - \Delta x_t' \hat{\Omega}_{vv}^{-1} \hat{\Omega}_{vu}$ and subtracts a specialized correction matrix $A^*$ derived from $M^*$ [9-11]. The CPR-specific polynomial correction term for the $j$-th regressor block takes the form $M_j^* := \hat{\Delta}_{v_ju}^+ \begin{bmatrix} T^{1/2}\sum x_{jt} & \dots & \sum x_{jt}^{p_j-1} \end{bmatrix}'$, where $\hat{\Delta}_{v_ju}^+$ is the fully modified one-sided long-run covariance, establishing a consistent zero-mean Gaussian mixture asymptotic distribution for the estimator $\hat{\theta}^+ := (Z'Z)^{-1}(Z'y^+ - A^*)$ [11, 12].
*   **Rank Conditions for Process Innovations:** The fundamental mechanical constraint required to prevent degenerate asymptotic distributions in the CPR framework mandates that the innovation matrix polynomial satisfies $\text{det}(C(1)) \neq 0$, coupled with a positive definite covariance matrix $\Sigma_{\eta_0\eta_0}$ [13, 14]. This rank condition mathematically ensures that the vector process $\{x_t\}$ is integrated but strictly *not* internally cointegrated, serving as a mandatory prerequisite to validate the invariance principle $\frac{1}{\sqrt{T}} \sum_{t=1}^{[rT]} \eta_t \Rightarrow B(r) = \Omega^{1/2} W(r)$ necessary for tracking the limiting partial sum processes of the errors under both the null and alternative hypotheses [9, 13, 14].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="11" source_id="86a8d87b-e96b-4fe5-9a58-7e354e8bfe4b" -->

<!-- SOURCE_INTELLIGENCE_ITEM_START index="12" source_id="ada0bbf7-27ab-4bde-a61a-510d978d2811" -->
### Source 12 — WagnerHyunhong2016.pdf

| Source field | Value |
|---|---|
| NotebookLM source ID | `ada0bbf7-27ab-4bde-a61a-510d978d2811` |
| Source type | `SourceType.PDF` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

The provided source material does not contain any relevant information regarding Cointegrating Polynomial Regressions (CPR) with $I(2)$ variables or interactive (cross-product) terms. The text explicitly limits its scope to $I(1)$ regressors and explicitly excludes cross-product terms of the integrated regressors due to an assumption of additive separability [1-3]. 

However, regarding the asymptotic mechanics, rank conditions, and estimator transformations for the additively separable $I(1)$ CPRs that the paper actually addresses, the 3 most critical contributions are:

*   **Estimator Transformations (FM-OLS Formulation):** The authors extend the Phillips and Hansen (1990) approach to CPRs by introducing a two-part data transformation to eliminate second-order bias [4, 5]. The estimator corrects the dependent variable as $y_t^+ := y_t - \Delta x_t'\hat{\Omega}_{vv}^{-1}\hat{\Omega}_{vu}$ and applies deterministic additive correction factors $M^*$ derived from one-sided long-run variance matrices ($\hat{\Lambda}_{vu}^+$ and $\hat{\Lambda}_{vv}^*$) to account for serial correlation and regressor endogeneity [6, 7].
*   **Asymptotic Mechanics:** The paper establishes that the modified estimator, $G^{-1}(\hat{\theta}^+ - \theta)$, weakly converges to the zero-mean Gaussian mixture limiting distribution $\left( \int J(r)J(r)'dr \right)^{-1} \int J(r)dB_{u.v}(r)$ [7]. Because the component process $J(r)$ is independent of the conditioned Brownian motion $B_{u.v}(r)$ by construction, this transformation yields a conditionally normal limit variance $V_{FM} = \omega_{u.v} \left( \int J(r)J(r)'dr \right)^{-1}$, validating standard asymptotic inference [7, 8].
*   **Rank Conditions for Constraint Matrices:** To support general Wald and LM specification testing when elements of $\hat{\theta}^+$ exhibit varying convergence rates, the authors define a necessary rank condition for the restriction matrix $R \in \mathbb{R}^{s \times (q+1+p)}$ [8, 9]. They prove that asymptotic $\chi^2_s$ inference holds if there exists a scaling matrix $G_R(T)$ such that the limit $\lim_{T \to \infty} G_R R G = R^*$ yields a matrix $R^*$ with full row rank $s$ [9, 10].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="12" source_id="ada0bbf7-27ab-4bde-a61a-510d978d2811" -->

<!-- SOURCE_INTELLIGENCE_ITEM_START index="13" source_id="3966dd86-315e-4c56-b307-88863d1679be" -->
### Source 13 — deJongWagner2025.pdf

| Source field | Value |
|---|---|
| NotebookLM source ID | `3966dd86-315e-4c56-b307-88863d1679be` |
| Source type | `SourceType.PDF` |
| Thread policy | New source-restricted thread |

#### Query

Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX.

#### Critical contributions

The provided sources do not contain information regarding Cointegrating Polynomial Regressions (CPR) with **$I(2)$ interactive terms** or **rank conditions**. The sources exclusively focus on panel CPRs involving a single $I(1)$ process and its polynomial terms (e.g., squares and cubes) rather than $I(2)$ variables [1-4]. 

However, focusing on your interest in **asymptotic mechanics** and **estimator transformations**, here are the 3 most critical contributions regarding $I(1)$ panel CPRs extracted from the text:

*   **Novel Estimator Transformations without Dependent Variable Modification:** The authors develop a "Modified OLS" estimator that leverages the large cross-sectional dimension ($N$) to consistently estimate and subtract an additive second-order endogeneity bias term $\tilde{C}_i$ directly [5-7]. Unlike the traditional Fully Modified OLS (FM-OLS) estimator—which requires transforming the dependent variable via $\tilde{y}_{it}^{+} = \tilde{y}_{it} - \hat{\Omega}_{uvi}\hat{\Omega}_{vvi}^{-1}v_{it}$ alongside bias correction $\tilde{C}_{i}^{+}$ [8, 9]—the Modified OLS approach achieves correction without altering $\tilde{y}_{it}$ [5, 10].
*   **Sequential Asymptotic Mechanics for Panel CPRs:** The paper establishes sequential asymptotic theory ($T \to \infty$ followed by $N \to \infty$) for both estimators within an i.i.d. random linear process framework [11-13]. The asymptotic mechanics demonstrate that both the Modified OLS and FM-OLS estimators successfully eliminate the second-order bias, achieving zero-mean Gaussian limiting distributions of the form $\sqrt{N}G_{T}^{-1}(\tilde{\beta} - \beta) \xrightarrow{d} \mathcal{N}(0, V_{1}^{-1}\Theta V_{1}^{-1})$, which allows for standard standard normal inference rather than non-standard "sandwich" distributions [14-17].
*   **Asymptotic Invariance to Two-Way Fixed Effects:** The asymptotic mechanics are expanded to accommodate both individual ($\alpha_i$) and time ($\gamma_t$) fixed effects [3, 18]. The authors prove that the presence of time effects only minimally impacts the limiting distributions; specifically, the additional cross-sectional averaging only alters the $(2,2)$-element of the variance matrix $V_{1}$ (creating $V_{2}$) due to the zero odd cross-moments of normal distributions governing the expected values of the transformed Brownian motions $\tilde{B}_{vi}(r)$ [19, 20].

<!-- SOURCE_INTELLIGENCE_ITEM_END index="13" source_id="3966dd86-315e-4c56-b307-88863d1679be" -->

<!-- SOURCE_INTELLIGENCE_END -->

<!-- AUDIT_PHASE_START phase="1" slug="i2-trap" source="cluster_1.csv" -->
## Phase 1 — The I(2) Trap

<!-- AUDIT_QUESTION_START id="1.1" phase="1" -->
### 1.1

| Audit field | Content |
|---|---|
| Literature target | Wagner & Hong (2016), Paruolo (1996) |
| Validation metric | Look for the expansion of the partial sum &#92;sum z_t into iterated stochastic integrals &#92;int W_1 dW_2. |

#### Audit question

Provide the exact Beveridge-Nelson decomposition for the product z_t = x_t y_t where "x_t, y_t \sim I(1)". Show mathematically why the cross-terms of the stochastic trends \sum \varepsilon_{1i} \sum \varepsilon_{2i} result in a quadratic trend O_p(T^2)", formally proving "z_t \sim I(2).

#### NotebookLM mathematical validation

**Verdict:** **FAIL**

The proposed validation metric is mathematically false and unsupported by the uploaded literature. Your notes fundamentally conflate the partial sum of a product, $\sum x_t y_t$, with the discrete-time summation-by-parts expansion of the product itself, $x_t y_t$. 

**Theorem/Lemma from Literature:** 
Wagner & Hong (2016, Proposition 1); Continuous Mapping Theorem for Cointegrating Polynomial Regressions (CPR); Functional Central Limit Theorem (FCLT) [1, 2].

**Mathematical Validation:**

Let $x_t$ and $y_t$ be $I(1)$ processes such that $T^{-1/2}x_{\lfloor Tr \rfloor} \Rightarrow B_x(r)$ and $T^{-1/2}y_{\lfloor Tr \rfloor} \Rightarrow B_y(r)$, where $B_x, B_y$ are Brownian motions [1, 3]. 

Your notes (Audit Ledger ID 1.1) claim that the partial sum of the product $z_t = x_t y_t$ expands into an iterated stochastic integral:
$$ \frac{1}{T^{3/2}} \sum_{t=1}^{\lfloor T r \rfloor} x_t y_t \xrightarrow{w} \int_0^r B_x(s) dB_y(s) + \int_0^r B_y(s) dB_x(s) + \text{drift terms} $$
This statement is mathematically false [4]. 

By the Continuous Mapping Theorem (CMT), the product $z_t = x_t y_t$ is $O_p(T)$, scaling as $T^{-1} z_{\lfloor Tr \rfloor} \Rightarrow B_x(r)B_y(r)$ [1, 5]. Therefore, the partial sum of $z_t$ requires a $T^{-2}$ scaling and converges to a standard Riemann integral, not an iterated stochastic integral:
$$ T^{-2} \sum_{t=1}^{\lfloor Tr \rfloor} x_t y_t = T^{-1} \sum_{t=1}^{\lfloor Tr \rfloor} \left(T^{-1/2} x_t\right) \left(T^{-1/2} y_t\right) \Rightarrow \int_0^r B_x(s)B_y(s)ds $$
This follows standard CPR limits [6]. 

The expression you erroneously attributed to the partial sum $\sum z_t$ is actually the continuous-time Itô decomposition of the scaled product itself (not its sum). In discrete time, this relies on summation-by-parts (Abel's lemma) of the product $x_t y_t$:
$$ x_t y_t = \sum_{i=1}^t x_{i-1} \Delta y_i + \sum_{i=1}^t y_{i-1} \Delta x_i + \sum_{i=1}^t \Delta x_i \Delta y_i $$
Scaling this identity by $T^{-1}$ recovers the weak convergence to the Itô formulation given in Wagner & Hong (2016, Proposition 1) and Kasparis (2008):
$$ T^{-1} x_{\lfloor Tr \rfloor} y_{\lfloor Tr \rfloor} \Rightarrow \int_0^r B_x(s) dB_y(s) + \int_0^r B_y(s) dB_x(s) + [B_x, B_y]_r $$
Thus, it is the partial sum of the cross-products of the *levels and differences* ($\sum x_{t-1} \Delta y_t$) that converges to the iterated stochastic integral $\int B_x dB_y$, not the partial sum of the product of levels $\sum x_t y_t$ [2, 5]. 

Furthermore, your claim that the cross-terms $\mu_{1t}\mu_{2t}$ result in a "quadratic trend $O_p(T^2)$" misrepresents the order of integration. The product of two $I(1)$ stochastic trends $\mu_{1t}\mu_{2t}$ is exactly $O_p(T^{1/2}) \times O_p(T^{1/2}) = O_p(T)$. It is only the *partial sum* of this product that operates at $O_p(T^2)$ [6]. The product acts as an $I(2)$ proxy specifically because its first difference, $\Delta(x_t y_t) = x_{t-1}\Delta y_t + y_t \Delta x_t$, consists of $I(1) \times I(0)$ processes and is therefore $I(1)$, perfectly conforming to the definitional requirement that the difference of an $I(2)$ process is $I(1)$ [7, 8].

*(Note: Standard properties of Itô's Lemma and Abel's summation by parts are utilized here for refutation, which represent fundamental econometric properties of Brownian limit processes derived directly from the provided source framework.)*

<!-- AUDIT_QUESTION_END id="1.1" phase="1" -->

<!-- AUDIT_QUESTION_START id="1.2" phase="1" -->
### 1.2

| Audit field | Content |
|---|---|
| Literature target | Haldrup (1998), Johansen (1995) |
| Validation metric | Look for conditions where the long-run covariance matrix &#92;Omega is singular or where x_t and y_t are strictly cointegrated such that the quadratic trend cancels. |

#### Audit question

Under what exact orthogonality or cointegration conditions between x_t and y_t does the product x_t y_t fail to be I(2) and revert to I(1)"? (i.e., When does the I(2) trap collapse?)"

#### NotebookLM mathematical validation

**Verdict: FAIL**

**Theorem/Lemma from Literature:**
Theorem 1 (Integration Order of Product of I(1) Processes) and Corollary 1 (Lagged Interaction) [1, 2]; Johansen's Representation Theorem for I(2) Systems (Paruolo 1996, Theorem 2.1) [3]; Continuous Mapping Theorem for Cointegrating Polynomial Regressions (Wagner & Hong 2016) [4].

**Mathematical Validation:**
The proposed validation metric is mathematically false and unsupported by the uploaded literature. The metric incorrectly asserts that strict cointegration (or a singular long-run covariance matrix $\Omega$) between $x_t$ and $y_t$ causes the quadratic stochastic trend of their product $x_t y_t$ to "cancel," thereby reverting the product to $I(1)$.

Let $x_t$ and $y_t$ be $I(1)$ processes. Using the Beveridge-Nelson decomposition, they can be represented as $x_t = \mu_{1t} + \tilde{x}_t$ and $y_t = \mu_{2t} + \tilde{y}_t$, where $\mu_{it} = \sum_{j=1}^t \varepsilon_{ij}$ are the random walk components and $\tilde{x}_t, \tilde{y}_t$ are stationary [1]. The product expands as:
$$x_t y_t = \mu_{1t}\mu_{2t} + \mu_{1t}\tilde{y}_t + \tilde{x}_t\mu_{2t} + \tilde{x}_t\tilde{y}_t$$
The dominant stochastic trend is the quadratic form $\mu_{1t}\mu_{2t}$. Its first difference is:
$$\Delta(\mu_{1t}\mu_{2t}) = \varepsilon_{1t}\mu_{2t} + \varepsilon_{2,t-1}\mu_{1t} + O_p(1)$$
Because $\mu_{it} \sim I(1)$ and $\varepsilon_{it} \sim I(0)$, the terms $\varepsilon_{1t}\mu_{2t}$ and $\varepsilon_{2,t-1}\mu_{1t}$ are $I(1)$ processes. Consequently, $\Delta(x_t y_t) \sim I(1)$, implying the product $x_t y_t \sim I(2)$ [1, 2]. 

If $x_t$ and $y_t$ are strictly cointegrated, they share a common stochastic trend, meaning $\mu_{2t} = \beta \mu_{1t}$. A singular long-run covariance matrix $\Omega$ implies exactly this cointegrating rank restriction [5-7]. Substituting this strict cointegration condition into the product yields:
$$x_t y_t = x_t(\beta x_t + u_t) = \beta x_t^2 + x_t u_t$$
where $u_t \sim I(0)$. The dominant trend of the product becomes $\beta \mu_{1t}^2$. The first difference of this squared trend is:
$$\Delta(\beta \mu_{1t}^2) = \beta(\mu_{1t}^2 - \mu_{1,t-1}^2) = 2\beta \mu_{1,t-1}\varepsilon_{1t} + \beta \varepsilon_{1t}^2$$
The cross-product $2\beta \mu_{1,t-1}\varepsilon_{1t}$ involves an $I(1)$ process multiplied by an $I(0)$ innovation. By standard Functional Central Limit Theorem (FCLT) limits applied in Cointegrating Polynomial Regressions (CPR), its partial sum converges to an Itô stochastic integral $\int W dW$, making the difference itself an $I(1)$ process [8, 9]. Thus, the first difference of the product remains $I(1)$, and the product $x_t y_t$ maintains its $I(2)$ property [1, 2]. 

The quadratic trend $\beta \mu_{1t}^2$ does *not* cancel under cointegration; rather, cointegration forces the stochastic trends to become perfectly collinear, strictly reinforcing the $I(2)$ nature of the interaction term.

According to the provided literature framework, the $I(2)$ trap collapses and the product reverts to $I(1)$ *if and only if* one of the constituent variables is strictly $I(0)$ to begin with. As formally stated in Corollary 1 (Lagged Interaction): "If $\omega_t \sim I(0)$, then $\tilde{k}_t \cdot \omega_{t-1} \sim I(1)$" [2]. Cointegration between two $I(1)$ processes does not reduce the integration order of their product to $I(1)$, rendering the proposed metric mathematically invalid.

<!-- AUDIT_QUESTION_END id="1.2" phase="1" -->

<!-- AUDIT_QUESTION_START id="1.3" phase="1" -->
### 1.3

| Audit field | Content |
|---|---|
| Literature target | Phillips (1986), Park & Phillips (1989) |
| Validation metric | Look for the diagonal standardization matrix "D_T = &#92;text{diag}(T^{1/2}, T, T^{3/2})" and how failing to use it ruins the Continuous Mapping Theorem (CMT) application. |

#### Audit question

Prove why the standard OLS projection matrix M_X = I - X(X'X)^{-1}X' becomes asymptotically degenerate when X contains a mix of I(1) and I(2) regressors without proper standardization matrices D_T.

#### NotebookLM mathematical validation

**Verdict: FAIL**

**Theorem/Lemma from Literature:**
Theorem 3.1 (Phillips & Hansen, 1990); Continuous Mapping Theorem (CMT); Lemma A.1 and Johansen's Representation Theorem for $I(2)$ processes (Paruolo, 1996); Asymptotic Distribution of the IM-OLS Estimator (Vogelsang & Wagner, 2014).

**Mathematical Validation:**
The proposed validation metric is mathematically false and unsupported by the uploaded literature in two fundamental ways. 

First, the metric incorrectly asserts that the standard OLS projection matrix $M_X = I - X(X'X)^{-1}X'$ becomes "asymptotically degenerate" without a proper standardization matrix $D_T$. The projection matrix $M_X$ maps onto the column space of $X$ and is algebraically invariant to any non-singular right-multiplication [1]. For any arbitrary non-singular diagonal standardization matrix $D_T$, the scaled projection matrix evaluates identically to the unscaled one:
$$ M_{X D_T} = I - X D_T (D_T X' X D_T)^{-1} D_T X' = I - X D_T D_T^{-1} (X'X)^{-1} D_T^{-1} D_T X' = I - X(X'X)^{-1}X' = M_X $$
Consequently, the projection matrix $M_X$ is scale-invariant; it does not suffer from asymptotic degeneracy simply due to an absence of standardization matrices [1].

Second, the metric proposes an incorrect scaling matrix $D_T = \text{diag}(T^{1/2}, T, T^{3/2})$. In the asymptotic theory of mixed-order nonstationary regressors, applying the Continuous Mapping Theorem (CMT) to ensure the weak convergence of sample moment matrices requires pre- and post-multiplication by a scaling matrix composed of **inverse** (negative) powers of the sample size $T$ to counteract the unbounded divergence of the partial sums [2, 3]. For instance, in Paruolo (1996), the normalization matrix $A_T$ used to establish the asymptotic distributions for sample moments in systems combining $I(0)$, $I(1)$, and $I(2)$ variables is formally defined as $A_T = \text{diag}(T^{-1/2}I_{p_0}, T^{-1}I_{p_1}, T^{-3/2}I_{p_2})$ [3]. Similarly, in Cointegrating Polynomial Regressions (CPRs) containing $I(1)$ processes and their higher-order powers (which behave as $I(2)$ or higher-order stochastic trends), the regressor scaling matrix $G_X$ strictly takes the form $\text{diag}(T^{-1}, T^{-3/2}, \ldots, T^{-(p_j+1)/2})$ to scale the sample cross-products into a non-degenerate functional of Brownian motions [2, 4]. 

While positive powers of $T$ define the super-consistent convergence rates of the *parameter estimates* (e.g., scaling the estimator via $T^{1/2}$ for $I(0)$ components, $T$ for $I(1)$ components, and $T^{3/2}$ for $I(2)$ components), the diagonal standardization matrix required to stabilize the data matrix $X$ inside the CMT framework strictly necessitates negative powers of $T$ [1, 4, 5]. Failing to use the correct negative-power scaling matrix causes the raw sample moment $(X'X)$ to diverge to infinity, which breaks the CMT limit, but this divergence applies to the moment matrices, not the scale-invariant projection matrix $M_X$ [3, 4]. Therefore, the proposed metric is mathematically false.

<!-- AUDIT_QUESTION_END id="1.3" phase="1" -->

<!-- AUDIT_PHASE_END phase="1" -->

<!-- AUDIT_PHASE_START phase="2" slug="dols-fmols" source="cluster_2.csv" -->
## Phase 2 — DOLS and FM-OLS

<!-- AUDIT_QUESTION_START id="2.1" phase="2" -->
### 2.1

| Audit field | Content |
|---|---|
| Literature target | Wagner & Hong (2016), Saikkonen (1991) |
| Validation metric | Look for the linear dependence between the levels ("x_t, y_t") and the differences (x_t &#92;Delta y_t") in the limit theory, proving the design matrix condition number explodes." |

#### Audit question

In DOLS" applied to a CPR, the differenced interaction term is "\Delta(x_t y_t) = x_t \Delta y_t + y_t \Delta x_t. Show the exact rank of the asymptotic covariance matrix of the augmented regressor set. Why does this guarantee severe finite-sample multicollinearity?

#### NotebookLM mathematical validation

**(1) Exact Theorem/Lemma name from the literature**
No theorem or lemma in the targeted literature supports the proposed validation metric. In fact, the metric is mathematically contradicted by **Proposition 1 of Wagner & Hong (2016)** and **Lemma A.3 of Saikkonen (1991)** (and further refuted by the canonical regressor transformations in **Stock & Watson 1993, Theorem 1**). 

**(2) Rigorous mathematical proof or condition**
The validation metric asserts that there is an asymptotic linear dependence between the levels ($x_t, y_t$) and the differenced interaction terms ($x_t \Delta y_t$) that causes the condition number of the design matrix to explode. This is mathematically false. 

Let the augmented DOLS regressor vector be partitioned as $Z_t = [X_{1t}', X_{2t}']'$, where $X_{1t}$ contains the integrated level variables ($I(1)$ and $I(2)$ processes such as $x_t, y_t, x_t y_t$) and $X_{2t}$ contains the augmented difference variables (e.g., $\Delta x_t, \Delta y_t, \Delta(x_t y_t)$). Because these variables possess different orders of integration, the sample moment matrix must be normalized by a diagonal scaling matrix $G_T = \text{diag}(G_{1T}, G_{2T})$ to ensure non-degenerate weak convergence [1, 2]. 

The asymptotic covariance matrix of the augmented regressor set converges to a block-diagonal limit:
$$ \lim_{T \to \infty} G_T \left( \sum_{t=1}^T Z_t Z_t' \right) G_T = \begin{bmatrix} \int_0^1 J(r)J(r)' dr & 0 \\ 0 & \Sigma_{22} \end{bmatrix} $$

By **Proposition 1 of Wagner & Hong (2016)**, the upper-left block corresponding to the continuous limit of the scaled integrated regressors, $\int_0^1 J(r)J(r)' dr$, is positive definite almost surely [3]. By **Lemma A.3 of Saikkonen (1991)**, the lower-right block corresponding to the stationary differences converges in probability to a non-singular covariance matrix $\Sigma_{22}$ [4]. 

Crucially, **the off-diagonal blocks containing the cross-moments between the levels and the differences vanish asymptotically**. This occurs because the cross-products between processes of different integration orders (e.g., $I(1)$ levels and $I(0)$ differences) are asymptotically negligible when standardized by the product of their respective convergence rates [4, 5]. Because the asymptotic design matrix is block-diagonal and strictly full-rank, the condition number does **not** explode in the limit. 

The severe multicollinearity observed in DOLS applied to a CPR is strictly a **finite-sample phenomenon** [6]. It is mechanically driven by the proliferation of parameters required to augment the regression with multiple leads and lags of $\Delta x_t$, $\Delta y_{t-1}$, and $\Delta(x_t y_{t-1})$, which drastically reduces degrees of freedom and inflates variance in small samples, rather than an asymptotic linear dependence [6-8]. 

**(3) Verdict**
**Fail**. The mandatory validation metric is mathematically false and entirely unsupported by the literature. The asymptotic covariance matrix of the augmented regressor set does not suffer from a rank deficiency between levels and differences in the limit theory. You are incorrectly conflating a finite-sample degrees-of-freedom exhaustion issue with an asymptotic design matrix singularity.

<!-- AUDIT_QUESTION_END id="2.1" phase="2" -->

<!-- AUDIT_QUESTION_START id="2.2" phase="2" -->
### 2.2

| Audit field | Content |
|---|---|
| Literature target | Wagner & Hong (2016), Choi & Kurozumi (2012) |
| Validation metric | Look for the spectral density at frequency zero for an I(2) process. The bias arises because the variance grows at O(T^3)", not "O(T)", requiring a different bandwidth penalty." |

#### Audit question

For FM-OLS", derive the exact bias term introduced if the "Long-Run Covariance (LRCV) matrix \Omega is estimated using a standard I(1)" kernel bandwidth (e.g., Andrews, "q=1/3) on an I(2) regressor.

#### NotebookLM mathematical validation

**(1) Exact Theorem/Lemma name from the literature**
No such theorem or lemma exists in the targeted literature, and the mandatory validation metric is theoretically invalid. The metric fundamentally mischaracterizes the Fully Modified OLS (FM-OLS) estimator for Cointegrating Polynomial Regressions (CPRs) as formulated by Wagner & Hong (2016) [1, 2]. Furthermore, Choi & Kurozumi (2012) does not address kernel bandwidth selection for FM-OLS; rather, it provides an Akaike Information Criterion (AIC) rule for selecting the number of leads and lags in the Dynamic OLS (DOLS) estimator [3]. 

**(2) Rigorous mathematical proof or condition**
The proposed validation metric claims that the Long-Run Covariance (LRCV) matrix $\Omega$ is estimated on an $I(2)$ regressor, causing the spectral density at frequency zero to explode due to the variance growing at $O(T^3)$. This is mathematically false on multiple fronts:

1. **The inputs to the LRCV matrix in FM-OLS are strictly $I(0)$:** 
Under Assumption 1 of Wagner & Hong (2016), the FM-OLS correction terms are derived from the long-run covariance matrix of the *stationary* innovations, not the integrated regressors. Let the error process be $u_t$ and the first difference of the integrated regressors be $v_t = \Delta x_t$. The process $\eta_t = [u_t, v_t']'$ is assumed to be an $I(0)$ stationary and ergodic martingale difference sequence [2]. The long-run covariance matrix is defined purely on these stationary differences:
$$ \Omega = \sum_{h=-\infty}^{\infty} E(\eta_0 \eta_h') = \begin{bmatrix} \Omega_{uu} & \Omega_{uv} \\ \Omega_{vu} & \Omega_{vv} \end{bmatrix} $$
Because $\eta_t \sim I(0)$, its spectral density at frequency zero is finite and well-defined. FM-OLS *never* estimates the LRCV matrix on $I(1)$ or $I(2)$ regressors [4].

2. **The "Standard" FM-LIN behavior on CPRs:**
If an analyst mistakenly applies "standard" linear FM-OLS to a polynomial regression (the FM-LIN approach), they compute the LRCV matrix using the differences of the powers, e.g., $w_t = \Delta(x_t^p)$ [5]. While these differences are nonstationary, they are *not* $I(2)$ processes. Theorem 1 of Grabarczyk (2017) shows that the formal "long-run covariance" of these nonstationary differences converges weakly to random limit functionals of Brownian motion, not a deterministic infinite spectral density [6, 7]. 

3. **The Bandwidth Penalty:**
To establish the asymptotic equivalence between the correct FM-CPR estimator and the improperly applied FM-LIN estimator, Grabarczyk's Assumption 4 restricts the bandwidth parameter $M_T = O(T^b)$ to require $0 < b < 1/3$ [8]. This tightened upper bound (standard approaches allow $b < 1/2$) is required to ensure that the kernel-weighted sum of the nonstationary components $\Delta(x_t^p)$ remains asymptotically negligible [9]. It has absolutely nothing to do with estimating the spectrum of an $I(2)$ process.

4. **Spectral Density of $I(2)$:**
By definition, if a process $z_t \sim I(2)$, its first difference is $I(1)$ and its variance grows at $O(t^3)$, rendering the sample moment $\sum_{t=1}^T z_t^2$ to be $O_p(T^5)$ [10]. The spectral density function at frequency zero for an $I(2)$ process exhibits a singularity of order $\omega^{-4}$. Thus, evaluating the "spectral density at frequency zero for an $I(2)$ process" is mathematically nonsensical.

**(3) Verdict**
**Fail**. The mandatory validation metric is mathematically false and unsupported by the cited literature. You have conflated the stationary inputs of the FM-OLS LRCV matrix ($I(0)$ differences) with the nonstationary levels of the regressors. Additionally, you incorrectly attributed Choi & Kurozumi (2012) to FM-OLS bandwidth selection, when the uploaded texts explicitly state their method is used for DOLS lead/lag length selection [3].

<!-- AUDIT_QUESTION_END id="2.2" phase="2" -->

<!-- AUDIT_QUESTION_START id="2.3" phase="2" -->
### 2.3

| Audit field | Content |
|---|---|
| Literature target | Phillips & Hansen (1990), Wagner (2015) |
| Validation metric | Look for the requirement that the nuisance parameter &#92;Omega_{uv}" must be estimated consistently, which fails if the "I(2) nature of z_t contaminates the pre-whitening filters. |

#### Audit question

Why does the Endogeneity Correction term in FM-OLS (\hat{\Delta}_{ue}^+) fail to fully purge the correlation between the I(2) regressor z_t and the error u_t if the error itself contains integrated components?

#### NotebookLM mathematical validation

**(1) Exact Theorem/Lemma name from the literature**
No theorem or lemma supports the proposed validation metric. The metric is mathematically false and contradicts the foundational assumptions of Cointegration Theory as established in the **Model and Background Theory (Section 2) of Phillips & Hansen (1990)** and **Assumption 1 of Wagner & Hong (2016)**.

**(2) Rigorous mathematical proof or condition**
The mandatory validation metric asserts that the endogeneity correction term fails because the "$I(2)$ nature of $z_t$ contaminates the pre-whitening filters," which supposedly prevents consistent estimation of $\Omega_{uv}$ when $u_t$ contains integrated components. This is theoretically flawed for two fundamental reasons:

1. **The Error Term Must Be Strictly $I(0)$ for Cointegration:** 
The Fully Modified OLS (FM-OLS) estimator is exclusively defined for cointegrated systems. According to the foundational setup of Phillips & Hansen (1990) and Assumption 1 of Wagner & Hong (2016), the regression error $u_t$ must be a strictly stationary, zero-mean $I(0)$ process [1-3]. If the error $u_t$ itself contains integrated components (e.g., $u_t \sim I(1)$), the variables are by definition **not cointegrated**, resulting in a spurious regression [4]. In a spurious regression, the true parameter values do not exist in a meaningful long-run equilibrium sense, and the entire framework of FM-OLS, including the endogeneity correction term $\hat{\Delta}_{vu}^+$, is rendered theoretically invalid. The failure is due to a lack of cointegration, not a "contamination of pre-whitening filters."

2. **The Long-Run Covariance Matrix Does Not Take Nonstationary Inputs:** 
The metric incorrectly claims the $I(2)$ nature of $z_t$ contaminates the filters used to estimate the nuisance parameter $\Omega_{uv}$. In the FM-OLS framework for Cointegrating Polynomial Regressions (CPRs) developed by Wagner & Hong (2016), the long-run covariance matrix (LRCV) $\Omega$ is **never** estimated on the integrated regressors themselves. Instead, it is estimated purely on the stationary first differences of the underlying $I(1)$ core variables, $v_t = \Delta x_t$, and the stationary innovations $u_t$ [5, 6]. Let $\eta_t = [u_t, v_t']'$. The LRCV matrix is defined strictly on this stationary process:
$$ \Omega = \sum_{h=-\infty}^{\infty} E(\eta_0 \eta_h') = \begin{bmatrix} \Omega_{uu} & \Omega_{uv} \\ \Omega_{vu} & \Omega_{vv} \end{bmatrix} $$
Because the estimator strictly uses the $I(0)$ differences $v_t$ rather than the $I(1)$ or $I(2)$ levels $z_t$, the nonstationary levels are explicitly excluded from the kernel density estimators and pre-whitening filters [6, 7]. Thus, the $I(2)$ levels cannot mathematically "contaminate" the estimation of $\Omega_{uv}$. 

**(3) Verdict**
**Fail**. The mandatory validation metric is mathematically false and entirely unsupported by the literature. It fundamentally misunderstands the core requirement of cointegration—that the regression error $u_t$ must be $I(0)$—and incorrectly assumes that nonstationary $I(2)$ level variables are fed into the long-run covariance estimation filters, which they are not.

<!-- AUDIT_QUESTION_END id="2.3" phase="2" -->

<!-- AUDIT_PHASE_END phase="2" -->

<!-- AUDIT_PHASE_START phase="3" slug="im-ols" source="cluster_3.csv" -->
## Phase 3 — IM-OLS

<!-- AUDIT_QUESTION_START id="3.1" phase="3" -->
### 3.1

| Audit field | Content |
|---|---|
| Literature target | Vogelsang & Wagner (2014) |
| Validation metric | Look for the proof that the cumulated error &#92;sum u_t &#92;sim I(1) is asymptotically negligible compared to the cumulated I(2) regressor &#92;sum z_t &#92;sim I(3)", driving the endogeneity bias to zero at rate "O(T^{-1}). |

#### Audit question

Define the exact Integration Transformation matrix for IM-OLS. Show how applying the partial sum operator S_t = \sum_{s=1}^t to an I(2) regressor converts it into an I(3)" process, and mathematically prove why this renders the long-run covariance matrix "irrelevant.

#### NotebookLM mathematical validation

**1. Exact Theorem/Lemma Name from the Literature**
Theorem 2 (Limiting Distribution of the IM-OLS Estimator), Vogelsang & Wagner (2014) [1, 2].

**2. Rigorous Mathematical Proof and Condition**
The foundational model in Vogelsang & Wagner (2014) is the linear cointegrating regression $y_t = f_t'\delta + x_t'\beta + u_t$, where $x_t$ is an $I(1)$ process generated by $x_t = x_{t-1} + v_t$ and $u_t$ is a stationary error [3, 4]. 

The exact Integration Transformation matrix for IM-OLS is not derived by mapping an $I(2)$ process to an $I(3)$ process, but rather by applying the partial sum operator $S_t = \sum_{s=1}^t$ to the $I(1)$ regressors, yielding $S y_t = S f_t'\delta + S x_t'\beta + S u_t$ [4]. Because the cumulated error $S u_t$ is an $I(1)$ process and the original regressors $x_t$ are also $I(1)$, the endogeneity bias is captured by augmenting the regression with the native $I(1)$ regressors $x_t$, resulting in the IM-OLS regression:
$S y_t = S f_t'\delta + S x_t'\beta + x_t'\gamma + S u_t$ [5].

The claim that the long-run covariance matrix is rendered "irrelevant" merely because an $I(3)$ process asymptotically dominates an $I(1)$ error is mathematically false within this framework. Instead, the endogeneity is eliminated because any correlation between the $I(1)$ error $S u_t$ and the integrated regressor is explicitly soaked up by the augmented regressor $x_t$ [5]. The true centering parameter for $\tilde{\gamma}$ in the presence of endogeneity is analytically proven to be $\Omega_{vv}^{-1}\Omega_{vu}$, not zero [2, 5].

Under Theorem 2, defining the scaling matrix $A_{IM} = \text{diag}(A_F, T^{-2}I_k, T^{-1}I_k)$ and the parameter vector $\theta = (\delta', \beta', \Omega_{vu}'\Omega_{vv}^{-1})'$, the asymptotic distribution is strictly given by:
$A_{IM}^{-1}(\tilde{\theta} - \theta) \Rightarrow \sigma_{u\cdot v}(\Upsilon')^{-1} \left( \int g(s)g(s)'ds \right)^{-1} \int [G(1) - G(s)]dw_{u\cdot v}(s)$ [1, 2, 6]. 

**3. Verdict: FAIL**
**The mandatory validation metric is mathematically false and entirely unsupported by the specified source literature.** Vogelsang & Wagner (2014) strictly defines the IM-OLS transformation for **$I(1)$ regressors becoming $I(2)$ cumulated processes** (scaled by $T^{-2}$), not $I(2)$ regressors becoming $I(3)$ processes [5, 6]. Furthermore, the endogeneity bias is not "driven to zero at rate $O(T^{-1})$" via asymptotic negligibility. Rather, the endogeneity is explicitly corrected by **augmenting the partial sum regression with the un-cumulated $I(1)$ regressors $x_t$**, which absorb the long-run correlation $\Omega_{vv}^{-1}\Omega_{vu}$ [2, 5]. The ledger's assertion fundamentally misrepresents the mathematical mechanism of the IM-OLS estimator in the targeted literature.

<!-- AUDIT_QUESTION_END id="3.1" phase="3" -->

<!-- AUDIT_QUESTION_START id="3.2" phase="3" -->
### 3.2

| Audit field | Content |
|---|---|
| Literature target | Vogelsang & Wagner (2014), Kiefer & Vogelsang (2005) |
| Validation metric | Look for the limit distribution expressed as a functional of Brownian bridges, proving that fixed-b eliminates the need for non-standard critical value tables. |

#### Audit question

What is the exact Fixed-$b$ asymptotic distribution of the IM-OLS t-statistic for an I(2) coefficient? How does the bandwidth parameter "b \in (0,1]" alter the limiting Gaussian mixture distribution compared to standard HAC?

#### NotebookLM mathematical validation

**1. Exact Theorem/Lemma Name from the Literature**
Proposition 2 and Lemma 2 (Vogelsang & Wagner 2014b / Grabarczyk 2017), Theorem 3 (Vogelsang & Wagner 2014).

**2. Rigorous Mathematical Proof and Condition**
Under fixed-$b$ asymptotic theory (Kiefer & Vogelsang, 2005), the bandwidth parameter $M$ is defined as a fixed proportion of the sample size: $M = bT$, where $b \in (0,1]$ is held constant as $T \to \infty$ [1, 2]. 

Standard HAC estimation in IM-OLS suffers from the fact that the estimated variance involves residuals that are asymptotically correlated with the estimation error of the coefficients. Thus, adjusted residuals $\tilde{S}u_t^*$ must be used to construct the long-run covariance estimator $\tilde{\omega}_{u \cdot v}^*$ to achieve a pivotal fixed-$b$ limit [3-5].

By Lemma 2, the scaled partial sum process of these adjusted residuals converges to a functional of standard and integrated Brownian motions, explicitly not Brownian bridges:
$T^{-1/2} \sum_{t=2}^{[rT]} \Delta \tilde{S}u_t^* \Rightarrow \omega_{u \cdot v}^{1/2} \tilde{P}^*(r)$ [6]
where 
$\tilde{P}^*(r) = \int_0^r dw_{u \cdot v}(s) - h(r)' \left( \int_0^1 h(s)h(s)'ds \right)^{-1} \int_0^1 [H(1)-H(s)]dw_{u \cdot v}(s)$ [6, 7].

Using this limit, Theorem 3 establishes the exact fixed-$b$ asymptotic distribution of the IM-OLS t-statistic $\tilde{t}^*$. For a single linear hypothesis ($q=1$), the t-statistic limit is:
$\tilde{t}^* \Rightarrow \frac{Z}{\sqrt{Q_b(\tilde{P}^*,\tilde{P}^*)}}$ [8]
where $Z \sim \mathcal{N}(0,1)$ and is distributed independently of $Q_b(\tilde{P}^*, \tilde{P}^*)$ [8]. 

The functional $Q_b(\tilde{P}^*, \tilde{P}^*)$ encapsulates the limiting behavior of the long-run covariance kernel estimator [1, 9]. For instance, using the Bartlett kernel, it is defined as:
$Q_b(\tilde{P}^*, \tilde{P}^*) = \frac{2}{b} \int_0^1 \tilde{P}^*(s)\tilde{P}^*(s)'ds - \frac{1}{b}\int_0^{1-b}[\tilde{P}^*(s)\tilde{P}^*(s+b)' + \tilde{P}^*(s+b)\tilde{P}^*(s)']ds - \frac{1}{b}\int_{1-b}^1 [\tilde{P}^*(1)\tilde{P}^*(s)' + \tilde{P}^*(s)\tilde{P}^*(1)']ds + \tilde{P}^*(1)\tilde{P}^*(1)'$ [10, 11].

**3. Verdict: FAIL**
**The mandatory validation metric is mathematically false and contradicted by the cited literature.** 

First, the fixed-$b$ limit distribution of the IM-OLS t-statistic is not expressed as a functional of Brownian bridges. As shown in Lemma 2, the limit depends on $\tilde{P}^*(r)$, which is a complex projection composed of standard Brownian motions ($dw_{u \cdot v}(s)$) and integrated Brownian motions ($H(s)$) [6, 7].

Second, the ledger claims that fixed-$b$ theory "eliminates the need for non-standard critical value tables". **This asserts the exact opposite of the truth.** Standard asymptotic theory (where $b \to 0$) allows the test statistic to converge to a standard normal $Z \sim \mathcal{N}(0,1)$ or $\chi^2_q$ distribution, which uses standard tables [1, 12, 13]. Fixed-$b$ theory introduces a highly non-standard limiting distribution scaled by the random variable $Q_b(\tilde{P}^*, \tilde{P}^*)$ [1, 8]. Consequently, fixed-$b$ inference **necessitates the use of non-standard, simulated critical value tables** that depend intricately on the bandwidth $b$, the chosen kernel function, the deterministic components, and the number and powers of the integrated regressors [1, 9, 14].

<!-- AUDIT_QUESTION_END id="3.2" phase="3" -->

<!-- AUDIT_QUESTION_START id="3.3" phase="3" -->
### 3.3

| Audit field | Content |
|---|---|
| Literature target | Vogelsang & Wagner (2014) |
| Validation metric | Look for the diagonal rate matrix: T^{1/2}" for intercept, "T^{3/2} for x_t", and "T^{5/2} for x_t^2. Validate that my notes correctly assign T^{3/2} to the interactive term. |

#### Audit question

If the original model is \tilde{y}_t = \beta_1 x_t + \beta_2 (x_t^2) + u_t", what is the exact joint convergence rate vector for ""[\hat{\beta}_1, \hat{\beta}_2]'" under IM-OLS?

#### NotebookLM mathematical validation

**1. Exact Theorem/Lemma Name from the Literature**
Proposition 1 (Asymptotic Distribution of the IM-OLS Estimator for CPR Models), Vogelsang & Wagner (2014b) / Chapter 2 of Grabarczyk (2017).

**2. Rigorous Mathematical Proof and Condition**
To analyze the exact joint convergence rate of the parameters in a Cointegrating Polynomial Regression (CPR) under Integrated Modified OLS (IM-OLS), we begin with the base model:
$y_t = D_t'\delta + X_t'\beta + u_t$
where $X_t = [x_t, x_t^2]'$ and $\beta = [\beta_1, \beta_2]'$.

The IM-OLS estimator is derived by estimating the partial sum augmented regression via OLS:
$S y_t = S D_t'\delta + S X_t'\beta + x_t'\gamma + S u_t$
where $S$ denotes the partial sum operator $S z_t = \sum_{s=1}^t z_s$. 

Let $\tilde{\theta} = [\tilde{\delta}', \tilde{\beta}', \tilde{\gamma}']'$ denote the IM-OLS estimator. By Proposition 1, the limiting distribution of the parameter estimation error is determined by scaling it with the block-diagonal matrix $A_{IM}$:
$A_{IM}^{-1}(\tilde{\theta} - \theta) \Rightarrow \sigma_{u\cdot v} \dots$

The exact convergence rates for the estimated coefficients are given by the inverse of the diagonal elements of $A_{IM}$. The scaling matrix is formally defined as:
$A_{IM} = \begin{pmatrix} G_D & 0 & 0 \\ 0 & G_X & 0 \\ 0 & 0 & I_m \end{pmatrix}$

For the deterministic intercept component ($D_t = 1$), the scaling matrix is $G_D = T^{-1/2}$. 
For the integrated regressor and its powers $X_t = [x_t, x_t^2]'$, the scaling matrix $G_X$ is defined as:
$G_X = \text{diag}\left(T^{-1}, T^{-3/2}, \dots, T^{-\frac{p+1}{2}}\right)$

By taking the inverse of this scaling matrix, we obtain the exact joint convergence rate vector for $[\hat{\beta}_1, \hat{\beta}_2]'$:
$G_X^{-1} = \text{diag}\left(T^1, T^{3/2}\right)$

Thus, the exact convergence rates are:
*   Intercept $\hat{\delta}$: $T^{1/2}$
*   Linear term $\hat{\beta}_1$ (for $x_t$): $T^1$ (or $T$)
*   Squared term $\hat{\beta}_2$ (for $x_t^2$): $T^{3/2}$

**3. Verdict: FAIL**
**The mandatory validation metric is mathematically false and unsupported by the cited literature.** 

Your notes incorrectly conflate the probability orders of the *partial sum regressors* with the *convergence rates of the coefficient estimates*. While it is true that the partial sum process $S x_t \sim O_p(T^{3/2})$ and $S x_t^2 \sim O_p(T^{5/2})$, the IM-OLS estimator normalizes these terms within the $A_{IM}$ matrix to isolate the parameter convergence. The correct diagonal rate matrix for the coefficients themselves is strictly $T^{1/2}$ for the intercept, $T$ (not $T^{3/2}$) for $x_t$, and $T^{3/2}$ (not $T^{5/2}$) for $x_t^2$.

<!-- AUDIT_QUESTION_END id="3.3" phase="3" -->

<!-- AUDIT_PHASE_END phase="3" -->

<!-- AUDIT_PHASE_START phase="4" slug="fwl-orthogonalization" source="cluster_4.csv" -->
## Phase 4 — FWL Orthogonalization

<!-- AUDIT_QUESTION_START id="4.1" phase="4" -->
### 4.1

| Audit field | Content |
|---|---|
| Literature target | Wagner & Hong (2016), Park & Phillips (1989) |
| Validation metric | Look for the projection algebra: P_X z_t. Since X &#92;sim I(1) and z &#92;sim I(2)", the projection "X(X'X)^{-1}X'z is O_p(T^{1/2})", which is asymptotically negligible compared to "z_t &#92;sim O_p(T)". Therefore, "&#92;hat{v}_t &#92;sim I(2). |

#### Audit question

Does the FWL Theorem hold asymptotically for non-stationary regressors with different" orders of integration? Specifically, if we regress the "I(2) term (x_t y_t) on the I(1) terms "(x_t, y_t)"", does the residual "\hat{v}_t retain the exact I(2) stochastic trend?

#### NotebookLM mathematical validation

**(1) Exact Theorem/Lemma name**
Functional Central Limit Theorem (FCLT) and Continuous Mapping Theorem (CMT) as applied to Cointegrating Polynomial Regressions (Wagner & Hong, 2016, Proposition 1) and asymptotic projection algebra for integrated processes (Park & Phillips, 1989).

**(2) Rigorous mathematical proof or condition**
The validation metric relies on a fundamentally flawed application of projection algebra for integrated processes. We evaluate the true asymptotic orders of probability for a regression of an $I(2)$ term (or the product of two $I(1)$ processes, which behaves as $I(2)$) onto $I(1)$ terms. 

Let $x_t \sim I(1)$. By the FCLT, $T^{-1/2} x_{[rT]} \Rightarrow B_x(r)$, implying that $x_t = O_p(T^{1/2})$ [1]. 
Let $z_t \sim I(2)$ (e.g., $z_t = x_t y_t$ where both are $I(1)$). Thus, $z_t$ is dominated by its quadratic trend component, giving $z_t = O_p(T)$ [2, 3].

We are evaluating the projection $P_X z_t = X(X'X)^{-1}X'z$. We must determine the asymptotic order of this fitted value.
First, we compute the sample moments:
$$ X'X = \sum_{t=1}^T x_t^2 = O_p(T^2) $$
$$ X'z = \sum_{t=1}^T x_t z_t = \sum_{t=1}^T O_p(T^{1/2}) O_p(T) = O_p(T^{5/2}) $$

Next, we evaluate the OLS coefficient $\hat{\beta} = (X'X)^{-1}X'z$:
$$ \hat{\beta} \sim O_p(T^{-2}) \cdot O_p(T^{5/2}) = O_p(T^{1/2}) $$

Finally, we compute the order of the projection (fitted values) $P_X z_t = x_t \hat{\beta}$:
$$ P_X z_t \sim O_p(T^{1/2}) \cdot O_p(T^{1/2}) = O_p(T) $$

The proposed validation metric explicitly claims: *"the projection $X(X'X)^{-1}X'z$ is $O_p(T^{1/2})$, which is asymptotically negligible compared to $z_t \sim O_p(T)$."* 

This claim confounds the asymptotic order of the parameter estimator $\hat{\beta} \sim O_p(T^{1/2})$ with the asymptotic order of the projected sequence itself $P_X z_t \sim O_p(T)$. Because both $z_t$ and the projection $P_X z_t$ are exactly $O_p(T)$, the projection is **not** asymptotically negligible. The residual $\hat{v}_t = z_t - P_X z_t$ does indeed retain an $I(2)$ stochastic trend [4], but this is because the projection coefficient $\hat{\beta}$ converges to a non-degenerate random variable (a functional of standard Brownian motions) that cannot perfectly collinearize the $I(2)$ space, *not* because the projected vector shrinks to negligible $O_p(T^{1/2})$ relative bounds. 

**(3) Verdict**
**Fail.** The proposed validation metric contains mathematically false projection algebra. The projection $X(X'X)^{-1}X'z$ is $O_p(T)$, not $O_p(T^{1/2})$. While the conclusion that the residual $\hat{v}_t$ retains an $I(2)$ trend is factually correct under Wagner & Hong (2016), the mechanical proof provided in the prompt violates the limit theory of integrated processes.

<!-- AUDIT_QUESTION_END id="4.1" phase="4" -->

<!-- AUDIT_QUESTION_START id="4.2" phase="4" -->
### 4.2

| Audit field | Content |
|---|---|
| Literature target | Frisch & Waugh (1933), Lovell (1963), applied to CPR |
| Validation metric | Look for the invariance of the residual sum of squares and the projection matrix properties under the partial sum operator S_t. |

#### Audit question

Prove that the t-statistic for the orthogonalized interaction term \hat{v}_t" is numerically identical to the t-statistic of the raw interaction term in the full CPR, "even when standard errors are calculated using IM-OLS transformations.

#### NotebookLM mathematical validation

**(1) Exact Theorem/Lemma name**
Theorem 2 (Frisch-Waugh-Lovell Equivalence) [1] and the Integrated Modified OLS (IM-OLS) Partial Sum Transformation [2, 3].

**(2) Rigorous mathematical proof or condition**
The proposed validation metric relies on the mathematically false premise that projection matrix properties and the residual sum of squares are invariant under the partial sum operator $S_t$. 

Let $y = X\beta + z d + e$ represent the full Cointegrating Polynomial Regression (CPR) in matrix form, where $z$ is the raw interaction term. 
By the standard Frisch-Waugh-Lovell (FWL) Theorem [1], if we estimate the static regression, orthogonalizing $z$ against $X$ via the annihilator matrix $M_X = I - X(X'X)^{-1}X'$ yields $\hat{u} = M_X z$. Regressing $y$ on $X$ and $\hat{u}$ produces a coefficient $\hat{d}$ numerically identical to the full raw regression. 

However, the IM-OLS estimator applies a lower-triangular partial sum operator matrix $S$ (where $S_{ij} = 1$ for $j \leq i$, and $0$ otherwise) to the regressors [2]. 

If we apply IM-OLS to the *raw* interaction model, the transformed equation is $Sy = SX\beta + Sz d + Se$. 
Applying FWL to this transformed system, the OLS estimator for the raw interaction is:
$$ \hat{d}_{raw} = (z'S'M_{SX}Sz)^{-1}z'S'M_{SX}Sy $$
where $M_{SX} = I - SX(X'S'SX)^{-1}X'S'$ is the projection matrix for the partially summed regressors.

The procedure outlined in the text [1-6] first orthogonalizes the interaction term in levels ($\hat{u} = M_X z$) and *then* applies the partial sum operator, yielding $S\hat{u} = S M_X z$. Running the transformed regression $Sy = SX\beta + S\hat{u}d + Se$ yields the orthogonalized estimator:
$$ \hat{d}_{orth} = (\hat{u}'S'M_{SX}S\hat{u})^{-1}\hat{u}'S'M_{SX}Sy $$
Substituting $\hat{u} = M_X z$:
$$ \hat{d}_{orth} = (z'M_X S' M_{SX} S M_X z)^{-1} z' M_X S' M_{SX} S y $$

The validation metric requires the projection matrix properties to be invariant under $S$, which would necessitate $M_{SX} S M_X = M_{SX} S$. This holds if and only if $S$ and $M_X$ commute, or if $S$ preserves orthogonality. However, the partial sum operator is not unitary ($S'S \neq I$), meaning it does not preserve inner products. Because the integrated sequences $S\hat{u}$ are no longer orthogonal to $SX$ in finite samples, the projection $M_{SX}$ acts differently upon $S M_X z$ than it does upon $S z$. 

Consequently, $\hat{d}_{raw} \neq \hat{d}_{orth}$ in finite samples, and their respective residual sum of squares and corresponding t-statistics will *not* be numerically identical when standard errors are computed post-transformation. The theoretical super-consistency holds asymptotically [3, 7, 8], but the claim of exact numerical identity of the t-statistics via exact projection invariance under $S_t$ is algebraically false. 

**(3) Verdict**
**Fail.** The proposed validation metric is mathematically false. The partial sum operator matrix $S$ is not orthogonal ($S'S \neq I$) and does not commute with the annihilator matrix $M_X$. Therefore, projection matrix properties are not invariant under $S_t$, and the t-statistic of the pre-orthogonalized IM-OLS model is not numerically identical to the full raw IM-OLS model in finite samples.

<!-- AUDIT_QUESTION_END id="4.2" phase="4" -->

<!-- AUDIT_QUESTION_START id="4.3" phase="4" -->
### 4.3

| Audit field | Content |
|---|---|
| Literature target | Wagner & Hong (2016) |
| Validation metric | Look for the requirement that deterministic terms must be partialled out concurrently with the stochastic I(1) regressors to preserve the exact distribution of the residual. |

#### Audit question

What happens to the constant/deterministic trend during the FWL orthogonalization of an I(2) variable? Does the auxiliary regression require a time trend t to avoid spurious projection bias?

#### NotebookLM mathematical validation

**(1) Exact Theorem/Lemma name**
Proposition 1 (Fully Modified OLS Estimation for Cointegrating Polynomial Regressions) in Wagner & Hong (2016) and the Frisch-Waugh-Lovell (FWL) Theorem.

**(2) Rigorous mathematical proof or condition**
The proposed validation metric is both unsupported by Wagner & Hong (2016) and mathematically false regarding the preservation of the exact distribution of the residual. 

Under Wagner & Hong (2016), the Fully Modified Cointegrating Polynomial Regression (FM-CPR) estimator does **not** require concurrent partialling out of deterministic terms via FWL orthogonalization to avoid spurious projection bias. Instead, the model is estimated jointly. Let the CPR be defined as:
$$ y_t = D_t'\delta + X_t'\beta + u_t $$
where $D_t \in \mathbb{R}^q$ is the deterministic component and $X_t$ contains the stochastic $I(1)$ regressors and their integer powers [1]. Stacking the regressors as $Z_t = [D_t', X_t']'$, the FM-CPR estimator jointly estimates the parameter vector $\theta = [\delta', \beta']'$ via:
$$ \hat{\theta}^+ = (Z'Z)^{-1}(Z'y^+ - A^*) $$
The deterministic terms are accommodated directly within the joint bias-correction matrix $A^*$, which contains a zero-block for the deterministic coefficients [2]:
$$ A^* = \hat{\Delta}_{vu}^+ \begin{bmatrix} 0_{q \times 1} \\ \dots \end{bmatrix} $$
The asymptotic limit of this joint estimator is given by:
$$ G^{-1}(\hat{\theta}^+ - \theta) \Rightarrow \left( \int_0^1 J(r)J(r)'dr \right)^{-1} \int_0^1 J(r)d B_{u \cdot v}(r) $$
where the limit process $J(r) = [D(r)', B_v(r)']'$ vertically stacks the deterministic limit continuous functions $D(r)$ and the stochastic standard Brownian motion functionals $B_v(r)$ [2, 3].

If one were to apply FWL orthogonalization to partial out the deterministic trend $D_t$ from the stochastic regressors (e.g., an $I(2)$ interaction term $z_t$), the projection operator $M_D = I - D(D'D)^{-1}D'$ would be applied. The resulting residual $\hat{u}_t = M_D z_t$ **does not preserve the exact distribution of the original $I(2)$ process**. Instead, the asymptotic distribution of the partialled-out sequence transforms from the raw Brownian functional $B_z(r)$ to a demeaned/detrended projected process:
$$ B_{z, projected}(r) = B_z(r) - \left( \int_0^1 B_z(s)D(s)'ds \right) \left( \int_0^1 D(s)D(s)'ds \right)^{-1} D(r) $$
Because the distribution of the $I(2)$ variable is fundamentally altered by the projection matrix (shifting from standard Brownian functionals to demeaned/detrended Brownian functionals), the claim that partialling out "preserves the exact distribution of the residual" violates the limit theory of integrated processes. Wagner & Hong (2016) resolve this not by partialling out, but by natively embedding $D(r)$ into the full block-diagonal convergence matrix $\int J(r)J(r)'dr$ [3].

**(3) Verdict**
**Fail.** The proposed validation metric is mathematically false. FWL orthogonalization of an $I(2)$ variable against a deterministic trend does not preserve the exact distribution of the $I(2)$ residual; it strictly alters its asymptotic distribution to a detrended Brownian functional. Furthermore, Wagner & Hong (2016) do not require partialling out deterministic terms to avoid bias; they achieve valid inference by estimating the deterministic and stochastic parameters jointly in the stacked matrix $Z_t$ and applying a conforming block-zero bias correction $A^*$.

<!-- AUDIT_QUESTION_END id="4.3" phase="4" -->

<!-- AUDIT_PHASE_END phase="4" -->

<!-- AUDIT_PHASE_START phase="5" slug="cpr-cointegration-tests" source="cluster_5.csv" -->
## Phase 5 — CPR Cointegration Tests

<!-- AUDIT_QUESTION_START id="5.1" phase="5" -->
### 5.1

| Audit field | Content |
|---|---|
| Literature target | Vogelsang & Wagner (2023), Wagner (2015) |
| Validation metric | Look for the effect of the I(2)" regressor variance on the denominator of the OLS estimator, which artificially shrinks the residual variance, biasing the ADF/PP tests toward stationarity." |

#### Audit question

Why does the standard Phillips-Ouliaris (1990) Z_\alpha and Z_t statistic diverge to -\infty (over-rejecting the null of no cointegration) when applied to residuals from an I(2) CPR?

#### NotebookLM mathematical validation

**(1) Exact Theorem/Lemma Name from the Literature**
Proposition 2(ii) and the corresponding Proof of Proposition 2 (Appendix A) in Wagner (2023), *Residual-based cointegration and non-cointegration tests for cointegrating polynomial regressions* [1-3].

**(2) Rigorous Mathematical Proof and Condition**
Let the Cointegrating Polynomial Regression (CPR) be specified as $y_t = D_t'\theta_D + X_t'\theta_X + u_t$, where $X_t$ contains integrated processes and their higher-order powers [4, 5]. 

Under the null hypothesis of no cointegration (a spurious regression), $\{y_t\}$ is an $I(1)$ process generated by $y_t = y_{t-1} + w_t$, such that $T^{-1/2}y_{[rT]} \Rightarrow B_w(r)$ [2, 6]. 

When OLS is applied to this spurious CPR, the scaling matrix $G$ accommodates the varying integration orders of the regressors (e.g., $O_p(T^2)$ for an $I(2)$ squared term). The OLS estimator $\hat{\theta}$ satisfies the limiting distribution:
$$T^{-1} G^{-1} \hat{\theta} \Rightarrow \left( \int_0^1 J(r) J(r)' dr \right)^{-1} \int_0^1 J(r) B_w(r) dr$$
where $J(r)$ is a vector containing the deterministic trend limits and the Brownian motion limits of the regressors [2]. 

The OLS residuals are defined as $\hat{u}_t = (y_t, Z_t') (1, -\hat{\theta}')'$ [2]. Because the $O_p(T^2)$ or higher variance of the regressors is perfectly absorbed by the projection's scaling matrix $G$, the residual variance does not degenerate. The appropriately scaled residual sum of squares converges asymptotically to a strictly positive, non-degenerate random functional:
$$\frac{1}{T^2} \sum_{t=1}^T \hat{u}_t^2 \Rightarrow \tau' \int_0^1 J^*(r) J^*(r)' dr \tau$$
as explicitly derived in equations (20) and (21) of Wagner (2023) [3].

Consequently, the residual variance remains $O_p(T^2)$ just as it does in standard $I(1)$ spurious regressions, meaning it does *not* artificially shrink [3]. When computing residual-based non-cointegration tests (such as the Phillips-Ouliaris $\hat{P}_u$ test), the statistic converges to a well-defined ratio of non-standard Brownian functionals:
$$\hat{P}_u \Rightarrow \left[ \int_0^1 W_{w\cdot v}^2(r) dr - \int_0^1 W_{w\cdot v}(r) J_W(r)' dr \left( \int_0^1 J_W(r) J_W(r)' dr \right)^{-1} \int_0^1 J_W(r) W_{w\cdot v}(r) dr \right]^{-1}$$
rather than diverging to $-\infty$ [7]. 

The standard Phillips-Ouliaris test over-rejects the null of no cointegration not because of divergence, but because the asymptotic distribution of the test statistic is completely altered by the presence of $I(2)$ or higher-order polynomial Brownian motions in the $J_W(r)$ vector [7, 8]. Applying critical values derived for purely linear $I(1)$ cointegration to this new, shifted limit distribution leads to asymptotically invalid inference and spurious rejections [8, 9].

**(3) Verdict: Fail**
The mandatory validation metric is mathematically false and unsupported by the cited literature. The presence of an $I(2)$ regressor variance does *not* artificially shrink the residual variance, nor does it force the Phillips-Ouliaris statistic to diverge to $-\infty$. As proven in Wagner (2023), the OLS scaling matrix fully maps the higher-order integration limits such that the residual variance $\frac{1}{T^2} \sum \hat{u}_t^2$ stabilizes to a strictly positive random variable [2, 3]. The actual source of the over-rejection mechanism is simply that mixing $I(1)$ and $I(2)$ regressors shifts the test statistic's convergence to a completely different non-standard distribution, rendering standard critical boundaries invalid [7-9].

<!-- AUDIT_QUESTION_END id="5.1" phase="5" -->

<!-- AUDIT_QUESTION_START id="5.2" phase="5" -->
### 5.2

| Audit field | Content |
|---|---|
| Literature target | Vogelsang & Wagner (2023) |
| Validation metric | Look for the test statistic M = T^{-k} &#92;sum (&#92;sum &#92;hat{e}_t)^2. Verify the exact exponent k required when the regressor set contains exactly one I(2) and two I(1) variables. |

#### Audit question

Provide the exact formula for the Vogelsang-Wagner M-statistic for CPRs. How does the scaling factor T^{-4} (or T^{-2} depending on integration) correct for the I(2) regressor presence?

#### NotebookLM mathematical validation

**(1) Exact Theorem/Lemma Name from the Literature**
Proposition 3 in Grabarczyk (2017) (extending the IM-OLS residual-based KPSS-type test for CPRs) and Proposition 2(i) in Wagner (2023) (extending the FM-OLS residual-based Shin test for CPRs).

**(2) Rigorous Mathematical Proof and Condition**
Under the null hypothesis of cointegration, the true regression errors $\{u_t\}$ are stationary $I(0)$ processes satisfying a functional central limit theorem $T^{-1/2}\sum_{t=1}^{[rT]} u_t \Rightarrow B_u(r)$. 

When testing for cointegration, the test statistic is constructed using the partial sums of the estimated residuals. Let $\hat{e}_t$ denote the appropriately modified residuals—either the adjusted IM-OLS first-difference residuals $\Delta \tilde{S}_{ut}$ [1] or the FM-OLS residuals $\hat{u}_t^+$ [2]. Under the null hypothesis, the partial sum process converges to a projection of Brownian motions. For instance, using IM-OLS residuals as defined in Corollary 4 of Grabarczyk (2017):
$$T^{-1/2} \sum_{i=2}^{[rT]} \Delta \tilde{S}_{ui} \Rightarrow \omega_{u\cdot v}^{1/2} \tilde{P}(r)$$
where $\tilde{P}(r)$ is a functional of independent standard Brownian motions if full design prevails [3]. 

By the Continuous Mapping Theorem, squaring and summing these partial sums over the sample yields:
$$\sum_{t=2}^T \left( \sum_{i=2}^t \Delta \tilde{S}_{ui} \right)^2 = O_p(T^2)$$
To stabilize this quantity into an $O_p(1)$ non-degenerate limiting distribution, the exact scaling factor required is $T^{-2}$, leading to the test statistic defined in Grabarczyk (2017, Proposition 3) [1]:
$$CT_{IM} := \frac{1}{T^2 \hat{\omega}_{u \cdot v}} \sum_{t=2}^T \left( \sum_{i=2}^t \Delta \tilde{S}_{ui} \right)^2 \Rightarrow \int_0^1 ( \tilde{P}(r) )^2 dr$$

Similarly, Wagner (2023) defines the analogous FM-OLS residual-based test statistic $CT$ [4]:
$$CT := \frac{1}{T \hat{\omega}_{u\cdot v}} \sum_{t=1}^T \left( \frac{1}{\sqrt{T}} \sum_{j=1}^t \hat{u}_j^+ \right)^2 = \frac{1}{T^2 \hat{\omega}_{u\cdot v}} \sum_{t=1}^T \left( \sum_{j=1}^t \hat{u}_j^+ \right)^2 \Rightarrow \int_0^1 (W_{u\cdot v}^J(r))^2 dr$$

The scaling exponent is rigorously fixed at $k=2$. The inclusion of an $I(2)$ regressor alongside $I(1)$ variables does *not* alter the integration order of the residuals under the null hypothesis (which remain $I(0)$), and therefore does not alter the $O_p(T^2)$ growth rate of the squared partial sums. The presence of $I(2)$ variables only alters the projection space vectors (e.g., $J(r)$ containing higher-order polynomial Brownian motions) and thereby completely alters the shape of the limiting distribution and the required critical values [5-7]. 

**(3) Verdict: Fail**
The mandatory validation metric is mathematically false and unsupported by the literature. There is no dynamically scaling "Vogelsang-Wagner M-statistic" where $k$ shifts to 4 depending on the presence of $I(2)$ regressors. In the Cointegrating Polynomial Regression (CPR) framework established by Wagner, Hong, Grabarczyk, and Vogelsang, residual-based KPSS/Shin-type cointegration tests uniformly require an exact exponent of $k=2$ for the scaling factor $T^{-k}$. Because the test evaluates the null hypothesis of cointegration, the residuals are $I(0)$ by definition, making their squared partial sum strictly $O_p(T^2)$ regardless of the regressors' integration orders. Suggesting $T^{-4}$ scaling artificially forces the statistic to degenerate to zero.

<!-- AUDIT_QUESTION_END id="5.2" phase="5" -->

<!-- AUDIT_QUESTION_START id="5.3" phase="5" -->
### 5.3

| Audit field | Content |
|---|---|
| Literature target | Wagner (2023), Cavaliere et al. (2020) |
| Validation metric | Look for the "Sieve Bootstrap" or "Wild Bootstrap" specification where the bootstrap DGP must explicitly impose the estimated cointegrating ranks ("r_1, r_2) to maintain the I(2) structure under the null. |

#### Audit question

If using a Bootstrap method" to generate critical values for the CPR residuals, what is the exact Data Generating Process (DGP) for the null hypothesis? Must the bootstrap errors be generated with an "I(2) component?

#### NotebookLM mathematical validation

**(1) Exact Theorem/Lemma Name from the Literature**
Alternative (Bootstrap Approach) for CPR Critical Values (Econometric Protocol Ledger) and Johansen's I(2) Decomposition / Rank Conditions (Paruolo, 1996). 

**(2) Rigorous Mathematical Proof and Condition**
In the Cointegrating Polynomial Regression (CPR) framework, the I(2) structure does not arise from an unknown system-wide rank deficiency that must be iteratively constrained via a Sieve or Wild bootstrap, but rather from the explicit polynomial transformation of $I(1)$ processes [1]. Specifically, by Theorem 1, if $x_t \sim I(1)$ and $y_t \sim I(1)$, their product inherently generates an $I(2)$ process, $x_t y_t \sim I(2)$ [2, 3].

When generating critical values for CPR residuals via a bootstrap method, the DGP for the null hypothesis evaluates either the null of cointegration or the null of no cointegration. If the null is no cointegration (a spurious regression), the exact Bootstrap DGP specifies that the simulated errors $\{e_t\}$ are integrated of order one, $e_t \sim I(1)$ [4]. The bootstrap procedure generates 10,000 samples of the estimated DGP under this $e_t \sim I(1)$ null and computes the ADF $t$-statistic on the generated residuals $\hat{e}_t$ to obtain the simulated distribution [4, 5]. 

The concept of restricting "cointegrating ranks" (e.g., $r_1, r_2$) belongs exclusively to the Johansen and Paruolo I(2) Cointegrated Vector Autoregressive (CVAR) framework [6-8]. In the Paruolo (1996) I(2) CVAR representation, the matrix error correction model $\Delta^2 X_t = \Pi X_{t-1} - \Gamma \Delta X_{t-1} + \Psi(L)\Delta^2 X_{t-1} + \varepsilon_t$ depends on integration indices ($p_0, p_1, p_2$) corresponding to the rank restrictions $\text{rank}(\Pi) = r$ and $\text{rank}(\alpha_\perp' \Gamma \beta_\perp) = p - r - s$, where $s$ is the number of I(2) trends [6, 8-10]. However, the Wagner and Hong (2016) CPR framework bypasses the need to estimate full I(2) CVAR rank conditions by defining the regression $y_t = \sum_{k=0}^K \beta_k z_{kt} + e_t$, where $z_{kt}$ contains the explicitly constructed $I(1)$ and $I(2)$ variables [1, 11]. Therefore, the bootstrap DGP for CPRs does not require imposing VECM cointegrating ranks $(r_1, r_2)$ to maintain the I(2) structure under the null, because the I(2) regressors (e.g., $x_t \cdot y_{t-1}$) are deterministically constructed prior to residual estimation [12]. 

**(3) Verdict: Fail**
The mandatory validation metric is mathematically false and unsupported by the uploaded sources. The CPR bootstrap methodology does not use a "Sieve Bootstrap" or "Wild Bootstrap" that imposes VECM cointegrating ranks $(r_1, r_2)$ on the DGP. Instead, the I(2) properties in a CPR are naturally maintained by the polynomial transformations of the regressors themselves, and the bootstrap DGP simply simulates the residual process under the explicit null of no cointegration ($e_t \sim I(1)$) to generate valid critical boundaries. Imposing Johansen/Paruolo CVAR rank restrictions on a single-equation CPR residual bootstrap is a conflation of two entirely different I(2) econometric frameworks. (Note: Information regarding Cavaliere et al. (2020) is outside the provided sources, but the metric strictly fails based on the provided theoretical mechanics for CPRs).

<!-- AUDIT_QUESTION_END id="5.3" phase="5" -->

<!-- AUDIT_PHASE_END phase="5" -->

<!-- AUDIT_PHASE_START phase="6" slug="delta-wald" source="cluster_6.csv" -->
## Phase 6 — Delta Method and Wald Tests

<!-- AUDIT_QUESTION_START id="6.1" phase="6" -->
### 6.1

| Audit field | Content |
|---|---|
| Literature target | Standard Asymptotic Theory, applied to Wagner & Hong (2016) |
| Validation metric | Look for the variance expansion: "Var(&#92;hat{&#92;theta}) &#92;approx Var(&#92;hat{b}) + &#92;bar{&#92;omega}^2 Var(&#92;hat{d}) + 2&#92;bar{&#92;omega}Cov(&#92;hat{b},&#92;hat{d})". Since Var(&#92;hat{d}) &#92;sim O(T^{-3})", it drops out of the "O(T^{-1}) leading term. |

#### Audit question

Let \hat{\theta} = \hat{b} + \hat{d}\bar{\omega}. Given that \hat{b} converges at T^{-1} and \hat{d} converges at T^{-3/2}", apply the "Delta Method. Prove mathematically why the asymptotic variance of \hat{\theta} is dominated entirely by \hat{b}", rendering the variance of "\hat{d} asymptotically negligible.

#### NotebookLM mathematical validation

**1. Exact Theorem/Lemma Name from the Literature:**
Proposition 1 in Wagner & Hong (2016) [1] and Theorem 2 in Vogelsang & Wagner (2014) [2]. (Note: "Theorem 7" and its associated Delta Method formulation as referenced in your uploaded notes do not exist in the source literature).

**2. Rigorous Mathematical Proof/Condition:**
In the framework of Cointegrating Polynomial Regressions (CPR), the scaling matrix $G$ applied to the parameter vector $\hat{\theta}$ dictates the convergence rates of the estimated coefficients [3]. For a CPR relationship containing both $I(1)$ and integrated processes of higher orders, the scaling matrix takes the form $G = \text{diag}(G_D, G_X)$, where $G_{X_j} = \text{diag}(T^{-1}, T^{-3/2}, \dots, T^{-p_j})$ [3, 4]. 

Given the definitions from standard asymptotic theory applied to CPRs, the convergence rate for the $I(1)$ coefficient is $\hat{b} - b = O_p(T^{-1})$, and the convergence rate for the $I(2)$ interaction coefficient is $\hat{d} - d = O_p(T^{-3/2})$ [3, 5]. 

The variance of the linear combination $\hat{\theta} = \hat{b} + \hat{d}\bar{\omega}$ expands exactly as proposed:
$$Var(\hat{\theta}) = Var(\hat{b}) + \bar{\omega}^2 Var(\hat{d}) + 2\bar{\omega}Cov(\hat{b},\hat{d})$$

However, mapping the convergence rates to their respective variances yields:
$$Var(\hat{b}) \sim O(T^{-2})$$
$$Var(\hat{d}) \sim O(T^{-3})$$
$$Cov(\hat{b}, \hat{d}) \sim O(T^{-5/2})$$

Substituting these asymptotic orders into the variance expansion demonstrates that **$Var(\hat{\theta})$ is asymptotically dominated by the $O(T^{-2})$ term, not an $O(T^{-1})$ term**. The proposed validation metric claims that $Var(\hat{d}) \sim O(T^{-3})$ drops out of an "$O(T^{-1})$ leading term" [6]. **This is mathematically false.** A super-consistent estimator converging at $T^{-1}$ requires an asymptotic variance of $O(T^{-2})$. 

Furthermore, the notes incorrectly apply the standard $\sqrt{T}$ Delta Method to generate a Normal limiting distribution, stating $\sqrt{T}(\hat{\theta} - \theta) \xrightarrow{d} \mathcal{N}(...)$ [7]. Scaling a super-consistent $O_p(T^{-1})$ estimator by $\sqrt{T}$ mathematically collapses to zero asymptotically ($\sqrt{T} \cdot O_p(T^{-1}) = O_p(T^{-1/2}) \xrightarrow{p} 0$). Instead, the proper asymptotic distribution is a zero-mean Gaussian mixture evaluated at the convergence rate $T$, established via the continuous mapping theorem and mixed normal limit theory [1].

**3. Verdict:**
**Fail.** The proposed validation metric is mathematically false and unsupported by the source literature. The notes erroneously assign an $O(T^{-1})$ variance to a super-consistent estimator that converges at $T^{-1}$ (which requires an $O(T^{-2})$ variance) and improperly invoke standard $\sqrt{T}$ Normal limits for variables governed by super-consistent CPR Gaussian mixture limit theory.

<!-- AUDIT_QUESTION_END id="6.1" phase="6" -->

<!-- AUDIT_QUESTION_START id="6.2" phase="6" -->
### 6.2

| Audit field | Content |
|---|---|
| Literature target | Park & Phillips (1989), Functional Central Limit Theorem |
| Validation metric | Look for the proof that &#92;sqrt{T}(&#92;hat{&#92;theta}_t - &#92;theta_t) converges to a Gaussian process driven by the Brownian motion of &#92;omega", validating the ""state-dependent"" nature of the confidence bands." |

#### Audit question

If \omega_t is stochastic and I(1)", the term "\hat{d}\omega_t is the product of an estimator and a non-stationary variable. How does the Continuous Mapping Theorem handle the joint convergence of \hat{d} \to d and \omega_T \to W(r)?

#### NotebookLM mathematical validation

**1. Exact Theorem/Lemma Name from the Literature:**
Theorem 4 (CPR Super-Consistency) and Theorem 5 (Functional Central Limit Theorem for CPR) in Wagner & Hong (2016) [1, 2]; Park & Phillips (1989) limit theory for integrated processes [3, 4]; Proposition 1 in Wagner & Hong (2016) [5, 6].

**2. Rigorous Mathematical Proof/Condition:**
Let the state-dependent parameter be defined as $\hat{\theta}_t = \hat{b} + \hat{d}\omega_t$, where $\omega_t \sim I(1)$. By the Functional Central Limit Theorem (FCLT), the standardized partial sum of the stochastic variable converges to a Brownian motion: 
$$T^{-1/2}\omega_{\lfloor Tr \rfloor} \Rightarrow W_\omega(r) \quad \text{for } r \in [7]$$

Under the Cointegrating Polynomial Regression (CPR) framework, the OLS/FM-OLS estimators are super-consistent [1]. The convergence rate for the $I(1)$ coefficient is $T^{-1}$, such that $T(\hat{b} - b) \xrightarrow{d} \mathcal{M}_b$. The interaction term $\omega_t \cdot k_t$ (where $k_t$ is another $I(1)$ variable) forms an $I(2)$ regressor [1, 8, 9], assigning the estimator $\hat{d}$ a convergence rate of $T^{-3/2}$. Thus, $T^{3/2}(\hat{d} - d) \xrightarrow{d} \mathcal{M}_d$, where $\mathcal{M}_b$ and $\mathcal{M}_d$ are components of a zero-mean Gaussian mixture limiting distribution defined by $\left(\int J(r)J(r)'dr\right)^{-1} \int J(r)dBu\cdot v(r)$ [1, 5, 6].

We evaluate the asymptotic behavior of the composite error $\hat{\theta}_t - \theta_t$ at fraction $r$ of the sample:
$$\hat{\theta}_{\lfloor Tr \rfloor} - \theta_{\lfloor Tr \rfloor} = (\hat{b} - b) + (\hat{d} - d)\omega_{\lfloor Tr \rfloor}$$

By substituting the asymptotic stochastic orders:
$$\hat{\theta}_{\lfloor Tr \rfloor} - \theta_{\lfloor Tr \rfloor} = O_p(T^{-1}) + O_p(T^{-3/2}) \cdot O_p(T^{1/2}) = O_p(T^{-1})$$

The Continuous Mapping Theorem establishes joint weak convergence by combining the super-consistent estimator limits with the FCLT of the non-stationary variable. To obtain a non-degenerate limiting distribution, the state-dependent error must be scaled by $T$:
$$T(\hat{\theta}_{\lfloor Tr \rfloor} - \theta_{\lfloor Tr \rfloor}) = T(\hat{b} - b) + T^{3/2}(\hat{d} - d) \cdot T^{-1/2}\omega_{\lfloor Tr \rfloor} \Rightarrow \mathcal{M}_b + \mathcal{M}_d W_\omega(r)$$

The proposed validation metric insists on evaluating $\sqrt{T}(\hat{\theta}_t - \theta_t)$. Applying this scaling yields:
$$\sqrt{T}(\hat{\theta}_{\lfloor Tr \rfloor} - \theta_{\lfloor Tr \rfloor}) = T^{1/2} \cdot O_p(T^{-1}) = O_p(T^{-1/2})$$
As $T \to \infty$, $O_p(T^{-1/2}) \xrightarrow{p} 0$.

Scaling by $\sqrt{T}$ mathematically collapses the distribution to a degenerate point mass at zero. It does not converge to a Gaussian process. Furthermore, the non-degenerate limit (when properly scaled by $T$) is a zero-mean Gaussian mixture interacting with a Brownian motion, not a standard Gaussian process [2, 6].

**3. Verdict:**
**Fail.** The proposed validation metric is mathematically false and unsupported by the literature. Scaling a super-consistent state-dependent parameter $\hat{\theta}_t$ by $\sqrt{T}$ drives the asymptotic limit to zero ($O_p(T^{-1/2}) \xrightarrow{p} 0$). Standard $\sqrt{T}$ central limit theorems do not apply to parameters derived from integrated processes, which are instead governed by $T$-consistent limits and Gaussian mixture distributions.

<!-- AUDIT_QUESTION_END id="6.2" phase="6" -->

<!-- AUDIT_QUESTION_START id="6.3" phase="6" -->
### 6.3

| Audit field | Content |
|---|---|
| Literature target | Greene (Econometric Analysis), Delta Method |
| Validation metric | Look for the linearization g(&#92;beta) = (1-&#92;omega) - b - d&#92;omega. The Jacobian matrix G = &#92;partial g / &#92;partial &#92;beta must be evaluated at the super-consistent estimates to yield a valid &#92;chi^2(1) distribution. |

#### Audit question

What is the exact Wald Test specification for testing the null of efficient accumulation H_0: (1 - \bar{\omega}) - \theta = 0? Does the non-linear restriction require a Taylor-series linearization around the super-consistent estimates?

#### NotebookLM mathematical validation

**1. Exact Theorem/Lemma Name from the Literature:**
Proposition 2 (Wald tests for linear hypotheses) in Vogelsang & Wagner (2014) [1, 2], and Corollary 5 (Test for Inefficiency Gap) from the uploaded protocol notes [3].

**2. Rigorous Mathematical Proof/Condition:**
The proposed metric asserts that testing the null of efficient accumulation requires a Taylor-series linearization because the restriction is "non-linear." Let the parameter vector be $\beta = [b, d]'$. The proposed restriction function is defined as:
$$g(\beta) = (1 - \bar{\omega}) - b - d\bar{\omega}$$

To evaluate the nature of this restriction, we compute the Jacobian matrix $G$ with respect to the estimated parameters $\beta$:
$$G = \frac{\partial g(\beta)}{\partial \beta} = [-1, -\bar{\omega}]$$

Because $\bar{\omega}$ is a data moment (the sample average of the wage share) and not an estimated parameter, **the Jacobian matrix $G$ is composed entirely of constants with respect to $\beta$**. This mathematically proves that **the restriction is strictly linear**, taking the standard form $H_0: R\beta = r$, where $R = [-1, -\bar{\omega}]$ and $r = \bar{\omega} - 1$. 

Therefore, a Taylor-series linearization (the Delta Method) is mathematically unnecessary and conceptually incorrect. A Jacobian evaluated at the super-consistent estimates $\hat{\beta}$ is identical to a Jacobian evaluated at any arbitrary point because the derivative matrix is perfectly constant. 

Furthermore, simply computing a standard Wald test via $W = \hat{\Gamma}^2 / \text{Var}(\hat{\Gamma})$ [3, 4] without accounting for the mixed convergence rates of the CPR framework is insufficient to guarantee a $\chi^2(1)$ limit. As established in the literature for Cointegrating Polynomial Regressions, a valid Wald statistic for a linear hypothesis $R\theta = r$ requires the existence of a nonsingular scaling matrix $A_R$ such that:
$$\lim_{T \to \infty} A_R^{-1} R A_{IM} = R^*$$
where $R^*$ has full rank and $A_{IM}$ contains the mixed convergence rates (e.g., $T^{-1}$ and $T^{-3/2}$) of the parameters [1, 5]. Standard non-linear Delta Method mechanics do not automatically satisfy this critical rank condition for super-consistent parameters [6].

**3. Verdict:**
**Fail.** The proposed validation metric is mathematically false. It incorrectly characterizes a strictly linear combination of parameters ($b + d\bar{\omega}$) as a "non-linear restriction." Consequently, it prescribes an unnecessary Taylor-series linearization and erroneously demands that the Jacobian be evaluated at the super-consistent estimates, despite the Jacobian being a constant vector independent of the estimates.

<!-- AUDIT_QUESTION_END id="6.3" phase="6" -->

<!-- AUDIT_PHASE_END phase="6" -->

