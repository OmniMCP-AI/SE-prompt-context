# 方案 2：双Redis缓存 + WebSocket心跳方案

## 架构特点
- 主备双Redis提供高可用性
- WebSocket替代SSE，支持双向通信和心跳
- 断点续传机制

```mermaid
sequenceDiagram
    participant F as Frontend
    participant B as Backend
    participant RP as Redis Primary
    participant RB as Redis Backup
    participant IS as Infrastructure Service
    participant LLM as LLM Service
    
    F->>B: 建立 WebSocket 连接
    loop 心跳检测
        F->>B: ping
        B->>F: pong
    end
    
    B->>RP: 写入请求（带序列号）
    B->>RB: 同步备份
    B->>IS: 发起请求（带断点信息）
    IS->>RP: 检查断点位置
    IS->>LLM: 调用 LLM stream
    
    alt 正常流程
        LLM-->>IS: 流式返回
        IS->>RP: 实时写入结果片段
        IS->>RB: 异步同步
        IS-->>B: 推送结果
        B-->>F: WebSocket 推送
    else 断连恢复
        Note over F,B: 检测到断连
        F->>B: 重连带上最后序列号
        B->>RP: 查询断点数据
        alt 主Redis故障
            B->>RB: 从备份读取
        end
        B-->>F: 续传剩余数据
    end
    
    Note over RP,RB: Redis Sentinel 自动故障转移
```

## 优势
1. **高可用性**：双Redis提供故障转移能力
2. **实时性**：WebSocket双向通信，心跳保活
3. **断点续传**：支持从断点位置恢复传输
4. **数据完整性**：序列号机制保证数据顺序和完整性

## 断连处理策略
- **连接层**：WebSocket自动重连，心跳检测
- **缓存层**：主备自动切换，数据不丢失
- **应用层**：基于序列号的断点续传
- **降级策略**：LLM服务不可用时返回缓存结果
