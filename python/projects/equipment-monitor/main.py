
import csv
from datetime import datetime
from pathlib import Path


# 日志文件保存在当前项目目录
LOG_FILE = Path("device_logs.csv")


def get_device_status():
    """获取并验证设备状态。"""

    status_map = {
        "1": "运行中",
        "2": "已停止",
        "3": "故障"
    }

    while True:
        print("\n请选择设备状态：")
        print("1. 运行中")
        print("2. 已停止")
        print("3. 故障")
        print("q. 结束记录")

        choice = input("请输入编号：").strip()

        if choice.lower() == "q":
            return None

        if choice in status_map:
            return status_map[choice]

        print("输入无效，请重新选择！")


def save_record(device_name, status):
    """将设备状态保存到CSV文件。"""

    file_exists = LOG_FILE.exists()
    need_header = not file_exists or LOG_FILE.stat().st_size == 0

    with LOG_FILE.open(
        "a",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        if need_header:
            writer.writerow([
                "设备名称",
                "设备状态",
                "记录时间"
            ])

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        writer.writerow([
            device_name,
            status,
            current_time
        ])

    print(f"记录已保存：{status}")


def main():
    print("================================")
    print("       设备运行状态监测系统")
    print("================================")

    device_name = input("请输入设备名称：").strip()

    if not device_name:
        print("设备名称不能为空！")
        return

    print(f"\n开始监测设备：{device_name}")

    while True:
        status = get_device_status()

        if status is None:
            break

        save_record(device_name, status)

    print("\n监测结束！")
    print(f"历史记录文件：{LOG_FILE.resolve()}")


if __name__ == "__main__":
    main()
