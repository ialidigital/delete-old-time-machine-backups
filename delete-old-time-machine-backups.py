__author__ = "Imran Ali"
__copyright__ = "Copyright 2025"
__license__ = "MIT"
__version__ = "1.0.0 GA"
__maintainer__ = "Imran Ali"
__status__ = "Production"

import subprocess
import time
from datetime import datetime
import re
import logging
import sys

def delete_old_time_machine_backups(threshold_months=24):
  """
  Deletes Time Machine backups older than the specified threshold.

  Args:
    threshold_months (int): The number of months to keep backups.

  Returns:
    tuple: A tuple containing the initial number of backups, 
           the number of backups deleted, 
           and a list of successfully deleted backups.
  """
  logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

  try:
    # Get initial number of backups
    initial_backups = len(subprocess.run(["/usr/bin/tmutil", "listbackups"], capture_output=True, text=True).stdout.strip().splitlines())
    logging.debug(f"Initial number of backups: {initial_backups}")

    # Calculate the threshold time in seconds
    threshold_seconds = time.time() - (threshold_months * 30 * 24 * 60 * 60) 
    logging.debug(f"Threshold (seconds): {threshold_seconds}")

    # Get a list of backups using tmutil
    result = subprocess.run(["/usr/bin/tmutil", "listbackups"], capture_output=True, text=True)
    backups = result.stdout.strip().splitlines()

    deleted_backups = []

    for backup in backups:
      logging.debug(f"Processing backup: {backup}")

      # Extract creation date from backup path 
      match = re.search(r"(\d{4}-\d{2}-\d{2}-\d{6})", backup) 
      if match:
        creation_date = match.group(1) 
        logging.debug(f"Extracted creation date: {creation_date}")
      else:
        logging.error(f"Error: Could not extract creation date from backup path: {backup}")
        continue

      try:
        creation_date_datetime = datetime.strptime(creation_date, "%Y-%m-%d-%H%M%S")
        creation_date_seconds = creation_date_datetime.timestamp()
        logging.debug(f"Parsed creation date (seconds): {creation_date_seconds}")

        if creation_date_seconds < threshold_seconds:
          logging.info(f"Deleting backup: {backup}")
          backup_mount_point = subprocess.run(["/usr/bin/tmutil", "machinedirectory"], capture_output=True, text=True).stdout.strip()
          logging.debug(f"Backup Mount Point: {backup_mount_point}")
          logging.debug(f"Deletion Command: sudo tmutil delete -d '{backup_mount_point}' -t '{creation_date}'")
          try:
            subprocess.run(["sudo", "tmutil", "delete", "-d", backup_mount_point, "-t", creation_date], check=True) 
            logging.info(f"Successfully deleted backup: {backup}")
            deleted_backups.append(backup)
          except subprocess.CalledProcessError as e:
            logging.error(f"Error deleting backup: {backup} - {e}")

      except ValueError:
        logging.error(f"Error parsing creation date: {creation_date}")

  except subprocess.CalledProcessError as e:
    logging.error(f"Error: tmutil command failed with error code: {e.returncode}")
  except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")

  # Get the final number of backups
  final_backups = len(subprocess.run(["/usr/bin/tmutil", "listbackups"], capture_output=True, text=True).stdout.strip().splitlines())

  return initial_backups, len(deleted_backups), deleted_backups

if __name__ == "__main__":
  if len(sys.argv) > 1:
    try:
      threshold_months = int(sys.argv[1])
    except ValueError:
      print("Error: Invalid input. Please provide an integer value for the number of months.")
      sys.exit(1)
  else:
    threshold_months = 24  # Default to 24 months if no argument is provided

  initial_backups, num_deleted, deleted_backups = delete_old_time_machine_backups(threshold_months)
  print(f"Initial backups: {initial_backups}")
  print(f"Backups deleted: {num_deleted}")
  print(f"Deleted backups: {deleted_backups}")
  