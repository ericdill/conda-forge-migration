from os.path import join, basename
import tqdm
import pandas as pd
import subprocess
import os
import fnmatch


pkg_dir_template = '{base}/{channel}/{platform}'


problematic_file_extensions = [
    'h',
    'so',
]

def files_in_tar(pkg_path):
    """
    List all files in the conda package path

    Parameters
    ----------
    pkg_path : str
        Full path to the conda package

    Returns
    -------
    list
        List of files in teh conda package
    """
    files = subprocess.check_output('tar -tf %s' % pkg_path, 
                                    shell=True).decode().split('\n')
    return [f for f in files if f]

def get_extensions(files):
    return set(os.path.splitext(f)[-1] for f in files)

def get_files(pkg_folder):
    packages = fnmatch.filter(os.listdir(pkg_folder), "*.tar.bz2")
    return [join(pkg_folder, f) for f in packages]


from multiprocessing import Pool

def func(pkg_path):
    return basename(pkg_path), get_extensions(files_in_tar(pkg_path))

def run(base, channel, platform):
    p = Pool(20)
    pkg_folder = pkg_dir_template.format(base=base, channel=channel, platform=platform)
    files = get_files(pkg_folder)
    files_subset = files
    all_extensions = []
    with tqdm.tqdm(total=len(files_subset)) as pbar:
        for fname, ext in p.imap_unordered(func, files_subset):
            pbar.update()           
            all_extensions.append({'name': fname, 'ext': ext})

    df = pd.DataFrame(all_extensions)
    df.to_csv('%s-%s.csv' % (channel, platform))

if __name__ == "__main__":
    import sys
    packages_path = sys.argv[1]
    packages_path = packages_path.rstrip('/')
    base, channel, platform = packages_path.rsplit('/', maxsplit=2)
    print('%s--%s--%s' % (base, channel, platform))

    run(base, channel, platform)
