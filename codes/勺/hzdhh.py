from rpze.basic import *
from rpze.flow import *
from rpze.iztest import *
from rpze.structs import *


def yupan(k, z):
    Z = [1.4, 1.4, 1.4, 1.5, 1.4, 1.4, 1.3, 1.4, 1.4, 1.4, 1.5, 1.4, 0.8, 0.9, 0.9, 0.8, 0.1, 0.2, 0.1, 0.1, 0.0, 0.0,
         0.0, 0.0, 2.4, 2.4, 2.3, 2.4, 2.3, 2.4, 2.4, 2.3, 1.2, 1.2, 1.2, 1.1, 1.3, 1.1, 1.2, 1.2, 0.1, 0.1, 0.1, 0.1,
         0.1, 0.1]
    w = k * 47 * 0.01 / sum(Z)
    x = z
    t = 0
    m = 0
    while int(x) > 230 or t % 4 != 0:
        t = t + 1
        m = (m + w) - int(m + w)
        p = int(m * len(Z) + 1)
        x = x - k * 47 * 0.01 * Z[p - 1] * (len(Z) + 1) / sum(Z)
    return (t, int(x))


def fun(ctler: Controller, jump_frame=True):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        3-2
        .....
        .....
        hzdhh
        .....
        .....
        lz 
        0  
        3-6''')

    bu_gui = 0
    bu_gan = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal bu_gui, bu_gan
        lz = iz_test.game_board.zombie_list[0]
        hh = iz_test.ground["3-4"]
        dp = iz_test.ground["3-3"]
        await until_plant_die(hh).after(4)
        sj = yupan(lz.dx, lz.x)[0]
        zb = yupan(lz.dx, lz.x)[1]
        await delay(sj - 406)
        if zb == 230:
            for i in range(0, 26):
                if dp.launch_cd == 50:
                    await delay(50)
                    place("xg 3-6")
                    bu_gui += 1
                await delay(1)
        else:
            for i in range(0, 24):
                if dp.launch_cd == 50:
                    await delay(50)
                    place("xg 3-6")
                    bu_gui += 1
                await delay(1)
        await until(lambda _: lz.is_dead)
        place("cg 3-6")
        bu_gan += 1

    @iz_test.on_game_end()
    def end_callback(result: bool):
        pass

    iz_test.start_test(jump_frame, speed_rate=5)
    print(bu_gui)
    print(bu_gan)


with InjectedGame(r"C:\Users\20631\Desktop\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    ctler = game.controller
    enter_ize(ctler)
    board = get_board(ctler)
    fun(ctler, 0)
