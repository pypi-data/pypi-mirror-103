import math


class NormalizarColuna(object):

    def __init__(self, dataframe):

        self.df = dataframe
        self.max_value = self.df.max()
        self.min_value = self.df.min()
        self.somatorio = self.df.sum()

    def norm_1(self):
        print(f'Aplicando normalização 1')
        new_df = []
        for i in self.df:
            norm = i / self.max_value
            new_df.append(norm)
        self.df = new_df
        return list(self.df)

    def norm_2(self):
        print(f'Aplicando normalização 1')
        new_df = []
        for i in self.df:
            norm = (i - self.min_value) / (self.max_value - self.min_value)
            new_df.append(norm)

        self.df = new_df
        return list(self.df)

    def norm_3(self):
        print(f'Aplicando normalização 1')
        new_df = []
        for i in self.df:
            norm = i / self.somatorio
            new_df.append(norm)

        self.df = new_df
        return list(self.df)

    def norm_4(self):
        print(f'Aplicando normalização 1')
        new_df = []
        for i in self.df:
            norm = i / math.sqrt(pow(i, 2))
            new_df.append(norm)

        self.df = new_df
        return list(self.df)


'''
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

'''