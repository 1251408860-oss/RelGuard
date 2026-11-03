# RelGuard: Source-Checked Relational Guards from Automatic State Contracts

RelGuard 是论文 **Source-Checked Relational Guards from Automatic State Contracts** 的核心研究实现。系统从原生执行中推断状态合约，验证合约与 C 源程序的联系，再构造可执行的关系守卫，用于按观测字段复用验证证据。

仓库围绕模型构建、独立检查和实验复现组织。下表将论文的各个部分映射到实现及参考数据，便于定位和运行。

[English](./README.md)

## 仓库导航与论文工件映射

| 论文组成或实验范围 | 内容 | 目录链接 |
| :--- | :--- | :--- |
| 合约模型与推断 | writer 位投影、仿射状态、整数表达式、有序比较及主动区分查询 | [模型](./scguard/models) · [推断](./scguard/inference) |
| 独立验证 | 模型与生成代码检查、消元证书回放、绑定原始验证记录的字段接纳 | [验证器](./scguard/checks) |
| 源程序义务与守卫生成 | CRC 组合、算术规范化、类型化源码桥接、writer 成对守卫和前缀生成 | [源程序义务](./scguard/source) · [代码生成](./scguard/codegen) · [公共接口](./scguard/core.py) |
| writer 实验 | 十二个源程序合约、八组版本转换、原生执行参考和匹配的策略比较结果 | [writer 数据](./scguard/data/writer) |
| 跨族实验 | CRC-32、Adler-32、内存移动和比较符号的十二个 API/版本任务，以及训练观测和关系证书 | [跨族数据](./scguard/data/cross_family) |
| 论文图表 | 两张结构图、两张实验图、两张表及可编辑 PDF/SVG/TeX 文件 | [绘图实现](./scguard/plotting) · [图表文件](./assets) |
| 复现与验证记录 | 统一复现入口、回归测试、文件指纹和本地验证记录 | [复现入口](./reproduce.py) · [测试](./tests) · [验证记录](./provenance) |

## 整体环境要求

封存结果复现流程支持 Windows 和 Ubuntu/Linux，使用 **Python 3.12 或更新版本**。Python 依赖见 [requirements.txt](./requirements.txt)：

- `z3-solver`：符号区分查询及受限生成代码检查；
- `numpy`、`matplotlib`：论文图表及表格预览。

GitHub 的 [Core checks 工作流](./.github/workflows/ci.yml) 在 Ubuntu 上执行单元测试、封存结果复现、候选推断和接口示例。

重新检查 C 源程序时，需要另外准备记录中的 **CBMC 6.11.0**、**ESBMC 8.6** 和 **GCC 13.3** 环境。数据协议提供源程序身份、包装函数、生成头文件设置、ABI 前提及检查器参数。具体流程见[源程序验证说明](./docs/source_checks.md)。

## 仓库内置参考数据

参考数据随仓库提供，位于 [scguard/data](./scguard/data)。两个实验目录包含模型、协议、请求记录、原生 O0/O2 输出、生成的 C 守卫、已保存的编译守卫输出及关系系统。跨族实验还包含重建候选所需的原始训练观测。

| 实验 | 有效请求 | SUPPORT | REFUTE |
| :--- | ---: | ---: | ---: |
| writer 类型化策略 | 122,880 | 72,162 | 50,718 |
| 跨族完成验证路线 | 49,896 | 13,076 | 36,820 |

在匹配的请求目录上，writer 守卫的确定性判定覆盖量是完整入口身份策略的 **4.8 倍**。跨族回放核对 **2,592 份仿射证书**及 **648 个整数或有序返回系统**，并核对同一批有效请求中 **17,496 次中间阶段弃权**的消解。两个最终实验目录中，错误的确定性判定均为零。数据同时保留中间结果、对比策略错误和非法请求控制。

按 [SHA-256 清单](./scguard/data/manifest.sha256.json)检查 **242 个参考文件**：

```bash
python -m scguard verify-data
```

数据内容及二进制记录格式见 [docs/data.md](./docs/data.md)。

## 快速安装

克隆仓库并安装 Python 依赖：

```bash
git clone https://github.com/1251408860-oss/RelGuard.git
cd RelGuard
python -m pip install -r requirements.txt
```

以下命令均在仓库根目录执行。

### 复现封存实验结果与论文图表

```bash
python reproduce.py
```

程序会校验参考文件，回放两个实验目录，重建四张图和两张表，并导出 CRC 示例守卫及已检查的关系核。该命令使用仓库内置的执行记录。

| 输出 | 内容 |
| :--- | :--- |
| `build/replay.json` | 172,776 条有效请求的重算结果及仿射证书检查 |
| `build/figures/` | 四组图、两张表的预览、可编辑 TeX 表格及布局和颜色检查 |
| `build/crc_kernel.json` | CRC 关系方程及经独立检查的消元证书 |
| `build/crc_guard.c` | 可执行 CRC 守卫示例 |
| `build/reproduction.json` | 复现汇总 |

### 重建候选与导出守卫

```bash
python -m scguard infer --task miniz-3.1.0-crc32 --output build/crc-model.json
python -m scguard export --left miniz-3.1.0-adler32 --right miniz-3.1.1-adler32 --output build/adler-guard.c
python -m scguard export --cohort writer --left libgrapheme-2.0.1 --right libgrapheme-2.0.2 --output build/writer-guard.c
python -m examples.quickstart
```

推断命令使用已保存的训练观测拟合跨族候选。writer 主动推断通过 `scguard.inference.active.learn_writer` 接收原生观测回调。源程序接纳步骤负责在记录的调用前提下建立候选与 C 实现之间的联系。

### 运行验证检查

```bash
python -m unittest discover -s tests -v
```

**28 项测试**覆盖模型格式、非法请求、主动推断、候选重建、生成代码破坏、消元证书破坏、守卫逐字重建和源程序字段证据接纳。

### 重新检查 C 源程序义务

执行新的源程序检查前，准备指定的上游源码、生成头文件和 C 验证工具。生成验证义务的示例：

```bash
python -m scguard harness --task miniz-3.1.0-crc32 --route crc-step --output build/checks/crc-step.c
```

[源程序验证说明](./docs/source_checks.md)列出了可用路线、所需前提、源码准备和原始结果读取方式。新的执行记录与历史结果一并保存。

接口用法、数据格式和源程序验证要求分别见[实现说明](./docs/implementation.md)、[数据说明](./docs/data.md)和[源程序验证说明](./docs/source_checks.md)。运行 `python -m scguard --help` 可查看各个命令。

## 工件与许可

项目自身代码目前未授予许可证。第三方字体声明保留在 [NOTICE.md](./NOTICE.md) 和 [third_party](./third_party)。
