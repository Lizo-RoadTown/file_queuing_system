# Diff report - Stochastic modeling of a mosquito-borne disease

**Curator:** @lmmaganto  
**Reviewer:** @Jampip  
**DOI:** https://doi.org/10.1186/s13662-020-02803-w  
**Figure:** 2 (#Source: see page 12)  
**Generated:** 2026-05-21 18:38 UTC  

---

## Summary

| | Count |
|---|---|
| Cells compared | 4 |
| Cells agreed | 3 |
| Cells with differences | 1 |
| Total lines changed | 12 |

## Agreements (3 cells)

The following cells matched exactly between curator and reviewer.

---

## Differences (12 lines changed across 1 cells)

### Cell 1 - page 12 under the figure 2

```diff
@@ -39,5 +39,6 @@
     A = 10000*(0.017/365),
     B = 240000 * (0.04),
-    a = 6.417E-5,
+    #changed -5 to -6 to match the paper
+    a = 6.417E-6,
     b = 0.075,
     c = 0.0375,
@@ -69,11 +70,14 @@
     """
     s, i, r, v, j = y
-    n = s + i + r
-    m = v + t 
+    # This paper’s SDE system doesn't use N or M directly in the drift/diffusion equations, so not needed in the code. 
+    #n = s + i + r
+    #m = v + t 
     mu, delta, theta, A, B, a, b, c, k, h,sigma,zeta  = p
     return [
         A - a * b * s * j + h * r - mu * s,
-        a * b * s * j - mu + k + delta * i,
-        k * i - mu + h * r,
+        #added parenthesis
+        a * b * s * j - (mu + k + delta) * i,
+        #added parenthesis
+        k * i - (mu + h) * r,
         B - a * c * v * i - theta * v,
         a * c * v * i - theta * j
@@ -93,6 +97,7 @@
     """
     s, i, r, v, j = y
-    n = s + i + r
-    m = v + t 
+    # This paper’s SDE system doesn't use N or M directly in the drift/diffusion equations, so not needed in the code. 
+    #n = s + i + r
+    #m = v + t 
     mu, delta, theta, A, B, a, b, c, k, h,sigma,zeta = p
     return [
```

**Reason:** not provided

---

## Curator notification

@lmmaganto - your submission has been second reviewed by @Jampip.

12 line(s) changed across 1 cell(s):

- `a = 6.417E-5,` changed to `#changed -5 to -6 to match the paper` - no reason provided
- `n = s + i + r` changed to `a = 6.417E-6,` - no reason provided
- `m = v + t` changed to `# This paper’s SDE system doesn't use N or M directly in the drift/diffusion equations, so not needed in the code.` - no reason provided
- `a * b * s * j - mu + k + delta * i,` changed to `#n = s + i + r` - no reason provided
- `k * i - mu + h * r,` changed to `#m = v + t` - no reason provided
- `n = s + i + r` changed to `#added parenthesis` - no reason provided
- `m = v + t` changed to `a * b * s * j - (mu + k + delta) * i,` - no reason provided
- added `#added parenthesis`
- added `k * i - (mu + h) * r,`
- added `# This paper’s SDE system doesn't use N or M directly in the drift/diffusion equations, so not needed in the code.`
- added `#n = s + i + r`
- added `#m = v + t`

If you agree with the changes comment `/complete` to finalize.
If you disagree comment on this issue explaining why.
The reviewer can update their notebook and comment `/approve` again to regenerate this report.
