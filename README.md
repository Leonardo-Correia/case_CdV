# Execution Case — Análise de Restrição COFF e SPEs Eólicas

Este repositório contém um notebook Jupyter para análise de dados de geração eólica, restrições COFF e desempenho de SPEs da Casa dos Ventos, a partir de bases do ONS. O fluxo inclui ingestão de CSVs, limpeza, integração de dados, análise exploratória, classificação de condições operacionais, modelagem preditiva da geração esperada e criação de um score por CEG/SPE.

## Estrutura esperada

```text
.
├── execution_case.ipynb
├── README.md
├── requirements.txt
└── data/                         # sugestão de organização local
    ├── dados_restricao_cof_SPEs/
    ├── dados_restricao_detalhamento_SPEs/
    └── spes_casa_dos_ventos.csv
```

> OBS - O caminho dos arquivo DEVEM ser ajustados de acordo com o caminho de pastas deseajado.

## Como executar

1. Instale as dependências:

```
pip install -r requirements.txt
```

2. Executar os scripts de scrap de dados 

```bash
python scrap_dados_cof_detail.py 
python scrap_dados_cof.py 
```

3. Organize os dados de entrada na pasta `data/`, seguindo a estrutura sugerida acima.

4. Ajuste os caminhos no notebook, se necessário:

5. Execute o notebook:

```bash
jupyter notebook execution_case.ipynb
```

## Variáveis de ambiente opcionais

O notebook possui uma função opcional para envio de relatório de qualidade por e-mail. Para utilizá-la, crie um arquivo `.env` na raiz do projeto:

```env
EMAIL_ADDRESS=seu_email@example.com
EMAIL_APP_PASSWORD=sua_senha_de_app
```

## Fluxo da solução

1. **Ingestão dos dados**
   - Leitura de múltiplos arquivos CSV separados por `;`.
   - Normalização dos nomes das colunas.
   - Conversão da coluna `din_instante` para datetime.

2. **Limpeza e validação**
   - Conversão de colunas numéricas.
   - Remoção de duplicidades.
   - Remoção de valores negativos inválidos.
   - Remoção de nulos críticos.
   - Filtro de registros com vento inválido.
   - Geração de relatório de qualidade.

3. **Integração das bases**
   - Extração do núcleo do código CEG.
   - Filtro das SPEs da Casa dos Ventos via arquivo de mapeamento.
   - Agregação por projeto, CEG e instante.
   - Merge entre dados de detalhamento e restrição COFF.

4. **Análise exploratória**
   - Estatísticas por estado, subsistema, projeto e tipo de restrição.
   - Curvas de potência por CEG.
   - Médias mensais de vento e geração.
   - Distribuição da velocidade do vento e comparação com distribuição Weibull.

5. **Modelagem**
   - Criação de variável de restrição ativa.
   - Classificação operacional com base nas restrições do ONS.
   - Clusterização com DBSCAN para filtrar pontos operacionais normais.
   - Treinamento de um `MLPRegressor` por CEG para estimar geração esperada a partir da velocidade do vento.
   - Avaliação por RMSE e R².

6. **Cálculo de perdas e score**
   - Estimativa de geração potencial.
   - Cálculo de perdas por constrained-off.
   - Disponibilidade energética.
   - Fator de capacidade.
   - Variância do vento.
   - Janela de potência nominal.
   - Score ponderado por CEG/SPE.

## Decisões técnicas

- **Pandas** foi usado como ferramenta principal de manipulação de dados por simplicidade e pelo volume/estrutura tabular do problema, .
- **DBSCAN** foi escolhido para separar regiões de operação normal sem exigir número prévio de clusters. Esse modelo é ideal para remover os outliers pois relaciona o número de elementos em um disco de raio pré-definido. 
- **MLPRegressor** foi usado para modelar a relação não linear entre velocidade do vento e geração verificada. A aparência das curvas de potência é semelahnte à uma sigmoide que ajuda em modelos com essa func de ativação. Entre os modelos avaliados, foi o que mostrou melhores resultados.
- **Normalização com StandardScaler** foi aplicada antes da modelagem neural para estabilizar o treinamento com muitos dados.
- **Score ponderado** foi adotado por ser simples, interpretável e ajustável conforme prioridades de negócio. 

## Sugestões 

- Utilizar um melhor framwork de manipulação de dados como pyspark.
- Testar outros métodos para remoção de outliers. Limitação por quantis não indicou bons resultados como indica a fig curv_wxp_percentil.png

## Premissas assumidas

- Os arquivos CSV de entrada seguem o padrão de separador `;`, encoding `utf-8` e decimal `,`.
- A coluna temporal principal chama-se `din_instante`.
- O código CEG possui estrutura separada por pontos, permitindo extrair o núcleo do CEG a partir da quarta posição.
- O arquivo `spes_casa_dos_ventos.csv` contém, no mínimo, as colunas `projeto`, `spe` e `ceg`.
- Valores negativos nas colunas de geração, disponibilidade e vento são tratados como inválidos.
- A flag `flg_dadoventoinvalido == 1` indica registro de vento inválido.
- Cada registro representa intervalo de 30 minutos; por isso, a energia em MWh é estimada multiplicando potência por `0.5`.
- A geração predita pelo modelo é usada como aproximação da geração potencial sem restrição.
- A potência projetada foi estimada como a potência nominal. 
- Os pesos do score foram definidos de forma heurística e podem ser ajustados conforme critérios de negócio.
