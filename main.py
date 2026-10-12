from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Collection
from enum import Enum

class DeviceStatus(Enum):
    ACTIVE = 1
    UNDER_MAINTENANCE = 2
    RETIRED = 3


class INetworkable(ABC):
    @property
    @abstractmethod
    def ip_address(self) -> str:
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def connect(self, ip_address: str) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass


class Device(ABC):
    def __init__(self, device_id: str, name: str, purchase_year: int, purchase_price: float, status: DeviceStatus):
        if not device_id or not device_id.strip():
            raise ValueError("Mã thiết bị không được rỗng.")
        if purchase_price <= 0:
            raise ValueError("Giá mua phải lớn hơn 0.")
        current_year = datetime.now().year
        if purchase_year > current_year:
            raise ValueError("Năm đưa vào sử dụng không được lớn hơn năm hiện tại.")

        self._device_id = device_id
        self._name = name
        self._purchase_year = purchase_year
        self._purchase_price = purchase_price
        self._status = status

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def purchase_year(self) -> int:
        return self._purchase_year

    @purchase_year.setter
    def purchase_year(self, value: int):
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError("Năm đưa vào sử dụng không được lớn hơn năm hiện tại.")
        self._purchase_year = value

    @property
    def purchase_price(self) -> float:
        return self._purchase_price

    @purchase_price.setter
    def purchase_price(self, value: float):
        if value <= 0:
            raise ValueError("Giá mua phải lớn hơn 0.")
        self._purchase_price = value

    @property
    def status(self) -> DeviceStatus:
        return self._status

    @status.setter
    def status(self, value: DeviceStatus):
        self._status = value

    @abstractmethod
    def calculate_annual_maintenance_cost(self) -> float:
        pass

    def get_age(self) -> int:
        return datetime.now().year - self._purchase_year

    def __str__(self) -> str:
        return f"[Mã: {self._device_id}] | Tên: {self._name} | Năm SD: {self._purchase_year} | Giá: {self._purchase_price:,.0f} VNĐ | Trạng thái: {self._status.name}"




class Computer(Device, INetworkable):
    def __init__(self, device_id: str, name: str, purchase_year: int, purchase_price: float, status: DeviceStatus,
                 ram_capacity: int, processor_type: str, has_discrete_gpu: bool):
        super().__init__(device_id, name, purchase_year, purchase_price, status)
        self.ram_capacity = ram_capacity
        self.processor_type = processor_type or "Unknown"
        self.has_discrete_gpu = has_discrete_gpu
        
        self._ip_address = ""
        self._is_connected = False

    @property
    def ip_address(self) -> str:
        return self._ip_address

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def connect(self, ip_address: str) -> None:
        if not ip_address or not ip_address.strip():
            raise ValueError("Địa chỉ IP không được rỗng.")
        if self._is_connected:
            raise RuntimeError("Thiết bị đang được kết nối, không thể kết nối lại.")
        
        self._ip_address = ip_address
        self._is_connected = True

    def disconnect(self) -> None:
        self._is_connected = False
        self._ip_address = ""

    def calculate_annual_maintenance_cost(self) -> float:
        cost = self.purchase_price * 0.05
        if self.has_discrete_gpu:
            cost += self.purchase_price * 0.02
        if self.get_age() > 5:
            cost += self.purchase_price * 0.01
        return cost

    def __str__(self) -> str:
        net_info = f"Connected ({self._ip_address})" if self._is_connected else "Disconnected"
        return super().__str__() + f" | RAM: {self.ram_capacity}GB | CPU: {self.processor_type} | GPU rời: {self.has_discrete_gpu} | Mạng: {net_info}"


class Printer(Device):
    def __init__(self, device_id: str, name: str, purchase_year: int, purchase_price: float, status: DeviceStatus,
                 printer_type: str, printed_pages_count: int, is_color: bool):
        super().__init__(device_id, name, purchase_year, purchase_price, status)
        self.printer_type = printer_type or "Laser"
        self.printed_pages_count = printed_pages_count
        self.is_color = is_color

    def calculate_annual_maintenance_cost(self) -> float:
        cost = self.purchase_price * 0.04
        if self.printed_pages_count > 100_000:
            cost += 500_000
        if self.is_color:
            cost += 300_000
        return cost

    def __str__(self) -> str:
        return super().__str__() + f" | Loại: {self.printer_type} | Số trang: {self.printed_pages_count:,} | In màu: {self.is_color}"


class NetworkPrinter(Printer, INetworkable):
    def __init__(self, device_id: str, name: str, purchase_year: int, purchase_price: float, status: DeviceStatus,
                 printer_type: str, printed_pages_count: int, is_color: bool):
        super().__init__(device_id, name, purchase_year, purchase_price, status, printer_type, printed_pages_count, is_color)
        self._ip_address = ""
        self._is_connected = False

    @property
    def ip_address(self) -> str:
        return self._ip_address

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def connect(self, ip_address: str) -> None:
        if not ip_address or not ip_address.strip():
            raise ValueError("Địa chỉ IP không được rỗng.")
        if self._is_connected:
            raise RuntimeError("Thiết bị đang được kết nối, không thể kết nối lại.")
        
        self._ip_address = ip_address
        self._is_connected = True

    def disconnect(self) -> None:
        self._is_connected = False
        self._ip_address = ""

    def __str__(self) -> str:
        net_info = f"Connected ({self._ip_address})" if self._is_connected else "Disconnected"
        return super().__str__() + f" | Mạng: {net_info}"


