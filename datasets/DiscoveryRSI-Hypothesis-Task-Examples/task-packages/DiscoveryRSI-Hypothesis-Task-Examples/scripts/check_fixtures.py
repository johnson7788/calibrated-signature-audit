"""Run the released synthetic fixtures in disposable output directories."""
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    report = []
    for package in sorted((ROOT / 'tasks').iterdir()):
        config = json.loads((package / 'validation.json').read_text())
        probes = [(p, '1') for p in config['good_solutions']]
        probes += [(p, '0') for p in config['bad_solutions']]
        for fixture, expected in probes:
            with tempfile.TemporaryDirectory(prefix='discoveryrsi-example-') as temporary:
                root = Path(temporary)
                for name in ['workspace', 'logs/verifier', 'validation', 'tests', 'bin']:
                    (root / name).mkdir(parents=True, exist_ok=True)
                for name in ['python', 'python3']:
                    (root / 'bin' / name).symlink_to(sys.executable)
                environment = {**os.environ, 'PATH': str(root / 'bin') + os.pathsep + os.environ.get('PATH', '')}
                for source in package.rglob('*'):
                    if not source.is_file():
                        continue
                    relative = source.relative_to(package)
                    if relative.parts[0] not in ['validation', 'tests']:
                        continue
                    text = source.read_text()
                    for prefix in ['/workspace', '/logs/verifier', '/validation', '/tests']:
                        text = text.replace(prefix, str(root / prefix.lstrip('/')))
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(text)
                generated = subprocess.run(['bash', str(root / fixture)], cwd=root, env=environment, capture_output=True, text=True, timeout=30)
                verified = subprocess.run(['bash', str(root / 'tests/test.sh')], cwd=root, env=environment, capture_output=True, text=True, timeout=30)
                reward_path = root / 'logs/verifier/reward.txt'
                reward = reward_path.read_text().strip() if reward_path.exists() else 'missing'
                passed = generated.returncode == 0 and verified.returncode == 0 and reward == expected
                report.append({'id': package.name, 'fixture': fixture, 'expected_reward': expected, 'actual_reward': reward, 'passed': passed})
                print(('PASS' if passed else 'FAIL'), package.name, fixture)
                if not passed:
                    print(generated.stderr[-1500:], verified.stdout[-1500:], verified.stderr[-1500:])
    print(f'{sum(r["passed"] for r in report)}/{len(report)} fixture checks passed')
    return 0 if report and all(r['passed'] for r in report) else 1


if __name__ == '__main__':
    raise SystemExit(main())
