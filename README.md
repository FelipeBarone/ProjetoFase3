Sistema Integrado de Gestão Energética e Suporte à Vida da Colônia

Esse repositório contém a implementação do sistema autônomo de gestão energética e tomada de decisão para uma colônia espacial. Este sistema foi criado com auxílio da IA Gemini para sofisticar o código sem dependências de bibliotecas externas, desenvolvido em Python. O Programa combina estruturas de dados hierárquicas, modelo de regressão linear simples por mínimos quadrados e lógica de seleção de cargas com corte seletivo de funções não primárias para priorizar o sistema de suporte à vida.

A Arquitetura do Sistema é modularizada em quatro camadas lógicas:

1. Sensores e Estruturas de Dados

2. Módulo Preditivo (Regressão)
Previsão de Geração Eólica: y = mx + b

3. Balanço Energético e Lógica de decisão

4. Atuador e Painel de Telemetria

Em relação a componentes do Software, a colônia é representada por dicionários  com variáveis climáticas, reserva energética e cargas elétricas:

- Sensores Ambientais que monitoram a velocidade do vento (km/h) e radiação solar (0% a 100%)

- Armazenamento que monitora carga percentual da bateria e define limites operacionais

- Subsistemas críticos que coloca suporte de vida e comunicações de emergência como prioridade essencial e jamais são desativados

- Subsistemas secundários como complexo de mineração, estudas hidropônicas, laboratório de pesquisa e iluminação que podem sofrer corte conforme a gravidade da economia energética.
 
A execução do arquivo roda três cenários predefinidos para validação dos protocolos:

Cenário 1: Déficit com Bateria Intermediária

Entradas: Vento = 11.0 KM/H, Radiação Solar = 0% e Bateria = 40.0%

Processamento: Geração Eólica Prevista = 27.5 kW, Consumo Inicial = 85.0 kW

Saída Gerada:

=================================================================
 CENÁRIO 1: DÉFICIT COM BATERIA INTERMEDIÁRIA
=================================================================
 Condições: Vento = 11.0 km/h | Radiação = 0%
 Geração Prevista: Eólica = 27.5 kW | Solar = 0.0 kW
 Geração Total: 27.5 kW
 Nível da Bateria: 40.0%
 Consumo: Inicial = 85.0 kW -> Pós-Ação = 55.0 kW
 Balanço Operacional Resultante: -27.5 kW
-----------------------------------------------------------------
 Mensagens do Sistema:
  [*] ALERTA: Consumo (85.0 kW) supera a geração (27.5 kW) [Déficit: -57.5 kW]
  [*] ATENÇÃO: Bateria em nível intermediário (< 50%). Ativando modo econômico.
 Ações Automáticas de Controle:
  [!] Modo Economia: desligando subsistema complexo_mineracao
  [!] Modo Economia: desligando subsistema iluminacao_auxiliar
=================================================================
 
Cenário 2: Crítico com Salvaguarda de Vida
Entradas: Vento = 4.0 km/h, Radiação Solar = 0%, Bateria = 22.0%
Processamento: Geração Eólica Prevista = 10.0 kW | Consumo Inicial = 55.0 kW | Bateria < 30%
Saída Gerada:
=================================================================
 CENÁRIO 2: CRÍTICO COM SALVAGUARDA DE VIDA
=================================================================
 Condições: Vento = 4.0 km/h | Radiação = 0%
 Geração Prevista: Eólica = 10.0 kW | Solar = 0.0 kW
 Geração Total: 10.0 kW
 Nível da Bateria: 22.0%
 Consumo: Inicial = 55.0 kW -> Pós-Ação = 35.0 kW
 Balanço Operacional Resultante: -25.0 kW
-----------------------------------------------------------------
 Mensagens do Sistema:
  [*] ALERTA: Consumo (55.0 kW) supera a geração (10.0 kW) [Déficit: -45.0 kW]
  [*] CRÍTICO: Bateria abaixo de 30% com geração deficitária.
 Ações Automáticas de Controle:
  [!] Alerta Crítico: corte do subsistema estufas_hidroponicas
  [!] Alerta Crítico: corte do subsistema laboratorio_pesquisa
=================================================================
 
Cenário 3: Superávit e Restauração Plena
Entradas: Vento = 24.0 km/h, Radiação Solar = 90%, Bateria = 85.0%
Processamento: Eólica = 60.0 kW, Solar = 36.0 kW (Total: 96.0 kW) | Consumo Nominal Restaurado = 85.0 kW
Saída Gerada:
=================================================================
 CENÁRIO 3: SUPERÁVIT E RESTAURAÇÃO PLENA
=================================================================
 Condições: Vento = 24.0 km/h | Radiação = 90%
 Geração Prevista: Eólica = 60.0 kW | Solar = 36.0 kW
 Geração Total: 96.0 kW
 Nível da Bateria: 85.0%
 Consumo: Inicial = 35.0 kW -> Pós-Ação = 85.0 kW
 Balanço Operacional Resultante: 11.0 kW
-----------------------------------------------------------------
 Mensagens do Sistema:
  [*] GERAÇÃO SUPERAVITÁRIA: Excedente de 61.0 kW gerado.
  [*] SUGESTÃO: Direcionando excedente para recarga das baterias.
 Ações Automáticas de Controle:
  [!] Religando subsistema: estufas_hidroponicas
  [!] Religando subsistema: complexo_mineracao
  [!] Religando subsistema: laboratorio_pesquisa
  [!] Religando subsistema: iluminacao_auxiliar
================================================================= 

Como Executar:
1. Python 3.8 ou superior
2. Clone o repositório ou baixe os arquivos
