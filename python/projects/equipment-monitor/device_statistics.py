import csv
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("device_logs.csv")


def calculate_statistics():
    if not LOG_FILE.exists():
        print("没有找到设备记录文件。")
        return

    records = []

    with LOG_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            records.append(row)

    if len(records) < 2:
        print("记录数量不足，暂时无法统计持续时间。")
        return

    running_seconds = 0
    stopped_seconds = 0
    fault_count = 0

    for i in range(len(records) - 1):
        current = records[i]
        next_record = records[i + 1]

        start_time = datetime.strptime(
            current["记录时间"], "%Y-%m-%d %H:%M:%S"
        )

        end_time = datetime.strptime(
            next_record["记录时间"], "%Y-%m-%d %H:%M:%S"
        )

        duration = (end_time - start_time).total_seconds()

        status = current["设备状态"]

        if status == "运行中":
            running_seconds += duration

        elif status == "已停止":
            stopped_seconds += duration

    for record in records:
        if record["设备状态"] == "故障":
            fault_count += 1

    print("\n====== 设备统计报告 ======")
    print(f"设备名称：{records[0]['设备名称']}")
    print(f"累计运行时间：{running_seconds} 秒")
    print(f"累计停止时间：{stopped_seconds} 秒")
    print(f"故障次数：{fault_count}")
    print("==========================")


if __name__ == "__main__":
    calculate_statistics()