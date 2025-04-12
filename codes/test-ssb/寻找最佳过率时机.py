from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller

def run_test(ctler: Controller, moment: int, n: int = 10000) -> float:
    """运行一次测试，返回通过率"""
    iz_test = IzTest(ctler).init_by_str(f'''
        {n} -1
        3-1
        .....
        .....
        2bllb
        .....
        .....
        cg ft
        0 {moment}
        3-6 3-6''')

    iz_test.start_test(jump_frame=1)

    # 计算通过率
    success_rate = iz_test._success_count / n
    return success_rate

def test_moments(ctler: Controller):
    """测试时机从 175 到 190 的通过率"""
    results = []
    for moment in range(175, 191):  # 测试时机从 175 到 190
        success_rate = run_test(ctler, moment)
        results.append((moment, success_rate))

    # 打印表格
    print("时机(cs)\t通过率(%)")
    for moment, rate in results:
        print(f"{moment}\t{rate * 100:.2f}%")

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    test_moments(game.controller)
