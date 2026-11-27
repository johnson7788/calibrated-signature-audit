# 复现审计结果

> 判定含义：robust=通过主检验且稳健性检查达标；fragile=主检验通过但稳健性不达标；not_reproduced=主检验未通过；inconclusive=数据不足。

| 主张 | 模式 | 特征数 | 效应 | p | 判定 |
|---|---|---|---|---|---|
| splitdown-a0.01: 下调签名 alpha=0.01 | signature | 98 | -1.240 | 0.0522 | **not_reproduced** |
| splitdown-a0.05: 下调签名 alpha=0.05 | signature | 98 | -1.240 | 0.0522 | **not_reproduced** |
| splitdown-a0.1: 下调签名 alpha=0.1 | signature | 98 | -1.240 | 0.0522 | **fragile** |

## 明细

### splitdown-a0.01: 下调签名 alpha=0.01

```json
{
  "paired": true,
  "claimed_direction": "a_lt_b",
  "dir_ok": true,
  "leave_one_out": {
    "applicable": true,
    "pass_fraction": 0.0,
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

### splitdown-a0.05: 下调签名 alpha=0.05

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

### splitdown-a0.1: 下调签名 alpha=0.1

```json
{
  "paired": true,
  "claimed_direction": "a_lt_b",
  "dir_ok": true,
  "leave_one_out": {
    "applicable": true,
    "pass_fraction": 0.5833333333333334,
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
