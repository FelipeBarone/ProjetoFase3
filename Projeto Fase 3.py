"""SISTEMA INTEGRADO DE GESTÃO ENERGÉTICA E SUPORTE À VIDA DA COLÔNIA

Módulos:
1. Estrutura e Inicialização dos Dados
2. Modelagem Matemática Preditiva (Regressão Linear)
3. Análise de Balanço e Priorização de Subsistemas
4. Tomada de Decisão e Protocolos de Operação
5. Execução de Simulações e Cenários de Teste
"""


# ==============================================================================
# 1. ESTRUTURAÇÃO HIERÁRQUICA DOS DADOS DA COLÔNIA
# ==============================================================================


def inicializar_colonia():
    """Cria e retorna a estrutura hierárquica inicial da colônia.

    Utiliza dicionários e listas nativas para representar variáveis
    climáticas, armazenamento e subsistemas categorizados por prioridade de
    corte.
    """
    return {
        "sensores_ambientais": {
            "vento_kmh": 0.0,
            "radiacao_solar_pct": 0.0,  # 0.0 a 1.0 (0 a 100% de sol)
        },
        "sistema_armazenamento": {
            "bateria_atual": 45.0,  # Nível atual em %
            "capacidade_maxima": 100.0,  # Capacidade total em %
            "limiar_critico": 30.0,  # Bateria mínima aceitável
            "limiar_seguro": 50.0,  # Bateria para operação sem restrições
        },
        "subsistemas_consumo": {
            # Prioridade 1: Sistemas essenciais para sobrevivência (nunca desligam)
            "criticos": {
                "suporte_de_vida": {
                    "consumo_nominal": 30.0,
                    "ativo": True,
                    "essencial": True,
                },
                "comunicacoes_emergencia": {
                    "consumo_nominal": 5.0,
                    "ativo": True,
                    "essencial": True,
                },
            },
            # Prioridade 2: Sistemas produtivos / científicos (desligáveis em alerta)
            "secundarios": {
                "estufas_hidroponicas": {
                    "consumo_nominal": 15.0,
                    "ativo": True,
                    "essencial": False,
                },
                "complexo_mineracao": {
                    "consumo_nominal": 25.0,
                    "ativo": True,
                    "essencial": False,
                },
                "laboratorio_pesquisa": {
                    "consumo_nominal": 10.0,
                    "ativo": True,
                    "essencial": False,
                },
                "iluminacao_auxiliar": {
                    "consumo_nominal": 5.0,
                    "ativo": True,
                    "essencial": False,
                },
            },
        },
    }


# ==============================================================================
# 2. MODELAGEM MATEMÁTICA E PREVISÃO (REGRESSÃO LINEAR)
# ==============================================================================


def treinar_regressao_linear(historico_x, historico_y):
    """Calcula os coeficientes angular (m) e linear (b) da reta y = mx + b."""
    n = len(historico_x)
    if n != len(historico_y) or n < 2:
        raise ValueError("Dados insuficientes ou de tamanhos incompatíveis.")

    soma_x = sum(historico_x)
    soma_y = sum(historico_y)
    soma_xy = sum(x * y for x, y in zip(historico_x, historico_y)) #Utilização da função zip para juntar dois iteráveis em um
    soma_x2 = sum(x**2 for x in historico_x)

    denominador = n * soma_x2 - (soma_x**2)
    if denominador == 0:
        raise ZeroDivisionError(
            "Variação nula nas variáveis de entrada (x constante)."
        )

    # Coeficiente angular (m) e coeficiente linear (b)
    m = (n * soma_xy - soma_x * soma_y) / denominador
    b = (soma_y - m * soma_x) / n

    return m, b


def prever_geracao_eolica(velocidade_vento, m, b):
    """Estima a geração de energia eólica a partir da velocidade do vento."""
    if velocidade_vento < 0:
        return 0.0
    estimativa = (m * velocidade_vento) + b
    # A geração física não pode ser negativa
    return max(0.0, round(estimativa, 2))


def estimar_geracao_solar(radiacao_pct, potencia_pico=40.0):
    """Calcula a geração solar baseada na radiação instantânea e capacidade instalada."""
    fator_radiacao = max(0.0, min(1.0, radiacao_pct))
    return round(fator_radiacao * potencia_pico, 2)


# ==============================================================================
# 3. GERENCIAMENTO DE CARGAS E CONSUMO
# ==============================================================================


def calcular_consumo_ativo(subsistemas_consumo):
    """Varre a hierarquia de subsistemas e calcula a demanda de energia atual."""
    consumo_total = 0.0

    for categoria in ["criticos", "secundarios"]:
        for nome, propriedades in subsistemas_consumo[categoria].items():
            if propriedades["ativo"]:
                consumo_total += propriedades["consumo_nominal"]

    return round(consumo_total, 2)


