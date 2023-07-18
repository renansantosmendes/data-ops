import os
import git
import shutil
import datetime
import argparse

parser = argparse.ArgumentParser(description='set parameters')
parser.add_argument('--username', required=True)
parser.add_argument('--password', required=True)
parser.add_argument('--original_file_url', required=True)


def main(args):
    local_path = 'data'
    str_date = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    new_file_name = f'data_{str_date}.csv'

    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    else:
        print('Path does not exist')

    repos = git.Repo.clone_from(url=f'https://{args.username}:{args.password}@github.com/renansantosmendes/mlops-datasets.git',
                                to_path=os.path.join('.', local_path))

    base_data = pd.read_csv(args.original_file_url)
    base_data.sample(frac=0.6).to_csv(os.path.join(local_path, new_file_name), index=False)
    repos.index.add([onew_file_name])
    repos.index.commit(f'add file {new_file_name}')
    origin = repos.remote('origin')
    origin.push()


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)