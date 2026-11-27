---
language:
  - en
library_name: transformers
base_model: Qwen/Qwen3.8-27B
base_model_relation: finetune
license: apache-2.0
pipeline_tag: text-generation
tags:
  - discoveryrsi
  - scientific-research
  - research-agent
  - instruction-tuning
  - biomedical-research
  - hypothesis-generation
---

<div align="center">

<h1>DiscoveryRSI-27B</h1>

<p align="center">
  <a href="https://arxiv.org/abs/2610.23839">
    <img src="https://img.shields.io/badge/arXiv-2610.23839-B31B1B?logo=arxiv&logoColor=white" alt="DiscoveryRSI on arXiv"/>
  </a>
  <a href="https://github.com/Gen-Verse/DiscoveryRSI">
    <img src="https://img.shields.io/badge/DiscoveryRSI-GitHub-black?logo=github&logoColor=white" alt="DiscoveryRSI on GitHub"/>
  </a>
  <a href="https://huggingface.co/Gen-Verse/DiscoveryRSI-27B">
    <img src="https://img.shields.io/badge/DiscoveryRSI--27B-Hugging%20Face-FFCC00?logo=huggingface&logoColor=black" alt="DiscoveryRSI-27B on Hugging Face"/>
  </a>
  <a href="https://huggingface.co/collections/Gen-Verse/discoveryrsi">
    <img src="https://img.shields.io/badge/DiscoveryRSI-Collection-FFD21E?logo=huggingface&logoColor=black" alt="DiscoveryRSI collection"/>
  </a>
  <a href="https://foundry-arena.rsi-arena.workers.dev/arena">
    <img src="https://img.shields.io/badge/Live%20Stream-Watch%20DiscoveryRSI-4C1D95" alt="DiscoveryRSI live stream"/>
  </a>
</p>

</div>

## 🎯 About This Repository

