# Review Notes

  - Reviewer: Jampip
  - Checkout Time: 2026-05-20T18:44:43.888Z
  - Paper Folder: Witbooi_Malaria
  - Issue: #29

  ## Summary
  A few minor mistakes that were corrected in reviewers copy. See copy, update, and resubmit.

  ## Required Changes
  Parameter_value (a) was off by a magnitude, change from a = 6.417E-5 to a = 6.417E-6.
  You do not need N and M as separate model variables, delete or comment out N and M equations from diff and drift.
  Paper states di = a * b * s * j - (mu + k + delta) * i. Parenthesis were added to multiply the sum of parameters mu, k, and delta to i.
  Paper states dr = k * i - (mu + h) * r. Parenthesis were added to multiply the sum of parameters mu and h to r.

  ## Comments
  The above changes resulted in a slightly different graph. 
  ## Decision
  - [ ] Approved
  - [X] Needs Changes
  