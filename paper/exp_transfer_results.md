# 留一队列：transfer-optimized vs effect-ranked

| 留出队列 | 规模 | 方向 | 标准 | 判定 | 效应 | p | LOO |
|---|---|---|---|---|---|---|---|
| GSE50760 | 50 | up | transfer | not_reproduced | -1.016 | 0.000671 | 0.00 |
| GSE50760 | 50 | up | effect | robust | +1.511 | 7.63e-05 | 1.00 |
| GSE50760 | 50 | down | transfer | inconclusive | +nan | nan | 0.00 |
| GSE50760 | 50 | down | effect | robust | -1.505 | 0.000145 | 1.00 |
| GSE50760 | 100 | up | transfer | not_reproduced | -0.858 | 0.00042 | 0.00 |
| GSE50760 | 100 | up | effect | robust | +1.228 | 0.000107 | 1.00 |
| GSE50760 | 100 | down | transfer | inconclusive | +nan | nan | 0.00 |
| GSE50760 | 100 | down | effect | robust | -1.179 | 0.000252 | 1.00 |
| GSE50760 | 200 | up | transfer | not_reproduced | -0.644 | 3.81e-05 | 0.00 |
| GSE50760 | 200 | up | effect | robust | +1.051 | 7.63e-05 | 1.00 |
| GSE50760 | 200 | down | transfer | inconclusive | +nan | nan | 0.00 |
| GSE50760 | 200 | down | effect | robust | -0.921 | 0.00105 | 1.00 |
| GSE95132 | 50 | up | transfer | not_reproduced | -0.804 | 0.0771 | 0.00 |
| GSE95132 | 50 | up | effect | robust | +1.344 | 0.000488 | 1.00 |
| GSE95132 | 50 | down | transfer | inconclusive | +nan | nan | 0.00 |
| GSE95132 | 50 | down | effect | fragile | -1.541 | 0.0342 | 0.42 |
| GSE95132 | 100 | up | transfer | not_reproduced | -0.631 | 0.0923 | 0.00 |
| GSE95132 | 100 | up | effect | robust | +1.219 | 0.000488 | 1.00 |
| GSE95132 | 100 | down | transfer | inconclusive | +nan | nan | 0.00 |
| GSE95132 | 100 | down | effect | fragile | -1.376 | 0.0425 | 0.42 |
| GSE95132 | 200 | up | transfer | not_reproduced | -0.469 | 0.176 | 0.00 |
| GSE95132 | 200 | up | effect | robust | +1.078 | 0.000488 | 1.00 |
| GSE95132 | 200 | down | transfer | inconclusive | +nan | nan | 0.00 |
| GSE95132 | 200 | down | effect | fragile | -1.152 | 0.0342 | 0.42 |
| GSE110224 | 50 | up | transfer | not_reproduced | -0.796 | 0.0079 | 0.00 |
| GSE110224 | 50 | up | effect | robust | +1.499 | 0.00258 | 1.00 |
| GSE110224 | 50 | down | transfer | inconclusive | +nan | nan | 0.00 |
| GSE110224 | 50 | down | effect | robust | -2.068 | 0.00385 | 1.00 |
| GSE110224 | 100 | up | transfer | not_reproduced | -0.791 | 0.0079 | 0.00 |
| GSE110224 | 100 | up | effect | robust | +1.266 | 0.00209 | 1.00 |
| GSE110224 | 100 | down | transfer | inconclusive | +nan | nan | 0.00 |
| GSE110224 | 100 | down | effect | robust | -1.714 | 0.00316 | 1.00 |
| GSE110224 | 200 | up | transfer | not_reproduced | -0.541 | 0.00665 | 0.00 |
| GSE110224 | 200 | up | effect | robust | +1.077 | 0.00258 | 1.00 |
| GSE110224 | 200 | down | transfer | inconclusive | +nan | nan | 0.00 |
| GSE110224 | 200 | down | effect | robust | -1.369 | 0.00258 | 1.00 |

## 汇总（判定 robust 比例 / 平均 |效应|）

| 标准 | robust 比例 | 平均 |效应| |
|---|---|---|
| transfer | 0.00 | 0.728 |
| effect | 0.83 | 1.339 |