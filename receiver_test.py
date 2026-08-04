from rdt import RDT

rdt = RDT("127.0.0.1", 5000)
print("Receiver ready...")
rdt.receive_file_reliable("received.jpg")
rdt.close()