import shutil
import os

# use this script to copy folders to the server
src_path = '/home/wholebrain/sleap_models/20240402_RR_n24/models/v003.6_240624_151538.single_instance.n=870'
dst_path = '/media/server/Restaurant Row/Data/sleap_models/v003.6_240624_151538.single_instance.n=870'
if not os.path.exists(os.path.dirname(dst_path)):
    os.makedirs(os.path.dirname(dst_path))

shutil.copytree(src_path, dst_path)