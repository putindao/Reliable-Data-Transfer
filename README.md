# Reliable Data Transfer (RDT) Module

## Giới thiệu

Đây là module **Reliable Data Transfer (RDT)** được xây dựng bằng Python trên nền giao thức UDP.

Module sử dụng cơ chế **Stop-and-Wait ARQ** nhằm đảm bảo dữ liệu được truyền chính xác và đầy đủ giữa Sender và Receiver.

---

## Chức năng

- Packet Serialization / Deserialization
- Checksum Verification
- Stop-and-Wait ARQ
- ACK Packet
- Timeout Detection
- Retransmission
- Duplicate Packet Detection
- Reliable File Transfer
- Packet Loss Simulation
- Binary File Transfer
- File Hash Verification (SHA256 / MD5)

---

## Cấu trúc thư mục

```
project/
│
├── packet.py
├── checksum.py
├── rdt.py
├── hash.py
│
├── sender_test.py
├── receiver_test.py
│
├── sender_loss_test.py
├── receiver_loss_test.py
│
├── hash_test.py
│
├── sample.txt
├── image.jpg
└── README.md
```

---

## Cấu trúc Packet

Packet gồm hai phần:

### Header

| Trường | Kích thước |
|---------|-----------:|
| Checksum | 2 bytes |
| Packet Type | 1 byte |
| Sequence Number | 1 byte |
| Data Length | 2 bytes |

### Data

```
+-----------+-----------+
|  Header   |   Data    |
+-----------+-----------+
```

---

## Stop-and-Wait ARQ

### Sender

```
Read File
    │
    ▼
Create DATA Packet
    │
    ▼
Send Packet
    │
    ▼
Wait ACK
    │
 ┌──┴──┐
 │     │
ACK  Timeout
 │     │
 ▼     ▼
Next  Retransmit
```

### Receiver

```
Receive Packet
      │
      ▼
Verify Checksum
      │
 ┌────┴────┐
 │         │
Valid   Invalid
 │         │
 ▼         ▼
Send ACK Discard
 │
 ▼
Write File
```

---

## Cách sử dụng

### Khởi tạo

```python
from rdt import RDT

rdt = RDT(
    "127.0.0.1",
    5000
)
```

---

### Gửi file

```python
rdt.send_file_reliable(
    "sample.txt",
    ("127.0.0.1", 5001)
)
```

---

### Nhận file

```python
rdt.receive_file_reliable(
    "received.txt"
)
```

---

## Packet Loss Simulation

Có thể mô phỏng mất gói bằng tham số `loss_rate`.

Ví dụ:

```python
rdt = RDT(
    "127.0.0.1",
    5000,
    loss_rate=0.3
)
```

Ý nghĩa:

| loss_rate | Mô tả |
|----------:|------|
| 0.0 | Không mất gói |
| 0.1 | Mất khoảng 10% DATA Packet |
| 0.3 | Mất khoảng 30% DATA Packet |
| 0.5 | Mất khoảng 50% DATA Packet |

Ví dụ log:

```
[SEND] DATA seq=0
[DROP] DATA seq=0
[TIMEOUT] Không nhận được ACK
[RETRANSMIT] Gửi lại packet...
[SEND] DATA seq=0
[RECV] ACK seq=0
```

---

## Kiểm tra Hash

Module hỗ trợ tính hash của file.

```python
from hash import calculate_file_hash

hash_value = calculate_file_hash("image.jpg")

print(hash_value)
```

Có thể sử dụng:

```python
calculate_file_hash("image.jpg")
```

hoặc

```python
calculate_file_hash("image.jpg", "md5")
```

---

## Kiểm thử

Đã kiểm thử thành công với:

- File văn bản (.txt)
- File ảnh (.jpg)
- Packet Loss Simulation
- Retransmission
- Timeout
- Binary File Transfer

Kết quả:

- File nhận được giống hoàn toàn file gốc.
- Giá trị SHA256 của hai file trùng khớp.
- Stop-and-Wait hoạt động đúng trong điều kiện mất gói.

---

## Thành viên thực hiện

**Đào Nhật Tân**

Phụ trách:

- Packet
- Checksum
- Reliable Data Transfer (RDT)
- File Transfer
- Packet Loss Simulation
- File Hash Verification