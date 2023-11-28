from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic
import inquirer

class Universidade:
    def __init__(self, nome, valor_vestibular, desconto_matricula, localidade, curso):
        self.nome = nome
        self.valor_vestibular = valor_vestibular
        self.desconto_matricula = desconto_matricula
        self.localidade = localidade
        self.curso = curso

class Curso:
    def __init__(self, nome, mensalidade):
        self.nome = nome
        self.mensalidade = mensalidade

# Dicionário simulando um banco de dados de universidades
universidades = {
    "Universidade Federal Fictícia": Universidade(
        "Universidade Federal Fictícia", 1000, 0.2, "Brasília",
        Curso("Ciência da Computação", 800)
    ),
    "Instituto Tecnológico Simulado": Universidade(
        "Instituto Tecnológico Simulado", 1200, 0.1, "São Paulo",
        Curso("Ciência da Computação", 1000)
    ),
    "Faculdade Imaginária": Universidade(
        "Faculdade Imaginária", 800, 0.15, "Rio de Janeiro",
        Curso("Ciência da Computação", 700)
    ),
    "Universidade Digital": Universidade(
        "Universidade Digital", 900, 0.18, "Belo Horizonte",
        Curso("Ciência da Computação", 850)
    ),
    "Centro de Educação Tecnológica": Universidade(
        "Centro de Educação Tecnológica", 1100, 0.12, "Curitiba",
        Curso("Ciência da Computação", 950)
    ),
    "Instituto de Ciência da Computação": Universidade(
        "Instituto de Ciência da Computação", 950, 0.2, "Porto Alegre",
        Curso("Ciência da Computação", 900)
    ),
    "Universidade Metropolitana": Universidade(
        "Universidade Metropolitana", 850, 0.1, "Recife",
        Curso("Ciência da Computação", 800)
    ),
    "Faculdade Progresso": Universidade(
        "Faculdade Progresso", 1000, 0.15, "Salvador",
        Curso("Ciência da Computação", 920)
    ),
    "Universidade Nova Era": Universidade(
        "Universidade Nova Era", 950, 0.17, "Fortaleza",
        Curso("Ciência da Computação", 890)
    ),
    "Instituto de Tecnologia Avançada": Universidade(
        "Instituto de Tecnologia Avançada", 1200, 0.2, "Manaus",
        Curso("Ciência da Computação", 1100)
    ),
    "Faculdade de Inovação": Universidade(
        "Faculdade de Inovação", 850, 0.13, "Porto Velho",
        Curso("Ciência da Computação", 800)
    ),
    "Universidade Moderna": Universidade(
        "Universidade Moderna", 1100, 0.18, "Goiânia",
        Curso("Ciência da Computação", 1000)
    ),
}

def obter_coordenadas(localidade):
    geolocator = Nominatim(user_agent="nome_do_seu_app")
    try:
        location = geolocator.geocode(localidade)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Coordenadas não encontradas para {localidade}.")
            return None
    except GeocoderTimedOut:
        print("Tempo de solicitação excedido. Tente novamente.")
        return None

def calcular_distancia(coordenadas1, coordenadas2):
    if coordenadas1 and coordenadas2:
        return geodesic(coordenadas1, coordenadas2).kilometers
    return float('inf')

def obter_localidade_valida():
    print("Selecione a localidade em que mora:")

    try:
        with open('Cidades.txt', 'r', encoding='utf-8') as file:
            cidades_brasileiras = [line.strip() for line in file]
    except FileNotFoundError:
        print("Arquivo 'Cidades.txt' não encontrado.")
        return None

    questions = [inquirer.List('localidade', message="Selecione a localidade:", choices=cidades_brasileiras)]
    answers = inquirer.prompt(questions)

    return answers.get('localidade', None)

