---
pretty_name: DiscoveryRSI Hypothesis Task Examples
license: apache-2.0
language:
  - en
task_categories:
  - other
size_categories:
  - n<1K
tags:
  - discoveryrsi
  - scientific-research
  - hypothesis-generation
  - compiled-tasks
  - harbor
  - biology
configs:
  - config_name: default
    data_files:
      - split: examples
        path: examples.jsonl
---

# DiscoveryRSI Hypothesis Task Examples

[![DiscoveryRSI on arXiv](https://img.shields.io/badge/arXiv-2610.23839-B31B1B?logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.23839)

Three real hypothesis tasks compiled during a [DiscoveryRSI](https://github.com/Gen-Verse/DiscoveryRSI) research campaign. Each example connects a frozen scientific proposal to computational instructions, required inputs, a verifier, and synthetic verification fixtures.

These examples show the compiler output used by the research harness. They are an illustrative subset, with two research domains and two public gene-expression studies; they are not a representative evaluation set or the complete DFM-Bench release.

## Examples

[Download the complete task packages](https://huggingface.co/datasets/Gen-Verse/DiscoveryRSI-Hypothesis-Task-Examples/resolve/main/task-packages.zip). The ZIP preserves the task-folder structure, source records, documentation, and reproducible checks.

| Example | Domain | Required public study |
| --- | --- | --- |
| Context-dependent transcript response to UNC106238 | Therapeutic targets | [E-MTAB-8316](https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-8316) |
| Macrophage–fibroblast signaling directionality | Disease mechanisms | [E-MTAB-8873](https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-8873) |
| Pathway-specific directional signaling | Disease mechanisms | [E-MTAB-8873](https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-8873) |

Each task folder inside the ZIP contains:

- `hypothesis.md`: the scientific proposal, including competing explanations and falsification criteria.
- `instruction.md` and `task.toml`: the compiled computational assignment and task metadata.
- `input-requirements.json` and `bindings.json`: expected prepared files, content hashes, and container mount targets.
- `tests/test.sh`, `validation.json`, and `validation/`: the verifier, output contract, and synthetic positive and negative fixtures.
- `key-references.json` and `provenance.json`: the campaign's claim-to-reference mappings, source artifact hashes, export changes, and validation scope.

## Load the examples

```python
from datasets import load_dataset

examples = load_dataset(
    "Gen-Verse/DiscoveryRSI-Hypothesis-Task-Examples",
    split="examples",
)
print(examples[0]["title"])
print(examples[0]["hypothesis"])
print(examples[0]["instruction"])
```

The JSONL table also includes the verifier text, task metadata, input requirements, reference manifest, provenance, and the path to the complete task folder inside the ZIP. JSON manifest columns are serialized strings so that the three records share a consistent table schema.

Download the dataset and extract the task folders with:

```python
from huggingface_hub import snapshot_download
from pathlib import Path
import zipfile

snapshot_download(
    repo_id="Gen-Verse/DiscoveryRSI-Hypothesis-Task-Examples",
    repo_type="dataset",
    local_dir="task-examples",
)
with zipfile.ZipFile("task-examples/task-packages.zip") as archive:
    archive.extractall("task-examples")
```

From the extracted `DiscoveryRSI-Hypothesis-Task-Examples` folder, run `python scripts/check_fixtures.py` to reproduce the synthetic fixture checks. The checker redirects the task's output paths into temporary directories and does not need the study data.

## Inputs and execution

The release contains task definitions and synthetic QA fixtures. Expression matrices, sample-level study records, full-text source snapshots, raw model traces, and private research datasets are not bundled.

For a scientific run, acquire the studies from their original repositories under their applicable terms. The compiled tasks expect **prepared** counts matrices and sample-design JSON files, not the raw study downloads. The exact expected filenames, hashes, and mount targets are recorded for each task. The original preparation pipeline and prepared inputs are not included, so downloading the study alone does not reproduce the original input snapshot.

The campaign used its project-specific `task.toml` schema version 1.4. Integration into another Harbor installation may require a format adapter. A public Python Dockerfile is provided as an example environment in place of the campaign's private image; that image has not been built or verified as part of this release.

## Provenance and validation

The tasks were compiled in the `raft-final-v2-20261016` release, trial `raft-final-v2-300-20261016`. Candidate IDs, parent IDs, original file hashes, and per-file export changes are retained in each task's provenance record. Private host paths were replaced with portable input references, and the private runtime image was replaced with a public Python example environment. Scientific wording and verifier logic are preserved.

All three source packages passed the campaign's task-readiness checks. For this export, all **11 declared synthetic fixture checks** passed: three positive fixtures were accepted and eight negative fixtures were rejected. Results are in [fixture-checks.json](https://huggingface.co/datasets/Gen-Verse/DiscoveryRSI-Hypothesis-Task-Examples/blob/main/fixture-checks.json).

These checks test the declared output contracts and selected rejection cases. They do not establish verifier completeness, validate the biological claims or reference interpretations, or demonstrate a successful scientific solution. The source campaign records the reference-solution status as `not_run` and the scientific result as `not_established`.

## Citation

If you use these task examples in your research, please cite our paper:

[**DiscoveryRSI: Recursively Learning to Discover Valuable Hypotheses**](https://arxiv.org/abs/2610.23839)

```bibtex
@article{zhong2026discoveryrsi,
  title={DiscoveryRSI: Recursively Learning to Discover Valuable Hypotheses},
  author={Zhong, Jianyuan and Wu, Chenwei and Yu, Zhaochen and Jiang, Xixian and Li, Xuewei and Xiao, Hao and Dai, Xilin and Wang, Junyang and Zou, Jiaru and Cui, Zhiqing and Zheng, Boyuan and Xiong, Jing and Zhang, Zhen and Gao, Qiang and Morley, Michael and Nakayama, Luis and Xu, Qiang and Shen, Liyue and Gui, Tao and Celi, Leo Anthony and Zou, James and Yin, Zhenfei and Wu, Yingcheng and Yang, Ling},
  journal={arXiv preprint arXiv:2610.23839},
  year={2026}
}
```

## License

The original task text, generated code, and release tooling are provided under [Apache-2.0](LICENSE), consistent with the DiscoveryRSI code repository. Referenced publications and external study data retain their own licenses and access terms.

Related resources: [DiscoveryRSI paper](https://arxiv.org/abs/2610.23839), [DiscoveryRSI code](https://github.com/Gen-Verse/DiscoveryRSI), [DiscoveryRSI-27B](https://huggingface.co/Gen-Verse/DiscoveryRSI-27B), and the [DiscoveryRSI collection](https://huggingface.co/collections/Gen-Verse/discoveryrsi).
