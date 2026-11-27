# DSH 沙箱旁路补丁：应用说明（请仔细阅读）

## 这是什么

一次性的本地补丁，给 DeepSeek Harness（@deepseek-ai/dsh **0.2.2-rc.1**，macOS）增加一个环境变量开关 `DSH_SANDBOX_OFF=1`：
开启后，所有命令**不再经过 `sandbox-exec` 包装**直接执行，用于解决本机 `spawn sandbox-exec EAGAIN`（沙箱 runner 无法 spawn，fail-closed 导致所有 bash 命令不可用）的问题。

补丁作用于 `dsh-sandbox-local/lib/index.js` 的 `LocalSandboxProvider.confine()`。

## 影响与风险（读清楚再决定）

1. **全局生效**：这是全局 npm 包修改，影响**所有使用该 DSH 安装的会话和设备**，不止当前会话。
2. **安全降级**：打开开关后命令无文件系统限制（原先 workspace-write/read-only 的隔离消失）。仅在你信任本机和本机用户的前提下使用。
3. **默认关闭**：不设置 `DSH_SANDBOX_OFF=1` 时行为完全不变（补丁只加了一个判断分支）。
4. **会被升级覆盖**：`dsh` 更新/重装后补丁丢失，需重新应用。
5. 应用后**必须重启 DSH 服务进程**才生效（模块已加载）。
6. 这是本地维护补丁，不是上游行为；报告 bug 前请先卸载补丁复现。

## 应用步骤

```bash
# 1) 备份
P=/opt/node-v24.22.2-darwin-arm64/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/dsh-sandbox-local/lib/index.js
cp "$P" "$P.bak-$(date +%Y%m%d-%H%M%S)"

# 2) 应用补丁（两种方式任选）
cd /opt/node-v24.22.2-darwin-arm64/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/dsh-sandbox-local
patch -p2 < /Users/admin/Documents/DiscoveryRSI/DSH改沙箱/dsh-sandbox-off.patch
# 或用编辑器手动把补丁里的 6 行插入 confine() 开头（policy 归一化之后、runnerCommand 分支之前）

# 3) 确认补丁在位
grep -n "DSH_SANDBOX_OFF" lib/index.js

# 4) 重启 DSH 服务，并在服务环境中注入 DSH_SANDBOX_OFF=1
#    例如 launchd: 在 plist 的 EnvironmentVariables 加 DSH_SANDBOX_OFF=1 后
#    launchctl unload/load；或由你当前的 dsh 启动方式决定
```

## 验证

重启后在本会话执行 `echo ok`——不再出现 `spawn sandbox-exec EAGAIN` 即为成功。
（本会话若仍失败，说明：a) 环境变量没进服务进程；b) DSH 没有重启；c) 补丁未应用。）

## 回滚

```bash
P=.../dsh-sandbox-local/lib/index.js
# 恢复最近备份
cp "$(ls -t "$P".bak-* | head -1)" "$P"
# 或删除补丁分支后重启。默认环境未设 DSH_SANDBOX_OFF 时补丁本身无行为差异。
```

## 备选（建议先做，成本为零）

在改代码前先排查 EAGAIN 根因，可能不用改：
- 进程数/内存资源：`launchctl limit maxproc`、`ulimit -u`、`sysctl kern.maxprocperuid`；
- 重启 DSH 服务试试是否自愈；
- 检查 `sandbox-exec` 是否还能单独运行：`/usr/bin/sandbox-exec -p '(version 1)(allow default)' /usr/bin/true`。