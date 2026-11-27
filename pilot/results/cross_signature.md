# 交叉签名矩阵

> 签名规模 top-100，|delta|≥1.5；行=签名来源队列，列=验证队列。
> 对角线=自验证（方法检查，必然偏大）；非对角线=跨队列复现。

## 上调签名

| 来源 \ 验证 | GSE50760 | GSE95132 | GSE110224 |
|---|---|---|---|
| GSE50760 | **robust (+1.99)**（自验证） | robust (+1.11) | robust (+1.33) |
| GSE95132 | robust (+1.25) | **robust (+2.11)**（自验证） | robust (+1.08) |
| GSE110224 | robust (+1.34) | robust (+1.18) | **robust (+2.10)**（自验证） |

## 下调签名

| 来源 \ 验证 | GSE50760 | GSE95132 | GSE110224 |
|---|---|---|---|
| GSE50760 | **robust (-2.77)**（自验证） | fragile (-1.34) | robust (-1.77) |
| GSE95132 | robust (-1.21) | **robust (-2.61)**（自验证） | robust (-1.12) |
| GSE110224 | robust (-2.10) | robust (-1.46) | **robust (-2.32)**（自验证） |

## 非对角线复现率（跨队列）

| 签名方向 | 复现 robust / 非对角单元数 |
|---|---|
| 上调 | 6/6 |
| 下调 | 5/6 |


# 复现审计结果

> 判定含义：robust=通过主检验且稳健性检查达标；fragile=主检验通过但稳健性不达标；not_reproduced=主检验未通过；inconclusive=数据不足。

## 方法学元数据（审计前锁定）

| 主张 | 模式 | 检验 | alpha | min_effect | min_stable |
|---|---|---|---|---|---|
| GSE50760-up->GSE50760 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE50760-up->GSE95132 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE50760-up->GSE110224 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE50760-down->GSE50760 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE50760-down->GSE95132 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE50760-down->GSE110224 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE95132-up->GSE50760 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE95132-up->GSE95132 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE95132-up->GSE110224 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE95132-down->GSE50760 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE95132-down->GSE95132 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE95132-down->GSE110224 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE110224-up->GSE50760 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE110224-up->GSE95132 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE110224-up->GSE110224 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE110224-down->GSE50760 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE110224-down->GSE95132 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| GSE110224-down->GSE110224 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |

## 审计结果

| 主张 | 模式 | 特征数 | 效应 | p | 判定 |
|---|---|---|---|---|---|
| GSE50760-up->GSE50760: GSE50760 up -> GSE50760 | signature | 100 | 1.989 | 1.53e-05 | **robust** |
| GSE50760-up->GSE95132: GSE50760 up -> GSE95132 | signature | 100 | 1.109 | 0.000488 | **robust** |
| GSE50760-up->GSE110224: GSE50760 up -> GSE110224 | signature | 80 | 1.331 | 0.00209 | **robust** |
| GSE50760-down->GSE50760: GSE50760 down -> GSE50760 | signature | 100 | -2.770 | 5.34e-05 | **robust** |
| GSE50760-down->GSE95132: GSE50760 down -> GSE95132 | signature | 98 | -1.341 | 0.0425 | **fragile** |
| GSE50760-down->GSE110224: GSE50760 down -> GSE110224 | signature | 92 | -1.766 | 0.00316 | **robust** |
| GSE95132-up->GSE50760: GSE95132 up -> GSE50760 | signature | 100 | 1.246 | 7.63e-05 | **robust** |
| GSE95132-up->GSE95132: GSE95132 up -> GSE95132 | signature | 100 | 2.113 | 0.000488 | **robust** |
| GSE95132-up->GSE110224: GSE95132 up -> GSE110224 | signature | 97 | 1.082 | 0.00557 | **robust** |
| GSE95132-down->GSE50760: GSE95132 down -> GSE50760 | signature | 100 | -1.206 | 0.000252 | **robust** |
| GSE95132-down->GSE95132: GSE95132 down -> GSE95132 | signature | 100 | -2.612 | 0.000977 | **robust** |
| GSE95132-down->GSE110224: GSE95132 down -> GSE110224 | signature | 96 | -1.116 | 0.0174 | **robust** |
| GSE110224-up->GSE50760: GSE110224 up -> GSE50760 | signature | 76 | 1.339 | 7.63e-06 | **robust** |
| GSE110224-up->GSE95132: GSE110224 up -> GSE95132 | signature | 76 | 1.176 | 0.000488 | **robust** |
| GSE110224-up->GSE110224: GSE110224 up -> GSE110224 | signature | 79 | 2.102 | 0.00134 | **robust** |
| GSE110224-down->GSE50760: GSE110224 down -> GSE50760 | signature | 95 | -2.102 | 5.34e-05 | **robust** |
| GSE110224-down->GSE95132: GSE110224 down -> GSE95132 | signature | 97 | -1.458 | 0.00342 | **robust** |
| GSE110224-down->GSE110224: GSE110224 down -> GSE110224 | signature | 100 | -2.317 | 0.00168 | **robust** |

## 明细

### GSE50760-up->GSE50760: GSE50760 up -> GSE50760

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

### GSE50760-up->GSE95132: GSE50760 up -> GSE95132

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

### GSE50760-up->GSE110224: GSE50760 up -> GSE110224

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
    "n_runs": 17
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```

### GSE50760-down->GSE50760: GSE50760 down -> GSE50760

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

### GSE50760-down->GSE95132: GSE50760 down -> GSE95132

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
    "pass_fraction": 0.4166666666666667,
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

### GSE50760-down->GSE110224: GSE50760 down -> GSE110224

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
    "n_runs": 17
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```

### GSE95132-up->GSE50760: GSE95132 up -> GSE50760

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

### GSE95132-up->GSE95132: GSE95132 up -> GSE95132

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

### GSE95132-up->GSE110224: GSE95132 up -> GSE110224

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
    "n_runs": 17
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```

### GSE95132-down->GSE50760: GSE95132 down -> GSE50760

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

### GSE95132-down->GSE95132: GSE95132 down -> GSE95132

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

### GSE95132-down->GSE110224: GSE95132 down -> GSE110224

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
    "n_runs": 17
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```

### GSE110224-up->GSE50760: GSE110224 up -> GSE50760

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

### GSE110224-up->GSE95132: GSE110224 up -> GSE95132

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

### GSE110224-up->GSE110224: GSE110224 up -> GSE110224

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
    "n_runs": 17
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```

### GSE110224-down->GSE50760: GSE110224 down -> GSE50760

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

### GSE110224-down->GSE95132: GSE110224 down -> GSE95132

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

### GSE110224-down->GSE110224: GSE110224 down -> GSE110224

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
    "n_runs": 17
  },
  "covariate_adjustment": {
    "applicable": false,
    "coefficient": null,
    "p_value": null
  },
  "min_stable_fraction": 0.8
}
```