This repository contains the **DiscoveryRSI-27B** model release for
[DiscoveryRSI](https://github.com/Gen-Verse/DiscoveryRSI), a research system
that recursively develops, evaluates, revises, and attributes scientific
hypotheses.

DiscoveryRSI-27B is an instruction-finetuned 27B language model intended for
research ideation and evidence-grounded planning. It helps turn a research
question and available evidence into an explicit hypothesis, investigation
plan, alternatives, decision criteria, and falsification conditions.

## 🌟 Introduction

DiscoveryRSI treats a hypothesis as a versioned research object rather than a
finished answer. The model is designed to support a loop of:

- 🔎 **Explore**: identify valuable questions and candidate explanations
- 🧪 **Evaluate**: propose tests, comparators, evidence, and decision criteria
- 🛠️ **Revise**: repair weak designs and incorporate criticism
- 🧬 **Attribute**: record which research behaviors improved a hypothesis
- 🔁 **Learn**: use replay and attribution to improve future research paths

The model works with the public DiscoveryRSI harness, role prompts, tool
registry, replay store, and domain adapters. The public system supports
life-science research workflows including GEO-derived pathway analysis and
therapeutic-target prioritization.

## 📦 Resources

| **Type** | **Name** | **Link** |
| --- | --- | --- |
| 📄 Paper | **DiscoveryRSI** | [arXiv:2610.23839](https://arxiv.org/abs/2610.23839) |
| 🤖 Model | **DiscoveryRSI-27B** | [🤗 Hugging Face](https://huggingface.co/Gen-Verse/DiscoveryRSI-27B) |
| 🧰 Code | **DiscoveryRSI harness** | [GitHub](https://github.com/Gen-Verse/DiscoveryRSI) |
| 📚 Collection | **DiscoveryRSI models** | [🤗 Hugging Face](https://huggingface.co/collections/Gen-Verse/discoveryrsi) |
| 📺 Demo | **DiscoveryRSI live stream** | [Open arena](https://foundry-arena.rsi-arena.workers.dev/arena) |

## 📋 Model Details

| **Property** | **Value** |
| --- | --- |
| Model name | DiscoveryRSI-27B |
| Model type | Instruction-finetuned causal language model |
| Parameter scale | 27B |
| Base model | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) |
| Weight precision | BF16 |
| Released checkpoint | Round 2, step 150 |
| Primary language | English |
| Primary use | Scientific hypothesis development and research planning |
| Library | Transformers |

This release contains the completed round-2 checkpoint, trained for 150 steps,
with BF16 weights, model configuration, tokenizer, chat template, and processor
files. See [release_manifest.json](release_manifest.json) for per-file sizes and
SHA-256 checksums. The visual and MTP components are preserved from the base
model; the DiscoveryRSI training and evaluation described here concern textual
scientific-research workflows. Private campaign traces, credentials, patient
rows, restricted datasets, and laboratory infrastructure are not included.

## 🚀 Intended Use

DiscoveryRSI-27B is intended for:

- research ideation and hypothesis generation;
- critique and revision of proposed experiments;
- evidence-grounded research planning;
- explicit alternatives, comparators, and falsification criteria; and
- use through the DiscoveryRSI agentic harness.

The model is not a medical device. Do not use it to make clinical, diagnostic,
treatment, or other high-stakes decisions. Generated hypotheses require expert
review and independent verification.

## 💻 Usage

The weights can be loaded directly from this repository. Use a recent
Transformers release supporting the exported `Qwen3_5ForConditionalGeneration`
architecture. Install the loading dependencies with:

```bash
pip install -U torch transformers accelerate jinja2
```

```python
from transformers import AutoTokenizer, Qwen3_5ForConditionalGeneration

model_id = "Gen-Verse/DiscoveryRSI-27B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = Qwen3_5ForConditionalGeneration.from_pretrained(
    model_id, device_map="auto", dtype="auto"
)

messages = [{
    "role": "user",
    "content": "Develop a testable research hypothesis about a disease pathway.",
}]
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    enable_thinking=False,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)
outputs = model.generate(**inputs, max_new_tokens=512)
print(tokenizer.decode(
    outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True
))
```

For multi-step research workflows, follow the [DiscoveryRSI quick
start](https://github.com/Gen-Verse/DiscoveryRSI#quick-start) and configure a
provider adapter for the checkpoint.

## 🧪 Training and Evaluation

DiscoveryRSI uses hypothesis development, criticism, revision, contribution
attribution, harness replay, and DFM-Bench-style process evaluation. Release
documentation should report the base-model identity, training-data provenance,
instruction format, evaluation configuration, and known limitations. Results
should be interpreted as research-process evidence rather than proof that a
generated hypothesis is correct or clinically useful.

## ⚠️ Limitations and Responsible Use

The model can produce plausible but unsupported claims, omit relevant evidence,
misread sources, or propose infeasible experiments. It may reflect biases and
errors in its base model and instruction-tuning data. Users should preserve
source provenance, check citations, inspect alternatives and falsification
criteria, and have a qualified researcher review outputs before acting on them.

## 📝 Citation

If you use DiscoveryRSI-27B or the accompanying harness in your research,
please cite our paper:

[**DiscoveryRSI: Recursively Learning to Discover Valuable Hypotheses**](https://arxiv.org/abs/2610.23839)

```bibtex
@article{zhong2026discoveryrsi,
  title={DiscoveryRSI: Recursively Learning to Discover Valuable Hypotheses},
  author={Zhong, Jianyuan and Wu, Chenwei and Yu, Zhaochen and Jiang, Xixian and Li, Xuewei and Xiao, Hao and Dai, Xilin and Wang, Junyang and Zou, Jiaru and Cui, Zhiqing and Zheng, Boyuan and Xiong, Jing and Zhang, Zhen and Gao, Qiang and Morley, Michael and Nakayama, Luis and Xu, Qiang and Shen, Liyue and Gui, Tao and Celi, Leo Anthony and Zou, James and Yin, Zhenfei and Wu, Yingcheng and Yang, Ling},
  journal={arXiv preprint arXiv:2610.23839},
  year={2026}
}
```

See the [repository citation section](https://github.com/Gen-Verse/DiscoveryRSI#-citation)
for the maintained technical-report and model links.

## 📄 License

The released model files are provided under the included
[Apache-2.0 license](LICENSE), inherited from the Qwen3.8-27B base-model release.
Referenced publications and external research datasets retain their own
licenses and access terms.
