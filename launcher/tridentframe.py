import subprocess
from multiprocessing import Pool


processes = ('./resources/app/engine/linux/main', './tridentframe-electron')


def run_process(process):
    subprocess.run(process)


pool = Pool(processes=2)
pool.map(run_process, processes)
