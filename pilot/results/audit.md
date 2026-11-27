# 复现审计结果

> 判定含义：robust=通过主检验且稳健性检查达标；fragile=主检验通过但稳健性不达标；not_reproduced=主检验未通过；inconclusive=数据不足。

## 方法学元数据（审计前锁定）

| 主张 | 模式 | 检验 | alpha | min_effect | min_stable |
|---|---|---|---|---|---|
| demo-scan | scan | paired_ttest | 0.05 | 1.0 | - |
| demo-sig-neg | signature | wilcoxon_signed_rank | 0.05 | 0.2 | 0.8 |

## 审计结果

| 主张 | 模式 | 特征数 | 效应 | p | 判定 |
|---|---|---|---|---|---|
| demo-scan: E-MTAB-8316: UNC106238 vs none 全特征扫描（配对设计） | scan | 36719 | -0.007 | 1.74e-05 | **no_signal** |
| demo-sig-neg: 负向对照：随机 50 基因签名（预期 not_reproduced/fragile） | signature | 50 | -0.006 | 0.844 | **not_reproduced** |

## 明细

### demo-scan: E-MTAB-8316: UNC106238 vs none 全特征扫描（配对设计）

```json
{
  "n_hits_fdr": 0,
  "fdr": 0.05,
  "paired": true,
  "test": "paired_ttest",
  "min_effect": 1.0,
  "top_hits": {},
  "sign_consistency_median": 0.5
}
```

### demo-sig-neg: 负向对照：随机 50 基因签名（预期 not_reproduced/fragile）

```json
{
  "paired": true,
  "claimed_direction": "any",
  "dir_ok": true,
  "test": "wilcoxon_signed_rank",
  "alpha": 0.05,
  "min_effect": 0.2,
  "leave_one_out": {
    "applicable": true,
    "pass_fraction": 0.0,
    "n_runs": 6
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```