def ajustar_cargas(subsistemas_consumo, modo):
    """Altera o status dos subsistemas conforme a política energética exigida.

    - Modo 'NOMINAL': todos os subsistemas ativos.
    - Modo 'ECONOMIA': desliga metade dos secundários (mineração e iluminação auxiliar).
    - Modo 'EMERGENCIA': desliga todos os secundários; mantém apenas críticos.
    """
    acoes_executadas = []

    if modo == "NOMINAL":
        for nome, prop in subsistemas_consumo["secundarios"].items():
            if not prop["ativo"]:
                prop["ativo"] = True
                acoes_executadas.append(f"Religando subsistema: {nome}")

    elif modo == "ECONOMIA":
        # Desliga os maiores consumidores não essenciais
        desligar = ["complexo_mineracao", "iluminacao_auxiliar"]
        for nome in desligar:
            if subsistemas_consumo["secundarios"][nome]["ativo"]:
                subsistemas_consumo["secundarios"][nome]["ativo"] = False
                acoes_executadas.append(
                    f"Modo Economia: desligando subsistema {nome}"
                )

    elif modo == "EMERGENCIA":
        # Desliga todos os sistemas secundários, preservando suporte à vida
        for nome, prop in subsistemas_consumo["secundarios"].items():
            if prop["ativo"]:
                prop["ativo"] = False
                acoes_executadas.append(
                    f"Alerta Crítico: corte do subsistema {nome}"
                )

    return acoes_executadas


# ==============================================================================
# 4. BALANÇO ENERGÉTICO E LÓGICA DE DECISÃO
# ==============================================================================


def processar_ciclo_colonia(colonia, vento_medido, radiacao_medida, modelo_m, modelo_b):
    """Executa um ciclo completo de monitoramento, previsão e controle inteligente.

    Etapas:
    1. Previsão de geração com regressão linear.
    2. Leitura do consumo nominal e balanço energético.
    3. Aplicação de regras lógicas de prioridade e salvaguarda.
    4. Atualização de status da bateria.
    """
    # 1. Atualizar sensores e estimar geração
    colonia["sensores_ambientais"]["vento_kmh"] = vento_medido
    colonia["sensores_ambientais"]["radiacao_solar_pct"] = radiacao_medida

    gen_eolica = prever_geracao_eolica(vento_medido, modelo_m, modelo_b)
    gen_solar = estimar_geracao_solar(radiacao_medida)
    geracao_total = round(gen_eolica + gen_solar, 2)

    # 2. Leitura de estado e consumo
    consumo_inicial = calcular_consumo_ativo(colonia["subsistemas_consumo"])
    bateria = colonia["sistema_armazenamento"]["bateria_atual"]
    balanco = round(geracao_total - consumo_inicial, 2)

    alertas = []
    acoes_corte = []

    # 3. Lógica de Decisão e Regras Condicionais
    if balanco < 0:
        alertas.append(
            f"ALERTA: Consumo ({consumo_inicial} kW) supera a geração ({geracao_total} kW) [Déficit: {balanco} kW]"
        )

        # Regra combinada: déficit + bateria baixa
        if bateria < colonia["sistema_armazenamento"]["limiar_critico"]:
            alertas.append(
                "CRÍTICO: Bateria abaixo de 30% com geração deficitária."
            )
            acoes_corte = ajustar_cargas(
                colonia["subsistemas_consumo"], modo="EMERGENCIA"
            )
        elif bateria < colonia["sistema_armazenamento"]["limiar_seguro"]:
            alertas.append(
                "ATENÇÃO: Bateria em nível intermediário (< 50%). Ativando modo econômico."
            )
            acoes_corte = ajustar_cargas(
                colonia["subsistemas_consumo"], modo="ECONOMIA"
            )
        else:
            alertas.append(
                "Bateria acima de 50%: amortecendo déficit temporário sem cortes de carga."
            )

    elif balanco > 0:
        alertas.append(
            f"GERAÇÃO SUPERAVITÁRIA: Excedente de {balanco} kW gerado."
        )
        if bateria < colonia["sistema_armazenamento"]["capacidade_maxima"]:
            alertas.append(
                "SUGESTÃO: Direcionando excedente para recarga das baterias."
            )
        else:
            alertas.append(
                "Baterias em 100%: dissipando ou armazenando calor auxiliar."
            )

        # Restaura sistemas se a geração for estável e a bateria estiver segura
        if bateria >= colonia["sistema_armazenamento"]["limiar_seguro"]:
            acoes_corte = ajustar_cargas(
                colonia["subsistemas_consumo"], modo="NOMINAL"
            )

    else:
        alertas.append("SISTEMA EQUILIBRADO: Geração e consumo equivalentes.")

    # 4. Recálculo pós-decisão
    consumo_final = calcular_consumo_ativo(colonia["subsistemas_consumo"])
    balanco_final = round(geracao_total - consumo_final, 2)

    return {
        "vento": vento_medido,
        "radiacao": radiacao_medida,
        "geracao_eolica": gen_eolica,
        "geracao_solar": gen_solar,
        "geracao_total": geracao_total,
        "consumo_inicial": consumo_inicial,
        "consumo_final": consumo_final,
        "balanco_final": balanco_final,
        "bateria": bateria,
        "alertas": alertas,
        "acoes": acoes_corte,
    }


