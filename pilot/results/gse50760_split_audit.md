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
| split-scan: 半样本验证：测试集原发 vs 正常（扫描） | scan | 23503 | -0.019 | 1.68e-07 | **signal_found** |
| split-up: 半样本验证：训练集上调 signature 在测试集复现 | signature | 100 | 1.718 | 0.00391 | **robust** |
| split-down: 半样本验证：训练集下调 signature 在测试集复现 | signature | 100 | -2.418 | 0.0117 | **robust** |

## 明细

### split-scan: 半样本验证：测试集原发 vs 正常（扫描）

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

### split-up: 半样本验证：训练集上调 signature 在测试集复现

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

### split-down: 半样本验证：训练集下调 signature 在测试集复现

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
