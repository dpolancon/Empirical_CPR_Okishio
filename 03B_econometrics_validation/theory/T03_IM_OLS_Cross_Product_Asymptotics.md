**We must derive T03 first.** 

Running a Monte Carlo simulation before formally deriving the asymptotic properties of the IM-OLS estimator for cross-products is flying blind. If you simulate the model without knowing the exact stochastic orders and the asymptotic distribution, you will not know:
1. Which normalization matrix to apply to the estimator in the simulation loop ($T$, $T^{1.5}$, or $T^2$?).
2. Whether the coverage failures in your previous smoke test were due to a coding bug or a fundamental misunderstanding of the limit theory.
3. How to construct the correct fixed-$b$ standard errors for the cross-product topology.

Deriving T03 provides the exact mathematical blueprint that the Monte Carlo simulation must test. Furthermore, this derivation reveals a beautiful mathematical reason *why* IM-OLS works for cross-products while FM-OLS fails.

Below is the formal derivation for **Task T03**. You can save this directly to your repository as `theory/T03_IM_OLS_Cross_Product_Asymptotics.md`.

***

# Theory Note T03: IM-OLS Asymptotics and the Annihilation of Endogeneity in Cross-Product CPRs

## 1. Correction to T01: The True OLS Convergence Rate
In T01, we established that the partial sum of the cross-product $z_t = x_t y_t$ scales with $T^{-2}$, meaning $z_t = O_p(T)$. 
Let us strictly define the OLS estimator on the levels equation $Y_t = \beta z_t + u_t$:
$$ \hat{\beta}_{OLS} - \beta = \frac{\sum_{t=1}^T z_t u_t}{\sum_{t=1}^T z_t^2} $$

*   **Denominator:** Since $z_t = O_p(T)$, $z_t^2 = O_p(T^2)$. Summing $T$ terms yields $\sum z_t^2 = O_p(T^3)$.
*   **Numerator:** By the Functional Central Limit Theorem (FCLT), $T^{-1} z_{\lfloor Tr \rfloor} \Rightarrow W_x(r) W_y(r)$. The error $u_t$ is $I(0)$. The sum $\sum z_t u_t$ behaves as a martingale difference sum scaled by $T$. Therefore, $\sum z_t u_t = O_p(T^{1.5})$.
*   **OLS Rate:** $\hat{\beta}_{OLS} - \beta = \frac{O_p(T^{1.5})}{O_p(T^3)} = \mathbf{O_p(T^{-1.5})}$.

**Correction:** OLS on the cross-product converges at rate **$T^{1.5}$** (not $T$). However, the limit distribution is severely contaminated by endogeneity.

## 2. The IM-OLS Transformation and Stochastic Orders
Integrated Modified OLS (IM-OLS) applies the partial sum operator $S_t = \sum_{j=1}^t$ to both sides of the regression:
$$ \tilde{Y}_t = \beta \tilde{z}_t + \tilde{u}_t $$
where $\tilde{z}_t = \sum_{j=1}^t x_j y_j$ and $\tilde{u}_t = \sum_{j=1}^t u_j$.

Let us map the stochastic orders using the FCLT limits:
1.  **The Integrated Regressor ($\tilde{z}_t$):** 
    Since $z_t = O_p(T)$, its partial sum scales one order higher: $\tilde{z}_t = O_p(T^2)$.
    Functional limit: $T^{-2} \tilde{z}_{\lfloor Tr \rfloor} \Rightarrow \int_0^r W_x(s) W_y(s) ds \equiv J(r)$.
2.  **The Integrated Error ($\tilde{u}_t$):** 
    Since $u_t = I(0)$ is $O_p(1)$, its partial sum is $I(1)$: $\tilde{u}_t = O_p(T^{1/2})$.
    Functional limit: $T^{-1/2} \tilde{u}_{\lfloor Tr \rfloor} \Rightarrow W_u(r)$.

## 3. The IM-OLS Limit Distribution
The IM-OLS estimator is:
$$ \hat{\beta}_{IM} - \beta = \frac{\sum_{t=1}^T \tilde{z}_t \tilde{u}_t}{\sum_{t=1}^T \tilde{z}_t^2} $$

*   **Denominator:** $\tilde{z}_t^2 = O_p(T^4)$. Summing $T$ terms yields $O_p(T^5)$.
    $$ T^{-5} \sum_{t=1}^T \tilde{z}_t^2 \Rightarrow \int_0^1 J(r)^2 dr $$
*   **Numerator:** $\tilde{z}_t \tilde{u}_t = O_p(T^2) \cdot O_p(T^{1/2}) = O_p(T^{2.5})$. Summing $T$ terms yields $O_p(T^{3.5})$.
    $$ T^{-3.5} \sum_{t=1}^T \tilde{z}_t \tilde{u}_t \Rightarrow \int_0^1 J(r) W_u(r) dr $$

**The IM-OLS Rate:**
$$ \hat{\beta}_{IM} - \beta = \frac{O_p(T^{3.5})}{O_p(T^5)} = \mathbf{O_p(T^{-1.5})} $$

**Crucial Finding:** IM-OLS converges at the **exact same rate** ($T^{1.5}$) as OLS on levels. The advantage of IM-OLS is *not* a faster convergence rate; it is the **topology of the limit distribution**.

## 4. The Annihilation of Endogeneity (Itô vs. Riemann)
Why does IM-OLS bypass the need for Long-Run Covariance (LRCV) estimation, which plagues FM-OLS for cross-products? The answer lies in the type of stochastic integral generated in the numerator.

*   **In OLS (and FM-OLS):** The numerator involves the level error $u_t$. The limit is an **Itô Integral**: $\int_0^1 W_x(r) W_y(r) dW_u(r)$. Because the integrator $dW_u$ is a martingale difference, the correlation between the regressor increments and error increments generates a complex, path-dependent endogeneity bias ($\Lambda_{zu}$) that cannot be purged with standard kernel estimators.
*   **In IM-OLS:** The numerator involves the *integrated* error $\tilde{u}_t$. The limit is a **Riemann Integral**: $\int_0^1 J(r) W_u(r) dr$. 

Because the integration operator acts as a natural low-pass filter, the high-frequency endogeneity (the correlation between $\Delta z_t$ and $u_t$) is asymptotically smoothed out. The Riemann integral $\int J(r) W_u(r) dr$ does not contain the one-sided long-run covariance nuisance parameter. 

**Theorem 2 (IM-OLS Nuisance Parameter Irrelevance for Cross-Products):**
> For a Cointegrating Polynomial Regression containing the cross-product of $I(1)$ processes, the IM-OLS estimator $\hat{\beta}_{IM}$ converges at rate $T^{1.5}$ to a mixed-normal limit distribution. Because the limit numerator is a Riemann integral of continuous processes, the endogeneity bias is asymptotically annihilated. Standard fixed-$b$ inference (using integrated residuals) yields asymptotically standard normal $t$-statistics without requiring explicit estimation of the cross-product LRCV matrix.