#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para análise da forma recente das equipes de futebol.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional

class RecentFormAnalyzer:
    """
    Classe para analisar a forma recente das equipes de futebol.
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
        self.team_form_data = processed_data.get("team_form", {})
    
    def analyze_team_momentum(self, team: str) -> Dict[str, Any]:
        """
        Analisa o momento atual da equipe.
        
        Args:
            team (str): Nome da equipe a ser analisada
            
        Returns:
            Dict[str, Any]: Análise do momento atual da equipe
        """
        if team not in self.team_form_data:
            return {"error": f"Dados de forma recente para {team} não disponíveis"}
        
        form_data = self.team_form_data[team]
        last_5_matches = form_data.get("last_5_matches", {})
        
        if not last_5_matches:
            return {"error": f"Dados dos últimos 5 jogos para {team} não disponíveis"}
        
        # Extrair dados relevantes
        matches = last_5_matches.get("matches", [])
        wins = last_5_matches.get("wins", 0)
        draws = last_5_matches.get("draws", 0)
        losses = last_5_matches.get("losses", 0)
        win_percentage = last_5_matches.get("win_percentage", 0)
        
        avg_goals_scored = last_5_matches.get("avg_goals_scored", 0)
        avg_goals_conceded = last_5_matches.get("avg_goals_conceded", 0)
        
        clean_sheets = last_5_matches.get("clean_sheets", 0)
        clean_sheets_percentage = last_5_matches.get("clean_sheets_percentage", 0)
        
        failed_to_score = last_5_matches.get("failed_to_score", 0)
        failed_to_score_percentage = last_5_matches.get("failed_to_score_percentage", 0)
        
        # Analisar sequência de resultados
        form_sequence = form_data.get("general_form", "")
        
        # Determinar momento atual
        momentum_level = "Neutro"
        momentum_description = "Forma recente equilibrada"
        
        if wins >= 4:
            momentum_level = "Excelente"
            momentum_description = "Sequência muito positiva de resultados"
        elif wins == 3 and draws >= 1:
            momentum_level = "Muito Bom"
            momentum_description = "Sequência positiva de resultados sem derrotas"
        elif wins == 3:
            momentum_level = "Bom"
            momentum_description = "Mais vitórias que derrotas recentemente"
        elif losses >= 4:
            momentum_level = "Muito Ruim"
            momentum_description = "Sequência muito negativa de resultados"
        elif losses == 3 and draws >= 1:
            momentum_level = "Ruim"
            momentum_description = "Sequência negativa de resultados sem vitórias"
        elif losses == 3:
            momentum_level = "Fraco"
            momentum_description = "Mais derrotas que vitórias recentemente"
        elif draws >= 3:
            momentum_level = "Estável"
            momentum_description = "Muitos empates recentemente"
        
        # Analisar tendência (melhorando, piorando ou estável)
        trend = "Estável"
        
        if len(form_sequence) >= 3:
            # Converter sequência para pontos (V=3, E=1, D=0)
            points = []
            for result in form_sequence:
                if result == 'V':
                    points.append(3)
                elif result == 'E':
                    points.append(1)
                else:
                    points.append(0)
            
            # Comparar primeira metade com segunda metade
            first_half = sum(points[:len(points)//2])
            second_half = sum(points[len(points)//2:])
            
            if second_half > first_half + 1:
                trend = "Melhorando"
            elif first_half > second_half + 1:
                trend = "Piorando"
        
        # Analisar desempenho ofensivo
        offensive_rating = "Médio"
        
        if avg_goals_scored >= 2.5:
            offensive_rating = "Excelente"
        elif avg_goals_scored >= 2.0:
            offensive_rating = "Muito Bom"
        elif avg_goals_scored >= 1.5:
            offensive_rating = "Bom"
        elif avg_goals_scored <= 0.5:
            offensive_rating = "Muito Fraco"
        elif avg_goals_scored < 1.0:
            offensive_rating = "Fraco"
        
        # Analisar desempenho defensivo
        defensive_rating = "Médio"
        
        if avg_goals_conceded <= 0.5 and clean_sheets >= 3:
            defensive_rating = "Excelente"
        elif avg_goals_conceded <= 0.8 and clean_sheets >= 2:
            defensive_rating = "Muito Bom"
        elif avg_goals_conceded <= 1.0:
            defensive_rating = "Bom"
        elif avg_goals_conceded >= 2.5:
            defensive_rating = "Muito Fraco"
        elif avg_goals_conceded >= 2.0:
            defensive_rating = "Fraco"
        
        return {
            "team": team,
            "matches": matches,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "win_percentage": win_percentage,
            "avg_goals_scored": avg_goals_scored,
            "avg_goals_conceded": avg_goals_conceded,
            "clean_sheets": clean_sheets,
            "clean_sheets_percentage": clean_sheets_percentage,
            "failed_to_score": failed_to_score,
            "failed_to_score_percentage": failed_to_score_percentage,
            "form_sequence": form_sequence,
            "momentum_level": momentum_level,
            "momentum_description": momentum_description,
            "trend": trend,
            "offensive_rating": offensive_rating,
            "defensive_rating": defensive_rating
        }
    
    def analyze_home_away_performance(self, team: str) -> Dict[str, Any]:
        """
        Analisa o desempenho da equipe como mandante ou visitante.
        
        Args:
            team (str): Nome da equipe a ser analisada
            
        Returns:
            Dict[str, Any]: Análise do desempenho como mandante/visitante
        """
        if team not in self.team_form_data:
            return {"error": f"Dados de forma recente para {team} não disponíveis"}
        
        form_data = self.team_form_data[team]
        stats = form_data.get("stats", {})
        
        if not stats:
            return {"error": f"Estatísticas para {team} não disponíveis"}
        
        # Extrair dados relevantes
        win_percentage = {
            "overall": stats.get("win_percentage", {}).get("overall", 0),
            "home": stats.get("win_percentage", {}).get("home", 0),
            "away": stats.get("win_percentage", {}).get("away", 0)
        }
        
        goals_scored = {
            "overall": stats.get("goals_scored_per_game", {}).get("overall", 0),
            "home": stats.get("goals_scored_per_game", {}).get("home", 0),
            "away": stats.get("goals_scored_per_game", {}).get("away", 0)
        }
        
        goals_conceded = {
            "overall": stats.get("goals_conceded_per_game", {}).get("overall", 0),
            "home": stats.get("goals_conceded_per_game", {}).get("home", 0),
            "away": stats.get("goals_conceded_per_game", {}).get("away", 0)
        }
        
        btts_percentage = {
            "overall": stats.get("btts_percentage", {}).get("overall", 0),
            "home": stats.get("btts_percentage", {}).get("home", 0),
            "away": stats.get("btts_percentage", {}).get("away", 0)
        }
        
        clean_sheets_percentage = {
            "overall": stats.get("clean_sheets_percentage", {}).get("overall", 0),
            "home": stats.get("clean_sheets_percentage", {}).get("home", 0),
            "away": stats.get("clean_sheets_percentage", {}).get("away", 0)
        }
        
        failed_to_score_percentage = {
            "overall": stats.get("failed_to_score_percentage", {}).get("overall", 0),
            "home": stats.get("failed_to_score_percentage", {}).get("home", 0),
            "away": stats.get("failed_to_score_percentage", {}).get("away", 0)
        }
        
        xG = {
            "overall": stats.get("xG", {}).get("overall", 0),
            "home": stats.get("xG", {}).get("home", 0),
            "away": stats.get("xG", {}).get("away", 0)
        }
        
        xGC = {
            "overall": stats.get("xGC", {}).get("overall", 0),
            "home": stats.get("xGC", {}).get("home", 0),
            "away": stats.get("xGC", {}).get("away", 0)
        }
        
        # Determinar se a equipe é melhor em casa ou fora
        home_away_difference = win_percentage["home"] - win_percentage["away"]
        
        home_away_strength = "Equilibrado"
        if home_away_difference >= 20:
            home_away_strength = "Muito melhor em casa"
        elif home_away_difference >= 10:
            home_away_strength = "Melhor em casa"
        elif home_away_difference <= -20:
            home_away_strength = "Muito melhor fora"
        elif home_away_difference <= -10:
            home_away_strength = "Melhor fora"
        
        # Analisar diferenças ofensivas e defensivas
        offensive_difference = goals_scored["home"] - goals_scored["away"]
        defensive_difference = goals_conceded["away"] - goals_conceded["home"]
        
        offensive_home_away = "Equilibrado"
        if offensive_difference >= 1.0:
            offensive_home_away = "Muito mais ofensivo em casa"
        elif offensive_difference >= 0.5:
            offensive_home_away = "Mais ofensivo em casa"
        elif offensive_difference <= -1.0:
            offensive_home_away = "Muito mais ofensivo fora"
        elif offensive_difference <= -0.5:
            offensive_home_away = "Mais ofensivo fora"
        
        defensive_home_away = "Equilibrado"
        if defensive_difference >= 1.0:
            defensive_home_away = "Muito mais sólido defensivamente em casa"
        elif defensive_difference >= 0.5:
            defensive_home_away = "Mais sólido defensivamente em casa"
        elif defensive_difference <= -1.0:
            defensive_home_away = "Muito mais sólido defensivamente fora"
        elif defensive_difference <= -0.5:
            defensive_home_away = "Mais sólido defensivamente fora"
        
        # Determinar relevância para o jogo atual
        is_home_team = team == self.home_team
        relevance = "Alta" if ((is_home_team and home_away_difference > 0) or 
                              (not is_home_team and home_away_difference < 0)) else "Média"
        
        return {
            "team": team,
            "is_home_team": is_home_team,
            "win_percentage": win_percentage,
            "goals_scored": goals_scored,
            "goals_conceded": goals_conceded,
            "btts_percentage": btts_percentage,
            "clean_sheets_percentage": clean_sheets_percentage,
            "failed_to_score_percentage": failed_to_score_percentage,
            "xG": xG,
            "xGC": xGC,
            "home_away_difference": home_away_difference,
            "home_away_strength": home_away_strength,
            "offensive_difference": offensive_difference,
            "offensive_home_away": offensive_home_away,
            "defensive_difference": defensive_difference,
            "defensive_home_away": defensive_home_away,
            "relevance": relevance
        }
    
    def compare_teams_form(self) -> Dict[str, Any]:
        """
        Compara a forma recente das duas equipes.
        
        Returns:
            Dict[str, Any]: Comparação da forma recente
        """
        home_momentum = self.analyze_team_momentum(self.home_team)
        away_momentum = self.analyze_team_momentum(self.away_team)
        
        if "error" in home_momentum or "error" in away_momentum:
            return {"error": "Dados insuficientes para comparar a forma das equipes"}
        
        # Comparar momento atual
        momentum_levels = {
            "Excelente": 5,
            "Muito Bom": 4,
            "Bom": 3,
            "Estável": 2,
            "Neutro": 2,
            "Fraco": 1,
            "Ruim": 0,
            "Muito Ruim": -1
        }
        
        home_momentum_score = momentum_levels.get(home_momentum["momentum_level"], 2)
        away_momentum_score = momentum_levels.get(away_momentum["momentum_level"], 2)
        
        momentum_difference = home_momentum_score - away_momentum_score
        
        momentum_advantage = None
        if momentum_difference >= 3:
            momentum_advantage = f"{self.home_team} (vantagem muito significativa)"
        elif momentum_difference >= 1:
            momentum_advantage = f"{self.home_team} (vantagem significativa)"
        elif momentum_difference <= -3:
            momentum_advantage = f"{self.away_team} (vantagem muito significativa)"
        elif momentum_difference <= -1:
            momentum_advantage = f"{self.away_team} (vantagem significativa)"
        else:
            momentum_advantage = "Equilibrado"
        
        # Comparar tendências
        trend_advantage = None
        if home_momentum["trend"] == "Melhorando" and away_momentum["trend"] != "Melhorando":
            trend_advantage = self.home_team
        elif away_momentum["trend"] == "Melhorando" and home_momentum["trend"] != "Melhorando":
            trend_advantage = self.away_team
        elif home_momentum["trend"] == "Piorando" and away_momentum["trend"] != "Piorando":
            trend_advantage = self.away_team
        elif away_momentum["trend"] == "Piorando" and home_momentum["trend"] != "Piorando":
            trend_advantage = self.home_team
        else:
            trend_advantage = "Equilibrado"
        
        # Comparar desempenho ofensivo
        offensive_ratings = {
            "Excelente": 5,
            "Muito Bom": 4,
            "Bom": 3,
            "Médio": 2,
            "Fraco": 1,
            "Muito Fraco": 0
        }
        
        home_offensive_score = offensive_ratings.get(home_momentum["offensive_rating"], 2)
        away_offensive_score = offensive_ratings.get(away_momentum["offensive_rating"], 2)
        
        offensive_difference = home_offensive_score - away_offensive_score
        
        offensive_advantage = None
        if offensive_difference >= 2:
            offensive_advantage = f"{self.home_team} (vantagem significativa)"
        elif offensive_difference >= 1:
            offensive_advantage = f"{self.home_team} (leve vantagem)"
        elif offensive_difference <= -2:
            offensive_advantage = f"{self.away_team} (vantagem significativa)"
        elif offensive_difference <= -1:
            offensive_advantage = f"{self.away_team} (leve vantagem)"
        else:
            offensive_advantage = "Equilibrado"
        
        # Comparar desempenho defensivo
        defensive_ratings = {
            "Excelente": 5,
            "Muito Bom": 4,
            "Bom": 3,
            "Médio": 2,
            "Fraco": 1,
            "Muito Fraco": 0
        }
        
        home_defensive_score = defensive_ratings.get(home_momentum["defensive_rating"], 2)
        away_defensive_score = defensive_ratings.get(away_momentum["defensive_rating"], 2)
        
        defensive_difference = home_defensive_score - away_defensive_score
        
        defensive_advantage = None
        if defensive_difference >= 2:
            defensive_advantage = f"{self.home_team} (vantagem significativa)"
        elif defensive_difference >= 1:
            defensive_advantage = f"{self.home_team} (leve vantagem)"
        elif defensive_difference <= -2:
            defensive_advantage = f"{self.away_team} (vantagem significativa)"
        elif defensive_difference <= -1:
            defensive_advantage = f"{self.away_team} (leve vantagem)"
        else:
            defensive_advantage = "Equilibrado"
        
        # Comparar estatísticas diretas
        home_wins = home_momentum["wins"]
        away_wins = away_momentum["wins"]
        home_goals_scored = home_momentum["avg_goals_scored"]
        away_goals_scored = away_momentum["avg_goals_scored"]
        home_goals_conceded = home_momentum["avg_goals_conceded"]
        away_goals_conceded = away_momentum["avg_goals_conceded"]
        
        return {
            "home_momentum": home_momentum,
            "away_momentum": away_momentum,
            "momentum_difference": momentum_difference,
            "momentum_advantage": momentum_advantage,
            "trend_advantage": trend_advantage,
            "offensive_difference": offensive_difference,
            "offensive_advantage": offensive_advantage,
            "defensive_difference": defensive_difference,
            "defensive_advantage": defensive_advantage,
            "direct_comparison": {
                "wins": {
                    "home": home_wins,
                    "away": away_wins,
                    "difference": home_wins - away_wins
                },
                "goals_scored": {
                    "home": home_goals_scored,
                    "away": away_goals_scored,
                    "difference": home_goals_scored - away_goals_scored
                },
                "goals_conceded": {
                    "home": home_goals_conceded,
                    "away": away_goals_conceded,
                    "difference": away_goals_conceded - home_goals_conceded  # Invertido para que positivo seja vantagem para casa
                }
            }
        }
    
    def analyze_match_context(self) -> Dict[str, Any]:
        """
        Analisa o contexto do jogo atual baseado na forma recente.
        
        Returns:
            Dict[str, Any]: Análise do contexto do jogo
        """
        home_momentum = self.analyze_team_momentum(self.home_team)
        away_momentum = self.analyze_team_momentum(self.away_team)
        
        if "error" in home_momentum or "error" in away_momentum:
            return {"error": "Dados insuficientes para analisar o contexto do jogo"}
        
        home_home_away = self.analyze_home_away_performance(self.home_team)
        away_home_away = self.analyze_home_away_performance(self.away_team)
        
        if "error" in home_home_away or "error" in away_home_away:
            return {"error": "Dados insuficientes para analisar o contexto do jogo"}
        
        # Determinar o favorito baseado na forma recente
        comparison = self.compare_teams_form()
        
        momentum_advantage = comparison.get("momentum_advantage", "Equilibrado")
        offensive_advantage = comparison.get("offensive_advantage", "Equilibrado")
        defensive_advantage = comparison.get("defensive_advantage", "Equilibrado")
        
        # Considerar o fator casa
        home_advantage = home_home_away.get("home_away_strength", "Equilibrado")
        away_disadvantage = away_home_away.get("home_away_strength", "Equilibrado")
        
        home_advantage_factor = 0
        if "melhor em casa" in home_advantage:
            home_advantage_factor += 1
            if "Muito" in home_advantage:
                home_advantage_factor += 1
        
        away_disadvantage_factor = 0
        if "melhor em casa" in away_disadvantage:
            away_disadvantage_factor += 1
            if "Muito" in away_disadvantage:
                away_disadvantage_factor += 1
        
        # Calcular vantagem total para o mandante
        total_home_advantage = home_advantage_factor + away_disadvantage_factor
        
        # Determinar o favorito final
        favorite_team = None
        favorite_strength = "Leve favorito"
        
        if self.home_team in momentum_advantage and total_home_advantage >= 2:
            favorite_team = self.home_team
            if "muito significativa" in momentum_advantage:
                favorite_strength = "Forte favorito"
            elif "significativa" in momentum_advantage:
                favorite_strength = "Favorito"
        elif self.away_team in momentum_advantage and total_home_advantage <= 1:
            favorite_team = self.away_team
            if "muito significativa" in momentum_advantage and total_home_advantage == 0:
                favorite_strength = "Forte favorito"
            elif "significativa" in momentum_advantage or total_home_advantage == 0:
                favorite_strength = "Favorito"
        elif total_home_advantage >= 3:
            favorite_team = self.home_team
            favorite_strength = "Favorito"
        elif total_home_advantage >= 2:
            favorite_team = self.home_team
        elif self.home_team in momentum_advantage:
            favorite_team = self.home_team
        elif self.away_team in momentum_advantage:
            favorite_team = self.away_team
        else:
            favorite_team = self.home_team  # Leve vantagem para o mandante em caso de equilíbrio
        
        # Prever padrão de jogo
        expected_goals = (home_momentum["avg_goals_scored"] + away_momentum["avg_goals_conceded"] + 
                         away_momentum["avg_goals_scored"] + home_momentum["avg_goals_conceded"]) / 2
        
        expected_btts = "Provável" if (home_momentum["avg_goals_scored"] > 1.0 and 
                                      away_momentum["avg_goals_scored"] > 1.0) else "Possível"
        
        if home_momentum["failed_to_score_percentage"] > 40 or away_momentum["failed_to_score_percentage"] > 40:
            expected_btts = "Improvável"
        
        expected_pattern = None
        if expected_goals >= 3.0 and expected_btts == "Provável":
            expected_pattern = "Jogo aberto com muitos gols e ambas equipes marcando"
        elif expected_goals >= 3.0:
            expected_pattern = "Jogo com muitos gols, possivelmente concentrados em uma equipe"
        elif expected_goals >= 2.5 and expected_btts == "Provável":
            expected_pattern = "Jogo com gols moderados e ambas equipes marcando"
        elif expected_goals >= 2.5:
            expected_pattern = "Jogo com gols moderados, possivelmente concentrados em uma equipe"
        elif expected_btts == "Provável":
            expected_pattern = "Jogo com poucos gols, mas ambas equipes marcando"
        else:
            expected_pattern = "Jogo fechado com poucos gols"
        
        return {
            "home_momentum": home_momentum,
            "away_momentum": away_momentum,
            "home_home_away": home_home_away,
            "away_home_away": away_home_away,
            "comparison": comparison,
            "total_home_advantage": total_home_advantage,
            "favorite_team": favorite_team,
            "favorite_strength": favorite_strength,
            "expected_goals": expected_goals,
            "expected_btts": expected_btts,
            "expected_pattern": expected_pattern
        }
    
    def generate_insights(self) -> Dict[str, Any]:
        """
        Gera insights baseados na análise da forma recente.
        
        Returns:
            Dict[str, Any]: Insights da forma recente
        """
        match_context = self.analyze_match_context()
        
        if "error" in match_context:
            return {"error": "Dados insuficientes para gerar insights"}
        
        # Extrair dados relevantes
        home_momentum = match_context["home_momentum"]
        away_momentum = match_context["away_momentum"]
        home_home_away = match_context["home_home_away"]
        away_home_away = match_context["away_home_away"]
        comparison = match_context["comparison"]
        
        favorite_team = match_context["favorite_team"]
        favorite_strength = match_context["favorite_strength"]
        expected_pattern = match_context["expected_pattern"]
        
        # Gerar insights principais
        insights = []
        
        # Insight sobre o favorito
        if favorite_team:
            insights.append(f"{favorite_team} é {favorite_strength.lower()} baseado na forma recente e no fator casa.")
        else:
            insights.append("Confronto muito equilibrado baseado na forma recente.")
        
        # Insight sobre momento das equipes
        insights.append(f"{self.home_team} está em momento {home_momentum['momentum_level'].lower()}: {home_momentum['momentum_description'].lower()}.")
        insights.append(f"{self.away_team} está em momento {away_momentum['momentum_level'].lower()}: {away_momentum['momentum_description'].lower()}.")
        
        # Insight sobre tendências
        if home_momentum["trend"] != "Estável":
            insights.append(f"{self.home_team} mostra tendência de {home_momentum['trend'].lower()} nas últimas partidas.")
        
        if away_momentum["trend"] != "Estável":
            insights.append(f"{self.away_team} mostra tendência de {away_momentum['trend'].lower()} nas últimas partidas.")
        
        # Insight sobre desempenho ofensivo/defensivo
        insights.append(f"Ofensivamente, {self.home_team} tem desempenho {home_momentum['offensive_rating'].lower()} " +
                       f"(média de {home_momentum['avg_goals_scored']:.1f} gols marcados por jogo).")
        
        insights.append(f"Defensivamente, {self.home_team} tem desempenho {home_momentum['defensive_rating'].lower()} " +
                       f"(média de {home_momentum['avg_goals_conceded']:.1f} gols sofridos por jogo).")
        
        insights.append(f"Ofensivamente, {self.away_team} tem desempenho {away_momentum['offensive_rating'].lower()} " +
                       f"(média de {away_momentum['avg_goals_scored']:.1f} gols marcados por jogo).")
        
        insights.append(f"Defensivamente, {self.away_team} tem desempenho {away_momentum['defensive_rating'].lower()} " +
                       f"(média de {away_momentum['avg_goals_conceded']:.1f} gols sofridos por jogo).")
        
        # Insight sobre fator casa/fora
        if "melhor em casa" in home_home_away["home_away_strength"]:
            insights.append(f"{self.home_team} é {home_home_away['home_away_strength'].lower()}, " +
                           f"com {home_home_away['win_percentage']['home']}% de vitórias em casa vs " +
                           f"{home_home_away['win_percentage']['away']}% fora.")
        
        if "melhor fora" in away_home_away["home_away_strength"]:
            insights.append(f"{self.away_team} é {away_home_away['home_away_strength'].lower()}, " +
                           f"com {away_home_away['win_percentage']['away']}% de vitórias fora vs " +
                           f"{away_home_away['win_percentage']['home']}% em casa.")
        
        # Insight sobre padrão esperado de jogo
        insights.append(f"Padrão esperado: {expected_pattern}.")
        
        # Insight sobre vantagens específicas
        if comparison["momentum_advantage"] != "Equilibrado":
            insights.append(f"Vantagem de momento: {comparison['momentum_advantage']}.")
        
        if comparison["offensive_advantage"] != "Equilibrado":
            insights.append(f"Vantagem ofensiva: {comparison['offensive_advantage']}.")
        
        if comparison["defensive_advantage"] != "Equilibrado":
            insights.append(f"Vantagem defensiva: {comparison['defensive_advantage']}.")
        
        return {
            "match_context": match_context,
            "insights": insights
        }
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """
        Executa uma análise completa da forma recente.
        
        Returns:
            Dict[str, Any]: Análise completa da forma recente
        """
        return self.generate_insights()
