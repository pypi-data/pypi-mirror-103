import math
import pandas as pd
from abc import abstractmethod, ABC

informacoes_classe = {'Classe': ('C20', 'C30', 'C40', 'C60'),
                      'Fc0k': (20, 30, 40, 60),
                      'Ec0m': (9500, 14500, 19500, 24500)}
tabela_classe = pd.DataFrame(informacoes_classe, index=(1, 2, 3, 4))

informacoes_kmod1 = {'Permanente': 0.6,
                     'Longa Duração': 0.7,
                     'Média Duração': 0.8,
                     'Curta Duração': 0.9,
                     'Instantânea': 1.1}

duracoes = ('Permanente', 'Longa Duração', 'Média Duração', 'Curta Duração', 'Instantânea')

informacoes_kmod2 = {'1': 1,
                     '2': 1,
                     '3': 0.8,
                     '4': 0.8}

informacoes_kmod3 = {'1ª Categoria': 1, '2ª Categoria': 0.8}

categorias = ('1ª Categoria', '2ª Categoria')


class MenuPrincipal:

    def __init__(self):
        print('\n\nBem vindo ao Calculador de Estruturas do 4º TE. A seguir, um pequeno tutorial de uso.\n\n')
        print('Não é necessário digitar as unidades dos valores, apenas o número é necessário.')
        print('Caso a unidade seja digitada, erros ocorrerão.')
        print('Quando aparecer um seletor, por exemplo: \n (1) Opção 1 \n (2) Opção 2')
        print('Digite somente o número que está dentro dos parênteses. Por exemplo, se sua a opção desejada for a 2,')
        print('digite apenas "2" (sem as aspas).\n\n')

        mensagem = '''Qual elemento estrutural irá ser calculado?
        
            (1) Pilar
            (2) Viga
            
            '''

        elemento = int(input(mensagem))

        if elemento == 1:
            PilarDeMadeira()
        elif elemento == 2:
            VigaDeMadeira()
        else:
            raise Exception('Digite um valor válido.')


class Pegador(ABC):

    @staticmethod
    @abstractmethod
    def pega_dimensoes(elemento):
        pass

    @staticmethod
    @abstractmethod
    def pega_comprimento():
        pass

    @staticmethod
    @abstractmethod
    def pega_cargas():
        pass

    @staticmethod
    def escolhe_tipo_elemento():

        mensagem = f'''O elemento é retangular ou circular?

                        (1) Circular
                        (2) Retangular

                    '''

        circulo_ou_retangulo = input(mensagem)
        if circulo_ou_retangulo in ('1', '2'):
            return circulo_ou_retangulo
        else:
            raise ValueError('Digite um valor válido.')

    @staticmethod
    def pega_classe_categoria_e_duracao():
        mensagem_classe = '''Informe a classe da madeira. 

                (1) C20
                (2) C30
                (3) C40
                (4) C60

                '''

        mensagem_categoria = '''Informe a categoria da madeira.

                (1) 1ª categoria
                (2) 2ª categoria

                '''

        mensagem_duracao = '''Informe a duração do carregamento.

                (1) Permanente
                (2) Longa Duração
                (3) Média Duração
                (4) Curta Duração
                (5) Instantânea

                '''

        classe = int(input(mensagem_classe))
        if classe not in (1, 2, 3, 4):
            raise ValueError('Digite um valor válido para classe. ')

        categoria = int(input(mensagem_categoria))
        if categoria not in (1, 2):
            raise ValueError('Digite um valor válido para categoria. ')

        duracao = int(input(mensagem_duracao))
        if duracao not in (1, 2, 3, 4, 5):
            raise ValueError('Digite um valor válido para duração. ')

        return classe, categoria, duracao

    @staticmethod
    def pega_classe_umidade():
        umidade = int(input('Informe a umidade ambiente. '))

        if umidade <= 65:
            classe_umidade = '1'
        elif 65 < umidade <= 75:
            classe_umidade = '2'
        elif 75 < umidade <= 85:
            classe_umidade = '3'
        else:
            classe_umidade = '4'

        return classe_umidade

    @staticmethod
    def pega_Fc0k(elemento):
        fc0k = tabela_classe.loc[elemento.classe, 'Fc0k']
        return fc0k

    @staticmethod
    def pega_kmod(elemento):
        duracao = duracoes[elemento.duracao - 1]
        kmod1 = informacoes_kmod1[duracao]

        kmod2 = informacoes_kmod2[elemento.classe_umidade]

        categoria = categorias[elemento.categoria - 1]
        kmod3 = informacoes_kmod3[categoria]

        kmod = kmod1 * kmod2 * kmod3

        return round(kmod, 3), (kmod1, kmod2, kmod3)

    @staticmethod
    def pega_Ec0m(elemento):
        Ec0m = tabela_classe.loc[elemento.classe, 'Ec0m']
        return Ec0m