def exibir_painel_telemetria(titulo_cenario, relatorio):
    """Formata e imprime o relatório operacional do ciclo no terminal."""
    print("\n" + "=" * 65)
    print(f" {titulo_cenario.upper()}")
    print("=" * 65)
    print(
        f" Condições: Vento = {relatorio['vento']} km/h | Radiação = {int(relatorio['radiacao'] * 100)}%"
    )
    print(
        f" Geração Prevista: Eólica = {relatorio['geracao_eolica']} kW | Solar = {relatorio['geracao_solar']} kW"
    )
    print(f" Geração Total: {relatorio['geracao_total']} kW")
    print(f" Nível da Bateria: {relatorio['bateria']}%")
    print(
        f" Consumo: Inicial = {relatorio['consumo_inicial']} kW -> Pós-Ação = {relatorio['consumo_final']} kW"
    )
    print(f" Balanço Operacional Resultante: {relatorio['balanco_final']} kW")
    print("-" * 65)
    print(" Mensagens do Sistema:")
    for alerta in relatorio["alertas"]:
        print(f"  [*] {alerta}")
    if relatorio["acoes"]:
        print(" Ações Automáticas de Controle:")
        for acao in relatorio["acoes"]:
            print(f"  [!] {acao}")
    else:
        print(" Ações Automáticas de Controle: Nenhuma alteração exigida.")
    print("=" * 65)


# ==============================================================================
# 5. EXECUÇÃO E SIMULAÇÃO DOS CENÁRIOS DE TESTE
# ==============================================================================


def main():
    # Calibração do Modelo de Regressão Linear Simples
    # Histórico de calibração: vento (km/h) vs energia gerada (kW)
    historico_vento = [8.0, 10.0, 12.0]
    historico_energia = [20.0, 25.0, 30.0]

    m, b = treinar_regressao_linear(historico_vento, historico_energia)
    print(">>> MODELO PREDITIVO CALIBRADO COM SUCESSO <<<")
    print(f"Reta de Regressão: Energia = {m:.2f} * Vento + {b:.2f}")

    # Instancia a colônia
    colonia = inicializar_colonia()

    # Cenário 1: Vento Moderado (11 km/h), sem sol, bateria em nível moderado (40%)
    # Previsão esperada de eólica: 2.5 * 11 + 0 = 27.5 kW. Consumo total = 85 kW.
    colonia["sistema_armazenamento"]["bateria_atual"] = 40.0
    relatorio_c1 = processar_ciclo_colonia(
        colonia=colonia,
        vento_medido=11.0,
        radiacao_medida=0.0,
        modelo_m=m,
        modelo_b=b,
    )
    exibir_painel_telemetria("Cenário 1: Déficit com Bateria Intermediária", relatorio_c1)

    # Cenário 2: Calmaria (vento = 4 km/h), noite, bateria crítica (22%)
    # Previsão: 10 kW eólica. Consumo alto -> Ativa emergência e desliga tudo secundário
    colonia["sistema_armazenamento"]["bateria_atual"] = 22.0
    relatorio_c2 = processar_ciclo_colonia(
        colonia=colonia,
        vento_medido=4.0,
        radiacao_medida=0.0,
        modelo_m=m,
        modelo_b=b,
    )
    exibir_painel_telemetria("Cenário 2: Crítico com Salvaguarda de Vida", relatorio_c2)

    # Cenário 3: Vento Alto (24 km/h) e Dia Ensolarado (90%), Bateria em 85%
    # Previsão eólica: 60 kW + solar 36 kW = 96 kW gerados. Superávit total.
    colonia["sistema_armazenamento"]["bateria_atual"] = 85.0
    relatorio_c3 = processar_ciclo_colonia(
        colonia=colonia,
        vento_medido=24.0,
        radiacao_medida=0.9,
        modelo_m=m,
        modelo_b=b,
    )
    exibir_painel_telemetria("Cenário 3: Superávit e Restauração Plena", relatorio_c3)


if __name__ == "__main__":
    main()