class Projector(Device):
    def __init__(self, device_id: str, name: str, purchase_year: int, purchase_price: float, status: DeviceStatus,
                 brightness_lumen: int, lamp_used_hours: int):
        super().__init__(device_id, name, purchase_year, purchase_price, status)
        self.brightness_lumen = brightness_lumen
        self.lamp_used_hours = lamp_used_hours

    def calculate_annual_maintenance_cost(self) -> float:
        cost = self.purchase_price * 0.03
        if self.lamp_used_hours > 3000:
            cost += 1_500_000
        return cost

    def __str__(self) -> str:
        return super().__str__() + f" | Độ sáng: {self.brightness_lumen} lm | Số giờ đèn: {self.lamp_used_hours}h"


class LabRoom:
    def __init__(self, room_id: str, room_name: str, capacity: int):
        self.room_id = room_id
        self.room_name = room_name
        self.capacity = capacity
        self._devices: List[Device] = []

    @property
    def devices(self) -> Collection[Device]:
        return tuple(self._devices)

    def add_device(self, device: Device) -> None:
        if device is None:
            raise ValueError("Không chấp nhận đối tượng thiết bị null.")
        if any(d.device_id == device.device_id for d in self._devices):
            raise RuntimeError(f"Thiết bị có mã '{device.device_id}' đã tồn tại trong phòng {self.room_name}.")
        self._devices.append(device)

    def remove_device(self, device_id: str) -> bool:
        device = self.find_device(device_id)
        if device:
            self._devices.remove(device)
            return True
        return False

    def find_device(self, device_id: str) -> Optional[Device]:
        return next((d for d in self._devices if d.device_id == device_id), None)

    def calculate_annual_maintenance_cost(self) -> float:
        # Tính đa hình thông qua phương thức calculate_annual_maintenance_cost()
        return sum(device.calculate_annual_maintenance_cost() for device in self._devices)

    def get_devices_requiring_maintenance(self) -> List[Device]:
        return [d for d in self._devices if d.status == DeviceStatus.UNDER_MAINTENANCE or d.get_age() > 5]


if __name__ == "__main__":
    print("CHƯƠNG TRÌNH QUẢN LÝ THIẾT BỊ VÀ BẢO TRÌ PHÒNG THỰC HÀNH\n")

    try:
        pc1 = Computer("PC01", "Dell OptiPlex", 2023, 15_000_000, DeviceStatus.ACTIVE, 16, "Intel Core i5", False)
        pc2 = Computer("PC02", "ASUS ROG Gaming", 2019, 32_000_000, DeviceStatus.ACTIVE, 32, "Intel Core i7", True)
        printer1 = Printer("PR01", "HP LaserJet Pro", 2024, 4_000_000, DeviceStatus.ACTIVE, "Laser", 120_000, False)
        printer2 = NetworkPrinter("PR02", "Canon Pixma Network", 2025, 6_500_000, DeviceStatus.UNDER_MAINTENANCE, "Inkjet", 15_000, True)
        projector1 = Projector("PJ01", "Sony VPL Projector", 2022, 12_000_000, DeviceStatus.ACTIVE, 3500, 3500)
        lab_a = LabRoom("LAB101", "Phòng Thực hành Mạng máy tính", 30)
        lab_b = LabRoom("LAB102", "Phòng Đồ họa & Trí tuệ nhân tạo", 25)
        lab_a.add_device(pc1)
        lab_a.add_device(printer1)
        lab_a.add_device(printer2)
        lab_b.add_device(pc2)
        lab_b.add_device(projector1)

        print("--- Kiểm tra lỗi trùng mã thiết bị ---")
        try:
            duplicate_pc = Computer("PC01", "Duplicate PC", 2024, 10_000_000, DeviceStatus.ACTIVE, 8, "Intel i3", False)
            lab_a.add_device(duplicate_pc)
        except Exception as ex:
            print(f"[Bắt lỗi thành công]: {ex}\n")

        print(f"--- Danh sách thiết bị {lab_a.room_name} ---")
        for d in lab_a.devices:
            print(f"- {d}")
        print(f"=> Tổng chi phí bảo trì dự kiến: {lab_a.calculate_annual_maintenance_cost():,.0f} VNĐ\n")

        print(f"--- Danh sách thiết bị {lab_b.room_name} ---")
        for d in lab_b.devices:
            print(f"- {d}")
        print(f"=> Tổng chi phí bảo trì dự kiến: {lab_b.calculate_annual_maintenance_cost():,.0f} VNĐ\n")

        print("--- Danh sách thiết bị cần bảo trì ---")
        maintenance_list = list(lab_a.get_devices_requiring_maintenance()) + list(lab_b.get_devices_requiring_maintenance())
        for d in maintenance_list:
            reason = "Đang bảo trì" if d.status == DeviceStatus.UNDER_MAINTENANCE else "Sử dụng trên 5 năm"
            print(f"- Mã: {d.device_id} | Tên: {d.name} | Lý do: {reason}")
        print()

        print("--- Kiểm tra kết nối mạng qua INetworkable ---")
        network_devices: List[INetworkable] = [pc1, pc2, printer2]

        network_devices[0].connect("192.168.1.10")
        network_devices[1].connect("192.168.1.15")
        network_devices[2].connect("192.168.1.100")

        for net_device in network_devices:
            dev_obj = net_device
            print(f"- Thiết bị: {dev_obj.name} | IP: {net_device.ip_address} | Trạng thái kết nối: {net_device.is_connected}")

        print("\nThực hiện ngắt kết nối thiết bị PR02...")
        printer2.disconnect()
        print(f"- Trạng thái PR02 sau ngắt kết nối - is_connected: {printer2.is_connected}, ip_address: '{printer2.ip_address}'")

    except Exception as ex:
        print(f"Lỗi hệ thống: {ex}")