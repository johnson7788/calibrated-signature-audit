# 复现审计结果

> 判定含义：robust=通过主检验且稳健性检查达标；fragile=主检验通过但稳健性不达标；not_reproduced=主检验未通过；inconclusive=数据不足。

| 主张 | 模式 | 特征数 | 效应 | p | 判定 |
|---|---|---|---|---|---|
| xstudy-scan: 跨队列：GSE95132 肿瘤 vs 癌旁（扫描） | scan | 23640 | -0.106 | 1.65e-06 | **signal_found** |
| xstudy-up: 跨队列复现：GSE50760 Atlas 上调签名 → GSE95132 | signature | 81 | 0.939 | 0.000488 | **robust** |
| xstudy-down: 跨队列复现：GSE50760 Atlas 下调签名 → GSE95132 | signature | 86 | -1.205 | 0.00342 | **robust** |
| xstudy-splitup: 跨队列复现：GSE50760 训练集上调签名 → GSE95132 | signature | 99 | 1.014 | 0.000488 | **robust** |
| xstudy-splitdown: 跨队列复现：GSE50760 训练集下调签名 → GSE95132 | signature | 98 | -1.240 | 0.0522 | **not_reproduced** |

## 明细

### xstudy-scan: 跨队列：GSE95132 肿瘤 vs 癌旁（扫描）

```json
{
  "n_hits_fdr": 35,
  "fdr": 0.05,
  "paired": true,
  "top_hits": {
    "CDH3": 3.212,
    "SERPINB5": 2.654,
    "NRXN1": -2.597,
    "CNR1": -2.508,
    "NAALADL1": -2.453,
    "PSAT1": 2.344,
    "EYA2": -2.21,
    "LGI4": -2.074,
    "PCSK9": 2.065,
    "USP2": -2.064
  },
  "sign_consistency_median": 0.6666666666666666
}
```

### xstudy-up: 跨队列复现：GSE50760 Atlas 上调签名 → GSE95132

```json
{
  "paired": true,
  "claimed_direction": "a_gt_b",
  "dir_ok": true,
  "leave_one_out": {
    "applicable": true,
    "pass_fraction": 1.0,
    "n_runs": 12
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```

### xstudy-down: 跨队列复现：GSE50760 Atlas 下调签名 → GSE95132

```json
{
  "paired": true,
  "claimed_direction": "a_lt_b",
  "dir_ok": true,
  "leave_one_out": {
    "applicable": true,
    "pass_fraction": 1.0,
    "n_runs": 12
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```

### xstudy-splitup: 跨队列复现：GSE50760 训练集上调签名 → GSE95132

```json
{
  "paired": true,
  "claimed_direction": "a_gt_b",
  "dir_ok": true,
  "leave_one_out": {
    "applicable": true,
    "pass_fraction": 1.0,
    "n_runs": 12
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```

### xstudy-splitdown: 跨队列复现：GSE50760 训练集下调签名 → GSE95132

```json
{
  "paired": true,
  "claimed_direction": "a_lt_b",
  "dir_ok": true,
  "leave_one_out": {
    "applicable": true,
    "pass_fraction": 0.25,
    "n_runs": 12
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```
