import scipy.integrate as spi  # 计算积分用

def calc_using_time(distance: float, is_uniform_speed: bool, speed_para: list) -> float:
    """
    根据给定的距离计算僵尸的行进时间（帧数），pvz中为cs。

    Args:
        distance: 行进的总距离（单位：像素）。
        is_uniform_speed: 是否为匀速运动，布尔值。
        speed_para: 速度参数范围，列表类型，假设是均匀分布的。

    Returns:
        所需要花费的期望时间（单位：帧），pvz中为cs。
    """
    # 1. 检测是否为匀速运动
    if is_uniform_speed:
        speed_para_min = min(speed_para)
        speed_para_max = max(speed_para)

        # 计算均匀分布情况下的时间期望值：
        # 期望计算公式：E[T] = ∫(distance / v) * f(v) dv，其中 f(v) = 1 / (b - a)
        _func = lambda v: (distance / v) * (1 / (speed_para_max - speed_para_min))

        # 使用数值积分计算期望时间
        expected_time, _ = spi.quad(func=_func, a=speed_para_min, b=speed_para_max)
        return expected_time
    else:
        # TODO: 处理非匀速运动情况
        pass


if __name__ == '__main__':
    # 测试1: 计算矿工僵尸在挖掘状态下的时间期望
    using_time = calc_using_time(distance=80, is_uniform_speed=True, speed_para=[0.66, 0.68])
    print(f"矿工僵尸挖掘状态所需时间期望值：{using_time:.2f} cs")
