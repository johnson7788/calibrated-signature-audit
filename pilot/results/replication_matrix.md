# 多队列复现矩阵

> 单元格式：判定（效应）。robust=通过主检验+留一稳健性；fragile=主检验过但稳健性不足；not_reproduced=主检验失败；inconclusive=数据不足。

## 上调签名

| 签名规模 | GSE50760 | GSE95132 | GSE110224 |
|---|---|---|---|
| top-50 | robust (+1.74) | robust (+1.18) | robust (+1.67) |
| top-100 | robust (+1.43) | robust (+0.92) | robust (+1.33) |
| top-200 | robust (+1.19) | robust (+0.68) | robust (+1.01) |

## 下调签名

| 签名规模 | GSE50760 | GSE95132 | GSE110224 |
|---|---|---|---|
| top-50 | robust (-1.71) | robust (-1.30) | robust (-1.21) |
| top-100 | robust (-1.48) | robust (-1.22) | robust (-1.01) |
| top-200 | robust (-1.36) | robust (-1.15) | robust (-0.97) |

## 复现率汇总

| 签名 | top-50 | top-100 | top-200 |
|---|---|---|---|
| 上调 | 3/3 | 3/3 | 3/3 |
| 下调 | 3/3 | 3/3 | 3/3 |

# 复现审计结果

> 判定含义：robust=通过主检验且稳健性检查达标；fragile=主检验通过但稳健性不达标；not_reproduced=主检验未通过；inconclusive=数据不足。

## 方法学元数据（审计前锁定）

| 主张 | 模式 | 检验 | alpha | min_effect | min_stable |
|---|---|---|---|---|---|
| up50-GSE50760 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| up50-GSE95132 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| up50-GSE110224 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| down50-GSE50760 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| down50-GSE95132 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| down50-GSE110224 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| up100-GSE50760 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| up100-GSE95132 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| up100-GSE110224 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| down100-GSE50760 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| down100-GSE95132 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| down100-GSE110224 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| up200-GSE50760 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| up200-GSE95132 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| up200-GSE110224 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| down200-GSE50760 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| down200-GSE95132 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |
| down200-GSE110224 | signature | wilcoxon_signed_rank | 0.05 | 0.5 | 0.8 |

## 审计结果

| 主张 | 模式 | 特征数 | 效应 | p | 判定 |
|---|---|---|---|---|---|
| up50-GSE50760: up top50 -> GSE50760 | signature | 43 | 1.739 | 1.53e-05 | **robust** |
| up50-GSE95132: up top50 -> GSE95132 | signature | 43 | 1.181 | 0.000488 | **robust** |
| up50-GSE110224: up top50 -> GSE110224 | signature | 45 | 1.674 | 0.00258 | **robust** |
| down50-GSE50760: down top50 -> GSE50760 | signature | 42 | -1.708 | 1.53e-05 | **robust** |
| down50-GSE95132: down top50 -> GSE95132 | signature | 42 | -1.300 | 0.00928 | **robust** |
| down50-GSE110224: down top50 -> GSE110224 | signature | 37 | -1.210 | 0.00107 | **robust** |
| up100-GSE50760: up top100 -> GSE50760 | signature | 80 | 1.429 | 1.53e-05 | **robust** |
| up100-GSE95132: up top100 -> GSE95132 | signature | 81 | 0.924 | 0.000488 | **robust** |
| up100-GSE110224: up top100 -> GSE110224 | signature | 83 | 1.334 | 0.00258 | **robust** |
| down100-GSE50760: down top100 -> GSE50760 | signature | 85 | -1.480 | 1.53e-05 | **robust** |
| down100-GSE95132: down top100 -> GSE95132 | signature | 86 | -1.218 | 0.00342 | **robust** |
| down100-GSE110224: down top100 -> GSE110224 | signature | 80 | -1.013 | 0.00134 | **robust** |
| up200-GSE50760: up top200 -> GSE50760 | signature | 157 | 1.190 | 1.53e-05 | **robust** |
| up200-GSE95132: up top200 -> GSE95132 | signature | 158 | 0.682 | 0.00342 | **robust** |
| up200-GSE110224: up top200 -> GSE110224 | signature | 162 | 1.006 | 0.00209 | **robust** |
| down200-GSE50760: down top200 -> GSE50760 | signature | 154 | -1.357 | 3.81e-05 | **robust** |
| down200-GSE95132: down top200 -> GSE95132 | signature | 157 | -1.155 | 0.00244 | **robust** |
| down200-GSE110224: down top200 -> GSE110224 | signature | 152 | -0.974 | 0.00209 | **robust** |

## 明细

### up50-GSE50760: up top50 -> GSE50760

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

### up50-GSE95132: up top50 -> GSE95132

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

### up50-GSE110224: up top50 -> GSE110224

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

### down50-GSE50760: down top50 -> GSE50760

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

### down50-GSE95132: down top50 -> GSE95132

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

### down50-GSE110224: down top50 -> GSE110224

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

### up100-GSE50760: up top100 -> GSE50760

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

### up100-GSE95132: up top100 -> GSE95132

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

### up100-GSE110224: up top100 -> GSE110224

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

### down100-GSE50760: down top100 -> GSE50760

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

### down100-GSE95132: down top100 -> GSE95132

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

### down100-GSE110224: down top100 -> GSE110224

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

### up200-GSE50760: up top200 -> GSE50760

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

### up200-GSE95132: up top200 -> GSE95132

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

### up200-GSE110224: up top200 -> GSE110224

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

### down200-GSE50760: down top200 -> GSE50760

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

### down200-GSE95132: down top200 -> GSE95132

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

### down200-GSE110224: down top200 -> GSE110224

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
