# 贡献指南

欢迎提交 Pull Request 或 Issue。

## 开发环境

```bash
# 克隆项目
git clone <repo-url>
cd tts

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn app.main:app --reload
```

## 代码规范

- Python 代码使用 `python -m py_compile` 确保无语法错误
- 前端代码使用原生 JS/CSS，无框架依赖
- 新增 API 端点需要在 `app/api/routes.py` 中注册

## Pull Request 流程

1. Fork 项目并创建分支
2. 确保代码通过语法检查
3. 提交时请描述清楚改动内容
4. 等待 Code Review

## 报告问题

请描述以下信息：
- 复现步骤
- 预期行为 vs 实际行为
- 环境信息（操作系统、Python 版本）
