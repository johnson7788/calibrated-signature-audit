# 复现审计结果

> 判定含义：robust=通过主检验且稳健性检查达标；fragile=主检验通过但稳健性不达标；not_reproduced=主检验未通过；inconclusive=数据不足。

## 方法学元数据（审计前锁定）

| 主张 | 模式 | 检验 | alpha | min_effect | min_stable |
|---|---|---|---|---|---|
| meth-crc-vs-adj | scan | welch_ttest | 0.05 | 0.1 | - |
| meth-adenoma-vs-normal | scan | welch_ttest | 0.05 | 0.1 | - |

## 审计结果

| 主张 | 模式 | 特征数 | 效应 | p | 判定 |
|---|---|---|---|---|---|
| meth-crc-vs-adj: 甲基化：CRC vs 癌旁正常（非配对扫描） | scan | 485578 | -0.003 | 2.49e-36 | **signal_found** |
| meth-adenoma-vs-normal: 甲基化：腺瘤 vs 健康正常（非配对扫描） | scan | 485578 | -0.025 | 3.93e-31 | **signal_found** |

## 明细

### meth-crc-vs-adj: 甲基化：CRC vs 癌旁正常（非配对扫描）

```json
{
  "n_hits_fdr": 78552,
  "fdr": 0.05,
  "paired": false,
  "test": "welch_ttest",
  "min_effect": 0.1,
  "top_hits": {
    "cg21101720": 0.589,
    "cg26256223": 0.541,
    "cg13895235": 0.541,
    "cg03061682": 0.527,
    "cg17698295": 0.522,
    "cg07136998": 0.522,
    "cg05920961": 0.519,
    "cg09296001": 0.518,
    "cg18601167": 0.515,
    "cg09383816": 0.508
  },
  "sign_consistency_median": 1.0
}
```

### meth-adenoma-vs-normal: 甲基化：腺瘤 vs 健康正常（非配对扫描）

```json
{
  "n_hits_fdr": 116917,
  "fdr": 0.05,
  "paired": false,
  "test": "welch_ttest",
  "min_effect": 0.1,
  "top_hits": {
    "cg09296001": 0.593,
    "cg14015706": 0.564,
    "cg17128947": 0.549,
    "cg11017065": 0.548,
    "cg13895235": 0.547,
    "cg06197966": -0.541,
    "cg17892556": 0.54,
    "cg06834177": -0.538,
    "cg19114576": -0.537,
    "cg23401796": -0.536
  },
  "sign_consistency_median": 1.0
}
```
