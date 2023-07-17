###########
# Importações #
###########

import math

##########
# Estruturas #
##########

class Estacao:
    def __init__(self,fronteiras: list[int] = [],
        estacaoAnterior: int = -1,
        numeroDaEstacao: int = -1,
        linhaDeVindaDaEstacaoAnterior: int = -1,
        linhaParaAProximaEstacao: int = -1,
        proximaEstacao: int = -1,
        temBaldeacaoParaAProximaEstacao: bool = False,
        estacoesASeremEvitadas: list[int] = []):
        self.fronteiras: list[int] = fronteiras
        self.estacaoAnterior: int = estacaoAnterior
        self.numeroDaEstacao: int = numeroDaEstacao
        self.linhaDeVindaDaEstacaoAnterior: int = linhaDeVindaDaEstacaoAnterior
        self.linhaParaAProximaEstacao: int = linhaParaAProximaEstacao
        self.proximaEstacao: int = proximaEstacao
        self.temBaldeacaoParaAProximaEstacao: bool = temBaldeacaoParaAProximaEstacao
        self.estacoesASeremEvitadas: list[int] = estacoesASeremEvitadas

    @property
    def fronteiras(self) -> list[int]:
        return self._fronteiras

    @property
    def estacaoAnterior(self) -> int:
        return self._estacaoAnterior

    @property
    def numeroDaEstacao(self) -> int:
        return self._numeroDaEstacao

    @property
    def linhaDeVindaDaEstacaoAnterior(self) -> int:
        return self._linhaDeVindaDaEstacaoAnterior

    @property
    def linhaParaAProximaEstacao(self) -> int:
        return self._linhaParaAProximaEstacao

    @property
    def proximaEstacao(self) -> int:
        return self._proximaEstacao

    @property
    def temBaldeacaoParaAProximaEstacao(self) -> int:
        return self._temBaldeacaoParaAProximaEstacao

    @property
    def estacoesASeremEvitadas(self) -> list[int]:
        return self._estacoesASeremEvitadas

    @fronteiras.setter
    def fronteiras(self, fronteiras: list[int]) -> None:
        self._fronteiras = fronteiras

    @estacaoAnterior.setter
    def estacaoAnterior(self, estacaoAnterior: int) -> None:
        self._estacaoAnterior = estacaoAnterior

    @numeroDaEstacao.setter
    def numeroDaEstacao(self, numeroDaEstacao: int) -> None:
        self._numeroDaEstacao = numeroDaEstacao

    @linhaDeVindaDaEstacaoAnterior.setter
    def linhaDeVindaDaEstacaoAnterior(self, linhaDeVindaDaEstacaoAnterior: int) -> None:
        self._linhaDeVindaDaEstacaoAnterior = linhaDeVindaDaEstacaoAnterior

    @linhaParaAProximaEstacao.setter
    def linhaParaAProximaEstacao(self, linhaParaAProximaEstacao: int) -> None:
        self._linhaParaAProximaEstacao = linhaParaAProximaEstacao

    @proximaEstacao.setter
    def proximaEstacao(self, proximaEstacao: int) -> None:
        self._proximaEstacao = proximaEstacao

    @temBaldeacaoParaAProximaEstacao.setter
    def temBaldeacaoParaAProximaEstacao(self, temBaldeacaoParaAProximaEstacao: int) -> None:
        self._temBaldeacaoParaAProximaEstacao = temBaldeacaoParaAProximaEstacao

    @estacoesASeremEvitadas.setter
    def estacoesASeremEvitadas(self, estacoesASeremEvitadas: list[int]) -> None:
        self._estacoesASeremEvitadas = estacoesASeremEvitadas

#################
# Definição de funções #
#################

def lerMatriz(nomeDoArquivo: str):
    with open(nomeDoArquivo, 'r') as arquivo:
        linhas: list [str] = arquivo.readlines()
        matriz: list[list[float]] = []

        for linha in linhas:
            campos = linha.replace("\n", "").split(" ")
            camposConvertidos:list[float] = []

            for campo in campos:
                camposConvertidos.append(float(campo))

            matriz.append(camposConvertidos)

    return matriz


