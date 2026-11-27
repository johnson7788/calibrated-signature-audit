"""executor.py — 本机子进程执行分析脚本（Q4：venv 子进程 + 超时 + 资源限额）。

- 用运行本模块的同一 Python 解释器执行目标脚本（venv 内已装 pinned 依赖）；
- 超时保护：subprocess timeout；
- 可选内存限额：子进程内 setrlimit(RLIMIT_AS) 包装（macOS 对 RLIMIT_AS 支持有限，
  设置失败时降级为无限制）；
- 返回 {returncode, stdout(截断), stderr(截断)}。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _mem_wrapper(script: Path, max_mem_mb: int) -> str:
    return (
        "import resource, sys, runpy\n"
        "try:\n"
        f"    resource.setrlimit(resource.RLIMIT_AS, ({max_mem_mb}*1024*1024, {max_mem_mb}*1024*1024))\n"
        "except (OSError, ValueError):\n"
        "    pass\n"
        f"runpy.run_path({str(script)!r}, run_name='__main__')\n"
    )


def run_script(script: str | Path, timeout: float = 120.0, max_mem_mb: int | None = None,
               env_extra: dict | None = None) -> dict:
    script = Path(script)
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)

    if max_mem_mb:
        cmd = [sys.executable, "-c", _mem_wrapper(script, max_mem_mb)]
    else:
        cmd = [sys.executable, str(script)]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
        return {
            "returncode": proc.returncode,
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-4000:],
        }
    except subprocess.TimeoutExpired:
        return {"returncode": -1, "stdout": "", "stderr": f"timeout after {timeout}s (pid killed)"}
    except OSError as exc:
        return {"returncode": -2, "stdout": "", "stderr": f"OSError: {exc}"}


def main() -> None:
    ap = argparse.ArgumentParser(description="closed_loop executor")
    ap.add_argument("--script", required=True)
    ap.add_argument("--timeout", type=float, default=120.0)
    ap.add_argument("--max-mem-mb", type=int, default=None)
    args = ap.parse_args()
    result = run_script(args.script, timeout=args.timeout, max_mem_mb=args.max_mem_mb)
    print(f"returncode={result['returncode']}")
    if result["stdout"]:
        print("-- stdout --\n" + result["stdout"])
    if result["stderr"]:
        print("-- stderr --\n" + result["stderr"])
    sys.exit(0 if result["returncode"] == 0 else 1)


if __name__ == "__main__":
    main()