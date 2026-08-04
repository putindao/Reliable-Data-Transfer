from rdt import RDT

# Receiver KHÔNG drop packet
rdt = RDT(
    "127.0.0.1",
    5000,
    loss_rate=0.0
)

print("Receiver ready...")

rdt.receive_file_reliable("received_loss.txt")

rdt.close()