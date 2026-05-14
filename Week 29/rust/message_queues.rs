// WEEK 29 - RUST ADVANCED TOPICS
// Topic: Message Queues - FIFO, Priority, Delayed, Pub/Sub
// File: message_queues.rs
//
// CONCEPT:
//   Decouple producers from consumers. Four flavours:
//     - FIFO: ordered consumption (VecDeque).
//     - PRIORITY: high priority first (BinaryHeap).
//     - DELAYED: messages visible after a deadline (BinaryHeap).
//     - PUB/SUB: one publish, many subscribers.
//
// KEY POINTS:
//   - At-least-once delivery requires acks + redelivery.
//   - Visibility timeout hides in-flight messages from other consumers.
//
// ALGORITHM / APPROACH:
//   PRIORITY: BinaryHeap is max-heap; push (priority, tie, msg).
//   DELAYED:  use std::cmp::Reverse((deadline, tie, msg)) for a min-heap.
//   PUBSUB:   broker -> topic -> Vec<Box<dyn Fn(...)>>; iterate.
//
// RUST-SPECIFIC NOTES:
//   - BinaryHeap is max-heap. Use std::cmp::Reverse for min-heap.
//   - Box<dyn Fn(&str)> stores subscriber callbacks.
//
// DRY RUN / EXAMPLE:
//   Priority pushes (0,'low'),(1,'med'),(2,'high') -> pop high,med,low.
//   Delayed put('A', 50 ms); poll now -> None; sleep 60 ms; poll -> 'A'.
//
// COMPLEXITY:
//   FIFO O(1); Priority/Delayed O(log n); Pub/Sub O(subs/publish).

use std::collections::{BinaryHeap, HashMap, VecDeque};
use std::cmp::Reverse;
use std::thread;
use std::time::{Duration, Instant};

pub struct FIFOQueue<T> { q: VecDeque<T> }
impl<T> FIFOQueue<T> {
    pub fn new() -> Self { Self { q: VecDeque::new() } }
    pub fn put(&mut self, m: T) { self.q.push_back(m); }
    pub fn get(&mut self) -> Option<T> { self.q.pop_front() }
    pub fn len(&self) -> usize { self.q.len() }
}

pub struct PriorityQueueMQ {
    tie: u64,
    h: BinaryHeap<(i32, i64, String)>, // (priority, -tie, msg)
}
impl PriorityQueueMQ {
    pub fn new() -> Self { Self { tie: 0, h: BinaryHeap::new() } }
    pub fn put(&mut self, msg: &str, priority: i32) {
        self.tie += 1;
        // negate tie so earlier inserts win on ties (max-heap on -tie -> smaller tie wins)
        self.h.push((priority, -(self.tie as i64), msg.to_string()));
    }
    pub fn get(&mut self) -> Option<String> { self.h.pop().map(|(_, _, m)| m) }
}

pub struct DelayedQueue {
    tie: u64,
    h: BinaryHeap<Reverse<(Instant, u64, String)>>,
}
impl DelayedQueue {
    pub fn new() -> Self { Self { tie: 0, h: BinaryHeap::new() } }
    pub fn put(&mut self, msg: &str, deliver_in: Duration) {
        self.tie += 1;
        self.h.push(Reverse((Instant::now() + deliver_in, self.tie, msg.to_string())));
    }
    pub fn poll(&mut self) -> Option<String> {
        if let Some(Reverse((dl, _, _))) = self.h.peek() {
            if *dl <= Instant::now() {
                return self.h.pop().map(|Reverse((_, _, m))| m);
            }
        }
        None
    }
}

pub struct PubSubBroker {
    topics: HashMap<String, Vec<Box<dyn Fn(&str)>>>,
}
impl PubSubBroker {
    pub fn new() -> Self { Self { topics: HashMap::new() } }
    pub fn subscribe<F: Fn(&str) + 'static>(&mut self, topic: &str, cb: F) {
        self.topics.entry(topic.to_string()).or_default().push(Box::new(cb));
    }
    pub fn publish(&self, topic: &str, msg: &str) {
        if let Some(list) = self.topics.get(topic) {
            for cb in list { cb(msg); }
        }
    }
}

fn main() {
    let mut fifo: FIFOQueue<&str> = FIFOQueue::new();
    for m in ["a","b","c"] { fifo.put(m); }
    print!("FIFO drain:");
    while let Some(m) = fifo.get() { print!(" {}", m); }
    println!();

    let mut pq = PriorityQueueMQ::new();
    pq.put("low", 0); pq.put("med", 1); pq.put("high", 2);
    print!("Priority drain:");
    while let Some(m) = pq.get() { print!(" {}", m); }
    println!();

    let mut dq = DelayedQueue::new();
    dq.put("future-A", Duration::from_millis(50));
    println!("Delayed poll now: {:?}", dq.poll());
    thread::sleep(Duration::from_millis(60));
    println!("Delayed poll later: {:?}", dq.poll());

    let mut broker = PubSubBroker::new();
    use std::sync::Mutex;
    use std::sync::Arc;
    let log: Arc<Mutex<Vec<String>>> = Arc::new(Mutex::new(Vec::new()));
    let log1 = Arc::clone(&log);
    let log2 = Arc::clone(&log);
    broker.subscribe("orders", move |m| log1.lock().unwrap().push(format!("sub1<-{}", m)));
    broker.subscribe("orders", move |m| log2.lock().unwrap().push(format!("sub2<-{}", m)));
    broker.publish("orders", "ORD#42");
    println!("Pub/Sub delivered: {:?}", log.lock().unwrap());
}

// NOTES
// -----
// Differences from Java:
//   * BinaryHeap is max-heap; std::cmp::Reverse wraps for min-heap.
//   * Pub/Sub callbacks use Box<dyn Fn(&str)>; we share state via Arc<Mutex>
//     because the closures must be 'static.