def identificarFronteiras(estacao:int,matrizDeLinhas:list[list[float]])-> list[int]:
    fronteiras: list[int]=[]

    #Percorre o vetor de linhas da estação desejada para ver quais linhas se conectam a essa estação, caso exista uma linha diferente de zero, ele pega o índice correspondente à posição do vetor e acrescenta +1, assim temos o número da estação que faz fronteira com a estação que queremos buscar a coluna
    for indice,coluna in enumerate(matrizDeLinhas[estacao-1]):
        if coluna !=0 :
            fronteiras.append(indice+1)

    return fronteiras


def identificarOMelhorFitness(estacaoAtual:int,estacaoDeDestino:int,ultimaEstacaoExpandida:int,fronteiras:list[int],estacoesQueDevemSerEvitadas:list[int],matrizDeDistanciasDiretas:list[list[float]],matrizDeDistanciasReais: list[list[float]]) -> int:
    vetorDeFitness:list[dict[int,float]] = []
    fronteiraValida:bool

    for fronteira in fronteiras:
        fronteiraValida = True

        if estacoesQueDevemSerEvitadas.__len__ != 0:
            for estacao in estacoesQueDevemSerEvitadas:
                if estacao == fronteira:
                    fronteiraValida = False
            
        if fronteira == ultimaEstacaoExpandida:
            fronteiraValida = False

        if fronteiraValida:
            valorDoFitnessDaFronteira = matrizDeDistanciasReais[estacaoAtual-1][fronteira-1] + matrizDeDistanciasDiretas[fronteira-1][estacaoDeDestino-1]

            vetorDeFitness.append({
                0: fronteira,
                1: valorDoFitnessDaFronteira
            })
        
    if(vetorDeFitness.__len__() == 0):
       return -1

    #Ordena o vetor de fitness com base nos valores dos conjuntos de fitness
    vetorDeFitness.sort(key= lambda conjunto: conjunto[1])

    #Retorna o número da fronteira que tem o menor valor de fitness
    return int(vetorDeFitness[0][0])


