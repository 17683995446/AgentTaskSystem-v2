# AgentTaskSystem 系统架构详解

## 📋 目录
- [系统概览](#系统概览)
- [二叉树结构](#二叉树结构)
- [模块详解](#模块详解)
- [流程图](#流程图)

---

## 系统概览

AgentTaskSystem 是一个**严格遵循二叉树架构规范 V2.0** 的智能任务调度系统，专为长时间、高可靠性的任务执行设计。

### 核心特性
- ✅ 二叉树模块化架构
- ✅ 接口严格隔离
- ✅ 任务断点续跑
- ✅ 智能失败重试
- ✅ 状态严格管理

---

## 二叉树结构

### 完整架构树

```
AgentTaskSystem (Level 0 - Root)
├─ TaskCore (Level 1 - Data Layer)
│  ├─ TaskDefine (Level 2 - Leaf)
│  │  ├─ interfaces/
│  │  │  ├─ ITaskDefine.py
│  │  │  └─ TaskStatusEnum.py
│  │  └─ impl/
│  │     ├─ TaskDefineImpl.py
│  │     └─ TaskDataDto.py
│  └─ TaskState (Level 2 - Leaf)
│     ├─ interfaces/
│     │  └─ ITaskState.py
│     └─ impl/
│        └─ TaskStateImpl.py
└─ AgentRuntime (Level 1 - Execution Layer)
   ├─ TaskSchedule (Level 2 - Leaf)
   │  ├─ interfaces/
   │  │  └─ ITaskSchedule.py
   │  └─ impl/
   │     └─ TaskScheduleImpl.py
   └─ TaskRunner (Level 2 - Leaf)
      ├─ interfaces/
      │  └─ ITaskRunner.py
      └─ impl/
         ├─ TaskRunnerImpl.py
         └─ TaskContextDto.py
```

### 层级说明

| 层级 | 模块 | 功能 |
|------|------|------|
| 0 | AgentTaskSystem | 根模块，系统入口 |
| 1 | TaskCore | 数据和状态层 |
| 1 | AgentRuntime | 执行和调度层 |
| 2 | TaskDefine | 任务定义和数据模型 |
| 2 | TaskState | 状态流转和快照 |
| 2 | TaskSchedule | 队列管理和调度策略 |
| 2 | TaskRunner | 任务执行和上下文管理 |

---

## 模块详解

### 1. TaskDefine - 任务定义模块

**文件位置**: [TaskCore/TaskDefine/](file:///workspace/AgentTaskSystem/TaskCore/TaskDefine/)

#### 核心职责
- 任务数据模型定义
- 任务创建和查询
- 任务状态枚举

#### 关键文件

| 文件 | 位置 | 功能 |
|------|------|------|
| ITaskDefine.py | interfaces/ | 任务定义接口 |
| TaskStatusEnum.py | interfaces/ | 任务状态枚举 |
| TaskDefineImpl.py | impl/ | 实现类 |
| TaskDataDto.py | impl/ | 任务数据传输对象 |

#### 任务状态枚举

```python
class TaskStatusEnum(Enum):
    PENDING = "pending"      # 待执行
    RUNNING = "running"      # 执行中
    PAUSED = "paused"        # 已暂停
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 已失败
    CANCELLED = "cancelled"  # 已取消
```

---

### 2. TaskState - 状态管理模块

**文件位置**: [TaskCore/TaskState/](file:///workspace/AgentTaskSystem/TaskCore/TaskState/)

#### 核心职责
- 状态流转验证
- 任务快照管理
- 异常状态回滚

#### 状态流转图

```
PENDING → RUNNING → COMPLETED
   ↓         ↓         ↓
CANCELLED  PAUSED    (END)
             ↓
         FAILED/RETRY
```

#### 关键方法
- `update_status()` - 更新任务状态（含验证）
- `create_snapshot()` - 创建任务快照
- `get_latest_snapshot()` - 获取最新快照

---

### 3. TaskSchedule - 任务调度模块

**文件位置**: [AgentRuntime/TaskSchedule/](file:///workspace/AgentTaskSystem/AgentRuntime/TaskSchedule/)

#### 核心职责
- 任务队列管理
- 调度策略实现
- 重试次数控制

#### 队列特性
- 优先级排序
- FIFO 执行
- 超时检测
- 去重机制

---

### 4. TaskRunner - 任务执行模块

**文件位置**: [AgentRuntime/TaskRunner/](file:///workspace/AgentTaskSystem/AgentRuntime/TaskRunner/)

#### 核心职责
- 任务实际执行
- 上下文管理
- 断点续跑支持

#### 关键功能
- 启动/暂停/停止
- 业务逻辑集成
- 异常处理和重试

---

## 流程图

### 1. 完整任务执行流程

```
┌─────────────────────────────────────────────────────────────────┐
│                      AgentTaskSystem 执行流程                     │
└─────────────────────────────────────────────────────────────────┘

            ┌───────────────┐
            │   用户创建     │
            │    任务       │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │  TaskDefine   │
            │  创建任务实体  │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │  TaskState    │
            │  初始状态:    │
            │    PENDING    │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │ TaskSchedule  │
            │  加入队列     │
            │  优先级排序   │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │  TaskRunner   │
            │  从队列取出   │
            │  更新状态:    │
            │    RUNNING    │
            └───────┬───────┘
                    │
                    ├──────────────────┐
                    │  正常执行        │
                    │                  │
                    ▼                  ▼
          ┌───────────────┐    ┌───────────────┐
          │  执行业务逻辑  │    │    发生异常    │
          │  逐步执行      │    │  捕获错误      │
          │  每步保存快照  │    └───────┬───────┘
          └───────┬───────┘            │
                  │                    │
                  ▼                    ▼
          ┌───────────────┐    ┌───────────────┐
          │ TaskState     │    │  TaskSchedule │
          │ 更新状态:     │    │  检查重试次数  │
          │  COMPLETED    │    └───────┬───────┘
          └───────────────┘            │
                                       ▼
                          ┌─────────────────────┐
                          │  还有重试次数?       │
                          └───────┬───────┬─────┘
                                  │       │
                                  Y       N
                                  │       │
                                  ▼       ▼
                         ┌──────────┐  ┌──────────┐
                         │  重试执行 │  │ FAILED  │
                         └──────────┘  └──────────┘
```

---

### 2. 状态流转详细流程

```
┌─────────────────────────────────────────────────────────────────┐
│                   TaskState 状态流转图                          │
└─────────────────────────────────────────────────────────────────┘

                      ┌─────────┐
                      │ PENDING │ ◄──────┐
                      └────┬────┘       │
                           │ 恢复       │
                           ▼            │
    ┌─────────────────────┬──────────┐ │
    │              ┌─────────┐      │ │
    │      ┌──────►│ PAUSED  │      │ │
    │      │       └────┬────┘      │ │
    │      │            │           │ │
    │      │            │ 继续      │ │
    │      │            ▼           │ │
    │      │      ┌─────────┐      │ │
    │      │      │ RUNNING │──────┘ │
    │      │      └────┬────┘        │
    │      │           │             │
    │      │           ▼             │
    │      │      ┌─────────┐       │
    │      │      │FAILED   │       │
    │      │      └────┬────┘       │
    │      │           │ 重试       │
    │      └───────────┘            │
    │                               │
    │      ┌─────────┐              │
    │      │COMPLETED│              │
    │      └────┬────┘              │
    │           │ 终止              │
    │           ▼                   │
    │      ┌─────────┐              │
    └─────►│CANCELLED│◄─────────────┘
           └─────────┘

【说明】
- PENDING → RUNNING: 任务开始执行
- RUNNING → PAUSED: 任务暂停
- PAUSED → RUNNING: 任务继续
- RUNNING → COMPLETED: 正常完成
- RUNNING → FAILED: 执行失败
- FAILED → PENDING: 重试队列
- 所有状态 → CANCELLED: 取消任务
```

---

### 3. 数据和控制流图

```
┌─────────────────────────────────────────────────────────────────┐
│                AgentTaskSystem 数据流和控制流                    │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐     ┌──────────────────┐
│   外部系统/用户  │─────▶│  ITaskDefine      │
│  创建任务请求    │     │  (Interface)      │
└──────────────────┘     └─────────┬────────┘
                               ┌─────┴──────┐
                               │            │
┌──────────────────┐     ┌─────▼──────┐   │
│  任务数据模型    │     │TaskDefine  │   │
│  (TaskDataDto)  │◀────│  (Impl)     │   │
└──────────────────┘     └─────┬──────┘   │
                               │            │
                               ▼            │
                      ┌─────────────────┐  │
                      │  ITaskState     │  │
                      │  (Interface)    │  │
                      └────────┬────────┘  │
                               │           │
                               ▼           │
                      ┌─────────────────┐  │
                      │ TaskStateImpl   │  │
                      │ 状态管理/快照    │  │
                      └────────┬────────┘  │
                               │           │
           ┌───────────────────┼───────────┤
           │                   │           │
┌──────────▼──────────┐ ┌──────▼───────┐  │
│  ITaskSchedule      │ │  ITaskRunner │  │
│  (Interface)        │ │  (Interface) │  │
└──────────┬──────────┘ └──────┬───────┘  │
           │                   │           │
           ▼                   ▼           │
   ┌────────────────┐   ┌────────────────┐ │
   │TaskScheduleImpl│   │ TaskRunnerImpl │ │
   │队列管理/重试    │   │ 执行引擎       │ │
   └────────────────┘   └────────────────┘ │
           │                   │           │
           └───────────┬───────┘           │
                       ▼                   │
              ┌─────────────────┐          │
              │   实际业务逻辑   │          │
              │  (可自定义)     │          │
              └─────────────────┘          │
                                           │
┌──────────────────────────────────────────┘
│
▼
┌─────────────────┐
│   AgentTaskSystem
│   (根入口)
└─────────────────┘
```

---

### 4. 集成到 DataVista Pro 后的完整流程

```
┌─────────────────────────────────────────────────────────────────┐
│            DataVista Pro + AgentTaskSystem 完整架构             │
└─────────────────────────────────────────────────────────────────┘

                ┌───────────────────────────┐
                │   用户界面 (Web前端)      │
                │ ┌───────────────────────┐ │
                │ │   数据可视化 (8种图) │ │
                │ └───────────────────────┘ │
                │ ┌───────────────────────┐ │
                │ │   任务管理界面        │ │
                │ └───────────────────────┘ │
                └───────────┬───────────────┘
                            │
                            ▼ HTTP/REST
                ┌───────────────────────────┐
                │   AgentTasks (新增模块)    │
                │ ┌───────────────────────┐ │
                │ │ DataCollectTask       │ │
                │ │ MonitorTasks          │ │
                │ │ ReportTasks           │ │
                │ └───────────────────────┘ │
                └───────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────────┐
                │   AgentTaskSystem (核心)  │
                │                           │
                │ ┌───────────────────────┐ │
                │ │ TaskCore (数据层)     │ │
                │ │ ├─ TaskDefine         │ │
                │ │ └─ TaskState          │ │
                │ └───────────────────────┘ │
                │                           │
                │ ┌───────────────────────┐ │
                │ │ AgentRuntime (执行层) │ │
                │ │ ├─ TaskSchedule       │ │
                │ │ └─ TaskRunner         │ │
                │ └───────────────────────┘ │
                └───────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────────┐
                │   DataVista Pro 可视化    │
                │  ──────────────────────  │
                │  8种图表类型              │
                │  数据展示/交互           │
                └───────────────────────────┘
```

---

## 关键接口说明

### 1. ITaskDefine ([TaskCore/TaskDefine/interfaces/ITaskDefine.py](file:///workspace/AgentTaskSystem/TaskCore/TaskDefine/interfaces/ITaskDefine.py))

```python
class ITaskDefine(ABC):
    @abstractmethod
    def create_task(self, name, type, params) -> str:
        # 创建新任务，返回 task_id
        
    @abstractmethod
    def update_indicator(self, task_id, updates) -> bool:
        # 更新任务信息
        
    @abstractmethod
    def delete_indicator(self, task_id) -> bool:
        # 删除任务
        
    @abstractmethod
    def get_indicator(self, task_id) -> Optional[Dict]:
        # 获取任务详情
        
    @abstractmethod
    def list_indicators(self, filters) -> List[Dict]:
        # 列出任务列表
```

### 2. ITaskState ([TaskCore/TaskState/interfaces/ITaskState.py](file:///workspace/AgentTaskSystem/TaskCore/TaskState/interfaces/ITaskState.py))

```python
class ITaskState(ABC):
    @abstractmethod
    def update_status(self, task_id, new_status) -> bool:
        # 更新状态（含验证）
        
    @abstractmethod
    def create_snapshot(self, task_id, context) -> str:
        # 创建快照
        
    @abstractmethod
    def restore_snapshot(self, task_id, snapshot_id) -> Dict:
        # 从快照恢复
        
    @abstractmethod
    def get_latest_snapshot(self, task_id) -> Dict:
        # 获取最新快照
```

### 3. ITaskSchedule ([AgentRuntime/TaskSchedule/interfaces/ITaskSchedule.py](file:///workspace/AgentTaskSystem/AgentRuntime/TaskSchedule/interfaces/ITaskSchedule.py))

```python
class ITaskSchedule(ABC):
    @abstractmethod
    def enqueue_task(self, task_id) -> bool:
        # 任务入队
        
    @abstractmethod
    def dequeue_task(self) -> Optional[str]:
        # 任务出队
        
    @abstractmethod
    def check_retry(self, task_id) -> bool:
        # 检查是否可以重试
        
    @abstractmethod
    def set_task_callback(self, callback):
        # 设置状态变更回调
```

### 4. ITaskRunner ([AgentRuntime/TaskRunner/interfaces/ITaskRunner.py](file:///workspace/AgentTaskSystem/AgentRuntime/TaskRunner/interfaces/ITaskRunner.py))

```python
class ITaskRunner(ABC):
    @abstractmethod
    async def start_task(self, task_id, logic) -> bool:
        # 启动任务
        
    @abstractmethod
    async def resume_task(self, task_id, logic) -> bool:
        # 从断点续跑
        
    @abstractmethod
    async def stop_task(self, task_id) -> bool:
        # 停止任务
```

---

## 总结

AgentTaskSystem 采用**严格的二叉树架构**，实现了：

- 📦 **清晰的模块划分** - 职责单一，互不干扰
- 🔒 **接口隔离** - 跨模块只访问 interface
- 🔄 **完整状态管理** - 状态机 + 快照支持
- ⚡ **智能调度** - 优先级 + 重试 + 超时
- 📊 **灵活集成** - 与 DataVista 等系统完美配合

所有模块都严格遵循 **V2.0 规范**：
- ✅ 模块结构公理
- ✅ 调用隔离公理
- ✅ 文件命名公理
- ✅ 方法行数公理
