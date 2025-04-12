from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager


def fun(ctler: Controller):
    n = 1000  # 测试样本量
    moment = 917+4*120
    iz_test = IzTest(ctler).init_by_str(f'''
        {n} -1
        2-5 
        sssss
        ssssc
        .....
        .....
        .....
        ft 
        0 
        1-6''')

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

    iz_test.start_test(jump_frame=1, print_interval=10)  # 跳帧且每1000次才打印

    aver_succ = succ_time / iz_test._success_count if iz_test._success_count != 0 else -1  # 单位cs
    print(f"测试{n}次, 成功{iz_test._success_count}次, 成功平均用时{aver_succ / 100:.2f}s")


with InjectedGame(r"../../pvz_v1.0.0.1051_EN/Plants vs. Zombies 1.0.0.1051 EN/PlantsVsZombies.exe") as game:
    fun(game.controller)
