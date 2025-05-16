import jsonlines

class IOJsonLines:

    @classmethod
    def write_out(cls, path, datas):
        with jsonlines.open(path, 'w') as writer:
            for data in datas:
                writer.write(data)
        print(f'写入文件到：{path}。')

    @classmethod
    def read_in(cls, path):
        datas = []
        with jsonlines.open(path) as reader:
            for data in reader:
                datas.append(data)
        return datas