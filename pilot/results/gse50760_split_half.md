# 半样本审计（out-of-sample）

- 训练配对：9（2, 3, 5, 6, 7, 8, 9, 10, 12）
- 留出配对：9（13, 17, 18, 19, 20, 21, 22, 23, 24）
- 签名规模：top-100，|delta|≥1.5
- 阈值：alpha=0.05，min_stable=0.8

# 复现审计结果

> 判定含义：robust=通过主检验且稳健性检查达标；fragile=主检验通过但稳健性不达标；not_reproduced=主检验未通过；inconclusive=数据不足。

## 方法学元数据（审计前锁定）

| 主张 | 模式 | 检验 | alpha | min_effect | min_stable |
|---|---|---|---|---|---|
| split-scan | scan | paired_ttest | 0.05 | 1.0 | - |
| split-up | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| split-down | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |

## 审计结果

| 主张 | 模式 | 特征数 | 效应 | p | 判定 |
|---|---|---|---|---|---|
| split-scan: 留出集扫描 | scan | 23503 | -0.019 | 1.68e-07 | **signal_found** |
| split-up: 训练集上调签名 → 留出集 | signature | 100 | 1.718 | 0.00391 | **robust** |
| split-down: 训练集下调签名 → 留出集 | signature | 100 | -2.418 | 0.0117 | **robust** |

## 明细

### split-scan: 留出集扫描

```json
{
  "n_hits_fdr": 164,
  "fdr": 0.05,
  "paired": true,
  "test": "paired_ttest",
  "min_effect": 1.0,
  "top_hits": {
    "CA7": -4.374,
    "BEST4": -4.309,
    "OTOP2": -4.169,
    "SPIB": -3.211,
    "ETV4": 3.054,
    "MMP7": 2.855,
    "ANPEP": -2.849,
    "ADH1B": -2.811,
    "CFD": -2.694,
    "SCARA5": -2.529
  },
  "sign_consistency_median": 0.7777777777777778
}
```

### split-up: 训练集上调签名 → 留出集

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
    "n_runs": 9
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```

### split-down: 训练集下调签名 → 留出集

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
    "n_runs": 9
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```
