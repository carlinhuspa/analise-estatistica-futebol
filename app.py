import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import os
import sys
import re
from typing import Dict, List, Tuple, Any, Optional

# Adicionar diretórios ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar módulos personalizados
from utils.text_extractor import FootballStatsExtractor
from utils.data_processor import FootballDataProcessor
from utils.visualizer import FootballVisualizer
from analyzers.head_to_head import HeadToHeadAnalyzer
from analyzers.recent_form import RecentFormAnalyzer
from analyzers.table_positions import TablePositionsAnalyzer
from analyzers.text_predictions import TextPredictionsAnalyzer
from analyzers.prediction_models import FootballPredictionModels

# Configuração da página
st.set_page_config(
    page_title="Análise Estatística de Futebol",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para processar o texto de entrada e extrair dados
def process_input_text(text: str) -> Dict[str, Any]:
    # Extrair dados do texto
    extractor = FootballStatsExtractor(text)
    extracted_data = extractor.extract_all_data()
    
    # Processar os dados extraídos
    processor = FootballDataProcessor(extracted_data)
    processed_data = processor.process_all_data()
    
    return processed_data

# Função para analisar os dados processados
def analyze_data(processed_data: Dict[str, Any]) -> Dict[str, Any]:
    # Analisar confrontos diretos
    h2h_analyzer = HeadToHeadAnalyzer(processed_data)
    h2h_analysis = h2h_analyzer.run_complete_analysis()
    
    # Analisar forma recente
    form_analyzer = RecentFormAnalyzer(processed_data)
    form_analysis = form_analyzer.run_complete_analysis()
    
    # Analisar posições nas tabelas
    table_analyzer = TablePositionsAnalyzer(processed_data)
    table_analysis = table_analyzer.run_complete_analysis()
    
    # Analisar textos e prognósticos
    text_analyzer = TextPredictionsAnalyzer(processed_data)
    text_analysis = text_analyzer.run_complete_analysis()
    
    # Executar modelos matemáticos
    models = FootballPredictionModels(processed_data)
    models_analysis = models.run_complete_analysis()
    
    return {
        "head_to_head": h2h_analysis,
        "recent_form": form_analysis,
        "table_positions": table_analysis,
        "text_predictions": text_analysis,
        "prediction_models": models_analysis
    }

# Função para criar visualizações
def create_visualizations(processed_data: Dict[str, Any]) -> Dict[str, Any]:
    visualizer = FootballVisualizer(processed_data)
    all_visualizations = visualizer.create_all_visualizations()
    # Não salvamos mais as visualizações como arquivos
    # Apenas retornamos os objetos de visualização diretamente
    return all_visualizations

# Função para exibir insights
def display_insights(analysis: Dict[str, Any], visualizations: Dict[str, Any]):
    home_team = analysis.get("head_to_head", {}).get("historical_dominance", {}).get("home_team", "Mandante")
    away_team = analysis.get("head_to_head", {}).get("historical_dominance", {}).get("away_team", "Visitante")
    
    st.header(f"📊 Análise: {home_team} vs {away_team}")
    
    # Criar abas para diferentes tipos de análise
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Confrontos Diretos", 
        "Forma Recente", 
        "Posições nas Tabelas", 
        "Textos e Prognósticos",
        "Modelos Matemáticos"
    ])
    
    # Aba de Confrontos Diretos
    with tab1:
        h2h_insights = analysis.get("head_to_head", {}).get("insights", [])
        if h2h_insights:
            st.subheader("Insights dos Confrontos Diretos")
            for insight in h2h_insights:
                st.write(f"• {insight}")
            
            # Exibir visualizações de confrontos diretos
            st.subheader("Visualizações")
            h2h_viz = visualizations.get("head_to_head", {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                if "results_distribution" in h2h_viz:
                    st.plotly_chart(h2h_viz["results_distribution"], use_container_width=True)
            
            with col2:
                if "last_matches" in h2h_viz:
                    st.plotly_chart(h2h_viz["last_matches"], use_container_width=True)
            
            if "goals_stats" in h2h_viz:
                st.plotly_chart(h2h_viz["goals_stats"], use_container_width=True)
        else:
            st.warning("Não foi possível gerar insights para os confrontos diretos.")
    
    # Aba de Forma Recente
    with tab2:
        form_insights = analysis.get("recent_form", {}).get("insights", [])
        if form_insights:
            st.subheader("Insights da Forma Recente")
            for insight in form_insights:
                st.write(f"• {insight}")
            
            # Exibir visualizações de forma recente
            st.subheader("Visualizações")
            form_viz = visualizations.get("team_form", {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                if home_team in form_viz and "results_distribution" in form_viz[home_team]:
                    st.plotly_chart(form_viz[home_team]["results_distribution"], use_container_width=True)
                    st.caption(f"Distribuição de resultados: {home_team}")
            
            with col2:
                if away_team in form_viz and "results_distribution" in form_viz[away_team]:
                    st.plotly_chart(form_viz[away_team]["results_distribution"], use_container_width=True)
                    st.caption(f"Distribuição de resultados: {away_team}")
            
            col3, col4 = st.columns(2)
            
            with col3:
                if home_team in form_viz and "goals" in form_viz[home_team]:
                    st.plotly_chart(form_viz[home_team]["goals"], use_container_width=True)
                    st.caption(f"Gols nos últimos jogos: {home_team}")
            
            with col4:
                if away_team in form_viz and "goals" in form_viz[away_team]:
                    st.plotly_chart(form_viz[away_team]["goals"], use_container_width=True)
                    st.caption(f"Gols nos últimos jogos: {away_team}")
        else:
            st.warning("Não foi possível gerar insights para a forma recente.")
    
    # Aba de Posições nas Tabelas
    with tab3:
        table_insights = analysis.get("table_positions", {}).get("insights", [])
        if table_insights:
            st.subheader("Insights das Posições nas Tabelas")
            for insight in table_insights:
                st.write(f"• {insight}")
            
            # Exibir visualizações de posições nas tabelas
            st.subheader("Visualizações")
            table_viz = visualizations.get("table_positions", {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                if "general_positions" in table_viz:
                    st.plotly_chart(table_viz["general_positions"], use_container_width=True)
            
            with col2:
                if "specific_positions" in table_viz:
                    st.plotly_chart(table_viz["specific_positions"], use_container_width=True)
            
            if "direct_comparison" in table_viz:
                st.plotly_chart(table_viz["direct_comparison"], use_container_width=True)
        else:
            st.warning("Não foi possível gerar insights para as posições nas tabelas.")
    
    # Aba de Textos e Prognósticos
    with tab4:
        text_insights = analysis.get("text_predictions", {}).get("insights", [])
        if text_insights:
            st.subheader("Insights dos Textos e Prognósticos")
            for insight in text_insights:
                st.write(f"• {insight}")
            
            # Exibir análise textual completa
            gpt_analysis = analysis.get("text_predictions", {}).get("gpt_analysis", {}).get("gpt_analysis", "")
            if gpt_analysis:
                with st.expander("Ver análise textual completa"):
                    st.write(gpt_analysis)
            
            # Exibir visualizações de prognósticos
            st.subheader("Visualizações")
            pred_viz = visualizations.get("predictions", {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                if "general_predictions" in pred_viz:
                    st.plotly_chart(pred_viz["general_predictions"], use_container_width=True)
            
            with col2:
                if "goals_detailed" in pred_viz:
                    st.plotly_chart(pred_viz["goals_detailed"], use_container_width=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                if "corners" in pred_viz:
                    st.plotly_chart(pred_viz["corners"], use_container_width=True)
            
            with col4:
                if "first_goal" in pred_viz:
                    st.plotly_chart(pred_viz["first_goal"], use_container_width=True)
        else:
            st.warning("Não foi possível gerar insights para os textos e prognósticos.")
    
    # Aba de Modelos Matemáticos
    with tab5:
        models_insights = analysis.get("prediction_models", {}).get("insights", [])
        if models_insights:
            st.subheader("Insights dos Modelos Matemáticos")
            for insight in models_insights:
                st.write(f"• {insight}")
            
            # Exibir resultados detalhados dos modelos
            ensemble_results = analysis.get("prediction_models", {}).get("ensemble_results", {})
            if ensemble_results:
                # Criar gráfico de probabilidades de resultados
                result_labels = [f'{home_team} Vitória', 'Empate', f'{away_team} Vitória']
                result_values = [
                    ensemble_results.get("home_win_prob", 0),
                    ensemble_results.get("draw_prob", 0),
                    ensemble_results.get("away_win_prob", 0)
                ]
                
                fig_results = go.Figure(data=[go.Pie(
                    labels=result_labels,
                    values=result_values,
                    hole=.3,
                    marker_colors=['red', 'gray', 'blue']
                )])
                
                fig_results.update_layout(
                    title_text='Probabilidades de Resultados (Modelo Ensemble)',
                    annotations=[dict(text='Probabilidades', x=0.5, y=0.5, font_size=15, showarrow=False)]
                )
                
                st.plotly_chart(fig_results)
                
                # Criar gráfico de probabilidades de over/under
                over_under_labels = ['Over 0.5', 'Over 1.5', 'Over 2.5', 'Over 3.5']
                over_under_values = [
                    ensemble_results.get("over_0_5_prob", 0),
                    ensemble_results.get("over_1_5_prob", 0),
                    ensemble_results.get("over_2_5_prob", 0),
                    ensemble_results.get("over_3_5_prob", 0)
                ]
                
                fig_over_under = go.Figure([go.Bar(
                    x=over_under_labels,
                    y=over_under_values,
                    marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
                )])
                
                fig_over_under.update_layout(
                    title_text='Probabilidades de Over/Under',
                    xaxis_title='Mercado',
                    yaxis_title='Probabilidade (%)',
                    yaxis=dict(range=[0, 100])
                )
                
                st.plotly_chart(fig_over_under)
                
                # Criar gráfico de probabilidade de BTTS
                btts_prob = ensemble_results.get("btts_prob", 0)
                no_btts_prob = 100 - btts_prob
                
                fig_btts = go.Figure(data=[go.Pie(
                    labels=['Ambas Marcam', 'Nem Todas Marcam'],
                    values=[btts_prob, no_btts_prob],
                    hole=.3,
                    marker_colors=['green', 'red']
                )])
                
                fig_btts.update_layout(
                    title_text='Probabilidade de Ambas Equipes Marcarem (BTTS)',
                    annotations=[dict(text=f'{btts_prob:.1f}%', x=0.5, y=0.5, font_size=15, showarrow=False)]
                )
                
                st.plotly_chart(fig_btts)
                
                # Exibir placares mais prováveis
                top_5_scores = ensemble_results.get("top_5_scores", [])
                if top_5_scores:
                    st.subheader("Placares Mais Prováveis")
                    
                    scores = [score.get("score", "") for score in top_5_scores]
                    probabilities = [score.get("probability", 0) for score in top_5_scores]
                    
                    fig_scores = go.Figure([go.Bar(
                        x=scores,
                        y=probabilities,
                        marker_color='purple'
                    )])
                    
                    fig_scores.update_layout(
                        title_text='Top 5 Placares Mais Prováveis',
                        xaxis_title='Placar',
                        yaxis_title='Probabilidade (%)',
                        yaxis=dict(range=[0, max(probabilities) * 1.2])
                    )
                    
                    st.plotly_chart(fig_scores)
        else:
            st.warning("Não foi possível gerar insights para os modelos matemáticos.")

# Função principal
def main():
    st.title("📊 Análise Estatística de Futebol")
    
    st.write("""
    Esta aplicação analisa estatísticas de futebol e gera insights detalhados para ajudar na análise de jogos.
    Cole o texto com as estatísticas do jogo no formato adequado e obtenha uma análise completa.
    """)
    
    # Área para entrada de texto
    text_input = st.text_area(
        "Cole o texto com as estatísticas do jogo aqui:",
        height=300,
        placeholder="Cole aqui o texto com estatísticas no formato adequado..."
    )
    
    # Botão para processar o texto
    if st.button("Analisar Estatísticas"):
        if not text_input:
            st.error("Por favor, insira o texto com as estatísticas do jogo.")
        else:
            # Mostrar spinner durante o processamento
            with st.spinner("Processando estatísticas..."):
                try:
                    # Processar o texto
                    processed_data = process_input_text(text_input)
                    
                    # Analisar os dados
                    analysis = analyze_data(processed_data)
                    
                    # Criar visualizações
                    visualizations = create_visualizations(processed_data)
                    
                    # Exibir insights e visualizações
                    display_insights(analysis, visualizations)
                    
                    # Adicionar seção de conclusão
                    st.header("🎯 Conclusão")
                    
                    # Extrair insights principais de cada análise
                    h2h_insights = analysis.get("head_to_head", {}).get("insights", [])
                    form_insights = analysis.get("recent_form", {}).get("insights", [])
                    table_insights = analysis.get("table_positions", {}).get("insights", [])
                    text_insights = analysis.get("text_predictions", {}).get("insights", [])
                    models_insights = analysis.get("prediction_models", {}).get("insights", [])
                    
                    # Selecionar insights mais relevantes para a conclusão
                    key_insights = []
                    
                    # Adicionar insight sobre o favorito dos modelos matemáticos
                    for insight in models_insights:
                        if "Resultado mais provável" in insight:
                            key_insights.append(insight)
                            break
                    
                    # Adicionar insight sobre o placar mais provável
                    for insight in models_insights:
                        if "Placar mais provável" in insight:
                            key_insights.append(insight)
                            break
                    
                    # Adicionar insight sobre over/under
                    for insight in models_insights:
                        if "Over 2.5 gols" in insight:
                            key_insights.append(insight)
                            break
                    
                    # Adicionar insight sobre BTTS
                    for insight in models_insights:
                        if "ambas equipes marcarem" in insight:
                            key_insights.append(insight)
                            break
                    
                    # Adicionar insight sobre confrontos diretos
                    for insight in h2h_insights:
                        if "dominância" in insight or "Histórico" in insight:
                            key_insights.append(insight)
                            break
                    
                    # Adicionar insight sobre forma recente
                    for insight in form_insights:
                        if "favorito" in insight or "momento" in insight:
                            key_insights.append(insight)
                            break
                    
                    # Exibir insights chave
                    for insight in key_insights:
                        st.write(f"• {insight}")
                    
                    # Adicionar nota final
                    st.info("""
                    **Nota:** Esta análise é baseada em dados históricos e modelos estatísticos. 
                    Os resultados reais podem variar devido a fatores imprevisíveis como lesões, 
                    condições climáticas, decisões de arbitragem, entre outros.
                    """)
                except Exception as e:
                    st.error(f"Ocorreu um erro ao processar o texto: {str(e)}")
                    st.info("Verifique se o formato do texto está correto e tente novamente.")

if __name__ == "__main__":
    main()
