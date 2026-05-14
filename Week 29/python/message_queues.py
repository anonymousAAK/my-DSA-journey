"""
WEEK 29 - PYTHON ADVANCED TOPICS
Topic: Message Queues - FIFO, Priority, Delayed, Pub/Sub
File: message_queues.py

CONCEPT:
    Message queues decouple producers from consumers. The four canonical
    flavours:
      1. FIFO queue: ordered delivery (single-consumer). Backbone of
         Kafka partitions, SQS standard queues, RabbitMQ classic queues.
      2. Priority queue: messages have priorities; high-priority pulls
         first. Used for job schedulers.
      3. Delayed / scheduled queue: messages become visible after a
         delay. Used in retries, cron-like schedulers.
      4. Pub/Sub: a topic broadcasts each message to all subscribers.
         Used in event-driven architectures (Kafka, Redis Pub/Sub,
         Cloud PubSub).

KEY POINTS:
    - At-least-once delivery requires acknowledgements + redelivery.
    - Visibility timeout (SQS) hides in-flight messages so two consumers
      can't process the same one.
    - Pub/Sub fans out to N subscribers; tasks queues fan in to 1.

ALGORITHM / APPROACH:
    FIFO:   collections.deque, popleft + append.
    PRIORITY:   heapq (min-heap on priority; negate for max).
    DELAYED:    heapq on (deliver_at_timestamp, message).
    PUBSUB:     publisher -> list of subscriber callbacks; iterate and
                deliver to each.

PYTHON-SPECIFIC NOTES:
    - heapq treats the smallest element as the highest priority — be sure
      to negate if you want highest numeric priority first.
    - asyncio could turn this into a real async queue; we use the
      synchronous primitives for clarity.

DRY RUN / EXAMPLE:
    Priority queue with messages [(2,'low'),(1,'med'),(0,'high')]:
        pop order -> 'high','med','low'.
    Delayed queue: put('A', deliver_in=0.05). poll within 50 ms returns
        None; after 50 ms returns 'A'.

COMPLEXITY:
    FIFO:        O(1) per op
    Priority:    O(log n) per op
    Delayed:     O(log n) per op
    Pub/Sub:     O(subscribers) per publish
"""

from __future__ import annotations

import heapq
import time
import itertools
from collections import deque
from typing import Any, Callable, Deque, List, Optional


# ---------------------------------------------------------------------------
# FIFO Queue
# ---------------------------------------------------------------------------
class FIFOQueue:
    def __init__(self) -> None:
        self.q: Deque[Any] = deque()

    def put(self, msg: Any) -> None:
        self.q.append(msg)

    def get(self) -> Optional[Any]:
        return self.q.popleft() if self.q else None

    def __len__(self) -> int:
        return len(self.q)


# ---------------------------------------------------------------------------
# Priority Queue (highest priority first; ties by FIFO via counter)
# ---------------------------------------------------------------------------
class PriorityQueue:
    def __init__(self) -> None:
        self._heap: List[tuple] = []
        self._tie = itertools.count()

    def put(self, msg: Any, priority: int) -> None:
        heapq.heappush(self._heap, (-priority, next(self._tie), msg))

    def get(self) -> Optional[Any]:
        return heapq.heappop(self._heap)[2] if self._heap else None

    def __len__(self) -> int:
        return len(self._heap)


# ---------------------------------------------------------------------------
# Delayed Queue
# ---------------------------------------------------------------------------
class DelayedQueue:
    def __init__(self) -> None:
        self._heap: List[tuple] = []
        self._tie = itertools.count()

    def put(self, msg: Any, deliver_in: float) -> None:
        heapq.heappush(self._heap,
                       (time.monotonic() + deliver_in, next(self._tie), msg))

    def poll(self) -> Optional[Any]:
        if not self._heap:
            return None
        if self._heap[0][0] <= time.monotonic():
            return heapq.heappop(self._heap)[2]
        return None


# ---------------------------------------------------------------------------
# Pub/Sub Broker
# ---------------------------------------------------------------------------
class PubSubBroker:
    def __init__(self) -> None:
        self._topics: dict[str, list[Callable[[Any], None]]] = {}

    def subscribe(self, topic: str, handler: Callable[[Any], None]) -> None:
        self._topics.setdefault(topic, []).append(handler)

    def publish(self, topic: str, message: Any) -> None:
        for h in self._topics.get(topic, []):
            h(message)


def _demo() -> None:
    fifo = FIFOQueue()
    for m in ["a", "b", "c"]:
        fifo.put(m)
    print(f"FIFO drain: {[fifo.get() for _ in range(3)]}")

    pq = PriorityQueue()
    pq.put("low", 0); pq.put("med", 1); pq.put("high", 2)
    print(f"Priority drain: {[pq.get() for _ in range(3)]}")

    dq = DelayedQueue()
    dq.put("future-A", deliver_in=0.05)
    print(f"Delayed poll now: {dq.poll()}  (expected None)")
    time.sleep(0.06)
    print(f"Delayed poll later: {dq.poll()}  (expected 'future-A')")

    broker = PubSubBroker()
    output: list[str] = []
    broker.subscribe("orders", lambda msg: output.append(f"sub1<-{msg}"))
    broker.subscribe("orders", lambda msg: output.append(f"sub2<-{msg}"))
    broker.publish("orders", "ORD#42")
    print(f"Pub/Sub delivered: {output}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Java's system_design.java doesn't cover message queues; we add
#     four flavours for spec completeness.
#   * `itertools.count()` provides a monotonic tie-breaker for stable
#     heap ordering (avoids comparing unhashable payloads).
#   * Pub/Sub is callback-based; in real systems it would push to subscriber
#     queues + use ack channels.