class PegadorViga(Pegador):

    @staticmethod
    def pega_dimensoes(viga):
        if viga.circulo_ou_retangulo == '1':
            diametro = float(input('Informe o diâmetro em centímetro da peça. '))
            return diametro / 100
        else:
            base = float(input('Informe a medida da base em centímetro da peça. '))
            altura = float(input('Informe a medida da altura em centímetro da peça. '))
            return base / 100, altura / 100

    @staticmethod
    def pega_comprimento():
        comprimento = float(input('Informe o comprimento em metro da viga. '))
        return comprimento

    @staticmethod
    def pega_cargas():
        peso_proprio = float(input('Informe o peso próprio da viga. '))
        carga_acidental = float(input('Informe a carga acidental da viga. '))

        return peso_proprio, carga_acidental
        


class PegadorPilar(Pegador):

    @staticmethod
    def pega_dimensoes(pilar):
        if pilar.circulo_ou_retangulo == '1':
            diametro = float(input('Informe o diâmetro em centímetro da peça. '))
            return diametro
        else:
            base = float(input('Informe a medida da base em centímetro da peça. '))
            altura = float(input('Informe a medida da altura em centímetro da peça. '))
            return base, altura

    @staticmethod
    def pega_comprimento():
        comprimento = float(input('Informe o comprimento em metro do pilar. '))
        return comprimento * 100

    @staticmethod
    def pega_cargas():
        flexao_composta = float(input('Informe o esforço de Flexão Composta (Nd) do pilar. '))
        momento_z = float(input('Informe o Momento Fletor no eixo Z (Mzd) do pilar. '))
        momento_y = float(input('Informe o Momento Fletor no eixo Y (Myd) do pilar. '))

        return flexao_composta, (momento_z, momento_y)


class Calculador(ABC):

    @staticmethod
    @abstractmethod
    def calcula_inercia(elemento):
        pass

    @staticmethod
    @abstractmethod
    def calcula_resistencia(elemento):
        pass

    @staticmethod
    def calcula_area(elemento):
        if elemento.circulo_ou_retangulo == '1':
            area = (math.pi * elemento.dimensoes ** 2) / 4
            return area
        else:
            area = elemento.dimensoes[0] * elemento.dimensoes[1]
            return round(area, 6)

    @staticmethod
    def calcula_fc0d(elemento):
        fc0d = (elemento.kmod * elemento.Fc0k) / 1.4
        return round(fc0d, 2)
    
    @staticmethod
    def calcula_modulo_elasticidade(viga):
        Eef = (viga.Ec0m * viga.kmod) * 1000
        return round(Eef, 2)


class CalculadorViga(Calculador):

    @staticmethod
    def calcula_inercia(viga):
        if viga.circulo_ou_retangulo == '1':
            inercia = (math.pi * (viga.dimensoes ** 4)) / 64
        else:
            inercia = (viga.dimensoes[0] * viga.dimensoes[1] ** 3) / 12

        return round(inercia, 8)

    @staticmethod
    def calcula_resistencia(viga):
        if viga.circulo_ou_retangulo == '1':
            W = (math.pi * (viga.dimensoes ** 3)) / 32
        else:
            W = (viga.dimensoes[0] * (viga.dimensoes[1] ** 2)) / 6

        return W

    @staticmethod
    def calcula_carga_permanente(viga):
        carga_permanente = viga.area * 10 + viga.peso_proprio
        return carga_permanente

    @staticmethod
    def calcula_momento_fletor(viga):
        momento_fletor = (1.4 * (viga.carga_permanente + viga.carga_acidental) * viga.comprimento ** 2) / 8
        return momento_fletor

    @staticmethod
    def calcula_tensao_normal(viga):
        tensao_normal = (viga.momento_fletor / viga.modulo_resistencia) / 1000
        return round(tensao_normal, 3)

    @staticmethod
    def calcula_flecha_maxima(viga):
        flecha_maxima = (viga.comprimento / 200) * 1000
        return flecha_maxima

    @staticmethod
    def calcula_flecha_efetiva(viga):
        Vef = ((5 * (viga.carga_permanente + 0.2 * viga.carga_acidental) * viga.comprimento ** 4) / (
                384 * viga.modulo_elasticidade * viga.inercia)) * 1000
        return round(Vef, 3)


