from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.plant_modifier import set_puff_x_offset


def fun(ctler: Controller, delta1: int, delta2: int, test_n: int = 1000) -> float:
    """运行测试并返回成功率"""
    iz_test = IzTest(ctler).init_by_str(f'''
        {test_n} -1
        3-1
        .....
        .....
        cdhpp
        .....
        .....
        cg
        0
        3-6''')

    @iz_test.flow_factory.add_flow()
    async def _(_):
        xp_4 = iz_test.ground["3-4"]
        set_puff_x_offset(xp_4, delta1)
        xp_5 = iz_test.ground["3-5"]
        set_puff_x_offset(xp_5, delta2)

    iz_test.start_test(jump_frame=1, print_interval=2000)

    # 计算成功率
    success_rate = iz_test._success_count / test_n
    return success_rate


def test_2delta(ctler: Controller):
    """测试 delta1 和 delta2 的组合，并打印二维表格"""
    results = []
    delta_range = range(-5, +4+1)
    # 遍历所有 delta1 和 delta2 的组合
    for delta1 in delta_range:
        row = []
        for delta2 in delta_range:
            # 运行测试并记录成功率
            succ_rate = fun(ctler, delta1, delta2, test_n=2000)
            row.append(succ_rate)
        results.append(row)

    # 打印表格
    print("delta1 \\ delta2", end="")
    for delta2 in delta_range:
        print(f"\t{delta2}", end="")
    print()

    for i, delta1 in enumerate(delta_range):
        print(f"{delta1}", end="")
        for succ_rate in results[i]:
            print(f"\t{succ_rate:.2f}", end="")
        print()


if __name__ == '__main__':
    with InjectedGame(r"../pvz_v1.0.0.1051_EN/Plants vs. Zombies 1.0.0.1051 EN/PlantsVsZombies.exe") as game:
        test_2delta(game.controller)