def aStar(estacaoDePartida:int, estacaoDeDestino:int, matrizDeLinhas:list[list[float]],matrizDeDistanciasDiretas:list[list[float]],matrizDeDistanciasReais: list[list[float]],arquivoDeSaida) -> None:
    # Definindo variáveis de uso local da função
    caminho: list[Estacao] = []
    estacaoAtual = estacaoDePartida
    tempoEstimadoDePercurso:float = 0
    ultimaEstacaoExpandida:int = -1
    ultimaLinhaPercorrida:int  = -1
    numeroDePassos = 0
    contadorDeBaldeacoes:int = 0

    while estacaoAtual != estacaoDeDestino:
        estacao = Estacao()
        """
        if estacaoAtual != estacaoDePartida:
            print('############',"\nTroca de estação\n#############\n")
        """
        #Atualiza a informação do número da estação
        estacao.numeroDaEstacao = estacaoAtual
        #print('Estação atual:',estacaoAtual,'\n')

        #Atualiza a informação da última estacao expandida
        estacao.estacaoAnterior = ultimaEstacaoExpandida
        #print('Última estação expandida:',ultimaEstacaoExpandida,'\n')

        #Atualiza a informação da última linha percorrida para chegar até a estação atual
        estacao.linhaDeVindaDaEstacaoAnterior = ultimaLinhaPercorrida
        #print('Última linha percorrida:',ultimaLinhaPercorrida,'\n')
    
        #Atualiza a informação dos fronteiras da estação atual
        estacao.fronteiras = identificarFronteiras(estacaoAtual,matrizDeLinhas)
        #print('Fronteiras:',estacao.fronteiras,'\n')

        #Obtém a estação com o menor valor de fitness e atualiza a informação da próxima estação para ser a o número da estação com o menor valor de fitness
        estacaoDeMelhorFitness: int = identificarOMelhorFitness(estacaoAtual,estacaoDeDestino,ultimaEstacaoExpandida,estacao.fronteiras,estacao.estacoesASeremEvitadas,matrizDeDistanciasDiretas,matrizDeDistanciasReais)
        #print('Estação de melhor fitness:',estacaoDeMelhorFitness,'\n')

        if estacaoDeMelhorFitness == -1:
            #print('Rebobinar')

            #Adiciona a estação atual ao vetor de estações que devem ser evitadas da estação anterior
            caminho[numeroDePassos-1].estacoesASeremEvitadas.append(estacaoAtual)

            #Verifica se na estacao anterior, teve baldeação para vir para a estação atual para que seja descontada a baldeação no tempo
            if caminho[numeroDePassos-1].temBaldeacaoParaAProximaEstacao:
                tempoEstimadoDePercurso -= 4*60

                #Desconsidera a baldeação realizada para chegar até a estação atual
                caminho[numeroDePassos-1].temBaldeacaoParaAProximaEstacao = False

            #Corrige o tempo estimado do percurso, já que ele contou essa expansão desnecessária

            distanciaAteAEstacaoAnterior = matrizDeDistanciasReais[estacaoAtual-1][ultimaEstacaoExpandida-1]

            tempoEstimadoDePercurso -= (distanciaAteAEstacaoAnterior*1000)/ (30/3.6)

            #Atualiza a ultima linha percorrida para ser a ultima linha percorrida para chegar à estação anterior
            ultimaLinhaPercorrida = caminho[numeroDePassos-1].linhaDeVindaDaEstacaoAnterior

            #Força o algoritmo a voltar para a estação anterior para expandir novamente
            estacaoAtual = ultimaEstacaoExpandida

            #Decrementa o vetor de caminho
            numeroDePassos -= 1
            continue

        estacao.proximaEstacao  = estacaoDeMelhorFitness

        #Identifica qual linha tomar para chegar à próxima estação
        estacao.linhaParaAProximaEstacao = int(matrizDeLinhas[estacaoAtual-1][estacaoDeMelhorFitness-1])
        #print('Linha para ir até a estação de melhor fitness:',estacao.linhaParaAProximaEstacao,'\n')

        #Verifica se deve haver baldeação para prosseguir para a próxima estação
        if ultimaLinhaPercorrida != -1 and ultimaLinhaPercorrida != estacao.linhaParaAProximaEstacao:
            estacao.temBaldeacaoParaAProximaEstacao = True
            contadorDeBaldeacoes +=1

            #Adiciona 4 minutos ao tempo total do percurso
            tempoEstimadoDePercurso += 4*60
        
        #Calcula o tempo estimado para ir da estação atual até a próxima estação e adiciona ao tempo estimado do percurso
        distanciaAteAProximaEstacao = matrizDeDistanciasReais[estacaoAtual-1][estacaoDeMelhorFitness-1]

        tempoEstimadoDePercurso += (distanciaAteAProximaEstacao*1000)/ (30/3.6)

        #Cria uma nova estação com os dados obtidos e adiciona ela ao vetor de caminho
        caminho.append(estacao)
        
        numeroDePassos += 1

        #Atualizando informações que serão utilizadas na próxima iteração
        ultimaEstacaoExpandida = estacaoAtual
        ultimaLinhaPercorrida =  estacao.linhaParaAProximaEstacao 
        estacaoAtual = estacaoDeMelhorFitness

    imprimir_caminho(caminho,estacaoDeDestino,arquivoDeSaida)

    print('O tempo estimado de percurso é de: {}'.format(converter_tempo(tempoEstimadoDePercurso)))
    arquivoDeSaida.write('\nO tempo estimado de percurso é de: {}'.format(converter_tempo(tempoEstimadoDePercurso)))


