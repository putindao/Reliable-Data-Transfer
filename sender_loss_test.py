from rdt import RDT

# Sender giả lập mất 30% packet
rdt = RDT(
    "127.0.0.1",
    5001,
    loss_rate=0.3
)

print("Sender ready...")

rdt.send_file_reliable(
    "image.png",
    ("127.0.0.1", 5000)
)

rdt.close()