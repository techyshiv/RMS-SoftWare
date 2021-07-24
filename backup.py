from datetime import date 
import shutil
def take_bkp(src_file_name,bkp_file_name=None,src_file_loc="",bkp_file_loc=""):
    # Source file name
    src_file=src_file_name + src_file_loc

    # Fetching Today's(Current Day) date
    today=date.today()
    date_format = today.strftime("%d_%b_%Y_")

    # Modified the name of the backup file
    if bkp_file_name is None or not bkp_file_name:
        bkp_file_name=src_file_name
        bkp_file=bkp_file_loc + date_format + bkp_file_name
    else:
        bkp_file=bkp_file_loc + date_format + bkp_file_name

    # Create the Backup Copy of the source file
    shutil.copy2(src_file,bkp_file)

    # Success Message
    print("Backup Successfull....")
  