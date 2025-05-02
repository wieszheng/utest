以下是常见的查询操作符 `eq`, `ne`, `gt`, `lt`, `ge`, `le`, `like`, `in` 的具体说明，常用于数据库查询条件构造（如 SQLAlchemy）：

| 操作符 | 全称          | 含义                       | 示例 SQL 表达式       | 用途说明                                                         |
| ------ | ------------- | -------------------------- | --------------------- | ---------------------------------------------------------------- |
| `eq`   | equal         | 等于                       | `column = value`      | 查询等于某值的记录                                               |
| `ne`   | not equal     | 不等于                     | `column != value`     | 查询不等于某值的记录                                             |
| `gt`   | greater than  | 大于                       | `column > value`      | 查询大于某值的记录                                               |
| `lt`   | less than     | 小于                       | `column < value`      | 查询小于某值的记录                                               |
| `ge`   | greater equal | 大于等于                   | `column >= value`     | 查询大于或等于某值的记录                                         |
| `le`   | less equal    | 小于等于                   | `column <= value`     | 查询小于或等于某值的记录                                         |
| `like` | like          | 模糊匹配（支持通配符 `%`） | `column LIKE pattern` | 查询符合某种模式的字符串，例如：`"abc%"` 匹配以 abc 开头的字符串 |
| `in`   | in            | 在一组值中                 | `column IN (values)`  | 查询字段值在指定集合中的记录                                     |

### 示例说明：

假设有一个用户表 `User`，包含字段 `name` 和 `age`。

- `eq`: 查询名字是 "Alice" 的用户

  ```python
  name={"eq": "Alice"}
  ```

- `ne`: 查询年龄不是 30 的用户

  ```python
  age={"ne": 30}
  ```

- `gt`: 查询年龄大于 25 的用户

  ```python
  age={"gt": 25}
  ```

- `lt`: 查询年龄小于 20 的用户

  ```python
  age={"lt": 20}
  ```

- `ge`: 查询年龄大于等于 18 的用户

  ```python
  age={"ge": 18}
  ```

- `le`: 查询年龄小于等于 60 的用户

  ```python
  age={"le": 60}
  ```

- `like`: 查询名字以 "Joh" 开头的用户

  ```python
  name={"like": "Joh%"}
  ```

- `in`: 查询年龄为 20、25 或 30 的用户
  ```python
  age={"in": [20, 25, 30]}
  ```

这些操作符通常用于构建灵活的查询条件，提升数据筛选能力。
