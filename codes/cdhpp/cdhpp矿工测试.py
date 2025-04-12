from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.plant_modifier import set_puff_x_offset
from random import randint

def fun(ctler: Controller, delta:int, test_n:int=1000):
    iz_test = IzTest(ctler).init_by_str(f'''
        {test_n} -1
        3-1
        .....
        .....
        cdhpp
        .....
        .....
        kg
        0
        3-6''')

    @iz_test.flow_factory.add_flow()
    async def _(_):
        xp_4 = iz_test.ground["3-4"]
        set_puff_x_offset(xp_4, delta)

    iz_test.start_test(jump_frame=1, print_interval=100)

    # 计算通过率
    success_rate = iz_test._success_count / test_n
    return success_rate

def test_delta(ctler:Controller):
    results = []
    for delta in range(-5, 0+1): #0后的和右偏是一样的，一定不会被打，实测其实-2-1也不会被打
        succ_rate = fun(ctler, delta, test_n=5000)
        results.append((delta, succ_rate))

    # 打印表格
    print("偏移(-5, +4)\t通过率(%)")
    for delta, rate in results:
        print(f"{delta}\t{rate * 100:.2f}%")

if __name__ == '__main__':
    with InjectedGame(r"../../pvz_v1.0.0.1051_EN/Plants vs. Zombies 1.0.0.1051 EN/PlantsVsZombies.exe") as game:
        test_delta(game.controller)
