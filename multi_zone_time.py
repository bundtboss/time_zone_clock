from rich import print, pretty, inspect
import sys
import time
import pytz
from datetime import datetime, date
from rich.live import Live
from rich.table import Table

# table generation function
def generate_table() -> Table:
    # define local timezone for comparisons, used for checking the date
    local_time = pytz.timezone("America/Chicago")
    # make a table
    table = Table()
    table.show_lines = True
    # define the table columns
    table.add_column("Timezone")
    table.add_column("Time")
    table.add_column("Date")
    # for each timezone add a row to the table
    for zone in zones:
        # define timezone
        tz = pytz.timezone(zone)
        # get date and tme
        date = datetime.now(tz).strftime("%D")
        time = datetime.now(tz).strftime("%H:%M")
        # add the row in three parts, columns are seperated by commas
        table.add_row(
            f"[bold white]{zones.get(zone)}",
            f"[gold3]{time}" if time < "12:00" else f"[deep_pink4]{time}",
            f"[red]{date}"
            if date != datetime.now(local_time).strftime("%D")
            else f"{date}",
        )
    return table


# make a table of Olson timezones and a prefered name
zones = {
    "America/New_York": "US East",
    "America/Chicago": "US Central",
    "America/Denver": "US Mountain",
    "America/Los_Angeles": "US West",
    "America/Denver": "US Mountain",
    "Asia/Kolkata": "India Standard",
    "Asia/Shanghai": "Shanghai China",
    "UTC": "UTC",
}
# check for arguments
# -l specifies "live" mode that runs for 12 hours
# no options generates the table once
n = len(sys.argv)
if n <= 1:
    print(generate_table())
if n >= 2:
    if sys.argv[1] == "-l":
        with Live(generate_table(), refresh_per_second=4) as live:
            for _ in range(720):
                time.sleep(1)
                live.update(generate_table())
    else:
        print("[red]That's not right, it's -l or nothing")