class FiltroPerfilUsuario:
    def __init__(self, faixa_salarial, local_moradia):
        self.faixa_salarial = faixa_salarial
        self.local_moradia = local_moradia

    def verificar_capacidade_pagamento(self, mensalidade, despesas_fixas, outras_dividas):
        fator_seguranca = 0.8  # Fator de segurança para despesas fixas e outras dívidas

        # Calcula o valor disponível após descontar despesas fixas e outras dívidas
        salario_disponivel = self.faixa_salarial * fator_seguranca - despesas_fixas - outras_dividas

        # Verifica se o valor disponível é suficiente para cobrir a mensalidade
        return salario_disponivel >= mensalidade

    def filtrar_universidades(self, universidades, distancia_maxima):
        universidades_filtradas = []
        coordenadas_usuario = obter_coordenadas(self.local_moradia)

        for nome, universidade in universidades.items():
            if coordenadas_usuario and self.verificar_acessibilidade(universidade, coordenadas_usuario, distancia_maxima):
                universidades_filtradas.append(universidade)

        return universidades_filtradas

    def verificar_acessibilidade(self, universidade, coordenadas_usuario, distancia_maxima):
        # Verifica se a universidade está dentro do limite de distância
        distancia = calcular_distancia(coordenadas_usuario, obter_coordenadas(universidade.localidade))
        return (
            universidade.valor_vestibular <= self.faixa_salarial
            and distancia <= distancia_maxima
        )

    def ordenar_universidades(self, universidades):
        opcoes_ordenacao = [
            inquirer.List("criterio", message="Escolha o critério de ordenação:",
                        choices=[
                            "Menor Valor-Vestibular",
                            "Maior Valor-Vestibular",
                            "Menor Desconto",
                            "Maior Desconto",
                            "Menor Distância",
                            "Maior Distância",
                            "Menor Mensalidade",
                            "Maior Mensalidade"
                        ]),
        ]

        answers = inquirer.prompt(opcoes_ordenacao)

        criterio = answers.get("criterio", None)

        if criterio == "Menor Valor-Vestibular":
            return sorted(universidades, key=lambda u: u.valor_vestibular)
        elif criterio == "Maior Valor-Vestibular":
            return sorted(universidades, key=lambda u: u.valor_vestibular, reverse=True)
        elif criterio == "Menor Desconto":
            return sorted(universidades, key=lambda u: u.desconto_matricula)
        elif criterio == "Maior Desconto":
            return sorted(universidades, key=lambda u: u.desconto_matricula, reverse=True)
        elif criterio == "Menor Distância":
            coordenadas_usuario = obter_coordenadas(self.local_moradia)
            return sorted(universidades, key=lambda u: calcular_distancia(coordenadas_usuario, obter_coordenadas(u.localidade)))
        elif criterio == "Maior Distância":
            coordenadas_usuario = obter_coordenadas(self.local_moradia)
            return sorted(universidades, key=lambda u: calcular_distancia(coordenadas_usuario, obter_coordenadas(u.localidade)), reverse=True)
        elif criterio == "Menor Mensalidade":
            return sorted(universidades, key=lambda u: u.curso.mensalidade)
        elif criterio == "Maior Mensalidade":
            return sorted(universidades, key=lambda u: u.curso.mensalidade, reverse=True)
        else:
            print("Critério inválido. As universidades serão apresentadas na ordem original.")
            return universidades

# Exemplo de uso:
faixa_salarial_usuario = float(input("Digite seu salário: "))
local_moradia_usuario = obter_localidade_valida()

# Verifica se a localidade foi selecionada com sucesso
if local_moradia_usuario is not None:
    usuario = FiltroPerfilUsuario(faixa_salarial=faixa_salarial_usuario, local_moradia=local_moradia_usuario)

    despesas_fixas = float(input("Digite o valor das despesas fixas mensais: "))
    outras_dividas = float(input("Digite o valor de outras dívidas mensais: "))

    # Passa a lista de universidades (o dicionário) para o método filtrar_universidades
    distancia_maxima = float(input("Digite a distância máxima que você está disposto a considerar (em km): "))
    universidades_recomendadas = usuario.filtrar_universidades(universidades, distancia_maxima)

    # Verifica se há universidades recomendadas
    if not universidades_recomendadas:
        print("Desculpe, não encontramos universidades que atendam aos seus critérios. Considere ajustar suas preferências.")
    else:
        # Ordena as universidades de acordo com o critério escolhido pelo usuário
        universidades_ordenadas = usuario.ordenar_universidades(universidades_recomendadas)

        print("\nUniversidades Recomendadas:")
        for universidade in universidades_ordenadas:
            if usuario.verificar_capacidade_pagamento(universidade.curso.mensalidade, despesas_fixas, outras_dividas):
                print(
                    f"{universidade.nome} - Valor do Vestibular: R${universidade.valor_vestibular}, "
                    f"Desconto Matrícula: {universidade.desconto_matricula*100}%, "
                    f"Curso: {universidade.curso.nome} - Mensalidade: R${universidade.curso.mensalidade}, "
                    f"Localidade: {universidade.localidade}, "
                    f"Distância: {calcular_distancia(obter_coordenadas(local_moradia_usuario), obter_coordenadas(universidade.localidade)):.2f} km"
                )