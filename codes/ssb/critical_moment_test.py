from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager


def run_test(ctler: Controller, moment: int, n: int = 1000) -> float:
    """运行一次测试，返回成功率"""
    iz_test = IzTest(ctler).init_by_str(f'''
        {n} -1
        1-0
        2bllb
        .....
        .....
        .....
        .....
        cg ft
        0 {moment}
        1-1 1-6''')

    succ_time = 0  # 记录成功测试的总用时
    game_res = False  # 记录每次测试是否成功

    @iz_test.on_game_end()
    def _(res: bool):  # 每次结束修改外部变量 game_res
        nonlocal game_res
        game_res = res

    @iz_test.flow_factory.add_destructor()
    def _(fm: FlowManager):  # destructor在测试结束的下一cs调用，因此真正总用时需要减去1cs
        nonlocal succ_time, game_res
        if game_res:
            succ_time += fm.time - 1 - 1

    iz_test.start_test(jump_frame=1, print_interval=100)  # 跳帧且每100次打印

    success_rate = iz_test._success_count / n  # 计算成功率
    aver_succ = succ_time / iz_test._success_count if iz_test._success_count != 0 else -1  # 单位cs
    print(
        f"时机={moment}cs, 测试{n}次, 成功{iz_test._success_count}次, 成功率{success_rate * 100:.2f}%, 成功平均用时{aver_succ / 100:.2f}s")

    return success_rate


def binary_search(ctler: Controller, low: int, high: int, min_success_rate: float, test_n: int = 100) -> int:
    """二分法寻找突变时机"""
    result = -1  # 记录突变时机
    while low <= high:
        mid = (low + high) // 2  # 取中间时机
        success_rate = run_test(ctler, mid, test_n)

        if success_rate == -1:  # 如果测试失败，直接跳过
            break

        if success_rate >= min_success_rate:
            high = mid - 1  # 如果成功率高，尝试更晚的时机
        else:
            result = mid  # 记录当前突变时机
            low = mid + 1  # 尝试更早的时机

    return result


def test_around_moment(ctler: Controller, moment: int, range_cs: int = 20, test_n: int = 100):
    """测试突变时机周围的数据，并按照规则打印"""
    result_records = []
    for m in range(moment - range_cs, moment + range_cs + 1):
        # 在突变时机附近增加测试样本量
        current_test_n = 1000 if abs(m - moment) <= 5 else test_n  # 如果距离突变时机 <= 5cs，测试样本量为1000
        success_rate = run_test(ctler, m, current_test_n)

        result_records.append((m, success_rate))

    # 打印结果表格
    print("\n时机(cs)\t成功率(%)")

    # 找到最早和最晚的100%时机
    first_100_index = -1
    last_100_index = -1
    for i, (moment, rate) in enumerate(result_records):
        if rate == 1.0:
            if first_100_index == -1:
                first_100_index = i
            last_100_index = i

    if first_100_index != -1 and last_100_index != -1:
        # 打印最早100%时机及其前一个时机
        for i in range(max(0, first_100_index - 1), first_100_index + 1):
            moment, rate = result_records[i]
            print(f"{moment}\t{rate * 100:.2f}%")

        # 如果最早和最晚100%时机之间有间隔，打印...
        if last_100_index > first_100_index + 1:
            print("...")

        # 打印最晚100%时机及其后两个时机
        for i in range(last_100_index, min(last_100_index + 3, len(result_records))):
            moment, rate = result_records[i]
            print(f"{moment}\t{rate * 100:.2f}%")

        # 打印突变（成功率从100%下降到不足100%）的最后一个时机
        if last_100_index + 1 < len(result_records):
            moment, rate = result_records[last_100_index + 1]
            print(f"{moment}\t{rate * 100:.2f}%")
    else:
        # 如果没有100%的结果，直接打印所有结果
        for moment, rate in result_records:
            print(f"{moment}\t{rate * 100:.2f}%")


def fun(ctler: Controller):
    test_n = 1000  # 每次测试的样本量
    init_moment = 200  # 初始时机，单位cs
    min_success_rate = 0.60  # 最低成功率(98%)
    rollbackable_moment = 30  # 可以回滚的时机
    range_cs = 20  # 突变周围10cs

    # 使用二分法寻找突变时机
    mutation_moment = binary_search(ctler, init_moment - rollbackable_moment, init_moment, min_success_rate, test_n)

    if mutation_moment != -1:
        print(f"找到突变时机：{mutation_moment}cs")
        print(f"测试突变时机周围{range_cs}cs的数据：")
        test_around_moment(ctler, mutation_moment, range_cs=range_cs, test_n=test_n)
    else:
        print("未找到突变时机")


with InjectedGame(r"../../pvz_v1.0.0.1051_EN/Plants vs. Zombies 1.0.0.1051 EN/PlantsVsZombies.exe") as game:
    fun(game.controller)
