import json
import datetime
import requests
import urllib
import pandas as pd
import seaborn as sns
import requests
from requests.auth import HTTPBasicAuth
import os

# 데이터셋 JSON 파일 경로
DATASET_DATA_PATH = 'dataset.json'
DATASET_DOWNLOAD_URL = 'https://raw.githubusercontent.com/braincrew/cds/main/mySUNI/data/dataset.json'

# 프로젝트 관련 파일 JSON 파일 경로
PROJECT_DATA_PATH = 'project.json'
PROJECT_DOWNLOAD_URL = 'https://raw.githubusercontent.com/braincrew/cds/main/mySUNI/data/project.json'



####### 데이터셋 관련 모듈 #######

class Dataset:

    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        # data 폴더 생성
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        r = requests.get(DATASET_DOWNLOAD_URL)
        open(DATASET_DATA_PATH, 'wb').write(r.content)

        with open(DATASET_DATA_PATH) as f:
            datasets = json.load(f)


        titles = []
        infos = []
        datas = []
        filenames = []

        for name_ in datasets:
            titles.append(name_)
            infos.append(datasets[name_]['info'])
            datas.append(datasets[name_]['data'])
            filenames.append(datasets[name_]['filename'])

        self.dataset = pd.DataFrame({
            'name': titles,
            'info': infos,
            'data': datas,
            'filename': filenames,
        })


    def info(self):
        display(self.dataset[['name', 'info', 'filename']])


    def load(self, dataset_names):
        global datasets
        username = 'mysuni'
        password = 'mysuni1!'

        if type(dataset_names) == str:
            df = self.dataset.loc[self.dataset['name'] == dataset_names]
            if df.shape[0] > 0:
                fileurl = df['data']
                filename = df['filename']
                for f_name, f_url in zip(filename.iloc[0], fileurl.iloc[0]):
                    r = requests.get(f_url, auth=HTTPBasicAuth(username, password))
                    filepath = os.path.join(self.data_dir, f_name)
                    open(filepath, 'wb').write(r.content)
                    print(f'파일 다운로드 완료\n====================\n\n데이터셋: {dataset_names}\n파일경로: {filepath}\n\n====================')
                return
            else:
                raise Exception('데이터셋 정보가 없습니다.')

        elif type(dataset_names) == list or type(dataset_names) == tuple:
            for dataset_name in dataset_names:
                df = self.dataset.loc[self.dataset['name'] == dataset_name]
                if df.shape[0] > 0:
                    fileurls = df['data'].iloc[0]
                    filenames = df['filename'].iloc[0]
                    for fileurl, filename in zip(fileurls, filenames):
                        r = requests.get(fileurl, auth=HTTPBasicAuth(username, password))
                        filepath = os.path.join(self.data_dir, filename)
                        open(filepath, 'wb').write(r.content)
                        print(f'파일 다운로드 완료\n====================\n\n데이터셋: {dataset_name}\n파일경로: {filepath}\n\n====================')
                else:
                    raise Exception('데이터셋 정보가 없습니다.')
            return
        else:
            raise Exception('잘못된 정보입니다.')


dataset = Dataset()


def list_data():
    global dataset
    dataset.info()


def download_data(dataset_name):
    global dataset
    return dataset.load(dataset_name)


####### 프로젝트 관련 모듈 #######

project = None


class Project:
    def __init__(self, project_name, class_info, email):
        self.project_name = project_name
        self.edu_name = "mySUNI"
        self.class_info = class_info
        self.email = email

        r = requests.get(PROJECT_DOWNLOAD_URL)
        open(PROJECT_DATA_PATH, 'wb').write(r.content)

    def __make_submission(self, submission):
        timestring = datetime.datetime.now().strftime('%H-%M-%S')
        filename = 'submission-{}.csv'.format(timestring)
        submission.to_csv(filename, index=False)
        print('파일을 저장하였습니다. 파일명: {}'.format(filename))
        return filename

    def __project_submission(self, file_name):
        file_path = './'
        url = f'http://manage.jaen.kr/api/studentProject/apiScoring?edu_name={self.edu_name}\
        &edu_rnd={self.class_info}&mail={self.email}&project_name={self.project_name}&file_name={file_name}'
        files = {'file': (file_name, open(file_path + file_name, 'rb'), 'text/csv')}
        r = requests.post(url, files=files)
        r.encoding = 'utf-8'
        message = ''
        if 'msg' in r.text:
            data = json.loads(r.text)
            message = '제출 여부 :{}\n오늘 제출 횟수 : {}\n제출 결과:{}'.format(data['msg'], data['trial'], data['score'])
        else:
            message = r.text
        return message

    def project_final_submission(self, name, csv_file_path, ipynb_file_path):
        url = "http://sk.jaen.kr/submission_final"
        files = [('file', open(csv_file_path, 'rb')), ('file', open(ipynb_file_path, 'rb'))]
        data = {'name': name}
        res = requests.post(url, data=data, files=files)
        print(res.text)

    def submit(self, submission):
        filename = self.__make_submission(submission)
        print(self.__project_submission(filename))


def download_project(project_name, class_info, email):
    global project, files
    try:
        project = Project(project_name, class_info=class_info, email=email)

        # data 폴더 경로 지정
        DATA_DIR = 'data'

        with open(PROJECT_DATA_PATH) as f:
            datasets = json.load(f)

        # data 폴더 생성
        if not os.path.exists(os.path.join(DATA_DIR, project_name)):
            os.makedirs(os.path.join(DATA_DIR, project_name))


        project_files = datasets[project_name]

        # auth
        username = 'mysuni'
        password = 'mysuni1!'

        print(f'프로젝트: {project_name}\n==============================\n파일 정보\n')
        for filename, fileurl in project_files.items():
            r = requests.get(fileurl, auth=HTTPBasicAuth(username, password))
            filepath = os.path.join(DATA_DIR, project_name, filename)
            open(filepath, 'wb').write(r.content)
            print(f'{filename}:\t {filepath}')
        print(f'\n==============================')
    except:
        raise Exception('잘못된 정보입니다.')


def submit(submission_file):
    global project
    project.submit(submission_file)


def end_project(name, csv_file_path, ipynb_file_path):
    global project
    project.project_final_submission(name, csv_file_path, ipynb_file_path)