class CalculadorPilar(Calculador):

    @staticmethod
    def calcula_inercia(pilar):
        if pilar.circulo_ou_retangulo == '1':
            inercia = (math.pi * (pilar.dimensoes ** 4)) / 64
            return inercia
        else:
            inercia_z = (pilar.dimensoes[0] * pilar.dimensoes[1] ** 3) / 12
            inercia_y = (pilar.dimensoes[1] * pilar.dimensoes[0] ** 3) / 12
            return inercia_z, inercia_y

    @staticmethod
    def calcula_resistencia(pilar):
        if pilar.circulo_ou_retangulo == '1':
            W = (math.pi * (pilar.dimensoes ** 3)) / 32
            return W
        else:
            Wz = (pilar.dimensoes[0] * (pilar.dimensoes[1] ** 2)) / 6
            Wy = (pilar.dimensoes[1] * (pilar.dimensoes[0] ** 2)) / 6
            return Wz, Wy

    @staticmethod
    def calcula_raio_giracao(pilar):
        raio_giracao_z = math.sqrt((pilar.inercia[0]/pilar.area))
        raio_giracao_y = math.sqrt((pilar.inercia[1]/pilar.area))

        return raio_giracao_z, raio_giracao_y

    @staticmethod
    def calcula_indice_esbeltez(pilar):
        esbeltez_z = pilar.comprimento/pilar.raio_giracao[0]
        esbeltez_y = pilar.comprimento/pilar.raio_giracao[1]

        return esbeltez_z, esbeltez_y

    @staticmethod
    def calcula_tensao_normal(pilar):
        tensao_normal = pilar.flexao_composta/pilar.area

        return tensao_normal * 10

    @staticmethod
    def calcula_tensao_momento_fletor(pilar):
        tensao_z = (pilar.momentos[0] * 100)/pilar.modulo_resistencia[0]
        tensao_y = (pilar.momentos[1] * 100)/pilar.modulo_resistencia[1]

        return (tensao_z * 10), (tensao_y * 10)

    @staticmethod
    def retorna_excentricidade(pilar):
        if (pilar.indice_esbeltez[0] > 40) and (pilar.indice_esbeltez[1] > 40):
            excentricidade = []
            for item in (0, 1):
                excentricidade.append(CalculadorPilar.calcula_excentricidade(pilar, item))

        elif pilar.indice_esbeltez[0] > 40:
            excentricidade = CalculadorPilar.calcula_excentricidade(pilar, 0)

        elif pilar.indice_esbeltez[1] > 40:
            excentricidade = CalculadorPilar.calcula_excentricidade(pilar, 1)

        else: 
            excentricidade = None

        return excentricidade

    @staticmethod
    def calcula_excentricidade(pilar, algo):
        
        excentricidade_acidental = (pilar.comprimento * 10) / 300
        eiz = (pilar.momentos[algo] / pilar.flexao_composta) * 1000
        e1z = excentricidade_acidental + eiz

        fe = ((math.pi**2) * pilar.modulo_elasticidade * pilar.inercia[algo] * 10**-8) / ((pilar.comprimento / 100) ** 2)
        ezd = e1z * (fe/(fe-pilar.flexao_composta))
        myd = (pilar.flexao_composta * (ezd * 10**-3))
        sigma_myd = myd / (pilar.modulo_resistencia[algo] * 10**-6) / 1000

        resultados = (sigma_myd, myd, fe, algo, (excentricidade_acidental, eiz, e1z, ezd))
        return resultados

            
