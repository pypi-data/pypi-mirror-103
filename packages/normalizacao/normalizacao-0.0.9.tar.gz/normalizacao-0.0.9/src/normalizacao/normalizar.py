import math


class NormalizarColuna(object):

    def __init__(self, dataframe, norm_value: int):

        self.df = dataframe
        self.normalizacao = norm_value
        self.max_value = self.df.max()
        self.min_value = self.df.min()
        self.somatorio = 0
        for k, v in self.df.items():
            self.somatorio += v

        if self.normalizacao == 1:
            self.norm_1()
        elif self.normalizacao == 2:
            self.norm_2()
        elif self.normalizacao == 3:
            self.norm_3()
        else:
            self.norm_4()

    def norm_1(self):
        print(f'Aplicando normalização 1')
        for key, value in self.df.items():
            print(f'Alternativa: {key}')
            norm = value/self.max_value
            self.df[key] = norm

    def norm_2(self):
        print(f'Aplicando normalização 2')
        for key, value in self.df.items():
            print(f'Alternativa: {key}')
            norm = (value - self.min_value)/(self.max_value - self.min_value)
            self.df[key] = norm

    def norm_3(self):
        print(f'Aplicando normalização 3')
        for key, value in self.df.items():
            print(f'Alternativa: {key}')
            norm = value / self.somatorio
            self.df[key] = norm

    def norm_4(self):
        print(f'Aplicando normalização 4')
        for key, value in self.df.items():
            print(f'Alternativa: {key}')
            norm = value / math.sqrt(pow(value, 2))
            self.df[key] = norm

class RenomearIndex(object):
    def __init__(self, dataframe, dicionario):
        self.df = dataframe
        self.dicionario = dicionario

    def rename(self):
        self.df.rename(index=self.dicionario)


class NormalizarDataFrame(object):

    def __init__(self, dataframe, norm_value: int):

        self.df = dataframe
        self.normalizacao = norm_value

    def normalizar(self):
        colunas = self.df.columns
        for i in colunas:
            n = NormalizarColuna(dataframe=self.df[i], norm_value=self.normalizacao)

        return 'Normalização do dataframe realizada com sucesso'


