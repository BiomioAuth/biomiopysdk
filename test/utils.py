import os


###################################################################################################
# Python Filesystem Extras - File Searching
# import os
def get_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
###################################################################################################
