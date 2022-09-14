if __name__ == "__main__":
    import os
    from bs4 import BeautifulSoup
    import pandas as pd
    from glob import glob

    result = [y for x in os.walk(os.getcwd()) for y in glob(os.path.join(x[0], '*.xml'))]

    ann_dict = {'filename': [], 'example': []}
    max_ann = 0

    for filename in result:
        if filename.endswith('xml'):
            with open(filename, 'r', encoding='UTF-8') as f:
                xml = f.read()

            soup = BeautifulSoup(xml, 'lxml')
            for s in soup.find_all('s'):
                if 'annotation' in s.attrs:
                    if '|' in str(s.attrs['annotation']) and max_ann < len(s.attrs['annotation'].split('|')):
                        max_ann = len(s.attrs['annotation'].split('|'))

    for i in range(max_ann):
        ann_dict['annotation' + str(i + 1)] = []

    for filename in result:
        if filename.endswith('xml'):
            with open(filename, 'r') as f:
                xml = f.read()

            soup = BeautifulSoup(xml, 'lxml')
            for s in soup.find_all('s'):
                if 'annotation' not in s.attrs:
                    ann_dict['filename'].append(filename.split('/')[len(filename.split('/')) - 1])
                    ann_dict['example'].append(s.text.strip())
                    for j in range(1, max_ann + 1):
                        ann_dict['annotation' + str(j)].append(' ')
                else:
                    if '|' in str(s.attrs['annotation']):
                        ann_split = s.attrs['annotation'].split('|')
                        ann_dict['filename'].append(filename.split('/')[len(filename.split('/')) - 1])
                        ann_dict['example'].append(s.text.strip())
                        for g, ann in enumerate(ann_split):
                            ann_dict['annotation' + str(g + 1)].append(ann.strip())
                        for j in range(len(ann_split) + 1, max_ann + 1):
                            ann_dict['annotation' + str(j)].append(' ')
                    else:
                        ann_dict['annotation1'].append(s.attrs['annotation'].strip())
                        for j in range(2, max_ann + 1):
                            ann_dict['annotation' + str(j)].append(' ')
                        ann_dict['filename'].append(filename.split('/')[len(filename.split('/')) - 1])
                        ann_dict['example'].append(s.text.strip())

    df = pd.DataFrame.from_dict(ann_dict)
    df.to_csv(r'table_of_annotations.csv', index=False, header=True, encoding='UTF-8')














