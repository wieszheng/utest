`cron` 是一种用于定时任务调度的表达式格式，常用于 Unix/Linux 系统和各种调度框架（如 APScheduler、Airflow、Quartz 等）中。它通过 **空格分隔的 5 或 6 个字段** 来定义任务执行的时间规则。

---

### 🧮 标准 `cron` 表达式格式

| 字段 | 允许值         | 含义                                   |
| ---- | -------------- | -------------------------------------- |
| 1    | 0-59           | 分钟（minute）                         |
| 2    | 0-59           | 秒（second） _(可选，部分系统支持6位)_ |
| 3    | 0-23           | 小时（hour）                           |
| 4    | 1-31           | 日（day of month）                     |
| 5    | 1-12 / JAN-DEC | 月（month）                            |
| 6    | 0-6 / SUN-SAT  | 星期几（day of week）                  |

> 在 `APScheduler` 中使用 `CronTrigger.from_crontab()` 时，通常只接受 **5 个字段**：`minute hour day month day_of_week`

---

### ✅ 示例说明

| cron 表达式     | 含义描述                   |
| --------------- | -------------------------- |
| `* * * * *`     | 每分钟执行一次             |
| `0 * * * *`     | 每小时整点执行一次         |
| `0 0 * * *`     | 每天午夜（00:00）执行      |
| `0 0 1 * *`     | 每月的第一天午夜执行       |
| `0 0 * * 0`     | 每周日午夜执行             |
| `0 0 8 1 *`     | 每月 1 号 08:00 执行       |
| `*/5 * * * *`   | 每 5 分钟执行一次          |
| `30 10 * * 1-5` | 每周一到周五 10:30 执行    |
| `0 0,12 * * *`  | 每天的 00:00 和 12:00 执行 |

---

### 🔁 特殊符号说明

| 符号  | 说明                                                      |
| ----- | --------------------------------------------------------- |
| `*`   | 任意值，例如 `*` 在分钟字段表示“每分钟”                   |
| `*/n` | 每 n 次执行一次，例如 `*/5` 表示“每 5 次”                 |
| `-`   | 范围，例如 `1-5` 表示“从 1 到 5”                          |
| `,`   | 枚举多个值，例如 `1,3,5` 表示“第 1、3、5 次”              |
| `L`   | 最后一天（仅在日字段中使用），如 `L` 表示“每月最后一天”   |
| `W`   | 工作日（周一至周五），如 `15W` 表示“离 15 号最近的工作日” |
| `#`   | 第几个星期几，如 `5#3` 表示“第三个星期五”                 |
| `?`   | 不指定值（通常用于日期/星期冲突时）                       |

---

### 📌 在你代码中的应用

你的代码中使用了：

```python
from apscheduler.triggers.cron import CronTrigger

trigger=CronTrigger.from_crontab(cron)
```

这意味着传入的 `cron` 字符串应为标准的 **5 字段 crontab 格式**，例如：

- `"0 0 * * *"` → 每天 00:00 执行
- `"30 8 * * 1"` → 每周一早上 8:30 执行
- `"*/10 * * * *"` → 每 10 分钟执行一次

---

### 💡 建议：可以使用的在线工具

你可以使用以下网站来测试和生成 `cron` 表达式：

- [https://crontab.guru](https://crontab.guru/)
- [https://www.freeformatter.com/cron-expression-generator-quartz.html](https://www.freeformatter.com/cron-expression-generator-quartz.html)

---

### 🧪 示例 API 请求体（FastAPI）

如果你通过接口添加任务，比如：

```python
@router.post("/job", summary='添加任务')
async def create_job(plan_id: str, plan_name: str, cron: str):
    ...
```

请求示例：

```bash
POST /job?plan_id=1&plan_name=demo&cron=0+0+12+*+*
```

即每天中午 12 点执行该任务。

---

### ✅ 总结

| 目的             | cron 示例      |
| ---------------- | -------------- |
| 每分钟           | `* * * * *`    |
| 每小时整点       | `0 * * * *`    |
| 每天凌晨         | `0 0 * * *`    |
| 每周一上午 9:30  | `30 9 * * 1`   |
| 每月第一天 00:00 | `0 0 1 * *`    |
| 每 10 分钟       | `*/10 * * * *` |

如需更复杂的调度逻辑，建议结合 `APScheduler` 的 `CronTrigger` 文档进行配置：[APScheduler CronTrigger](https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html)