class VigaDeMadeira:

    def __init__(self):
        self.circulo_ou_retangulo = PegadorViga.escolhe_tipo_elemento()
        self.dimensoes = PegadorViga.pega_dimensoes(self)
        self.comprimento = PegadorViga.pega_comprimento()
        self.peso_proprio, self.carga_acidental = PegadorViga.pega_cargas()
        self.classe, self.categoria, self.duracao = PegadorViga.pega_classe_categoria_e_duracao()
        self.classe_umidade = PegadorViga.pega_classe_umidade()
        self.Fc0k = PegadorViga.pega_Fc0k(self)
        self.kmod, self.kmods = PegadorViga.pega_kmod(self)
        self.Ec0m = PegadorViga.pega_Ec0m(self)

        self.area = CalculadorViga.calcula_area(self)
        self.inercia = CalculadorViga.calcula_inercia(self)
        self.modulo_resistencia = CalculadorViga.calcula_resistencia(self)
        self.carga_permanente = CalculadorViga.calcula_carga_permanente(self)
        self.momento_fletor = CalculadorViga.calcula_momento_fletor(self)
        self.tensao_normal = CalculadorViga.calcula_tensao_normal(self)
        self.fc0d = CalculadorViga.calcula_fc0d(self)
        self.flecha_maxima = CalculadorViga.calcula_flecha_maxima(self)
        self.modulo_elasticidade = CalculadorViga.calcula_modulo_elasticidade(self)
        self.flecha_efetiva = CalculadorViga.calcula_flecha_efetiva(self)

        print(self)

    def compara_estado_limite_ultimo(self):
        if self.tensao_normal <= self.fc0d:
            return 'Passou!'
        else:
            return 'Não passou!'

    def compara_flecha(self):
        if self.flecha_efetiva <= self.flecha_maxima:
            return 'Passou!'
        else:
            return 'Não passou!'

    def __str__(self):
        return f'''

\033[1mÁrea (A)\033[0m: {round(self.area, 3)} m²
\033[1mMomento de Inércia (Iz)\033[0m: {round(self.inercia, 3)} m⁴
\033[1mMódulo de Resistência (W)\033[0m: {round(self.modulo_resistencia, 3)} m³
\033[1mCarga Permanente (gk)\033[0m: {round(self.carga_permanente, 3)} kN/m
\033[1mMomento Fletor Máximo (Mzd)\033[0m: {round(self.momento_fletor, 3)} kNm
\033[1mTensão Máxima (σMzd)\033[0m: {round(self.tensao_normal, 3)} MPa
\033[1mResistência a Compressão (Fc0k)\033[0m: {self.Fc0k} MPa
\033[1mKmod1, Kmod2, Kmod3\033[0m: {self.kmods}
\033[1mKmod\033[0m: {self.kmod}
\033[1mResistência da Madeira (Fc0d)\033[0m: {self.fc0d} MPa

\033[1mVerificação Parte 3\033[0m: {round(self.tensao_normal, 3)} <= {self.fc0d}
        \033[1m{self.compara_estado_limite_ultimo()}\033[0m

\033[1mFlecha Limite (Vlim)\033[0m: {self.flecha_maxima} mm
\033[1mEc0m\033[0m: {self.Ec0m} MPa
\033[1mModulo de Elasticidade Efetivo (Eef)\033[0m: {self.modulo_elasticidade} kN/m²
\033[1mFlecha Efetiva (Vef)\033[0m: {round(self.flecha_efetiva, 3)} mm

\033[1mVerificação Parte 4\033[0m: {round(self.flecha_efetiva, 3)} <= {self.flecha_maxima}
        \033[1m{self.compara_flecha()}\033[0m


'''


