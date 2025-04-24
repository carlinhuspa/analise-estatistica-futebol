#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para análise das posições nas tabelas das equipes de futebol.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional

class TablePositionsAnalyzer:
    """
    Classe para analisar as posições nas tabelas das equipes de futebol.
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
        self.table_positions = processed_data.get("table_positions", {})
    
    def analyze_general_positions(self) -> Dict[str, Any]:
        """
        Analisa as posições gerais das equipes na tabela.
        
        Returns:
            Dict[str, Any]: Análise das posições gerais
        """
        if not self.table_positions:
            return {"error": "Dados de posições nas tabelas não disponíveis"}
        
        home_position_data = self.table_positions.get(self.home_team, {})
        away_position_data = self.table_positions.get(self.away_team, {})
        
        if not home_position_data or not away_position_data:
            return {"error": "Dados de posições para uma ou ambas as equipes não disponíveis"}
        
        # Extrair posições gerais
        home_general_position = home_position_data.get("general_position", 0)
        away_general_position = away_position_data.get("general_position", 0)
        total_teams = home_position_data.get("total_teams", 20)
        
        # Calcular percentis (quanto maior, melhor)
        home_percentile = ((total_teams - home_general_position + 1) / total_teams) * 100
        away_percentile = ((total_teams - away_general_position + 1) / total_teams) * 100
        
        # Determinar diferença de qualidade baseada na posição
        position_difference = away_general_position - home_general_position
        percentile_difference = home_percentile - away_percentile
        
        # Classificar a diferença
        quality_difference_level = "Equilibrado"
        if position_difference >= 10:
            quality_difference_level = "Grande vantagem para o mandante"
        elif position_difference >= 5:
            quality_difference_level = "Vantagem significativa para o mandante"
        elif position_difference >= 2:
            quality_difference_level = "Leve vantagem para o mandante"
        elif position_difference <= -10:
            quality_difference_level = "Grande vantagem para o visitante"
        elif position_difference <= -5:
            quality_difference_level = "Vantagem significativa para o visitante"
        elif position_difference <= -2:
            quality_difference_level = "Leve vantagem para o visitante"
        
        # Classificar as equipes por zona da tabela
        def classify_position(position, total):
            if position <= total * 0.15:  # Primeiros 15%
                return "Zona de título"
            elif position <= total * 0.3:  # Até 30%
                return "Zona de classificação para competições europeias"
            elif position <= total * 0.5:  # Até 50%
                return "Meio da tabela superior"
            elif position <= total * 0.7:  # Até 70%
                return "Meio da tabela inferior"
            elif position <= total * 0.85:  # Até 85%
                return "Zona de risco"
            else:  # Últimos 15%
                return "Zona de rebaixamento"
        
        home_zone = classify_position(home_general_position, total_teams)
        away_zone = classify_position(away_general_position, total_teams)
        
        return {
            "home_general_position": home_general_position,
            "away_general_position": away_general_position,
            "total_teams": total_teams,
            "home_percentile": home_percentile,
            "away_percentile": away_percentile,
            "position_difference": position_difference,
            "percentile_difference": percentile_difference,
            "quality_difference_level": quality_difference_level,
            "home_zone": home_zone,
            "away_zone": away_zone
        }
    
    def analyze_home_away_tables(self) -> Dict[str, Any]:
        """
        Analisa as posições das equipes nas tabelas de casa e fora.
        
        Returns:
            Dict[str, Any]: Análise das posições nas tabelas de casa e fora
        """
        if not self.table_positions:
            return {"error": "Dados de posições nas tabelas não disponíveis"}
        
        home_position_data = self.table_positions.get(self.home_team, {})
        away_position_data = self.table_positions.get(self.away_team, {})
        
        if not home_position_data or not away_position_data:
            return {"error": "Dados de posições para uma ou ambas as equipes não disponíveis"}
        
        # Extrair posições nas tabelas de casa e fora
        home_home_position = home_position_data.get("home_position")
        away_away_position = away_position_data.get("away_position")
        total_teams = home_position_data.get("total_teams", 20)
        
        if home_home_position is None or away_away_position is None:
            return {"error": "Dados de posições nas tabelas de casa e fora não disponíveis"}
        
        # Calcular percentis (quanto maior, melhor)
        home_home_percentile = ((total_teams - home_home_position + 1) / total_teams) * 100
        away_away_percentile = ((total_teams - away_away_position + 1) / total_teams) * 100
        
        # Determinar diferença de qualidade baseada na posição específica
        specific_position_difference = away_away_position - home_home_position
        specific_percentile_difference = home_home_percentile - away_away_percentile
        
        # Classificar a diferença específica
        specific_quality_difference_level = "Equilibrado"
        if specific_position_difference >= 10:
            specific_quality_difference_level = "Grande vantagem para o mandante em casa"
        elif specific_position_difference >= 5:
            specific_quality_difference_level = "Vantagem significativa para o mandante em casa"
        elif specific_position_difference >= 2:
            specific_quality_difference_level = "Leve vantagem para o mandante em casa"
        elif specific_position_difference <= -10:
            specific_quality_difference_level = "Grande vantagem para o visitante fora"
        elif specific_position_difference <= -5:
            specific_quality_difference_level = "Vantagem significativa para o visitante fora"
        elif specific_position_difference <= -2:
            specific_quality_difference_level = "Leve vantagem para o visitante fora"
        
        # Comparar posições gerais vs específicas
        home_position_difference = home_position_data.get("general_position", 0) - home_home_position
        away_position_difference = away_position_data.get("general_position", 0) - away_away_position
        
        home_specific_strength = None
        if home_position_difference >= 5:
            home_specific_strength = "Muito mais forte em casa"
        elif home_position_difference >= 2:
            home_specific_strength = "Significativamente mais forte em casa"
        elif home_position_difference >= 1:
            home_specific_strength = "Ligeiramente mais forte em casa"
        elif home_position_difference <= -5:
            home_specific_strength = "Muito mais fraco em casa"
        elif home_position_difference <= -2:
            home_specific_strength = "Significativamente mais fraco em casa"
        elif home_position_difference <= -1:
            home_specific_strength = "Ligeiramente mais fraco em casa"
        else:
            home_specific_strength = "Desempenho similar em casa e fora"
        
        away_specific_strength = None
        if away_position_difference <= -5:
            away_specific_strength = "Muito mais forte fora"
        elif away_position_difference <= -2:
            away_specific_strength = "Significativamente mais forte fora"
        elif away_position_difference <= -1:
            away_specific_strength = "Ligeiramente mais forte fora"
        elif away_position_difference >= 5:
            away_specific_strength = "Muito mais fraco fora"
        elif away_position_difference >= 2:
            away_specific_strength = "Significativamente mais fraco fora"
        elif away_position_difference >= 1:
            away_specific_strength = "Ligeiramente mais fraco fora"
        else:
            away_specific_strength = "Desempenho similar em casa e fora"
        
        return {
            "home_home_position": home_home_position,
            "away_away_position": away_away_position,
            "total_teams": total_teams,
            "home_home_percentile": home_home_percentile,
            "away_away_percentile": away_away_percentile,
            "specific_position_difference": specific_position_difference,
            "specific_percentile_difference": specific_percentile_difference,
            "specific_quality_difference_level": specific_quality_difference_level,
            "home_position_difference": home_position_difference,
            "away_position_difference": away_position_difference,
            "home_specific_strength": home_specific_strength,
            "away_specific_strength": away_specific_strength
        }
    
    def analyze_performance_metrics(self) -> Dict[str, Any]:
        """
        Analisa as métricas de desempenho das equipes.
        
        Returns:
            Dict[str, Any]: Análise das métricas de desempenho
        """
        if not self.table_positions:
            return {"error": "Dados de posições nas tabelas não disponíveis"}
        
        direct_comparison = self.table_positions.get("direct_comparison", {})
        
        if not direct_comparison:
            return {"error": "Dados de comparação direta não disponíveis"}
        
        # Extrair métricas relevantes
        home_win_percentage = direct_comparison.get("home_win_percentage", 0)
        away_win_percentage = direct_comparison.get("away_win_percentage", 0)
        
        home_goals_scored = direct_comparison.get("home_goals_scored", 0)
        away_goals_scored = direct_comparison.get("away_goals_scored", 0)
        
        home_goals_conceded = direct_comparison.get("home_goals_conceded", 0)
        away_goals_conceded = direct_comparison.get("away_goals_conceded", 0)
        
        home_xG = direct_comparison.get("home_xG", 0)
        away_xG = direct_comparison.get("away_xG", 0)
        
        home_xGC = direct_comparison.get("home_xGC", 0)
        away_xGC = direct_comparison.get("away_xGC", 0)
        
        # Calcular diferenças
        win_percentage_difference = home_win_percentage - away_win_percentage
        goals_scored_difference = home_goals_scored - away_goals_scored
        goals_conceded_difference = away_goals_conceded - home_goals_conceded  # Invertido para que positivo seja vantagem para casa
        xG_difference = home_xG - away_xG
        xGC_difference = away_xGC - home_xGC  # Invertido para que positivo seja vantagem para casa
        
        # Classificar vantagens
        win_advantage = None
        if win_percentage_difference >= 25:
            win_advantage = f"{self.home_team} (vantagem muito significativa)"
        elif win_percentage_difference >= 15:
            win_advantage = f"{self.home_team} (vantagem significativa)"
        elif win_percentage_difference >= 5:
            win_advantage = f"{self.home_team} (leve vantagem)"
        elif win_percentage_difference <= -25:
            win_advantage = f"{self.away_team} (vantagem muito significativa)"
        elif win_percentage_difference <= -15:
            win_advantage = f"{self.away_team} (vantagem significativa)"
        elif win_percentage_difference <= -5:
            win_advantage = f"{self.away_team} (leve vantagem)"
        else:
            win_advantage = "Equilibrado"
        
        offensive_advantage = None
        if goals_scored_difference >= 1.0:
            offensive_advantage = f"{self.home_team} (vantagem muito significativa)"
        elif goals_scored_difference >= 0.5:
            offensive_advantage = f"{self.home_team} (vantagem significativa)"
        elif goals_scored_difference >= 0.2:
            offensive_advantage = f"{self.home_team} (leve vantagem)"
        elif goals_scored_difference <= -1.0:
            offensive_advantage = f"{self.away_team} (vantagem muito significativa)"
        elif goals_scored_difference <= -0.5:
            offensive_advantage = f"{self.away_team} (vantagem significativa)"
        elif goals_scored_difference <= -0.2:
            offensive_advantage = f"{self.away_team} (leve vantagem)"
        else:
            offensive_advantage = "Equilibrado"
        
        defensive_advantage = None
        if goals_conceded_difference >= 1.0:
            defensive_advantage = f"{self.home_team} (vantagem muito significativa)"
        elif goals_conceded_difference >= 0.5:
            defensive_advantage = f"{self.home_team} (vantagem significativa)"
        elif goals_conceded_difference >= 0.2:
            defensive_advantage = f"{self.home_team} (leve vantagem)"
        elif goals_conceded_difference <= -1.0:
            defensive_advantage = f"{self.away_team} (vantagem muito significativa)"
        elif goals_conceded_difference <= -0.5:
            defensive_advantage = f"{self.away_team} (vantagem significativa)"
        elif goals_conceded_difference <= -0.2:
            defensive_advantage = f"{self.away_team} (leve vantagem)"
        else:
            defensive_advantage = "Equilibrado"
        
        xG_advantage = None
        if xG_difference >= 0.5:
            xG_advantage = f"{self.home_team} (vantagem significativa)"
        elif xG_difference >= 0.2:
            xG_advantage = f"{self.home_team} (leve vantagem)"
        elif xG_difference <= -0.5:
            xG_advantage = f"{self.away_team} (vantagem significativa)"
        elif xG_difference <= -0.2:
            xG_advantage = f"{self.away_team} (leve vantagem)"
        else:
            xG_advantage = "Equilibrado"
        
        xGC_advantage = None
        if xGC_difference >= 0.5:
            xGC_advantage = f"{self.home_team} (vantagem significativa)"
        elif xGC_difference >= 0.2:
            xGC_advantage = f"{self.home_team} (leve vantagem)"
        elif xGC_difference <= -0.5:
            xGC_advantage = f"{self.away_team} (vantagem significativa)"
        elif xGC_difference <= -0.2:
            xGC_advantage = f"{self.away_team} (leve vantagem)"
        else:
            xGC_advantage = "Equilibrado"
        
        return {
            "win_percentage": {
                "home": home_win_percentage,
                "away": away_win_percentage,
                "difference": win_percentage_difference,
                "advantage": win_advantage
            },
            "goals_scored": {
                "home": home_goals_scored,
                "away": away_goals_scored,
                "difference": goals_scored_difference,
                "advantage": offensive_advantage
            },
            "goals_conceded": {
                "home": home_goals_conceded,
                "away": away_goals_conceded,
                "difference": goals_conceded_difference,
                "advantage": defensive_advantage
            },
            "xG": {
                "home": home_xG,
                "away": away_xG,
                "difference": xG_difference,
                "advantage": xG_advantage
            },
            "xGC": {
                "home": home_xGC,
                "away": away_xGC,
                "difference": xGC_difference,
                "advantage": xGC_advantage
            }
        }
    
    def analyze_match_quality(self) -> Dict[str, Any]:
        """
        Analisa a qualidade esperada do jogo baseado nas posições das equipes.
        
        Returns:
            Dict[str, Any]: Análise da qualidade esperada do jogo
        """
        general_positions = self.analyze_general_positions()
        
        if "error" in general_positions:
            return {"error": "Dados insuficientes para analisar a qualidade do jogo"}
        
        home_position = general_positions["home_general_position"]
        away_position = general_positions["away_general_position"]
        total_teams = general_positions["total_teams"]
        
        # Calcular média das posições
        average_position = (home_position + away_position) / 2
        
        # Calcular diferença absoluta de posições
        position_gap = abs(home_position - away_position)
        
        # Classificar qualidade do jogo
        match_quality = None
        if average_position <= total_teams * 0.2:  # Top 20%
            if position_gap <= 3:
                match_quality = "Jogo de altíssima qualidade entre equipes de elite"
            else:
                match_quality = "Jogo de alta qualidade com favorito claro"
        elif average_position <= total_teams * 0.4:  # Top 40%
            if position_gap <= 3:
                match_quality = "Jogo de boa qualidade entre equipes fortes"
            else:
                match_quality = "Jogo de qualidade média-alta com favorito claro"
        elif average_position <= total_teams * 0.6:  # Meio da tabela
            if position_gap <= 3:
                match_quality = "Jogo equilibrado entre equipes de meio de tabela"
            else:
                match_quality = "Jogo de qualidade média com favorito"
        elif average_position <= total_teams * 0.8:  # Bottom 40%
            if position_gap <= 3:
                match_quality = "Jogo equilibrado entre equipes da parte inferior da tabela"
            else:
                match_quality = "Jogo de qualidade média-baixa com favorito"
        else:  # Bottom 20%
            if position_gap <= 3:
                match_quality = "Jogo de luta contra o rebaixamento"
            else:
                match_quality = "Jogo de baixa qualidade com favorito"
        
        # Classificar equilíbrio do jogo
        match_balance = None
        if position_gap <= 2:
            match_balance = "Muito equilibrado"
        elif position_gap <= 5:
            match_balance = "Equilibrado"
        elif position_gap <= 10:
            match_balance = "Desequilibrado"
        else:
            match_balance = "Muito desequilibrado"
        
        # Determinar importância do jogo
        home_importance = None
        away_importance = None
        
        # Para o mandante
        if home_position <= 3:
            home_importance = "Luta pelo título"
        elif home_position <= 6:
            home_importance = "Luta por vaga em competições europeias"
        elif home_position >= total_teams - 3:
            home_importance = "Luta contra o rebaixamento"
        elif home_position >= total_teams - 6:
            home_importance = "Afastamento da zona de rebaixamento"
        else:
            home_importance = "Manutenção na parte média da tabela"
        
        # Para o visitante
        if away_position <= 3:
            away_importance = "Luta pelo título"
        elif away_position <= 6:
            away_importance = "Luta por vaga em competições europeias"
        elif away_position >= total_teams - 3:
            away_importance = "Luta contra o rebaixamento"
        elif away_position >= total_teams - 6:
            away_importance = "Afastamento da zona de rebaixamento"
        else:
            away_importance = "Manutenção na parte média da tabela"
        
        return {
            "home_position": home_position,
            "away_position": away_position,
            "average_position": average_position,
            "position_gap": position_gap,
            "match_quality": match_quality,
            "match_balance": match_balance,
            "home_importance": home_importance,
            "away_importance": away_importance
        }
    
    def generate_insights(self) -> Dict[str, Any]:
        """
        Gera insights baseados na análise das posições nas tabelas.
        
        Returns:
            Dict[str, Any]: Insights das posições nas tabelas
        """
        general_positions = self.analyze_general_positions()
        home_away_tables = self.analyze_home_away_tables()
        performance_metrics = self.analyze_performance_metrics()
        match_quality = self.analyze_match_quality()
        
        if ("error" in general_positions or "error" in home_away_tables or 
            "error" in performance_metrics or "error" in match_quality):
            return {"error": "Dados insuficientes para gerar insights"}
        
        # Gerar insights principais
        insights = []
        
        # Insight sobre posições gerais
        insights.append(f"{self.home_team} está na {general_positions['home_general_position']}ª posição " +
                       f"({general_positions['home_zone']}), enquanto {self.away_team} está na " +
                       f"{general_positions['away_general_position']}ª posição ({general_positions['away_zone']}).")
        
        # Insight sobre diferença de qualidade
        insights.append(f"Diferença de qualidade: {general_positions['quality_difference_level']}.")
        
        # Insight sobre desempenho específico casa/fora
        insights.append(f"{self.home_team} está na {home_away_tables['home_home_position']}ª posição na tabela de mandantes " +
                       f"({home_away_tables['home_specific_strength']}).")
        
        insights.append(f"{self.away_team} está na {home_away_tables['away_away_position']}ª posição na tabela de visitantes " +
                       f"({home_away_tables['away_specific_strength']}).")
        
        # Insight sobre vantagens específicas
        win_advantage = performance_metrics["win_percentage"]["advantage"]
        if win_advantage != "Equilibrado":
            insights.append(f"Vantagem em percentual de vitórias: {win_advantage}.")
        
        offensive_advantage = performance_metrics["goals_scored"]["advantage"]
        if offensive_advantage != "Equilibrado":
            insights.append(f"Vantagem ofensiva: {offensive_advantage}.")
        
        defensive_advantage = performance_metrics["goals_conceded"]["advantage"]
        if defensive_advantage != "Equilibrado":
            insights.append(f"Vantagem defensiva: {defensive_advantage}.")
        
        xG_advantage = performance_metrics["xG"]["advantage"]
        if xG_advantage != "Equilibrado":
            insights.append(f"Vantagem em Expected Goals (xG): {xG_advantage}.")
        
        xGC_advantage = performance_metrics["xGC"]["advantage"]
        if xGC_advantage != "Equilibrado":
            insights.append(f"Vantagem em Expected Goals Conceded (xGC): {xGC_advantage}.")
        
        # Insight sobre qualidade e equilíbrio do jogo
        insights.append(f"Qualidade esperada do jogo: {match_quality['match_quality']}.")
        insights.append(f"Equilíbrio do jogo: {match_quality['match_balance']}.")
        
        # Insight sobre importância do jogo para cada equipe
        insights.append(f"Importância para {self.home_team}: {match_quality['home_importance']}.")
        insights.append(f"Importância para {self.away_team}: {match_quality['away_importance']}.")
        
        # Insight sobre confronto específico casa vs fora
        insights.append(f"No confronto específico {self.home_team} (casa) vs {self.away_team} (fora): " +
                       f"{home_away_tables['specific_quality_difference_level']}.")
        
        return {
            "general_positions": general_positions,
            "home_away_tables": home_away_tables,
            "performance_metrics": performance_metrics,
            "match_quality": match_quality,
            "insights": insights
        }
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """
        Executa uma análise completa das posições nas tabelas.
        
        Returns:
            Dict[str, Any]: Análise completa das posições nas tabelas
        """
        return self.generate_insights()
