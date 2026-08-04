import socket
import random
from packet import Packet


class RDT:
    """
    Reliable Data Transfer (Stop-and-Wait ARQ)
    """

    def __init__(self, local_ip: str, local_port: int, timeout: float = 2.0, loss_rate: float = 0.0):
        """
        local_ip    : IP của máy hiện tại
        local_port  : Port lắng nghe
        timeout     : Thời gian chờ ACK
        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sock.bind((local_ip, local_port))

        self.timeout = timeout

        self.loss_rate = loss_rate

        # Sequence number của sender
        self.seq = 0

        # Sequence number receiver mong đợi
        self.expected_seq = 0


    def close(self):
        self.sock.close()


    def _send_packet(self, packet: Packet, dest_addr):
        """
        Gửi một Packet qua UDP.
        Có thể giả lập mất gói (packet loss).

        Returns
        -------
        bool
            True nếu packet được gửi.
            False nếu packet bị drop.
        """

        # Chỉ giả lập mất DATA packet
        if (
            packet.packet_type == Packet.DATA
            and random.random() < self.loss_rate
        ):
            print(f"[DROP] DATA seq={packet.seq}")
            return False

        raw_data = packet.to_bytes()

        self.sock.sendto(raw_data, dest_addr)

        return True


    def _receive_packet(self):
        """
        Nhận một Packet từ UDP.

        Returns
        -------
        (Packet, address)
        """
        while True:
            raw_data, addr = self.sock.recvfrom(2048)

            try:
                packet = Packet.from_bytes(raw_data)
                return packet, addr
            except ValueError:
                print("[ERROR] Invalid checksum. Packet discarded.")

    def _wait_ack(self):

        """
        Chờ ACK trong khoảng thời gian timeout.
        """

        self.sock.settimeout(self.timeout)

        try:

            raw_data, _ = self.sock.recvfrom(2048)

            ack = Packet.from_bytes(raw_data)

            return ack

        except socket.timeout:
            return None

        finally:

            # Trả socket về blocking mode
            self.sock.settimeout(None)


    def _send_ack(self, seq, dest_addr):
        """
        Gửi ACK packet.
        """

        ack = Packet(
            packet_type=Packet.ACK,
            seq=seq
        )

        self._send_packet(ack, dest_addr)

        print(f"[SEND] ACK seq={seq}")


    def send(self, data: bytes, dest_addr):
        """
        Gửi dữ liệu theo giao thức Stop-and-Wait ARQ.

        Parameters
        ----------
        data : bytes
            Dữ liệu cần gửi.

        dest_addr : tuple
            (ip, port) của máy nhận.
        """

        # Tạo DATA packet
        packet = Packet(
            packet_type=Packet.DATA,
            seq=self.seq,
            data=data
        )

        while True:

            # Gửi packet
            # Gửi packet
            sent = self._send_packet(packet, dest_addr)

            if sent:
                print(f"[SEND] DATA seq={self.seq}")

            # Chờ ACK
            ack = self._wait_ack()

            # Timeout
            if ack is None:
                print("[TIMEOUT] Không nhận được ACK")
                print("[RETRANSMIT] Gửi lại packet...")
                continue

            # ACK hợp lệ
            if (
                ack.packet_type == Packet.ACK
                and ack.seq == self.seq
            ):

                print(f"[RECV] ACK seq={ack.seq}")

                # Đổi sequence number
                self.seq ^= 1

                return True

            # ACK sai
            print("[WARN] ACK không hợp lệ")

    def send_file_reliable(self, file_path: str, dest_addr, chunk_size: int = 1024):
        """
        Gửi một file bằng giao thức Stop-and-Wait.

        Parameters
        ----------
        file_path : str
            Đường dẫn file cần gửi.

        dest_addr : tuple
            (ip, port) của receiver.

        chunk_size : int
            Kích thước mỗi gói dữ liệu.
        """

        with open(file_path, "rb") as f:

            while True:

                chunk = f.read(chunk_size)

                # Hết file
                if not chunk:
                    break

                self.send(chunk, dest_addr)

        # Gửi packet rỗng để báo kết thúc file
        self.send(b"", dest_addr)

        print("[INFO] File sent successfully.")

                

    def recv(self):
        """
        Nhận DATA packet theo Stop-and-Wait.
        """

        while True:

            packet, addr = self._receive_packet()

            if packet.packet_type != Packet.DATA:
                continue

            print(f"[RECV] DATA seq={packet.seq}")

            # Packet đúng
            if packet.seq == self.expected_seq:

                self._send_ack(
                    self.expected_seq,
                    addr
                )

                self.expected_seq ^= 1

                return packet.data, addr

            # Packet bị gửi lại
            else:

                print("[INFO] Duplicate packet")

                self._send_ack(
                    self.expected_seq ^ 1,
                    addr
                )

    def receive_file_reliable(self, output_path: str):
        """
        Nhận file bằng giao thức Stop-and-Wait.

        Parameters
        ----------
        output_path : str
            Đường dẫn lưu file nhận được.
        """

        with open(output_path, "wb") as f:

            while True:

                data, addr = self.recv()

                # EOF
                if data == b"":
                    break

                f.write(data)

        print("[INFO] File received successfully.")