class PilarDeMadeira:

    def __init__(self):
        self.circulo_ou_retangulo = PegadorPilar.escolhe_tipo_elemento()
        self.dimensoes = PegadorPilar.pega_dimensoes(self)
        self.comprimento = PegadorPilar.pega_comprimento()
        self.flexao_composta, self.momentos = PegadorPilar.pega_cargas()
        self.classe, self.categoria, self.duracao = PegadorPilar.pega_classe_categoria_e_duracao()
        self.classe_umidade = PegadorPilar.pega_classe_umidade()
        self.Fc0k = PegadorPilar.pega_Fc0k(self)
        self.kmod, self.kmods = PegadorPilar.pega_kmod(self)
        self.Ec0m = PegadorPilar.pega_Ec0m(self)

        self.area = CalculadorPilar.calcula_area(self)
        self.inercia = CalculadorPilar.calcula_inercia(self)
        self.modulo_resistencia = CalculadorPilar.calcula_resistencia(self)
        self.raio_giracao = CalculadorPilar.calcula_raio_giracao(self)
        self.indice_esbeltez = CalculadorPilar.calcula_indice_esbeltez(self)
        self.fc0d = CalculadorPilar.calcula_fc0d(self)
        self.tensao_normal = CalculadorPilar.calcula_tensao_normal(self)
        self.tensao_momento_fletor = CalculadorPilar.calcula_tensao_momento_fletor(self)
        self.modulo_elasticidade = CalculadorPilar.calcula_modulo_elasticidade(self)
        self.excentricidade = CalculadorPilar.retorna_excentricidade(self)

        print(self)

    def verificacao_parte_1(self):
        verificacao = ((self.tensao_normal/self.fc0d)**2 +
                       self.tensao_momento_fletor[1]/self.fc0d +
                       0.5 * (self.tensao_momento_fletor[0]/self.fc0d))
        if verificacao < 1:
            return 'Passou!', verificacao
        else:
            return 'Não passou!', verificacao

    def verificacao_parte_2(self):
        verificacao = ((self.tensao_normal/self.fc0d)**2 +
                       0.5 * (self.tensao_momento_fletor[1]/self.fc0d) +
                       self.tensao_momento_fletor[0]/self.fc0d)
        if verificacao < 1:
            return 'Passou!', verificacao
        else:
            return 'Não passou!', verificacao

    def verificacao_parte_3(self):
        if type(self.excentricidade) == type(None):
            return ''

        elif type(self.excentricidade) == type(tuple()):
            calculo_verificacao = ((self.tensao_normal/self.fc0d) +
                                   (self.excentricidade[0] / self.fc0d))
            if calculo_verificacao <= 1:
                verificacao = 'Passou!'
            else:
                verificacao = 'Não passou!'

            z_ou_y = (('eiy', 'e1y', 'Mzd', 'σMzd', 'Z', 'eyd'), ('eiz', 'e1z', 'Myd', 'σMyd', 'Y', 'ezd'))
            
            return f'''\033[1mExcentricidade acidental (ea)\033[0m: {self.excentricidade[4][0]} mm
\033[1m{z_ou_y[self.excentricidade[3]][0]}\033[0m: {self.excentricidade[4][1]} mm
\033[1m{z_ou_y[self.excentricidade[3]][1]}\033[0m: {self.excentricidade[4][2]} mm
\033[1mEc0m\033[0m: {self.Ec0m} MPa
\033[1mMódulo de Elasticidade (Ec0ef)\033[0m: {self.modulo_elasticidade} kN/m²
\033[1mFe\033[0m: {round(self.excentricidade[2], 3)} kN
\033[1m{z_ou_y[self.excentricidade[3]][5]}\033[0m: {round(self.excentricidade[4][-1], 3)} mm
\033[1mNovo Momento Fletor em {z_ou_y[self.excentricidade[3]][4]} ({z_ou_y[self.excentricidade[3]][2]})\033[0m: {round(self.excentricidade[1], 3)} kNm
\033[1mNova Tensão Momento Fletor em {z_ou_y[self.excentricidade[3]][4]} ({z_ou_y[self.excentricidade[3]][3]})\033[0m: {round(self.excentricidade[0], 3)} MPa

\033[1mVerificação Parte 4\033[0m: {calculo_verificacao} <= 1
        \033[1m{verificacao}\033[0m
    '''

        elif type(self.excentricidade) == type(list()):

            calculo_verificacao_z = ((self.tensao_normal/self.fc0d) +
                                   (self.excentricidade[0][0] / self.fc0d))
            if calculo_verificacao_z <= 1:
                verificacao_z = 'Passou!'
            else:
                verificacao_z = 'Não passou!'

            calculo_verificacao_y = ((self.tensao_normal/self.fc0d) +
                                   (self.excentricidade[1][0] / self.fc0d))
            if calculo_verificacao_y <= 1:
                verificacao_y = 'Passou!'
            else:
                verificacao_y = 'Não passou!'

            return f'''\033[1mExcentricidade acidental (ea)\033[0m: {self.excentricidade[0][4][0]} mm
\033[1mEc0m\033[0m: {self.Ec0m} MPa
\033[1mMódulo de Elasticidade (Ec0ef)\033[0m: {self.modulo_elasticidade} kN/m²
            
\033[1mVerificação em Z:\033[0m
\033[1meiy\033[0m: {self.excentricidade[0][4][1]} mm
\033[1me1y\033[0m: {self.excentricidade[0][4][2]} mm
\033[1mFe\033[0m: {round(self.excentricidade[0][2], 3)} kN
\033[1meyd\033[0m: {round(self.excentricidade[0][4][-1], 3)} mm
\033[1mNovo Momento Fletor em Z (Mzd)\033[0m: {round(self.excentricidade[0][1], 3)} kNm
\033[1mNova Tensão Momento Fletor em Z (σMzd)\033[0m: {round(self.excentricidade[0][0], 3)} MPa

\033[1mVerificação Parte 4 em Z\033[0m: {round(calculo_verificacao_z, 6)} <= 1
        \033[1m{verificacao_z}\033[0m

\033[1mVerificação em Y:\033[0m
\033[1meiz\033[0m: {self.excentricidade[1][4][1]} mm
\033[1me1z\033[0m: {self.excentricidade[1][4][2]} mm
\033[1mFe\033[0m: {round(self.excentricidade[1][2], 3)} kN
\033[1mezd\033[0m: {round(self.excentricidade[1][4][-1], 3)} mm
\033[1mNovo Momento Fletor em Y (Myd)\033[0m: {round(self.excentricidade[1][1], 3)} kNm
\033[1mNova Tensão Momento Fletor em Y (σMyd)\033[0m: {round(self.excentricidade[1][0], 3)} MPa

\033[1mVerificação Parte 4 em Y\033[0m: {round(calculo_verificacao_y, 6)} <= 1
        \033[1m{verificacao_y}\033[0m
    '''

    def __str__(self):
        return f'''

\033[1mÁrea (A)\033[0m: {round(self.area, 3)} cm²
\033[1mMomento de Inércia em z (Iz)\033[0m: {round(self.inercia[0], 3)} cm⁴
\033[1mMomento de Inércia em y (Iy)\033[0m: {round(self.inercia[1], 3)} cm⁴
\033[1mMódulo de Resistência em z (Wz)\033[0m: {round(self.modulo_resistencia[0], 3)} cm³
\033[1mMódulo de Resistência em y (Wy)\033[0m: {round(self.modulo_resistencia[1], 3)} cm³
\033[1mRaio de Giração em z (iz)\033[0m: {round(self.raio_giracao[0], 3)} cm
\033[1mRaio de Giração em y (iy)\033[0m: {round(self.raio_giracao[1], 3)} cm
\033[1mÍndice de Esbeltez em z (λz)\033[0m: {round(self.indice_esbeltez[0], 3)}
\033[1mÍndice de Esbeltez em y (λy)\033[0m: {round(self.indice_esbeltez[1], 3)}

\033[1mResistência a Compressão (Fc0k)\033[0m: {self.Fc0k} MPa
\033[1mKmod1, Kmod2, Kmod3\033[0m: {self.kmods}
\033[1mKmod\033[0m: {self.kmod}
\033[1mResistência da Madeira (Fc0d)\033[0m: {self.fc0d} MPa

\033[1mTensão Normal (σNd)\033[0m: {round(self.tensao_normal, 3)} MPa
\033[1mTensão Momento Fletor em z (σMz)\033[0m: {round(self.tensao_momento_fletor[0], 3)} MPa
\033[1mTensão Momento Fletor em y (σMy)\033[0m: {round(self.tensao_momento_fletor[1], 3)} MPa

\033[1mVerificação Parte 3.1\033[0m: {round(self.verificacao_parte_1()[1], 6)} < 1
        \033[1m{self.verificacao_parte_1()[0]}\033[0m

\033[1mVerificação Parte 3.2\033[0m: {round(self.verificacao_parte_2()[1], 6)} < 1
        \033[1m{self.verificacao_parte_2()[0]}\033[0m

{self.verificacao_parte_3()}

'''


if __name__ == '__main__':
    MenuPrincipal()
