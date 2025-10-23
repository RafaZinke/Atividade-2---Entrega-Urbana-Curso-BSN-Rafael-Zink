"""
Sistema de Cálculo de Entregas Urbanas
Implementação usando Programação Funcional
"""

from typing import Dict, List, Tuple
from functools import reduce

# Constantes de configuração
PRECOS_BASE_ZONA = {
    'zona1': 15.0,
    'zona2': 25.0,
    'zona3': 35.0,
    'zona4': 50.0
}

PEDAGIO_POR_ZONA = {
    'zona1': 0.0,
    'zona2': 5.50,
    'zona3': 8.00,
    'zona4': 12.00
}

SOBRETAXA_PESO = 2.50  # por kg acima de 10kg
LIMITE_PESO_GRATIS = 10.0

SOBRETAXA_VOLUME = 3.00  # por m³ acima de 0.5m³
LIMITE_VOLUME_GRATIS = 0.5

CUSTO_JANELA_CRITICA = 15.0


# ========== FUNÇÕES PURAS DE VALIDAÇÃO ==========

def validar_numero_positivo(valor: float, nome_campo: str) -> Tuple[bool, str]:
    """
    Função pura: valida se um valor é numérico e positivo
    Retorna: (True, "") se válido, (False, mensagem_erro) se inválido
    """
    if not isinstance(valor, (int, float)):
        return False, f"{nome_campo} deve ser um número"
    if valor < 0:
        return False, f"{nome_campo} não pode ser negativo"
    return True, ""


def validar_zona(zona: str) -> Tuple[bool, str]:
    """
    Função pura: valida se a zona existe no sistema
    """
    if zona not in PRECOS_BASE_ZONA:
        return False, f"Zona '{zona}' inválida. Zonas válidas: {list(PRECOS_BASE_ZONA.keys())}"
    return True, ""


def validar_janela_critica(janela_critica: bool) -> Tuple[bool, str]:
    """
    Função pura: valida o campo janela crítica
    """
    if not isinstance(janela_critica, bool):
        return False, "Janela crítica deve ser True ou False"
    return True, ""


def validar_entrega(entrega: Dict) -> Tuple[bool, List[str]]:
    """
    Função pura de ordem superior: valida todos os campos de uma entrega
    Usa map para aplicar validações e filter para capturar erros
    """
    validacoes = [
        validar_numero_positivo(entrega.get('peso', -1), 'Peso'),
        validar_numero_positivo(entrega.get('volume', -1), 'Volume'),
        validar_zona(entrega.get('zona', '')),
        validar_janela_critica(entrega.get('janela_critica', None))
    ]

    # Filter: filtra apenas validações que falharam
    erros = list(filter(lambda v: not v[0], validacoes))

    # Map: extrai apenas as mensagens de erro
    mensagens_erro = list(map(lambda e: e[1], erros))

    return len(erros) == 0, mensagens_erro


# ========== FUNÇÕES PURAS DE CÁLCULO ==========

def calcular_custo_base(zona: str) -> float:
    """
    Função pura: retorna o custo base da zona
    """
    return PRECOS_BASE_ZONA.get(zona, 0.0)


def calcular_pedagio(zona: str) -> float:
    """
    Função pura: retorna o custo do pedágio da zona
    """
    return PEDAGIO_POR_ZONA.get(zona, 0.0)


def calcular_sobretaxa_peso(peso: float) -> float:
    """
    Função pura: calcula sobretaxa por peso excedente
    Imutabilidade: não modifica o peso original
    """
    if peso > LIMITE_PESO_GRATIS:
        excedente = peso - LIMITE_PESO_GRATIS
        return excedente * SOBRETAXA_PESO
    return 0.0


def calcular_sobretaxa_volume(volume: float) -> float:
    """
    Função pura: calcula sobretaxa por volume excedente
    Imutabilidade: não modifica o volume original
    """
    if volume > LIMITE_VOLUME_GRATIS:
        excedente = volume - LIMITE_VOLUME_GRATIS
        return excedente * SOBRETAXA_VOLUME
    return 0.0


def calcular_custo_janela_critica(janela_critica: bool) -> float:
    """
    Função pura: retorna custo adicional para janela crítica
    """
    return CUSTO_JANELA_CRITICA if janela_critica else 0.0


def calcular_custo_entrega(entrega: Dict) -> Dict:
    """
    Função pura: calcula todos os componentes de custo de uma entrega
    Retorna novo dicionário sem modificar o original (imutabilidade)
    """
    # Extrai valores da entrega original (imutabilidade)
    zona = entrega['zona']
    peso = entrega['peso']
    volume = entrega['volume']
    janela_critica = entrega['janela_critica']

    # Calcula cada componente de custo
    custo_base = calcular_custo_base(zona)
    pedagio = calcular_pedagio(zona)
    sobretaxa_peso = calcular_sobretaxa_peso(peso)
    sobretaxa_volume = calcular_sobretaxa_volume(volume)
    custo_janela = calcular_custo_janela_critica(janela_critica)

    # Lista de componentes para usar reduce
    componentes = [custo_base, pedagio, sobretaxa_peso, sobretaxa_volume, custo_janela]

    # Reduce: soma todos os componentes
    total = reduce(lambda acc, valor: acc + valor, componentes, 0.0)

    # Retorna novo dicionário (imutabilidade)
    return {
        **entrega,  # Mantém dados originais
        'custo_base': custo_base,
        'pedagio': pedagio,
        'sobretaxa_peso': sobretaxa_peso,
        'sobretaxa_volume': sobretaxa_volume,
        'custo_janela_critica': custo_janela,
        'total': total
    }


