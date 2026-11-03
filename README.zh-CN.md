# RelGuard

论文核心研究的当前实现。代码按功能组织，统一入口负责数据校验、结果回放、关系核与守卫生成、验证义务生成以及图表重建。

[English](README.md) · [代码说明](docs/implementation.md) · [数据格式](docs/data.md) · [源程序验证](docs/source_checks.md)

## 直接运行

使用 Python 3.12 或更新版本。在本目录打开终端，执行：

```sh
python -m pip install -r requirements.txt
python reproduce.py
```

程序会校验参考数据，回放两个实验目录的结果，重建四张图和两张表，并生成 CRC 示例守卫及关系核。输出保存在 `build/`：

| 输出 | 内容 |
| --- | --- |
| `replay.json` | 两个实验目录的完整回放统计 |
| `figures/` | 四张图、两张表及布局与颜色检查 |
| `crc_kernel.json` | 独立检查的关系核 |
| `crc_guard.c` | 示例 C 守卫 |
| `reproduction.json` | 本次运行汇总 |

检查代码：

```sh
python -m unittest discover -s tests -v
```

## 目录

| 目录或文件 | 用途 |
| --- | --- |
| `scguard/models/` | writer 位投影、仿射状态、整数和有序比较模型 |
| `scguard/inference/` | 主动查询推断与封存观测数据上的候选重建 |
| `scguard/checks/` | 模型、生成代码、消元证书及字段证据检查 |
| `scguard/source/` | CRC 组合证明义务、算术范围义务与规范化 |
| `scguard/codegen/` | 整数前缀代码生成 |
| `scguard/plotting/figures.py` | 你微调后的结构图与论文图表生成 |
| `scguard/core.py` | 对外调用接口 |
| `scguard/data/` | 模型、协议、输入输出和训练观测记录 |
| `tests/` | 回归和推断测试 |
| `examples/quickstart.py` | 接口调用示例 |
| `assets/` | 四图两表的预览及可编辑文件 |
| `reproduce.py` | 统一运行入口 |

每项功能只保留当前实现。公开代码没有历史实验调度目录，也不依赖原项目的实验路径。

## 单独使用功能

```sh
python -m scguard --help
python -m scguard verify-data
python -m scguard replay --cohort all --output build/replay.json
python -m scguard infer --task miniz-3.1.0-adler32 --output build/adler-model.json
python -m scguard kernel --left miniz-3.1.0-crc32 --right miniz-3.1.1-crc32 --observer return --output build/crc-kernel.json
python -m scguard export --left miniz-3.1.0-adler32 --right miniz-3.1.1-adler32 --output build/adler-guard.c
python -m scguard export --cohort writer --left libgrapheme-2.0.1 --right libgrapheme-2.0.2 --output build/writer-guard.c
python -m scguard harness --task libgrapheme-2.0.1 --cohort writer --output build/writer-check.c
python -m scguard figures --output build/figures
python -m examples.quickstart
```

`infer` 使用已封存的跨族训练观测重新拟合候选。writer 主动推断的接口是 `scguard.inference.active.learn_writer`，调用示例见代码说明。候选推断不会自动把候选当作已证明合约。

## 实验与公开范围

writer 回放包含 122,880 条有效请求，跨族回放包含 49,896 条有效请求，并独立回放 2,592 份仿射证书。中间阶段 UNKNOWN、对比策略错误判定和非法请求控制继续保留在数据中。

包内可直接运行结果回放、候选重建、验证义务生成和图表生成。重新检查 C 源程序需要另外准备指定的第三方源码及模型检查器，具体步骤见源程序验证说明。原项目的封存实验、完整历史工作区和真人问卷不在本公开目录中。

## 工件与许可

本仓库公开论文核心实现和结果回放数据。项目自身代码暂不添加许可证，第三方字体声明保留，详见 NOTICE.md。
