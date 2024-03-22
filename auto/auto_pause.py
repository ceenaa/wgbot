import sched
import time
import sheet.sheet as sheet
import gspread
import repo.peer
import service.peer

delay_time = 60 * 60 * 12

sa = gspread.service_account(filename='keys.json')
sh = sa.open_by_key(sheet.sheet_id)
wks = sh.worksheet("Sheet1")


def daily_pause(scheduler):
    scheduler.enter(delay_time, 1, daily_pause, (scheduler,))
    try:
        sheet.main()
        names = wks.col_values(3)
        status = wks.col_values(6)
        days = wks.col_values(5)

        for i in range(1, len(names)):
            if repo.peer.is_name_exists(names[i]) is False:
                continue

            if days[i] == "31" and status[i] == "1":
                service.peer.pause_peer(names[i])
                sheet.main()

    except Exception as err:
        print(type(err).__name__ + " " + str(err))


def auto():
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(1, 1, daily_pause, (my_scheduler,))
    my_scheduler.run()
