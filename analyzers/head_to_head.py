#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para análise de confrontos diretos entre equipes de futebol.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional

class HeadToHeadAnalyzer:
    """
    Classe para analisar confrontos diretos entre equipes de futebol.
    """
    
    def __init__(self, processed_data: Dict[str, Any]):
        """
        Inicializa o analisador com os dados processados.
        
        Args:
            processed_data (Dict[str, Any]): Dados processados
        """
        self.data = processed_data
        self.home_team = processed_data["basic_info"]["home_team"]
        self.away_team = processed_data["basic_info"]["away_team"]
        self.h2h_data = processed_data.get("head_to_head", {})
    
    def analyze_historical_dominance(self) -> Dict[str, Any]:
        """
        Analisa a dominância histórica entre as equipes.
        
        Returns:
            Dict[str, Any]: Análise de dominância histórica
        """
        if not self.h2h_data:
            return {"error": "Dados de confrontos diretos não disponíveis"}
        
        total_matches = self.h2h_data.get("total_matches", 0)
        home_wins = self.h2h_data.get("home_team_wins", 0)
        away_wins = self.h2h_data.get("away_team_wins", 0)
        draws = self.h2h_data.get("draws", 0)
        
        home_win_percentage = self.h2h_data.get("home_win_percentage", 0)
        away_win_percentage = self.h2h_data.get("away_win_percentage", 0)
        draw_percentage = self.h2h_data.get("draw_percentage", 0)
        
        # Determinar dominância
        dominance_threshold = 60  # Percentual para considerar dominância
        significant_matches = 5    # Número mínimo de jogos para considerar significativo
        
        dominant_team = None
        dominance_level = "Equilibrado"
        
        if total_matches >= significant_matches:
            if home_win_percentage >= dominance_threshold:
                dominant_team = self.home_team
                if home_win_percentage >= 75:
                    dominance_level = "Forte"
                else:
                    dominance_level = "Moderado"
            elif away_win_percentage >= dominance_threshold:
                dominant_team = self.away_team
                if away_win_percentage >= 75:
                    dominance_level = "Forte"
                else:
                    dominance_level = "Moderado"
            elif draw_percentage >= dominance_threshold:
                dominance_level = "Tendência a empates"
        
        return {
            "total_matches": total_matches,
            "home_team_wins": home_wins,
            "away_team_wins": away_wins,
            "draws": draws,
            "home_win_percentage": home_win_percentage,
            "away_win_percentage": away_win_percentage,
            "draw_percentage": draw_percentage,
            "dominant_team": dominant_team,
            "dominance_level": dominance_level,
            "is_significant": total_matches >= significant_matches
        }
    
    def analyze_goal_patterns(self) -> Dict[str, Any]:
        """
        Analisa padrões de gols nos confrontos diretos.
        
        Returns:
            Dict[str, Any]: Análise de padrões de gols
        """
        if not self.h2h_data:
            return {"error": "Dados de confrontos diretos não disponíveis"}
        
        goals_stats = self.h2h_data.get("goals_stats", {})
        if not goals_stats:
            return {"error": "Estatísticas de gols não disponíveis"}
        
        over_1_5_percent = goals_stats.get("over_1_5_percent", 0)
        over_2_5_percent = goals_stats.get("over_2_5_percent", 0)
        over_3_5_percent = goals_stats.get("over_3_5_percent", 0)
        btts_percent = goals_stats.get("btts_percent", 0)
        
        # Determinar tendências de gols
        high_scoring_threshold = 60  # Percentual para considerar jogos de muitos gols
        low_scoring_threshold = 40   # Percentual para considerar jogos de poucos gols
        btts_threshold = 60          # Percentual para considerar tendência de ambas marcarem
        
        is_high_scoring = over_2_5_percent >= high_scoring_threshold
        is_low_scoring = over_2_5_percent <= low_scoring_threshold
        is_btts_trend = btts_percent >= btts_threshold
        
        # Classificar o padrão de gols
        if is_high_scoring and is_btts_trend:
            goal_pattern = "Jogos abertos com muitos gols e ambas equipes marcando"
        elif is_high_scoring and not is_btts_trend:
            goal_pattern = "Jogos com muitos gols, geralmente de uma equipe"
        elif is_low_scoring and is_btts_trend:
            goal_pattern = "Jogos equilibrados com poucos gols, mas ambas equipes marcando"
        elif is_low_scoring and not is_btts_trend:
            goal_pattern = "Jogos fechados com poucos gols"
        else:
            goal_pattern = "Padrão de gols variável"
        
        return {
            "over_1_5_percent": over_1_5_percent,
            "over_2_5_percent": over_2_5_percent,
            "over_3_5_percent": over_3_5_percent,
            "btts_percent": btts_percent,
            "is_high_scoring": is_high_scoring,
            "is_low_scoring": is_low_scoring,
            "is_btts_trend": is_btts_trend,
            "goal_pattern": goal_pattern
        }
    
    def analyze_recent_trend(self) -> Dict[str, Any]:
        """
        Analisa a tendência recente nos confrontos diretos.
        
        Returns:
            Dict[str, Any]: Análise de tendência recente
        """
        if not self.h2h_data:
            return {"error": "Dados de confrontos diretos não disponíveis"}
        
        last_5_matches = self.h2h_data.get("last_5_matches", {})
        if not last_5_matches:
            return {"error": "Dados dos últimos 5 confrontos não disponíveis"}
        
        matches = last_5_matches.get("matches", [])
        if not matches:
            return {"error": "Detalhes dos últimos confrontos não disponíveis"}
        
        home_wins = last_5_matches.get("home_wins", 0)
        away_wins = last_5_matches.get("away_wins", 0)
        draws = last_5_matches.get("draws", 0)
        
        avg_home_goals = last_5_matches.get("avg_home_goals", 0)
        avg_away_goals = last_5_matches.get("avg_away_goals", 0)
        avg_total_goals = last_5_matches.get("avg_total_goals", 0)
        
        btts_percentage = last_5_matches.get("btts_percentage", 0)
        over_2_5_percentage = last_5_matches.get("over_2_5_percentage", 0)
        
        # Determinar tendência recente
        recent_dominant_team = None
        recent_dominance_level = "Equilibrado"
        
        if home_wins >= 4:
            recent_dominant_team = self.home_team
            recent_dominance_level = "Forte"
        elif home_wins == 3:
            recent_dominant_team = self.home_team
            recent_dominance_level = "Moderado"
        elif away_wins >= 4:
            recent_dominant_team = self.away_team
            recent_dominance_level = "Forte"
        elif away_wins == 3:
            recent_dominant_team = self.away_team
            recent_dominance_level = "Moderado"
        elif draws >= 3:
            recent_dominance_level = "Tendência a empates"
        
        # Analisar tendência de gols recente
        recent_goal_trend = None
        
        if avg_total_goals >= 3.5:
            if btts_percentage >= 60:
                recent_goal_trend = "Jogos recentes com muitos gols e ambas equipes marcando"
            else:
                recent_goal_trend = "Jogos recentes com muitos gols, geralmente de uma equipe"
        elif avg_total_goals >= 2.5:
            if btts_percentage >= 60:
                recent_goal_trend = "Jogos recentes com gols moderados e ambas equipes marcando"
            else:
                recent_goal_trend = "Jogos recentes com gols moderados, geralmente de uma equipe"
        else:
            if btts_percentage >= 60:
                recent_goal_trend = "Jogos recentes com poucos gols, mas ambas equipes marcando"
            else:
                recent_goal_trend = "Jogos recentes fechados com poucos gols"
        
        # Verificar se há mudança na tendência histórica
        historical_dominance = self.analyze_historical_dominance()
        historical_dominant_team = historical_dominance.get("dominant_team")
        
        trend_change = False
        trend_change_description = None
        
        if historical_dominant_team and recent_dominant_team and historical_dominant_team != recent_dominant_team:
            trend_change = True
            trend_change_description = f"Mudança de dominância: historicamente {historical_dominant_team}, recentemente {recent_dominant_team}"
        elif historical_dominant_team and not recent_dominant_team:
            trend_change = True
            trend_change_description = f"Mudança de dominância: historicamente {historical_dominant_team}, recentemente equilibrado"
        elif not historical_dominant_team and recent_dominant_team:
            trend_change = True
            trend_change_description = f"Mudança de dominância: historicamente equilibrado, recentemente {recent_dominant_team}"
        
        return {
            "matches": matches,
            "home_wins": home_wins,
            "away_wins": away_wins,
            "draws": draws,
            "avg_home_goals": avg_home_goals,
            "avg_away_goals": avg_away_goals,
            "avg_total_goals": avg_total_goals,
            "btts_percentage": btts_percentage,
            "over_2_5_percentage": over_2_5_percentage,
            "recent_dominant_team": recent_dominant_team,
            "recent_dominance_level": recent_dominance_level,
            "recent_goal_trend": recent_goal_trend,
            "trend_change": trend_change,
            "trend_change_description": trend_change_description
        }
    
    def analyze_home_away_factor(self) -> Dict[str, Any]:
        """
        Analisa o fator casa/fora nos confrontos diretos.
        
        Returns:
            Dict[str, Any]: Análise do fator casa/fora
        """
        if not self.h2h_data:
            return {"error": "Dados de confrontos diretos não disponíveis"}
        
        matches = self.h2h_data.get("last_matches", [])
        if not matches:
            return {"error": "Detalhes dos confrontos não disponíveis"}
        
        # Contar vitórias em casa e fora para cada equipe
        home_team_home_wins = 0
        home_team_away_wins = 0
        away_team_home_wins = 0
        away_team_away_wins = 0
        
        for match in matches:
            home_team_in_match = match.get("home_team", "")
            away_team_in_match = match.get("away_team", "")
            home_score = match.get("home_score", 0)
            away_score = match.get("away_score", 0)
            
            if home_team_in_match == self.home_team and home_score > away_score:
                home_team_home_wins += 1
            elif home_team_in_match == self.away_team and home_score > away_score:
                away_team_home_wins += 1
            elif away_team_in_match == self.home_team and away_score > home_score:
                home_team_away_wins += 1
            elif away_team_in_match == self.away_team and away_score > home_score:
                away_team_away_wins += 1
        
        # Calcular total de jogos em casa e fora para cada equipe
        home_team_home_games = sum(1 for m in matches if m.get("home_team") == self.home_team)
        home_team_away_games = sum(1 for m in matches if m.get("away_team") == self.home_team)
        away_team_home_games = sum(1 for m in matches if m.get("home_team") == self.away_team)
        away_team_away_games = sum(1 for m in matches if m.get("away_team") == self.away_team)
        
        # Calcular percentuais de vitória
        home_team_home_win_pct = (home_team_home_wins / home_team_home_games * 100) if home_team_home_games else 0
        home_team_away_win_pct = (home_team_away_wins / home_team_away_games * 100) if home_team_away_games else 0
        away_team_home_win_pct = (away_team_home_wins / away_team_home_games * 100) if away_team_home_games else 0
        away_team_away_win_pct = (away_team_away_wins / away_team_away_games * 100) if away_team_away_games else 0
        
        # Determinar importância do fator casa
        home_advantage_threshold = 20  # Diferença percentual para considerar vantagem em casa significativa
        
        home_team_home_advantage = home_team_home_win_pct - home_team_away_win_pct
        away_team_home_advantage = away_team_home_win_pct - away_team_away_win_pct
        
        home_advantage_significant = (home_team_home_advantage > home_advantage_threshold or 
                                     away_team_home_advantage > home_advantage_threshold)
        
        # Determinar qual equipe se beneficia mais do fator casa
        home_advantage_team = None
        if home_team_home_advantage > away_team_home_advantage and home_team_home_advantage > home_advantage_threshold:
            home_advantage_team = self.home_team
        elif away_team_home_advantage > home_team_home_advantage and away_team_home_advantage > home_advantage_threshold:
            home_advantage_team = self.away_team
        
        return {
            "home_team_home_wins": home_team_home_wins,
            "home_team_away_wins": home_team_away_wins,
            "away_team_home_wins": away_team_home_wins,
            "away_team_away_wins": away_team_away_wins,
            "home_team_home_games": home_team_home_games,
            "home_team_away_games": home_team_away_games,
            "away_team_home_games": away_team_home_games,
            "away_team_away_games": away_team_away_games,
            "home_team_home_win_pct": home_team_home_win_pct,
            "home_team_away_win_pct": home_team_away_win_pct,
            "away_team_home_win_pct": away_team_home_win_pct,
            "away_team_away_win_pct": away_team_away_win_pct,
            "home_team_home_advantage": home_team_home_advantage,
            "away_team_home_advantage": away_team_home_advantage,
            "home_advantage_significant": home_advantage_significant,
            "home_advantage_team": home_advantage_team
        }
    
    def generate_insights(self) -> Dict[str, Any]:
        """
        Gera insights baseados na análise dos confrontos diretos.
        
        Returns:
            Dict[str, Any]: Insights dos confrontos diretos
        """
        if not self.h2h_data:
            return {"error": "Dados de confrontos diretos não disponíveis"}
        
        historical_dominance = self.analyze_historical_dominance()
        goal_patterns = self.analyze_goal_patterns()
        recent_trend = self.analyze_recent_trend()
        home_away_factor = self.analyze_home_away_factor()
        
        # Gerar insights principais
        insights = []
        
        # Insight sobre dominância histórica
        if historical_dominance.get("is_significant"):
            dominant_team = historical_dominance.get("dominant_team")
            dominance_level = historical_dominance.get("dominance_level")
            
            if dominant_team:
                insights.append(f"{dominant_team} tem dominância {dominance_level.lower()} no histórico de confrontos, " +
                               f"com {historical_dominance.get('home_win_percentage' if dominant_team == self.home_team else 'away_win_percentage'):.1f}% " +
                               f"de vitórias em {historical_dominance.get('total_matches')} jogos.")
            elif dominance_level == "Tendência a empates":
                insights.append(f"Histórico com forte tendência a empates ({historical_dominance.get('draw_percentage'):.1f}% " +
                               f"dos {historical_dominance.get('total_matches')} jogos).")
            else:
                insights.append(f"Histórico equilibrado entre as equipes em {historical_dominance.get('total_matches')} jogos.")
        
        # Insight sobre padrões de gols
        goal_pattern = goal_patterns.get("goal_pattern")
        if goal_pattern:
            insights.append(f"Padrão de gols: {goal_pattern}. " +
                           f"{goal_patterns.get('over_2_5_percent')}% dos jogos têm mais de 2.5 gols e " +
                           f"{goal_patterns.get('btts_percent')}% têm ambas equipes marcando.")
        
        # Insight sobre tendência recente
        recent_dominant_team = recent_trend.get("recent_dominant_team")
        recent_dominance_level = recent_trend.get("recent_dominance_level")
        
        if recent_dominant_team:
            insights.append(f"Tendência recente: {recent_dominant_team} tem dominância {recent_dominance_level.lower()} " +
                           f"nos últimos 5 jogos, vencendo {recent_trend.get('home_wins' if recent_dominant_team == self.home_team else 'away_wins')} vezes.")
        elif recent_dominance_level == "Tendência a empates":
            insights.append(f"Tendência recente: Forte tendência a empates nos últimos 5 jogos ({recent_trend.get('draws')} empates).")
        else:
            insights.append(f"Tendência recente: Equilíbrio nos últimos 5 jogos.")
        
        # Insight sobre tendência de gols recente
        recent_goal_trend = recent_trend.get("recent_goal_trend")
        if recent_goal_trend:
            insights.append(f"Tendência de gols recente: {recent_goal_trend}. " +
                           f"Média de {recent_trend.get('avg_total_goals'):.1f} gols por jogo nos últimos 5 confrontos.")
        
        # Insight sobre mudança de tendência
        if recent_trend.get("trend_change"):
            insights.append(f"Mudança de tendência detectada: {recent_trend.get('trend_change_description')}.")
        
        # Insight sobre fator casa
        home_advantage_team = home_away_factor.get("home_advantage_team")
        if home_advantage_team:
            home_advantage = home_away_factor.get("home_team_home_advantage" if home_advantage_team == self.home_team else "away_team_home_advantage")
            insights.append(f"Fator casa: {home_advantage_team} se beneficia significativamente de jogar em casa " +
                           f"(+{home_advantage:.1f}% de vitórias em casa vs fora).")
        elif home_away_factor.get("home_advantage_significant"):
            insights.append(f"Fator casa: Ambas as equipes se beneficiam de jogar em casa neste confronto.")
        else:
            insights.append(f"Fator casa: O fator casa não parece ser significativo neste confronto.")
        
        # Insight sobre o jogo atual
        current_match_insight = self.generate_current_match_insight(historical_dominance, goal_patterns, recent_trend, home_away_factor)
        if current_match_insight:
            insights.append(f"Para o jogo atual: {current_match_insight}")
        
        return {
            "historical_dominance": historical_dominance,
            "goal_patterns": goal_patterns,
            "recent_trend": recent_trend,
            "home_away_factor": home_away_factor,
            "insights": insights
        }
    
    def generate_current_match_insight(self, historical_dominance: Dict[str, Any], 
                                      goal_patterns: Dict[str, Any], 
                                      recent_trend: Dict[str, Any],
                                      home_away_factor: Dict[str, Any]) -> str:
        """
        Gera insight específico para o jogo atual baseado nas análises.
        
        Args:
            historical_dominance (Dict[str, Any]): Análise de dominância histórica
            goal_patterns (Dict[str, Any]): Análise de padrões de gols
            recent_trend (Dict[str, Any]): Análise de tendência recente
            home_away_factor (Dict[str, Any]): Análise do fator casa/fora
        
        Returns:
            str: Insight para o jogo atual
        """
        # Priorizar tendência recente sobre histórico
        dominant_team = recent_trend.get("recent_dominant_team") or historical_dominance.get("dominant_team")
        
        # Considerar fator casa para o jogo atual
        home_advantage_team = home_away_factor.get("home_advantage_team")
        home_advantage_significant = home_away_factor.get("home_advantage_significant")
        
        # Considerar padrões de gols
        is_high_scoring = goal_patterns.get("is_high_scoring")
        is_btts_trend = goal_patterns.get("is_btts_trend")
        
        # Gerar insight
        insight = ""
        
        # Parte 1: Quem tem vantagem
        if dominant_team == self.home_team and (home_advantage_team == self.home_team or home_advantage_significant):
            insight += f"{self.home_team} tem vantagem significativa jogando em casa contra {self.away_team}. "
        elif dominant_team == self.away_team and home_advantage_team != self.home_team:
            insight += f"Apesar de jogar fora, {self.away_team} tem mostrado superioridade nos confrontos contra {self.home_team}. "
        elif dominant_team == self.home_team:
            insight += f"{self.home_team} tem vantagem histórica, mas o fator casa não é tão significativo neste confronto. "
        elif dominant_team == self.away_team and home_advantage_team == self.home_team:
            insight += f"Confronto equilibrado: {self.away_team} tem vantagem no histórico, mas {self.home_team} se beneficia de jogar em casa. "
        elif home_advantage_team == self.home_team:
            insight += f"Confronto equilibrado com leve vantagem para {self.home_team} por jogar em casa. "
        else:
            insight += f"Confronto bastante equilibrado baseado no histórico. "
        
        # Parte 2: Expectativa de gols
        if is_high_scoring and is_btts_trend:
            insight += f"Alta probabilidade de um jogo aberto com ambas equipes marcando e mais de 2.5 gols no total. "
        elif is_high_scoring:
            insight += f"Expectativa de um jogo com muitos gols, possivelmente concentrados em uma equipe. "
        elif is_btts_trend:
            insight += f"Boa chance de ambas equipes marcarem, mas provavelmente com placar moderado. "
        else:
            insight += f"Histórico sugere um jogo mais fechado em termos de gols. "
        
        # Parte 3: Tendência recente
        recent_goal_trend = recent_trend.get("recent_goal_trend")
        if recent_goal_trend and "recentes" in recent_goal_trend:
            insight += f"Confrontos recentes indicam {recent_goal_trend[9:].lower()}."
        
        return insight
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """
        Executa uma análise completa dos confrontos diretos.
        
        Returns:
            Dict[str, Any]: Análise completa dos confrontos diretos
        """
        return self.generate_insights()
