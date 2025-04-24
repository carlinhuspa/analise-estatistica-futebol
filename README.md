# README - Aplicação de Análise Estatística de Futebol

## Visão Geral

Esta aplicação Streamlit foi desenvolvida para realizar análises estatísticas detalhadas de partidas de futebol. O programa permite que você cole o texto com estatísticas de uma partida e obtenha automaticamente uma análise completa, incluindo confrontos diretos, forma recente das equipes, posições nas tabelas, análise de textos e prognósticos, além de predições baseadas em modelos matemáticos.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
/
├── app.py                    # Aplicação principal Streamlit
├── test_app.py               # Script para testar a aplicação localmente
├── create_requirements.py    # Script para gerar o arquivo requirements.txt
├── requirements.txt          # Dependências do projeto
├── guia_publicacao_streamlit.md  # Guia passo a passo para publicação
├── utils/                    # Módulos utilitários
│   ├── __init__.py
│   ├── text_extractor.py     # Extração de dados do texto
│   ├── data_processor.py     # Processamento dos dados extraídos
│   └── visualizer.py         # Criação de visualizações
└── analyzers/                # Módulos de análise
    ├── __init__.py
    ├── head_to_head.py       # Análise de confrontos diretos
    ├── recent_form.py        # Análise da forma recente
    ├── table_positions.py    # Análise das posições nas tabelas
    ├── text_predictions.py   # Análise de textos e prognósticos
    └── prediction_models.py  # Modelos matemáticos para predições
```

## Funcionalidades

A aplicação oferece as seguintes funcionalidades:

1. **Extração de Dados**: Extrai automaticamente informações relevantes do texto fornecido.
2. **Análise de Confrontos Diretos**: Analisa o histórico de confrontos entre as equipes.
3. **Análise da Forma Recente**: Avalia o desempenho recente de cada equipe.
4. **Análise das Posições nas Tabelas**: Examina as posições das equipes nas tabelas geral, mandante e visitante.
5. **Análise de Textos e Prognósticos**: Analisa textos de análise e prognósticos disponíveis.
6. **Modelos Matemáticos**: Implementa modelos estatísticos para predição de resultados.
7. **Visualizações**: Gera gráficos e visualizações para facilitar a compreensão dos dados.

## Como Usar

### Execução Local

1. Certifique-se de ter todas as dependências instaladas:
   ```
   pip install -r requirements.txt
   ```

2. Execute o script de teste para verificar se tudo está configurado corretamente:
   ```
   python test_app.py
   ```

3. Acesse a aplicação em seu navegador através do endereço fornecido (geralmente http://localhost:8501).

4. Cole o texto com as estatísticas da partida na área de texto.

5. Clique no botão "Analisar Estatísticas" e explore os resultados nas diferentes abas.

### Publicação no Streamlit Cloud

Para publicar a aplicação no Streamlit Cloud, siga as instruções detalhadas no arquivo `guia_publicacao_streamlit.md`.

## Requisitos

As principais dependências do projeto são:

- streamlit==1.22.0
- pandas==1.5.3
- numpy==1.24.3
- matplotlib==3.7.1
- plotly==5.14.1
- scipy==1.10.1
- scikit-learn==1.2.2

Para gerar o arquivo `requirements.txt` automaticamente, execute:
```
python create_requirements.py
```

## Notas Importantes

- A aplicação foi projetada para processar textos com um formato específico de estatísticas de futebol.
- Os modelos matemáticos implementados são simplificações e devem ser usados apenas como referência.
- As predições são baseadas em dados históricos e não consideram fatores imprevisíveis como lesões, condições climáticas, etc.

## Próximos Passos

Algumas melhorias que podem ser implementadas no futuro:

1. Suporte para diferentes formatos de entrada de dados
2. Modelos matemáticos mais avançados
3. Análise de mais métricas e estatísticas
4. Integração com APIs de dados de futebol em tempo real
5. Personalização das visualizações e relatórios

---

Desenvolvido com ❤️ para análise estatística de futebol
