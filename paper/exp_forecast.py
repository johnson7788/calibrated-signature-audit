"""exp_forecast.py — 能否用源队列统计量预测跨队列复现？

对每个 (来源队列, 规模, 标准, 方向) 构造签名：
  源特征：源效应、源 p、源 LOO 稳定率、源配对对数、规模、标准
  目标：在另一个队列的判定（robust=1）
用 leave-one-source-out 逻辑回归评估 AUC。
"""
from __future__ import annotations
import itertools
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import roc_auc_score
from pilot.audit import load_matrix, load_metadata, to_log2x

ROOT = Path(__file__).resolve().parents[1]
C = {
 "GSE50760": dict(matrix="pilot/data/gse50760/GSE50760_log2fpkm.tsv.gz", meta="pilot/data/gse50760/design.json", value_type="log", col="condition", a="primary", b="normal", pair="patient"),
 "GSE95132": dict(matrix="pilot/data/gse95132/GSE95132_counts.tsv.gz", meta="pilot/data/gse95132/design.json", value_type="counts", col="tissue", a="tumor", b="adjacent", pair="patient"),
 "GSE110224": dict(matrix="pilot/data/gse110224/matrix.tsv.gz", meta="pilot/data/gse110224/design.json", value_type="log", col="condition", a="cancer", b="normal", pair="patient"),
}
ALPHA, MIN_STABLE = 0.05, 0.8

def load(cfg):
    expr = to_log2x(load_matrix(Path(cfg["matrix"])), cfg["value_type"])
    meta = load_metadata(Path(cfg["meta"])); meta["sample_id"]=meta["sample_id"].astype(str)
    ds=[]; pairs=[]
    for key,grp in meta.groupby(cfg["pair"]):
        a=grp[grp[cfg["col"]]==cfg["a"]]["sample_id"]; b=grp[grp[cfg["col"]]==cfg["b"]]["sample_id"]
        if len(a)==1 and len(b)==1:
            ds.append(expr[a.iloc[0]]-expr[b.iloc[0]]); pairs.append(str(key))
    return expr, pd.DataFrame(ds), pairs

def sig_stats(deltas):
    m=deltas.mean(axis=0); sd=deltas.std(axis=0,ddof=1).replace(0,np.nan)
    return pd.DataFrame({"mean":m,"t":m/sd,"cons":(np.sign(deltas)==np.sign(m)).sum(axis=0)/len(deltas)})

def select(st, common, crit, direction, n):
    sign=1 if direction=="up" else -1
    s=st.loc[common]
    if crit=="effect": key=s["mean"]*sign
    elif crit=="tstat": key=s["t"]*sign
    elif crit=="consistency": key=s["cons"]*1000+s["mean"]*sign
    key=key[key>0]
    return key.sort_values(ascending=False).head(n).index.tolist()

def audit(expr, deltas, genes, direction):
    present=[g for g in genes if g in expr.index]
    if len(present)<5: return dict(effect=np.nan,p=np.nan,loo=0.0,robust=0)
    v=deltas[present].mean(axis=1).values
    eff=float(v.mean())
    try: p=float(stats.wilcoxon(v).pvalue)
    except ValueError: p=np.nan
    loo=0
    for i in range(len(v)):
        sub=np.delete(v,i)
        try: pi=float(stats.wilcoxon(sub).pvalue)
        except ValueError: pi=np.nan
        if np.isfinite(pi) and pi<ALPHA and ((sub.mean()>0)==(direction=="up")): loo+=1
    loo/=max(len(v),1)
    ok=np.isfinite(p) and p<ALPHA and ((eff>0)==(direction=="up"))
    return dict(effect=eff,p=p,loo=loo,robust=int(ok and loo>=MIN_STABLE))

def main():
    data={k:load(cfg) for k,cfg in C.items()}
    common=set(data["GSE50760"][0].index)
    for k in data: common&=set(data[k][0].index)
    common=sorted(common)
    rows=[]
    for S in C:
        st=sig_stats(data[S][1])
        for size,crit,direction in itertools.product([50,100,200],["effect","tstat","consistency"],["up","down"]):
            genes=select(st,common,crit,direction,size)
            src=audit(data[S][0],data[S][1],genes,direction)
            for T in C:
                if T==S: continue
                tr=audit(data[T][0],data[T][1],genes,direction)
                rows.append(dict(source=S,target=T,size=size,criterion=crit,direction=direction,
                    src_effect=src["effect"],src_p=src["p"],src_loo=src["loo"],
                    tgt_effect=tr["effect"],tgt_p=tr["p"],tgt_loo=tr["loo"],tgt_robust=tr["robust"]))
    df=pd.DataFrame(rows)
    df.to_csv(ROOT/"paper"/"forecast_data.csv", index=False)
    print("claims:", len(df), "| robust rate:", df.tgt_robust.mean().round(3))
    feats=["src_effect","src_loo","size","src_n"]
    df["src_n"]=df["source"].map({"GSE50760":18,"GSE95132":12,"GSE110224":17})
    X=df[["src_effect","src_loo","size","src_n"]].fillna(0).values
    y=df["tgt_robust"].values
    groups=df["source"].values
    logo=LeaveOneGroupOut()
    if len(set(y))>1:
        clf=LogisticRegression(max_iter=1000)
        pred=np.zeros(len(y))
        for tr,te in logo.split(X,y,groups):
            clf.fit(X[tr],y[tr]); pred[te]=clf.predict_proba(X[te])[:,1]
        auc=roc_auc_score(y,pred)
        print(f"AUC (leave-one-source-out): {auc:.3f}")
        # 单变量 AUC
        for f in ["src_effect","src_loo","size"]:
            v=df[f].fillna(0).values
            try: print(f"  AUC({f}) = {roc_auc_score(y,v):.3f}")
            except Exception: pass
    else:
        print("y 只有一个类别，无法算 AUC")

if __name__=="__main__":
    main()
