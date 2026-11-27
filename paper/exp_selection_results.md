# 实验：签名选择标准 × 跨队列可迁移性

来源队列 GSE50760；签名规模 top-100；四标准对比；三个队列验证。

| 标准 | 方向 | 目标队列 | 判定 | 效应 | p | LOO | 效应保留率 |
|---|---|---|---|---|---|---|---|
| effect | up | GSE50760 | robust | +1.880 | 2.29e-05 | 1.00 | 1.00 |
| effect | up | GSE95132 | robust | +1.219 | 0.000488 | 1.00 | 0.65 |
| effect | up | GSE110224 | robust | +1.266 | 0.00209 | 1.00 | 0.67 |
| effect | down | GSE50760 | robust | -2.702 | 5.34e-05 | 1.00 | 1.00 |
| effect | down | GSE95132 | fragile | -1.376 | 0.0425 | 0.42 | 0.51 |
| effect | down | GSE110224 | robust | -1.714 | 0.00316 | 1.00 | 0.63 |
| tstat | up | GSE50760 | robust | +0.931 | 7.63e-06 | 1.00 | 1.00 |
| tstat | up | GSE95132 | robust | +0.849 | 0.00146 | 1.00 | 0.91 |
| tstat | up | GSE110224 | robust | +0.637 | 0.00258 | 1.00 | 0.68 |
| tstat | down | GSE50760 | robust | -1.167 | 7.63e-06 | 1.00 | 1.00 |
| tstat | down | GSE95132 | robust | -1.128 | 0.00146 | 1.00 | 0.97 |
| tstat | down | GSE110224 | robust | -0.746 | 0.00316 | 1.00 | 0.64 |
| stability | up | GSE50760 | robust | +1.848 | 7.63e-06 | 1.00 | 1.00 |
| stability | up | GSE95132 | robust | +1.144 | 0.000488 | 1.00 | 0.62 |
| stability | up | GSE110224 | robust | +1.276 | 0.00209 | 1.00 | 0.69 |
| stability | down | GSE50760 | robust | -2.687 | 5.34e-05 | 1.00 | 1.00 |
| stability | down | GSE95132 | fragile | -1.433 | 0.0269 | 0.50 | 0.53 |
| stability | down | GSE110224 | robust | -1.717 | 0.00316 | 1.00 | 0.64 |
| consistency | up | GSE50760 | robust | +1.102 | 7.63e-06 | 1.00 | 1.00 |
| consistency | up | GSE95132 | robust | +0.885 | 0.000488 | 1.00 | 0.80 |
| consistency | up | GSE110224 | robust | +0.923 | 0.00134 | 1.00 | 0.84 |
| consistency | down | GSE50760 | robust | -1.416 | 7.63e-06 | 1.00 | 1.00 |
| consistency | down | GSE95132 | robust | -1.163 | 0.00146 | 1.00 | 0.82 |
| consistency | down | GSE110224 | robust | -0.929 | 0.00258 | 1.00 | 0.66 |

## 汇总（非来源队列平均效应保留率）

| 标准 | 上调 | 下调 |
|---|---|---|
| effect | 0.66 | 0.57 |
| tstat | 0.80 | 0.80 |
| stability | 0.66 | 0.58 |
| consistency | 0.82 | 0.74 |