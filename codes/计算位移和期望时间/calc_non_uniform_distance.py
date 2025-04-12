import numpy as np

# 非匀速僵尸运动片段移动量表
non_uniform_zombie_movents = {
    "tie_zombie": {
        "speed_para": [0.23, 0.37],
        "segment_movement": [1.3, 1.2, 1.3, 1.3, 1.3, 1.3, 1.2, 1.2, 1.3, 1.2,
                             1.3, 1.3, 1.3, 1.3, 1.2, 1.3, 0.1, 0.1, 0.0, 0.1,
                             0.0, 0.1, 0.1, 1.8, 1.7, 1.8, 1.8, 1.8, 1.7, 1.8,
                             1.8, 1.8, 1.8, 1.7, 1.8, 1.7, 1.9, 1.7, 1.8, 0.1,
                             0.0, 0.1, 0.2, 0.1, 0.0, 0.1],
        "total_movement": 49.8
    },
    "ladder_zombie": {  # 扶梯僵尸（有梯）
        "speed_para": [0.79, 0.81],
        "segment_movement": [
            0.8, 0.9, 0.8, 0.8, 2.9, 2.9, 2.8, 2.9, 3.9, 3.9,
            4.0, 3.9, 3.9, 0.8, 0.7, 0.8, 0.7, 0.8, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.8, 1.0, 0.9, 0.9, 2.2, 2.1, 2.3,
            2.1, 2.2, 2.0, 2.1, 2.1, 2.1, 2.0, 0.5, 0.5, 0.4,
            0.5, 0.0, 0.0, 0.0, 0.0, 0.0
        ],
        "total_movement": 65.9
    }
}


def calc_non_uniform_displacement(zombie_type: str, cs: int, speed: float) -> float:
    """
    计算非匀速僵尸在 cs 帧后的位移。

    Args:
        zombie_type: 僵尸类型 ("tie_zombie" 或 "ladder_zombie")
        cs: 计算到第 cs 帧
        speed: 僵尸的速度参数

    Returns:
        该帧的位移量
    """
    # 读取僵尸数据
    zombie_data = non_uniform_zombie_movents.get(zombie_type)
    if not zombie_data:
        raise ValueError("未知的僵尸类型")

    segment_movements = zombie_data["segment_movement"]
    total_movement = zombie_data["total_movement"]
    total_segments = len(segment_movements)

    # 1. 计算 动画进度Δ, Δ = 速度参数 * 47 * 0.01 / 所有运动片段移动量总和
    # 僵尸出生的那一帧，动画进度初始化为Δ，之后每cs加Δ，若超过1则减去1。
    delta = (speed * 47 * 0.01) / total_movement  # Δ = speed * 47 * 0.01 / 总位移
    # 2. 计算当前运动片段, int(动画进度 * 运动片段总数 + 1)
    # PS：僵尸进行【啃食】、【投掷】、【举锤】动作时，行走动画进度会被重置，这也就是常说的“相位重置”。这些动作执行完毕后，动画进度会重新从Δ开始。
    current_segment = int(delta * total_segments * cs + 1)  # int(Δ * 片段数 * cs + 1)
    # 运动片段范围修正
    current_segment = min(current_segment, total_segments)  # 片段不能超出范围

    # 3. 查表获取运动片段的移动量
    move_amount = segment_movements[current_segment - 1]  # 列表索引从 0 开始
    # 4. 计算最终位移
    displacement = speed * 47 * 0.01 * move_amount * (total_segments + 1) / total_movement

    return displacement


if __name__ == '__main__':
    cs = 100
    speed = 0.80
    displacement = calc_non_uniform_displacement("ladder_zombie", cs, speed)
    print(f"速度 {speed:.2f} 的扶梯僵尸在 {cs}cs 时的位移：{displacement:.4f} px")
