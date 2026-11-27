# 复现审计结果

> 判定含义：robust=通过主检验且稳健性检查达标；fragile=主检验通过但稳健性不达标；not_reproduced=主检验未通过；inconclusive=数据不足。

## 方法学元数据（审计前锁定）

| 主张 | 模式 | 检验 | alpha | min_effect | min_stable |
|---|---|---|---|---|---|
| gse50760-scan | scan | paired_ttest | 0.05 | 1.0 | - |
| gse50760-up | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| gse50760-down | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |

## 审计结果

| 主张 | 模式 | 特征数 | 效应 | p | 判定 |
|---|---|---|---|---|---|
| gse50760-scan: GSE50760: 原发肿瘤 vs 正常（配对扫描） | scan | 23503 | 0.001 | 3.75e-10 | **signal_found** |
| gse50760-up: 论文声称：原发肿瘤上调 signature（Atlas top-100 up） | signature | 80 | 1.402 | 1.53e-05 | **robust** |
| gse50760-down: 论文声称：原发肿瘤下调 signature（Atlas top-100 down） | signature | 86 | -1.448 | 1.53e-05 | **robust** |

## 明细

### gse50760-scan: GSE50760: 原发肿瘤 vs 正常（配对扫描）

```json
{
  "n_hits_fdr": 847,
  "fdr": 0.05,
  "paired": true,
  "test": "paired_ttest",
  "min_effect": 1.0,
  "top_hits": {
    "CA1": -5.106,
    "AQP8": -4.842,
    "CLCA4": -4.815,
    "CA7": -4.652,
    "BEST4": -4.534,
    "GUCA2B": -4.516,
    "MS4A12": -4.392,
    "OTOP2": -4.216,
    "TMIGD1": -4.205,
    "SLC26A3": -4.152
  },
  "sign_consistency_median": 0.7222222222222222
}
```

### gse50760-up: 论文声称：原发肿瘤上调 signature（Atlas top-100 up）

```json
{
  "paired": true,
  "claimed_direction": "a_gt_b",
  "dir_ok": true,
  "test": "wilcoxon_signed_rank",
  "alpha": 0.05,
  "min_effect": 0.5,
  "leave_one_out": {
    "applicable": true,
    "pass_fraction": 1.0,
    "n_runs": 18
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```

### gse50760-down: 论文声称：原发肿瘤下调 signature（Atlas top-100 down）

```json
{
  "paired": true,
  "claimed_direction": "a_lt_b",
  "dir_ok": true,
  "test": "wilcoxon_signed_rank",
  "alpha": 0.05,
  "min_effect": 0.5,
  "leave_one_out": {
    "applicable": true,
    "pass_fraction": 1.0,
    "n_runs": 18
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```