def imprimir_caminho(caminho: list[Estacao],estacaoDeDestino:int,arquivoDeSaida) -> None:
    if caminho.__len__() ==0:
        print("Você já está na estação desejada")
        arquivoDeSaida.write("Você já está na estação desejada")
        return

    print('O caminho mais rápido para ir da estação {} até a estação {} está descrito abaixo:\n'.format(caminho[0].numeroDaEstacao,estacaoDeDestino))
    arquivoDeSaida.write('O caminho mais rápido para ir da estação {} até a estação {} está descrito abaixo:\n\n'.format(caminho[0].numeroDaEstacao,estacaoDeDestino))
    
    for indice,passo in enumerate(caminho):
        if indice == 0:
            #Se só tiver 2 estações no caminho
            if indice == (caminho.__len__() -1 ) :
                print("Partindo da estação {}, pegue a linha {} para ir até o seu destino.".format(passo.numeroDaEstacao,nomear_linha(passo.linhaParaAProximaEstacao)))

                arquivoDeSaida.write("Partindo da estação {}, pegue a linha {} para ir até o seu destino.\n".format(passo.numeroDaEstacao,nomear_linha(passo.linhaParaAProximaEstacao)))
            else:
                print("Partindo da estação {}, pegue a linha {} para ir até a estação {}.".format(passo.numeroDaEstacao,nomear_linha(passo.linhaParaAProximaEstacao),passo.proximaEstacao))

                arquivoDeSaida.write("Partindo da estação {}, pegue a linha {} para ir até a estação {}.\n".format(passo.numeroDaEstacao,nomear_linha(passo.linhaParaAProximaEstacao),passo.proximaEstacao))
            continue
        
        if passo.temBaldeacaoParaAProximaEstacao:
            mensagem = "aguarde 4 minutos e troque para a linha {}".format(nomear_linha(passo.linhaParaAProximaEstacao))
        else:
            mensagem= "pegue a linha {}".format(nomear_linha(passo.linhaParaAProximaEstacao))

        if indice == (caminho.__len__() -1):
           print("Na estação {}, {} para ir até o seu destino.\n".format(passo.numeroDaEstacao,mensagem))

           arquivoDeSaida.write("Na estação {}, {} para ir até o seu destino.\n".format(passo.numeroDaEstacao,mensagem))
           break

        print("Na estação {}, {} para ir até a estacao {}.".format(passo.numeroDaEstacao,mensagem,passo.proximaEstacao))

        arquivoDeSaida.write("Na estação {}, {} para ir até a estacao {}.\n".format(passo.numeroDaEstacao,mensagem,passo.proximaEstacao))
    

def nomear_linha(numero_linha: int):
    if numero_linha == 1:
        return "azul"
    elif numero_linha == 2:
        return "amarela"
    elif numero_linha == 3:
        return "vermelha"
    elif numero_linha == 4:
        return "verde"
    else:
        return ""


def converter_tempo(tempo_segundos):
    horas = tempo_segundos/3600
    tempo_segundos = math.fmod(tempo_segundos, 3600)
    minutos = tempo_segundos/60
    tempo_segundos = math.fmod(tempo_segundos, 60)
    horas = int(horas)
    minutos = int(minutos)
    tempo_segundos = int(tempo_segundos)

    return "{} horas {} minutos e {} segundos\n" .format(horas,minutos,tempo_segundos)

######
# Main #
######

#Define o arquivo de teste
arquivoDeSaida = open('teste.txt','a')

# Carrega as matrizes
matrizDeLinhas = lerMatriz('Linhas.txt')
matrizDeDistanciasDiretas= lerMatriz('DistanciasDiretas.txt')
matrizDeDistanciasReais= lerMatriz('DistanciasReais.txt')
"""
aStar(13,14,matrizDeLinhas,matrizDeDistanciasDiretas,matrizDeDistanciasReais,arquivoDeSaida)
arquivoDeSaida.write('\n================================\n\n')
"""

for contador1 in range(14):
       aStar(14,contador1+1,matrizDeLinhas,matrizDeDistanciasDiretas,matrizDeDistanciasReais,arquivoDeSaida)
       arquivoDeSaida.write('\n================================\n\n')

