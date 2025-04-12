from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.cond_funcs import until_plant_die
from rpze.flow.utils import until
from rpze.iztest.operations import place
from rpze.rp_extend import Controller


def fun(ctler: Controller):
    test_n = 1000
    iz_test = IzTest(ctler).init_by_str(f'''
        {test_n} -1
        1-0
        sss1j
        .....
        .....
        .....
        .....
        kg 
        0
        1-1''')

    game_res = False  # 记录每次测试是否成功

    @iz_test.on_game_end()
    def _(res: bool):  # 每次结束修改外部变量 game_res
        nonlocal game_res
        game_res = res

    @iz_test.flow_factory.add_flow()
    async def _(_):
        plant_1_4 = iz_test.ground["1-4"]
        # await until_plant_die(plant_1_4).after(487+1)
        await until(lambda _: plant_1_4.hp <= 172)
        # 44必过，100必过，120必过
        place("xg 1-6")

    iz_test.start_test(jump_frame=1, print_interval=10)
    print(f"测试{test_n}次, 成功{iz_test._success_count}次")


with InjectedGame(r"../../pvz_v1.0.0.1051_EN/Plants vs. Zombies 1.0.0.1051 EN/PlantsVsZombies.exe") as game:
    fun(game.controller)
