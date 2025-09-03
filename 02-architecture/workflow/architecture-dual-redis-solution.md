# 方案 2：双Redis缓存 + WebSocket心跳方案（加注控制面/数据面）

## 架构特点
- 主备双Redis提供高可用性（建议 Redis Streams 实现有序流 + 消费组）
- WebSocket 替代 SSE，支持双向通信和心跳保活
- 基于序列号（seq）的断点续传机制
- 明确区分 控制面（Backend⇄Infra 的指令） 与 数据面（结果流转）

```mermaid
sequenceDiagram
    participant F as Frontend
    participant B as Backend
    participant RP as Redis Primary
    participant RB as Redis Backup
    participant IS as Infra Service
    participant LLM as LLM Service

    F->>B: 建立 WebSocket 连接
    loop 心跳检测
        F->>B: ping
        B->>F: pong
    end

    Note over B,IS: 控制面（gRPC/HTTP）
    B->>RP: XADD requests {session_id, last_seq, prompt, meta}
    B->>IS: StartSession(session_id, last_seq, prompt, meta)
    IS->>RP: 读取/校验断点（XRANGE/XINFO）

    Note over RP,RB: 数据面（Redis Streams）
    B->>RB: 主从/哨兵自动同步（无需业务显式写）
    IS->>LLM: 调用 LLM stream

    loop 流式结果
        LLM-->>IS: 返回 chunk
        IS->>RP: XADD responses:{session_id} {seq, chunk}
        IS->>RB: 异步复制（由 Redis 负责）
        B->>RP: XREADGROUP responses:{session_id} BLOCK 0
        B-->>F: WebSocket 推送 chunk
    end

    alt 断连恢复
        Note over F,B: 客户端重连并携带 last_seq
        F->>B: Reconnect(session_id, last_seq)
        B->>RP: XRANGE responses:{session_id} from last_seq+1
        alt 主 Redis 故障
            B->>RB: 从备库读取并继续消费
        end
        B-->>F: 续传剩余数据
    end

    Note over RP,RB: Redis Sentinel/Cluster 负责主备切换与复制
```

## 通信通道说明
- 控制面（Backend ⇄ Infra）：建议使用 gRPC（或 HTTP+重试）
  - StartSession(session_id, last_seq, prompt, meta)
  - CancelSession(session_id)、Heartbeat(session_id)（可选）
- 数据面（Infra → Backend）：通过 Redis Streams（responses:{session_id}）进行结果传输；Backend 用消费组阻塞读取并推送给前端。

## 优势
1. **高可用性**：双Redis提供故障转移能力
2. **实时性**：WebSocket双向通信，心跳保活
3. **断点续传**：基于序列号从断点位置恢复传输
4. **数据完整性**：Streams + 消费组保证顺序与至少一次投递

## 断连处理策略
- **连接层**：WebSocket 自动重连 + 心跳检测
- **缓存/队列层**：Redis 主备切换，结果流不丢失
- **应用层**：基于 last_seq 的断点续传
- **降级策略**：LLM 服务不可用时，返回最新可用片段/缓存或提示稍后重试
