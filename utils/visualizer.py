#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para visualização de dados estatísticos de futebol.
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
import os

class FootballVisualizer:
    """
    Classe para criar visualizações de dados estatísticos de futebol.
    """
    
    def __init__(self, processed_data: Dict[str, Any]):
        """
        Inicializa o visualizador com os dados processados.
        
        Args:
            processed_data (Dict[str, Any]): Dados processados
        """
        self.data = processed_data
        self.home_team = processed_data["basic_info"]["home_team"]
        self.away_team = processed_data["basic_info"]["away_team"]
        
        # Criar diretório para salvar visualizações
        os.makedirs("visualizations", exist_ok=True)
    
    def create_head_to_head_visualizations(self) -> Dict[str, Any]:
        """
        Cria visualizações para os dados de confrontos diretos.
        
        Returns:
            Dict[str, Any]: Objetos de visualização para confrontos diretos
        """
        h2h_data = self.data.get("head_to_head", {})
        if not h2h_data:
            return {}
        
        visualizations = {}
        
        # Gráfico de pizza para distribuição de resultados
        home_wins = h2h_data.get("home_team_wins", 0)
        away_wins = h2h_data.get("away_team_wins", 0)
        draws = h2h_data.get("draws", 0)
        
        labels = [f'{self.home_team} Vitórias', 'Empates', f'{self.away_team} Vitórias']
        values = [home_wins, draws, away_wins]
        colors = ['red', 'gray', 'blue']
        
        fig_results = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.3,
            marker_colors=colors
        )])
        
        fig_results.update_layout(
            title_text=f'Distribuição de Resultados: {self.home_team} vs {self.away_team}',
            annotations=[dict(text=f'Total: {sum(values)}', x=0.5, y=0.5, font_size=15, showarrow=False)]
        )
        
        visualizations["results_distribution"] = fig_results
        
        # Gráfico de barras para os últimos 5 confrontos
        last_matches = h2h_data.get("last_5_matches", {}).get("matches", [])
        
        if last_matches:
            dates = []
            home_goals = []
            away_goals = []
            
            for match in last_matches:
                date = match.get("date", "")
                home_team_in_match = match.get("home_team", "")
                away_team_in_match = match.get("away_team", "")
                home_score = match.get("home_score", 0)
                away_score = match.get("away_score", 0)
                
                dates.append(date)
                
                # Ajustar para garantir que os gols sejam atribuídos às equipes corretas
                if home_team_in_match == self.home_team:
                    home_goals.append(home_score)
                    away_goals.append(away_score)
                else:
                    home_goals.append(away_score)
                    away_goals.append(home_score)
            
            # Inverter a ordem para que o jogo mais recente fique à direita
            dates.reverse()
            home_goals.reverse()
            away_goals.reverse()
            
            fig_last_matches = go.Figure()
            
            fig_last_matches.add_trace(go.Bar(
                x=dates,
                y=home_goals,
                name=self.home_team,
                marker_color='red'
            ))
            
            fig_last_matches.add_trace(go.Bar(
                x=dates,
                y=away_goals,
                name=self.away_team,
                marker_color='blue'
            ))
            
            fig_last_matches.update_layout(
                title_text=f'Últimos 5 Confrontos: {self.home_team} vs {self.away_team}',
                xaxis_title='Data',
                yaxis_title='Gols',
                barmode='group'
            )
            
            visualizations["last_matches"] = fig_last_matches
        
        # Gráfico de barras para estatísticas de gols
        goals_stats = h2h_data.get("goals_stats", {})
        
        if goals_stats:
            categories = ['Mais de 1.5 gols', 'Mais de 2.5 gols', 'Mais de 3.5 gols', 'Ambas Marcam']
            percentages = [
                goals_stats.get("over_1_5_percent", 0),
                goals_stats.get("over_2_5_percent", 0),
                goals_stats.get("over_3_5_percent", 0),
                goals_stats.get("btts_percent", 0)
            ]
            
            fig_goals_stats = go.Figure([go.Bar(
                x=categories,
                y=percentages,
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            )])
            
            fig_goals_stats.update_layout(
                title_text=f'Estatísticas de Gols: {self.home_team} vs {self.away_team}',
                xaxis_title='Categoria',
                yaxis_title='Porcentagem (%)',
                yaxis=dict(range=[0, 100])
            )
            
            visualizations["goals_stats"] = fig_goals_stats
        
        return visualizations
    
    def create_team_form_visualizations(self) -> Dict[str, Dict[str, Any]]:
        """
        Cria visualizações para os dados de forma recente das equipes.
        
        Returns:
            Dict[str, Dict[str, Any]]: Objetos de visualização para forma recente
        """
        team_form_data = self.data.get("team_form", {})
        if not team_form_data:
            return {}
        
        visualizations = {}
        
        for team, form_data in team_form_data.items():
            team_visualizations = {}
            
            # Gráfico de pizza para distribuição de resultados nos últimos 5 jogos
            last_5_matches = form_data.get("last_5_matches", {})
            
            wins = last_5_matches.get("wins", 0)
            draws = last_5_matches.get("draws", 0)
            losses = last_5_matches.get("losses", 0)
            
            labels = ['Vitórias', 'Empates', 'Derrotas']
            values = [wins, draws, losses]
            colors = ['green', 'gray', 'red']
            
            fig_results = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.3,
                marker_colors=colors
            )])
            
            fig_results.update_layout(
                title_text=f'Últimos 5 Jogos: {team}',
                annotations=[dict(text=f'Total: {sum(values)}', x=0.5, y=0.5, font_size=15, showarrow=False)]
            )
            
            team_visualizations["results_distribution"] = fig_results
            
            # Gráfico de barras para gols marcados e sofridos nos últimos 5 jogos
            matches = last_5_matches.get("matches", [])
            
            if matches:
                match_numbers = list(range(1, len(matches) + 1))
                goals_scored = []
                goals_conceded = []
                
                for match in matches:
                    home_team = match.get("home_team", "")
                    away_team = match.get("away_team", "")
                    home_score = match.get("home_score", 0)
                    away_score = match.get("away_score", 0)
                    
                    if home_team == team:
                        goals_scored.append(home_score)
                        goals_conceded.append(away_score)
                    else:
                        goals_scored.append(away_score)
                        goals_conceded.append(home_score)
                
                # Inverter a ordem para que o jogo mais recente fique à direita
                match_numbers.reverse()
                goals_scored.reverse()
                goals_conceded.reverse()
                
                fig_goals = go.Figure()
                
                fig_goals.add_trace(go.Bar(
                    x=match_numbers,
                    y=goals_scored,
                    name='Gols Marcados',
                    marker_color='green'
                ))
                
                fig_goals.add_trace(go.Bar(
                    x=match_numbers,
                    y=goals_conceded,
                    name='Gols Sofridos',
                    marker_color='red'
                ))
                
                fig_goals.update_layout(
                    title_text=f'Gols nos Últimos 5 Jogos: {team}',
                    xaxis_title='Jogo (mais recente à direita)',
                    yaxis_title='Gols',
                    barmode='group'
                )
                
                team_visualizations["goals"] = fig_goals
            
            # Gráfico de radar para estatísticas gerais
            stats = form_data.get("stats", {})
            
            if stats:
                categories = ['Vitória %', 'Gols Marcados', 'Gols Sofridos', 'Ambas Marcam %', 'Clean Sheets %']
                
                # Valores para casa, fora e geral
                values_home = [
                    stats.get("win_percentage", {}).get("home", 0),
                    stats.get("goals_scored_per_game", {}).get("home", 0) * 20,  # Escalar para visualização
                    stats.get("goals_conceded_per_game", {}).get("home", 0) * 20,  # Escalar para visualização
                    stats.get("btts_percentage", {}).get("home", 0),
                    stats.get("clean_sheets_percentage", {}).get("home", 0)
                ]
                
                values_away = [
                    stats.get("win_percentage", {}).get("away", 0),
                    stats.get("goals_scored_per_game", {}).get("away", 0) * 20,  # Escalar para visualização
                    stats.get("goals_conceded_per_game", {}).get("away", 0) * 20,  # Escalar para visualização
                    stats.get("btts_percentage", {}).get("away", 0),
                    stats.get("clean_sheets_percentage", {}).get("away", 0)
                ]
                
                values_overall = [
                    stats.get("win_percentage", {}).get("overall", 0),
                    stats.get("goals_scored_per_game", {}).get("overall", 0) * 20,  # Escalar para visualização
                    stats.get("goals_conceded_per_game", {}).get("overall", 0) * 20,  # Escalar para visualização
                    stats.get("btts_percentage", {}).get("overall", 0),
                    stats.get("clean_sheets_percentage", {}).get("overall", 0)
                ]
                
                fig_radar = go.Figure()
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=values_home,
                    theta=categories,
                    fill='toself',
                    name='Casa'
                ))
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=values_away,
                    theta=categories,
                    fill='toself',
                    name='Fora'
                ))
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=values_overall,
                    theta=categories,
                    fill='toself',
                    name='Geral'
                ))
                
                fig_radar.update_layout(
                    title_text=f'Estatísticas Gerais: {team}',
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=True
                )
                
                team_visualizations["stats_radar"] = fig_radar
            
            visualizations[team] = team_visualizations
        
        return visualizations
    
    def create_table_positions_visualizations(self) -> Dict[str, Any]:
        """
        Cria visualizações para os dados de posições nas tabelas.
        
        Returns:
            Dict[str, Any]: Objetos de visualização para posições nas tabelas
        """
        positions_data = self.data.get("table_positions", {})
        if not positions_data:
            return {}
        
        visualizations = {}
        
        # Gráfico de barras para posições gerais
        teams = [self.home_team, self.away_team]
        positions = [
            positions_data.get(self.home_team, {}).get("general_position", 0),
            positions_data.get(self.away_team, {}).get("general_position", 0)
        ]
        
        # Inverter posições para que menor seja melhor visualmente
        positions_inverted = [21 - pos for pos in positions]
        
        fig_positions = go.Figure([go.Bar(
            x=teams,
            y=positions_inverted,
            marker_color=['red', 'blue'],
            text=positions,
            textposition='auto'
        )])
        
        fig_positions.update_layout(
            title_text='Posições na Tabela Geral',
            xaxis_title='Equipe',
            yaxis_title='Posição (invertida para visualização)',
            yaxis=dict(range=[0, 20], tickvals=list(range(0, 21, 5)), ticktext=[str(21-i) for i in range(0, 21, 5)])
        )
        
        visualizations["general_positions"] = fig_positions
        
        # Gráfico de barras para comparação casa/fora
        home_position = positions_data.get(self.home_team, {}).get("home_position", 0)
        away_position = positions_data.get(self.away_team, {}).get("away_position", 0)
        
        if home_position and away_position:
            categories = [f'{self.home_team} (Casa)', f'{self.away_team} (Fora)']
            positions_specific = [home_position, away_position]
            
            # Inverter posições para que menor seja melhor visualmente
            positions_specific_inverted = [21 - pos for pos in positions_specific]
            
            fig_specific_positions = go.Figure([go.Bar(
                x=categories,
                y=positions_specific_inverted,
                marker_color=['darkred', 'darkblue'],
                text=positions_specific,
                textposition='auto'
            )])
            
            fig_specific_positions.update_layout(
                title_text='Posições nas Tabelas Casa/Fora',
                xaxis_title='Equipe',
                yaxis_title='Posição (invertida para visualização)',
                yaxis=dict(range=[0, 20], tickvals=list(range(0, 21, 5)), ticktext=[str(21-i) for i in range(0, 21, 5)])
            )
            
            visualizations["specific_positions"] = fig_specific_positions
        
        # Gráfico de comparação direta entre mandante e visitante
        direct_comparison = positions_data.get("direct_comparison", {})
        
        if direct_comparison:
            categories = [
                'Vitória %', 
                'Gols Marcados/Jogo', 
                'Gols Sofridos/Jogo', 
                'xG', 
                'xGC'
            ]
            
            home_values = [
                direct_comparison.get("home_win_percentage", 0),
                direct_comparison.get("home_goals_scored", 0),
                direct_comparison.get("home_goals_conceded", 0),
                direct_comparison.get("home_xG", 0),
                direct_comparison.get("home_xGC", 0)
            ]
            
            away_values = [
                direct_comparison.get("away_win_percentage", 0),
                direct_comparison.get("away_goals_scored", 0),
                direct_comparison.get("away_goals_conceded", 0),
                direct_comparison.get("away_xG", 0),
                direct_comparison.get("away_xGC", 0)
            ]
            
            fig_comparison = go.Figure()
            
            fig_comparison.add_trace(go.Bar(
                x=categories,
                y=home_values,
                name=f'{self.home_team} (Casa)',
                marker_color='red'
            ))
            
            fig_comparison.add_trace(go.Bar(
                x=categories,
                y=away_values,
                name=f'{self.away_team} (Fora)',
                marker_color='blue'
            ))
            
            fig_comparison.update_layout(
                title_text=f'Comparação Direta: {self.home_team} (Casa) vs {self.away_team} (Fora)',
                xaxis_title='Métrica',
                yaxis_title='Valor',
                barmode='group'
            )
            
            visualizations["direct_comparison"] = fig_comparison
        
        return visualizations
    
    def create_predictions_visualizations(self) -> Dict[str, Any]:
        """
        Cria visualizações para os dados de prognósticos.
        
        Returns:
            Dict[str, Any]: Objetos de visualização para prognósticos
        """
        predictions_data = self.data.get("predictions", {})
        if not predictions_data:
            return {}
        
        visualizations = {}
        
        # Gráfico de barras para prognósticos gerais vs média da liga
        general_predictions = predictions_data.get("general", {})
        
        if general_predictions:
            categories = ['Mais de 2.5', 'Mais de 1.5', 'Ambas Marcam', 'Gols/Jogo', 'Cartões/Jogo', 'Cantos/Jogo']
            
            match_values = [
                general_predictions.get("over_2_5_percentage", 0),
                general_predictions.get("over_1_5_percentage", 0),
                general_predictions.get("btts_percentage", 0),
                general_predictions.get("goals_per_game", 0) * 20,  # Escalar para visualização
                general_predictions.get("cards_per_game", 0) * 10,  # Escalar para visualização
                general_predictions.get("corners_per_game", 0) * 5   # Escalar para visualização
            ]
            
            league_values = [
                general_predictions.get("over_2_5_league_avg", 0),
                general_predictions.get("over_1_5_league_avg", 0),
                general_predictions.get("btts_league_avg", 0),
                general_predictions.get("goals_per_game_league_avg", 0) * 20,  # Escalar para visualização
                general_predictions.get("cards_per_game_league_avg", 0) * 10,  # Escalar para visualização
                general_predictions.get("corners_per_game_league_avg", 0) * 5   # Escalar para visualização
            ]
            
            fig_general = go.Figure()
            
            fig_general.add_trace(go.Bar(
                x=categories,
                y=match_values,
                name='Jogo Atual',
                marker_color='green'
            ))
            
            fig_general.add_trace(go.Bar(
                x=categories,
                y=league_values,
                name='Média da Liga',
                marker_color='gray'
            ))
            
            fig_general.update_layout(
                title_text=f'Prognósticos Gerais: {self.home_team} vs {self.away_team}',
                xaxis_title='Categoria',
                yaxis_title='Valor',
                barmode='group'
            )
            
            visualizations["general_predictions"] = fig_general
        
        # Gráfico de barras para prognósticos detalhados de gols
        goals_detailed = predictions_data.get("goals_detailed", {})
        
        if goals_detailed:
            categories = ['Mais de 0.5', 'Mais de 1.5', 'Mais de 2.5', 'Mais de 3.5', 'Mais de 4.5', 'Ambas Marcam']
            
            home_values = [
                goals_detailed.get("over_0_5", {}).get("home", 0),
                goals_detailed.get("over_1_5", {}).get("home", 0),
                goals_detailed.get("over_2_5", {}).get("home", 0),
                goals_detailed.get("over_3_5", {}).get("home", 0),
                goals_detailed.get("over_4_5", {}).get("home", 0),
                goals_detailed.get("btts", {}).get("home", 0)
            ]
            
            away_values = [
                goals_detailed.get("over_0_5", {}).get("away", 0),
                goals_detailed.get("over_1_5", {}).get("away", 0),
                goals_detailed.get("over_2_5", {}).get("away", 0),
                goals_detailed.get("over_3_5", {}).get("away", 0),
                goals_detailed.get("over_4_5", {}).get("away", 0),
                goals_detailed.get("btts", {}).get("away", 0)
            ]
            
            average_values = [
                goals_detailed.get("over_0_5", {}).get("average", 0),
                goals_detailed.get("over_1_5", {}).get("average", 0),
                goals_detailed.get("over_2_5", {}).get("average", 0),
                goals_detailed.get("over_3_5", {}).get("average", 0),
                goals_detailed.get("over_4_5", {}).get("average", 0),
                goals_detailed.get("btts", {}).get("average", 0)
            ]
            
            fig_goals = go.Figure()
            
            fig_goals.add_trace(go.Bar(
                x=categories,
                y=home_values,
                name=self.home_team,
                marker_color='red'
            ))
            
            fig_goals.add_trace(go.Bar(
                x=categories,
                y=away_values,
                name=self.away_team,
                marker_color='blue'
            ))
            
            fig_goals.add_trace(go.Bar(
                x=categories,
                y=average_values,
                name='Média',
                marker_color='green'
            ))
            
            fig_goals.update_layout(
                title_text='Prognósticos Detalhados de Gols',
                xaxis_title='Categoria',
                yaxis_title='Porcentagem (%)',
                barmode='group',
                yaxis=dict(range=[0, 100])
            )
            
            visualizations["goals_detailed"] = fig_goals
        
        # Gráfico de barras para prognósticos de cantos
        corners = predictions_data.get("corners", {})
        
        if corners:
            categories = ['Mais de 6', 'Mais de 7', 'Mais de 8', 'Mais de 9', 'Mais de 10']
            
            values = [
                corners.get("over_6_corners_percentage", 0),
                corners.get("over_7_corners_percentage", 0),
                corners.get("over_8_corners_percentage", 0),
                corners.get("over_9_corners_percentage", 0),
                corners.get("over_10_corners_percentage", 0)
            ]
            
            fig_corners = go.Figure([go.Bar(
                x=categories,
                y=values,
                marker_color='orange'
            )])
            
            fig_corners.update_layout(
                title_text='Prognósticos de Cantos',
                xaxis_title='Categoria',
                yaxis_title='Porcentagem (%)',
                yaxis=dict(range=[0, 100])
            )
            
            visualizations["corners"] = fig_corners
        
        # Gráfico de barras para prognósticos de cartões
        cards = predictions_data.get("cards", {})
        
        if cards:
            categories = ['Mais de 2.5', 'Mais de 3.5', 'Mais de 4.5']
            
            values = [
                cards.get("over_2_5_cards_percentage", 0),
                cards.get("over_3_5_cards_percentage", 0),
                cards.get("over_4_5_cards_percentage", 0)
            ]
            
            fig_cards = go.Figure([go.Bar(
                x=categories,
                y=values,
                marker_color='yellow'
            )])
            
            fig_cards.update_layout(
                title_text='Prognósticos de Cartões',
                xaxis_title='Categoria',
                yaxis_title='Porcentagem (%)',
                yaxis=dict(range=[0, 100])
            )
            
            visualizations["cards"] = fig_cards
        
        # Gráfico de barras para prognósticos de primeiro tempo/segundo tempo
        halftime_fulltime = predictions_data.get("halftime_fulltime", {})
        
        if halftime_fulltime:
            categories = ['Vitória 1T', 'Vitória 2T', 'Empate 1T', 'Empate 2T', 'Derrota 1T', 'Derrota 2T']
            
            home_values = [
                halftime_fulltime.get("home_win_1h", 0),
                halftime_fulltime.get("home_win_2h", 0),
                halftime_fulltime.get("home_draw_1h", 0),
                halftime_fulltime.get("home_draw_2h", 0),
                halftime_fulltime.get("home_loss_1h", 0),
                halftime_fulltime.get("home_loss_2h", 0)
            ]
            
            away_values = [
                halftime_fulltime.get("away_win_1h", 0),
                halftime_fulltime.get("away_win_2h", 0),
                halftime_fulltime.get("away_draw_1h", 0),
                halftime_fulltime.get("away_draw_2h", 0),
                halftime_fulltime.get("away_loss_1h", 0),
                halftime_fulltime.get("away_loss_2h", 0)
            ]
            
            fig_ht_ft = go.Figure()
            
            fig_ht_ft.add_trace(go.Bar(
                x=categories,
                y=home_values,
                name=self.home_team,
                marker_color='red'
            ))
            
            fig_ht_ft.add_trace(go.Bar(
                x=categories,
                y=away_values,
                name=self.away_team,
                marker_color='blue'
            ))
            
            fig_ht_ft.update_layout(
                title_text='Prognósticos de Primeiro Tempo/Segundo Tempo',
                xaxis_title='Categoria',
                yaxis_title='Porcentagem (%)',
                barmode='group',
                yaxis=dict(range=[0, 100])
            )
            
            visualizations["halftime_fulltime"] = fig_ht_ft
        
        # Gráfico de barras para prognósticos de quem marca primeiro
        first_goal = predictions_data.get("first_goal", {})
        
        if first_goal:
            teams = [self.home_team, self.away_team]
            
            values = [
                first_goal.get("home_first_goal_percentage", 0),
                first_goal.get("away_first_goal_percentage", 0)
            ]
            
            fig_first_goal = go.Figure([go.Bar(
                x=teams,
                y=values,
                marker_color=['red', 'blue']
            )])
            
            fig_first_goal.update_layout(
                title_text='Quem Marca Primeiro',
                xaxis_title='Equipe',
                yaxis_title='Porcentagem (%)',
                yaxis=dict(range=[0, 100])
            )
            
            visualizations["first_goal"] = fig_first_goal
        
        return visualizations
    
    def create_all_visualizations(self) -> Dict[str, Any]:
        """
        Cria todas as visualizações disponíveis.
        
        Returns:
            Dict[str, Any]: Todos os objetos de visualização
        """
        h2h_visualizations = self.create_head_to_head_visualizations()
        team_form_visualizations = self.create_team_form_visualizations()
        table_positions_visualizations = self.create_table_positions_visualizations()
        predictions_visualizations = self.create_predictions_visualizations()
        
        return {
            "head_to_head": h2h_visualizations,
            "team_form": team_form_visualizations,
            "table_positions": table_positions_visualizations,
            "predictions": predictions_visualizations
        }
    
    def save_visualizations(self, visualizations: Dict[str, Any], format: str = 'png') -> Dict[str, str]:
        """
        Salva todas as visualizações em arquivos.
        
        Args:
            visualizations (Dict[str, Any]): Objetos de visualização
            format (str, optional): Formato de arquivo. Defaults to 'png'.
        
        Returns:
            Dict[str, str]: Caminhos dos arquivos salvos
        """
        saved_files = {}
        
        # Salvar visualizações de confrontos diretos
        h2h_visualizations = visualizations.get("head_to_head", {})
        for name, fig in h2h_visualizations.items():
            filename = f"visualizations/h2h_{name}.{format}"
            fig.write_image(filename)
            saved_files[f"h2h_{name}"] = filename
        
        # Salvar visualizações de forma recente
        team_form_visualizations = visualizations.get("team_form", {})
        for team, team_vis in team_form_visualizations.items():
            for name, fig in team_vis.items():
                team_safe = team.replace(" ", "_").lower()
                filename = f"visualizations/form_{team_safe}_{name}.{format}"
                fig.write_image(filename)
                saved_files[f"form_{team_safe}_{name}"] = filename
        
        # Salvar visualizações de posições nas tabelas
        table_positions_visualizations = visualizations.get("table_positions", {})
        for name, fig in table_positions_visualizations.items():
            filename = f"visualizations/table_{name}.{format}"
            fig.write_image(filename)
            saved_files[f"table_{name}"] = filename
        
        # Salvar visualizações de prognósticos
        predictions_visualizations = visualizations.get("predictions", {})
        for name, fig in predictions_visualizations.items():
            filename = f"visualizations/pred_{name}.{format}"
            fig.write_image(filename)
            saved_files[f"pred_{name}"] = filename
        
        return saved_files
