import codecs
import json
import os

# 코드 입력 문구 (코드를 삭제하고 출력을 박제하는 Cell)
code_input_msgs = [
    '# 코드입력',
    '# 코드를 입력하세요.',
    '# 코드를 입력해 주세요',
]

# 검증코드 (출력 값을 삭제하지 않음)
validation_msgs =  [
    '# 검증코드',
    '# 코드 검증',
    '# 코드검증',
]


# from_file: 읽어 올 해설 파일 이름
# to_file: 변환 후 내보낼 파일 명, None
# folder_path: 기본 값 None. None이 아니면 해당 폴더경로에 생성
# post_fix: 파일 뒤에 붙혀줌. 그대로 두면 -변환 이라고 postfix 가 붙어서 자동 생성
def convert_ipynb(from_file, to_file=None, folder_path=None, post_fix='-변환.ipynb'):
    try:
        f = codecs.open(from_file, 'r')
    except UnicodeDecodeError:
        f = codecs.open(from_file, 'r', encoding='utf-8')
    except Exception as e:
        raise Exception("파일 변환에 실패 했습니다. 에러 메세지:" + e)
    source = f.read()
    y = json.loads(source)

    idx = []
    sources = []

    for i, x in enumerate(y['cells']):
        flag = False
        valid_flag = False
        for x2 in x['source']:
            for msg in code_input_msgs:
                if msg in x2:
                    flag = True
                    break

            for valid_msg in validation_msgs:
                if valid_msg in x2:
                    valid_flag = True
                    break

        if flag:
            new_text = []
            for x2 in x['source']:
                if x2.startswith('#'):
                    new_text.append(x2)
            x['source'] = new_text

        if 'outputs' in x.keys():
            if not flag and not valid_flag:
                x['outputs'] = []
            elif len(x['outputs']) > 0:
                if 'data' in x['outputs'][0].keys():
                    if 'text/html' in x['outputs'][0]['data'].keys():
                        idx.append(i)
                        html_text = x['outputs'][0]['data']['text/html']
                        html_text.insert(0, '<p><strong>[출력 결과]</strong></p>')
                        sources.append(html_text)
                        x['outputs'] = []
                    elif 'text/plain' in x['outputs'][0]['data'].keys():
                        idx.append(i)
                        plain_text = x['outputs'][0]['data']['text/plain']

                        plain_text[0] = '<pre>' + plain_text[0]
                        plain_text[len(plain_text) - 1] = plain_text[len(plain_text) - 1] + '</pre>'
                        plain_text.insert(0, '<p><strong>[출력 결과]</strong></p>')
                        sources.append(plain_text)
                        x['outputs'] = []

                if len(x['outputs']) > 0 and 'text' in x['outputs'][0].keys():
                    idx.append(i)
                    text = x['outputs'][0]['text']

                    text[0] = '<pre>' + text[0]
                    text[len(text) - 1] = text[len(text) - 1] + '</pre>'
                    text.insert(0, '<p><strong>[출력 결과]</strong></p>')
                    sources.append(text)
                    x['outputs'][0]['text'] = []

        if 'execution_count' in x.keys():
            x['execution_count'] = None

    cnt = 0
    tmp = []
    for i, s in zip(idx, sources):
        v = {'cell_type': 'markdown',
             'metadata': {},
             'source': s}
        tmp.append((i + 1 + cnt, v))
        cnt += 1

    for i in range(len(tmp)):
        y['cells'].insert(tmp[i][0], tmp[i][1])

    if to_file is None:
        if '해설' in from_file:
            to_file = from_file.replace('해설', '실습')
            to_file = to_file[:-6] + post_fix
        else:
            to_file = from_file[:-6] + post_fix

    if folder_path is not None:
        # 폴더 경로 없으면 생성
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        # 폴더 경로를 포함한 파일 경로 생성
        to_file = os.path.join(folder_path, os.path.basename(to_file))

    with open(to_file, "w") as json_file:
        json.dump(y, json_file)
    print('생성완료')
    print(f'파일명: {to_file}')
