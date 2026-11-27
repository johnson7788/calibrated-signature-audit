"""closed_loop：DiscoveryRSI 可执行闭环包（本方案新增，独立于原仓库 src）。

目标：把 DiscoveryRSI 的断环接上——
  选中假设 → 编译成可执行分析 → 真实执行 → 验证 → 结果回流 → 下一轮进化。

目标任务（M0–M3）：unc106238-context-response
规格书：closed_loop/specs/unc106238-context-response.md

模块：
  verifier.py      移植自任务包 tests/test.sh 的 10 项结果检查（防过度声称）
  prepare_data.py  原始数据 → prepared counts/design
  analysis_reference.py  M1 参考实现（真实数据跑通，通过 verifier）
  compiler.py      M2 模板化编译：instruction → 分析脚本（LLM 仅补缝隙）
  executor.py      M2 本机子进程执行（超时 + 可选内存限额）
  result_bridge.py （M3）结果回流：outcome/统计 → 候选 evidence + 上下文
  run.py           （M3）包装 DiscoveryLoop 的闭环编排

LLM 客户端：OpenAI 兼容（litellm 中转），密钥从环境变量 DISCOVERY_RSI_API_KEY 读取。
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib.request import Request, urlopen


@dataclass
class LLMClient:
    """最小 OpenAI 兼容客户端（标准库实现，供 compiler/critic/proposer 使用）。"""

    base_url: str = "https://litellm.infox-med.com/v1"
    api_key: str = ""
    model: str = "deepseek-v4-flash"
    timeout: float = 120.0

    def __post_init__(self) -> None:
        if not self.api_key:
            self.api_key = os.environ.get("DISCOVERY_RSI_API_KEY", "")

    def complete(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("DISCOVERY_RSI_API_KEY not set")
        body = json.dumps(
            {"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.2}
        ).encode()
        req = Request(
            self.base_url.rstrip("/") + "/chat/completions",
            data=body,
            headers={"Authorization": "Bearer " + self.api_key, "Content-Type": "application/json"},
        )
        with urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode())
        return data["choices"][0]["message"]["content"]