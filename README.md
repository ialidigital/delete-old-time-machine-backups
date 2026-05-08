# Delete-Old-Time-Machine-Backups

## Description:

A macOS utility written in python that helps automate clean up of old Time Machine backups, freeing up disk space while keeping the backups you still need

By default Time Machine will use up all the free space on the allocated volume, and then overwrite old backups as the volume fills up. If you arent happy with that then you can clean up manually (messy), or use this script which leverages the underlying MacOS services to cleanly erase backups older than X amount of months old.

You can run this script manually from the cmdline, or setup a monthly or quarterly cron as part of your housekeeping - set and forget.

You run this from the cmdline, of the machine who is the source for the backups - not on the machine with the target volume or backup archives. It utilises the native MacOs services to query the Time Machine database - this is only possible from the host only.


## Signature:

```yaml
 Deletes Time Machine backups older than the specified threshold.

  Args:
    threshold_months (int): The number of months to keep backups.
    (The script has a default value of 24, ie 24 months if no parameter value is passed when calling the script)


  Returns:
   tuple: A tuple containing the initial number of backups, 
           the number of backups deleted, 
           and a list of successfully deleted backups.
```

## Usage:

make executable by respective user, eg:

`❯ chmod u+x delete-old-time-machine-backups.py`


then, run on cmdline to delete backup archives more than 60 months old from today's date: 

`❯ python3 ./delete-old-time-machine-backups.py 60`

output:

```yaml
2026-05-08 23:01:16,058 - DEBUG - Initial number of backups: 0
2026-05-08 23:01:16,059 - DEBUG - Threshold (seconds): 1622757676.059632
Initial backups: 0
Backups deleted: 0
Deleted backups: []
```