def verificar_invariante(resultado: Dict) -> bool:
    """
    Função pura: verifica invariante (soma componentes == total)
    """
    componentes = [
        resultado['custo_base'],
        resultado['pedagio'],
        resultado['sobretaxa_peso'],
        resultado['sobretaxa_volume'],
        resultado['custo_janela_critica']
    ]
    soma_componentes = reduce(lambda acc, v: acc + v, componentes, 0.0)
    return abs(soma_componentes - resultado['total']) < 0.01


# ========== FUNÇÕES DE ORDEM SUPERIOR ==========

def processar_entregas(entregas: List[Dict]) -> List[Dict]:
    """
    Função de ordem superior: processa lista de entregas
    Usa map para aplicar cálculo a cada entrega
    """
    # Map: aplica cálculo de custo a cada entrega
    return list(map(calcular_custo_entrega, entregas))


def filtrar_entregas_validas(entregas: List[Dict]) -> List[Dict]:
    """
    Função de ordem superior: filtra apenas entregas válidas
    """
    # Filter: mantém apenas entregas válidas
    return list(filter(lambda e: validar_entrega(e)[0], entregas))


def calcular_total_geral(resultados: List[Dict]) -> float:
    """
    Função de ordem superior: calcula total geral de todas as entregas
    Usa reduce para somar todos os totais
    """
    return reduce(lambda acc, r: acc + r['total'], resultados, 0.0)


# ========== FUNÇÕES DE INTERFACE ==========

def formatar_resultado(resultado: Dict) -> str:
    """
    Função pura: formata resultado para exibição
    """
    return f"""
╔══════════════════════════════════════════════════════╗
║           DETALHAMENTO DA ENTREGA                    ║
╚══════════════════════════════════════════════════════╝
Zona: {resultado['zona']}
Peso: {resultado['peso']:.2f} kg
Volume: {resultado['volume']:.3f} m³
Janela Crítica: {'Sim' if resultado['janela_critica'] else 'Não'}

┌──────────────────────────────────────────────────────┐
│ CUSTOS DETALHADOS                                    │
├──────────────────────────────────────────────────────┤
│ Custo Base (Zona):        R$ {resultado['custo_base']:>10.2f} │
│ Pedágio:                  R$ {resultado['pedagio']:>10.2f} │
│ Sobretaxa Peso:           R$ {resultado['sobretaxa_peso']:>10.2f} │
│ Sobretaxa Volume:         R$ {resultado['sobretaxa_volume']:>10.2f} │
│ Custo Janela Crítica:     R$ {resultado['custo_janela_critica']:>10.2f} │
├──────────────────────────────────────────────────────┤
│ TOTAL:                    R$ {resultado['total']:>10.2f} │
└──────────────────────────────────────────────────────┘
Invariante verificado: {'✓ OK' if verificar_invariante(resultado) else '✗ ERRO'}
"""


def obter_entrada_usuario() -> Dict:
    """
    Função para obter entrada do usuário via terminal
    """
    print("\n" + "=" * 56)
    print("     SISTEMA DE CÁLCULO DE ENTREGAS URBANAS")
    print("=" * 56)

    try:
        zona = input("\nZona de destino (zona1/zona2/zona3/zona4): ").strip().lower()
        peso = float(input("Peso do pacote (kg): "))
        volume = float(input("Volume do pacote (m³): "))
        janela = input("Janela de entrega crítica? (s/n): ").strip().lower()

        return {
            'zona': zona,
            'peso': peso,
            'volume': volume,
            'janela_critica': janela == 's'
        }
    except ValueError:
        print("\nx Erro: Valor inválido inserido!")
        return None


# ========== PROGRAMA PRINCIPAL ==========

def main():
    """
    Função principal do programa
    """
    print("\n Sistema de Entrega Urbana - Programação Funcional")
    print("Desenvolvido por: Rafael Zink\n")

    # Obter entrada do usuário
    entrega = obter_entrada_usuario()

    if entrega is None:
        return

    # Validar entrada (função pura)
    valido, erros = validar_entrega(entrega)

    if not valido:
        print("\nx ERROS DE VALIDAÇÃO:")
        for erro in erros:
            print(f"   • {erro}")
        return

    print("\n✓ Entrega validada com sucesso!")

    # Calcular custos (função pura)
    resultado = calcular_custo_entrega(entrega)

    # Exibir resultado
    print(formatar_resultado(resultado))

    # Exemplo com múltiplas entregas (demonstrando map e reduce)
    print("\n" + "=" * 56)
    print("     EXEMPLO: PROCESSAMENTO EM LOTE")
    print("=" * 56)

    entregas_exemplo = [
        {'zona': 'zona1', 'peso': 5.0, 'volume': 0.3, 'janela_critica': False},
        {'zona': 'zona2', 'peso': 15.0, 'volume': 0.8, 'janela_critica': True},
        {'zona': 'zona3', 'peso': 8.0, 'volume': 0.4, 'janela_critica': False},
    ]

    # Map: processa todas as entregas
    resultados = processar_entregas(entregas_exemplo)

    # Reduce: calcula total geral
    total_geral = calcular_total_geral(resultados)

    print(f"\nTotal de entregas processadas: {len(resultados)}")
    print(f"Valor total geral: R$ {total_geral:.2f}")

    # Map: mostra resumo de cada entrega
    for i, r in enumerate(resultados, 1):
        print(f"\nEntrega {i}: {r['zona']} - R$ {r['total']:.2f}")


if __name__ == "__main__":
    main()