/*
 * WEEK 29 - JAVA ADVANCED TOPICS
 * Topic: Message Queues -- FIFO, Priority, Delayed, Pub/Sub
 * File: message_queues.java
 *
 * CONCEPT:
 *     Message queues decouple producers from consumers. The four canonical
 *     flavours:
 *       1. FIFO queue: ordered delivery. Backbone of Kafka partitions,
 *          SQS standard queues, RabbitMQ classic queues.
 *       2. Priority queue: messages have priorities; high-priority pulls
 *          first. Used by job schedulers.
 *       3. Delayed / scheduled queue: messages become visible after a
 *          delay. Used in retries, cron-like schedulers.
 *       4. Pub/Sub: a topic broadcasts each message to all subscribers.
 *          Used in event-driven architectures (Kafka, Redis Pub/Sub,
 *          Cloud PubSub).
 *
 * KEY POINTS:
 *     - At-least-once delivery requires acknowledgements + redelivery.
 *     - Visibility timeout (SQS) hides in-flight messages so two consumers
 *       can't process the same one.
 *     - Pub/Sub fans out to N subscribers; task queues fan in to 1.
 *
 * ALGORITHM / APPROACH:
 *     FIFO:     ArrayDeque, offer + poll.
 *     PRIORITY: PriorityQueue with composite key (priority desc, fifo asc).
 *     DELAYED:  PriorityQueue keyed by deliverAt timestamp.
 *     PUBSUB:   topic -> list of subscriber callbacks; iterate and deliver
 *               on publish.
 *
 * DRY RUN / EXAMPLE:
 *     Priority queue with messages (2,'low'), (1,'med'), (0,'high'):
 *         pop order -> 'high','med','low' when (priority desc) is enforced.
 *     Delayed queue: put('A', deliverIn=50ms). poll within 50ms returns
 *         null; after 50ms returns 'A'.
 *
 * COMPLEXITY:
 *     FIFO:     O(1).
 *     Priority: O(log n).
 *     Delayed:  O(log n).
 *     Pub/Sub:  O(subscribers) per publish.
 */

// snake_case filename is fine; class MessageQueues is package-private.

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Deque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.function.Consumer;
import java.util.concurrent.atomic.AtomicLong;

class MessageQueues {

    // -----------------------------------------------------------------------
    // FIFO Queue
    // -----------------------------------------------------------------------
    static class FIFOQueue<T> {
        final Deque<T> q = new ArrayDeque<>();
        void put(T msg) { q.offerLast(msg); }
        T get() { return q.pollFirst(); }
        int size() { return q.size(); }
    }

    // -----------------------------------------------------------------------
    // Priority Queue (highest numeric priority first; ties by FIFO)
    // -----------------------------------------------------------------------
    static class PriorityMQ<T> {
        static class Entry<T> {
            final int priority;
            final long tie;
            final T msg;
            Entry(int p, long t, T m) { priority = p; tie = t; msg = m; }
        }

        final PriorityQueue<Entry<T>> heap = new PriorityQueue<>(
            Comparator.<Entry<T>>comparingInt((Entry<T> e) -> -e.priority)
                      .thenComparingLong(e -> e.tie));
        final AtomicLong counter = new AtomicLong();

        void put(T msg, int priority) {
            heap.offer(new Entry<>(priority, counter.getAndIncrement(), msg));
        }
        T get() { Entry<T> e = heap.poll(); return e == null ? null : e.msg; }
        int size() { return heap.size(); }
    }

    // -----------------------------------------------------------------------
    // Delayed Queue
    // -----------------------------------------------------------------------
    static class DelayedQueue<T> {
        static class Entry<T> {
            final long deliverAtNanos;
            final long tie;
            final T msg;
            Entry(long t, long s, T m) { deliverAtNanos = t; tie = s; msg = m; }
        }

        final PriorityQueue<Entry<T>> heap = new PriorityQueue<>(
            Comparator.<Entry<T>>comparingLong((Entry<T> e) -> e.deliverAtNanos)
                      .thenComparingLong(e -> e.tie));
        final AtomicLong counter = new AtomicLong();

        void put(T msg, double deliverInSeconds) {
            long at = System.nanoTime() + (long)(deliverInSeconds * 1_000_000_000L);
            heap.offer(new Entry<>(at, counter.getAndIncrement(), msg));
        }

        T poll() {
            Entry<T> top = heap.peek();
            if (top == null) return null;
            if (top.deliverAtNanos <= System.nanoTime()) return heap.poll().msg;
            return null;
        }
    }

    // -----------------------------------------------------------------------
    // Pub/Sub Broker
    // -----------------------------------------------------------------------
    static class PubSubBroker {
        final Map<String, List<Consumer<Object>>> topics = new HashMap<>();
        void subscribe(String topic, Consumer<Object> handler) {
            topics.computeIfAbsent(topic, k -> new ArrayList<>()).add(handler);
        }
        void publish(String topic, Object message) {
            List<Consumer<Object>> subs = topics.get(topic);
            if (subs != null) for (Consumer<Object> h : subs) h.accept(message);
        }
    }

    public static void main(String[] args) throws InterruptedException {
        FIFOQueue<String> fifo = new FIFOQueue<>();
        for (String m : new String[]{"a", "b", "c"}) fifo.put(m);
        System.out.print("FIFO drain:");
        for (int i = 0; i < 3; i++) System.out.print(" " + fifo.get());
        System.out.println();

        PriorityMQ<String> pq = new PriorityMQ<>();
        pq.put("low", 0); pq.put("med", 1); pq.put("high", 2);
        System.out.print("Priority drain:");
        for (int i = 0; i < 3; i++) System.out.print(" " + pq.get());
        System.out.println();

        DelayedQueue<String> dq = new DelayedQueue<>();
        dq.put("future-A", 0.05);
        System.out.println("Delayed poll now:   " + dq.poll() + "   (expected null)");
        Thread.sleep(60);
        System.out.println("Delayed poll later: " + dq.poll() + "   (expected future-A)");

        PubSubBroker broker = new PubSubBroker();
        List<String> output = new ArrayList<>();
        broker.subscribe("orders", msg -> output.add("sub1<-" + msg));
        broker.subscribe("orders", msg -> output.add("sub2<-" + msg));
        broker.publish("orders", "ORD#42");
        System.out.println("Pub/Sub delivered: " + output);
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in message_queues.py:
 *   - Java's PriorityQueue is a min-heap of Comparable; we use a custom
 *     Comparator and a tie-breaker counter to mimic heapq + itertools.count.
 *   - System.nanoTime() / 1e9 stands in for time.monotonic().
 *   - Pub/Sub uses java.util.function.Consumer<Object> as the handler type.
 *   - The companion system_design.java does NOT cover message queues; this
 *     file fills the gap to match the Python / C++ / Rust splits.
 */
