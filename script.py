import os
import git
import shutil
import datetime

local_path = 'data'
str_date = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
new_file_name = f'data_{str_date}.csv'
username = 'renansantosmendes'
password = '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'

if os.path.exists(local_path):
    shutil.rmtree(local_path)
else:
    print('Path does not exist')

repos = git.Repo.clone_from(url=f'https://{username}:{password}@github.com/renansantosmendes/mlops-datasets.git',
                            to_path=local_path)

base_data.sample(frac=0.6).to_csv(os.path.join(local_path, new_file_name), index=False)

repos.index.add([new_file_name])
repos.index.commit(f'add file {new_file_name}')
origin = repos.remote('origin')
origin.push()
