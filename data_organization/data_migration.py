import os
import shutil

def migrate_data(src_root, dst_root):
    # Ensure the destination root directory exists
    if not os.path.exists(dst_root):
        os.makedirs(dst_root)
    
    for p in os.listdir(src_root):
        src_pname = os.path.join(src_root, p)
        dst_pname = os.path.join(dst_root, p)
        
        if os.path.isdir(src_pname):
            # If it's a directory, create the corresponding directory in the destination
            if not os.path.exists(dst_pname):
                os.makedirs(dst_pname)
            # Recursively call the function for the subdirectory
            migrate_data(src_pname, dst_pname)
        else:
            # If it's a file, copy it to the new location
            shutil.copyfile(src_pname, dst_pname)

src_path = '/Users/yang/Documents/Wilbrecht_Lab/sleap_videos/intermediate_track_files'
dst_path = '/Users/yang/Documents/Wilbrecht_Lab/sleap_videos 2/intermediate_track_files'
migrate_data(src_path, dst_path)
