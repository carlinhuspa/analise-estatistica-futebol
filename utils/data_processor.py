#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para processamento e estruturação de dados estatísticos de futebol.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional

class FootballDataProcessor:
    """
    Classe para processar e estruturar dados estatísticos de futebol.
    """
    
    def __init__(self, extracted_data: Dict[str, Any]):
        """
        Inicializa o processador com os dados extraídos.
        
        Args:
            extracted_data (Dict[str, Any]): Dados extraídos do texto
        """
        self.data = extracted_data
        self.home_team = extracted_data["basic_info"]["home_team"]
        self.away_team = extracted_data["basic_info"]["away_team"]
    
    def process_head_to_head(self) -> Dict[str, Any]:
        """
        Processa os dados de confrontos diretos.
        
        Returns:
            Dict[str, Any]: Dados processados de confrontos diretos
        """
        h2h_data = self.data.get("head_to_head", {})
        if not h2h_data:
            return {}
        
        # Calcular estatísticas adicionais
        total_matches = h2h_data.get("total_matches", 0)
        home_wins = h2h_data.get("home_team_wins", 0)
        away_wins = h2h_data.get("away_team_wins", 0)
        draws = h2h_data.get("draws", 0)
        
        # Calcular médias de gols nos últimos 5 confrontos
        last_matches = h2h_data.get("last_matches", [])
        
        home_goals = []
        away_goals = []
        total_goals = []
        btts_matches = 0
        over_2_5_matches = 0
        
        for match in last_matches:
            home_team_in_match = match.get("home_team", "")
            away_team_in_match = match.get("away_team", "")
            home_score = match.get("home_score", 0)
            away_score = match.get("away_score", 0)
            
            # Ajustar para garantir que os gols sejam atribuídos às equipes corretas
            if home_team_in_match == self.home_team:
                home_goals.append(home_score)
                away_goals.append(away_score)
            else:
                home_goals.append(away_score)
                away_goals.append(home_score)
            
            total_goals.append(home_score + away_score)
            
            if home_score > 0 and away_score > 0:
                btts_matches += 1
            
            if home_score + away_score > 2.5:
                over_2_5_matches += 1
        
        # Calcular médias
        avg_home_goals = np.mean(home_goals) if home_goals else 0
        avg_away_goals = np.mean(away_goals) if away_goals else 0
        avg_total_goals = np.mean(total_goals) if total_goals else 0
        
        # Calcular percentuais para os últimos 5 jogos
        btts_percentage = (btts_matches / len(last_matches)) * 100 if last_matches else 0
        over_2_5_percentage = (over_2_5_matches / len(last_matches)) * 100 if last_matches else 0
        
        # Criar DataFrame para os últimos confrontos
        last_matches_df = pd.DataFrame(last_matches)
        
        # Adicionar resultados processados
        processed_h2h = {
            "total_matches": total_matches,
            "home_team_wins": home_wins,
            "away_team_wins": away_wins,
            "draws": draws,
            "home_win_percentage": (home_wins / total_matches) * 100 if total_matches else 0,
            "away_win_percentage": (away_wins / total_matches) * 100 if total_matches else 0,
            "draw_percentage": (draws / total_matches) * 100 if total_matches else 0,
            "last_5_matches": {
                "matches": last_matches,
                "avg_home_goals": avg_home_goals,
                "avg_away_goals": avg_away_goals,
                "avg_total_goals": avg_total_goals,
                "btts_percentage": btts_percentage,
                "over_2_5_percentage": over_2_5_percentage,
                "home_wins": sum(1 for m in last_matches if 
                                (m.get("home_team") == self.home_team and m.get("home_score") > m.get("away_score")) or
                                (m.get("away_team") == self.home_team and m.get("away_score") > m.get("home_score"))),
                "away_wins": sum(1 for m in last_matches if 
                                (m.get("home_team") == self.away_team and m.get("home_score") > m.get("away_score")) or
                                (m.get("away_team") == self.away_team and m.get("away_score") > m.get("home_score"))),
                "draws": sum(1 for m in last_matches if m.get("home_score") == m.get("away_score"))
            }
        }
        
        # Adicionar estatísticas de gols dos confrontos diretos
        if "goals_stats" in h2h_data:
            processed_h2h["goals_stats"] = h2h_data["goals_stats"]
        
        return processed_h2h
    
    def process_team_form(self) -> Dict[str, Dict[str, Any]]:
        """
        Processa os dados de forma recente das equipes.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dados processados de forma recente
        """
        team_form_data = self.data.get("team_form", {})
        if not team_form_data:
            return {}
        
        processed_form = {}
        
        for team, form_data in team_form_data.items():
            last_matches = form_data.get("last_matches", [])
            
            # Calcular estatísticas dos últimos jogos
            wins = sum(1 for m in last_matches if m.get("result") == "V")
            draws = sum(1 for m in last_matches if m.get("result") == "E")
            losses = sum(1 for m in last_matches if m.get("result") == "D")
            
            goals_scored = []
            goals_conceded = []
            clean_sheets = 0
            failed_to_score = 0
            
            for match in last_matches:
                home_team = match.get("home_team", "")
                away_team = match.get("away_team", "")
                home_score = match.get("home_score", 0)
                away_score = match.get("away_score", 0)
                
                if home_team == team:
                    goals_scored.append(home_score)
                    goals_conceded.append(away_score)
                    if away_score == 0:
                        clean_sheets += 1
                    if home_score == 0:
                        failed_to_score += 1
                else:
                    goals_scored.append(away_score)
                    goals_conceded.append(home_score)
                    if home_score == 0:
                        clean_sheets += 1
                    if away_score == 0:
                        failed_to_score += 1
            
            # Calcular médias
            avg_goals_scored = np.mean(goals_scored) if goals_scored else 0
            avg_goals_conceded = np.mean(goals_conceded) if goals_conceded else 0
            
            # Criar DataFrame para os últimos jogos
            last_matches_df = pd.DataFrame(last_matches)
            
            # Adicionar estatísticas processadas
            processed_form[team] = {
                "general_form": form_data.get("general_form", ""),
                "home_form": form_data.get("home_form", ""),
                "away_form": form_data.get("away_form", ""),
                "last_5_matches": {
                    "matches": last_matches,
                    "wins": wins,
                    "draws": draws,
                    "losses": losses,
                    "win_percentage": (wins / len(last_matches)) * 100 if last_matches else 0,
                    "draw_percentage": (draws / len(last_matches)) * 100 if last_matches else 0,
                    "loss_percentage": (losses / len(last_matches)) * 100 if last_matches else 0,
                    "avg_goals_scored": avg_goals_scored,
                    "avg_goals_conceded": avg_goals_conceded,
                    "clean_sheets": clean_sheets,
                    "clean_sheets_percentage": (clean_sheets / len(last_matches)) * 100 if last_matches else 0,
                    "failed_to_score": failed_to_score,
                    "failed_to_score_percentage": (failed_to_score / len(last_matches)) * 100 if last_matches else 0
                }
            }
            
            # Adicionar estatísticas gerais
            if "stats" in form_data:
                processed_form[team]["stats"] = form_data["stats"]
        
        return processed_form
    
    def process_table_positions(self) -> Dict[str, Dict[str, Any]]:
        """
        Processa os dados de posições nas tabelas.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dados processados de posições nas tabelas
        """
        positions_data = self.data.get("table_positions", {})
        if not positions_data:
            return {}
        
        processed_positions = {}
        
        for team, position_data in positions_data.items():
            # Calcular percentis de posição
            general_position = position_data.get("general_position", 0)
            total_teams = position_data.get("total_teams", 20)
            
            general_percentile = ((total_teams - general_position + 1) / total_teams) * 100 if total_teams else 0
            
            # Adicionar dados processados
            processed_positions[team] = {
                "general_position": general_position,
                "total_teams": total_teams,
                "general_percentile": general_percentile,
                "home_position": position_data.get("home_position"),
                "away_position": position_data.get("away_position")
            }
            
            # Adicionar comparações entre equipes
            if team == self.home_team and self.away_team in positions_data:
                away_position = positions_data[self.away_team].get("general_position", 0)
                position_difference = away_position - general_position
                processed_positions[team]["position_difference"] = position_difference
                processed_positions[team]["is_higher_ranked"] = position_difference > 0
            
            if team == self.away_team and self.home_team in positions_data:
                home_position = positions_data[self.home_team].get("general_position", 0)
                position_difference = home_position - general_position
                processed_positions[team]["position_difference"] = position_difference
                processed_positions[team]["is_higher_ranked"] = position_difference > 0
        
        # Adicionar comparação direta entre mandante e visitante
        if self.home_team in processed_positions and self.away_team in processed_positions:
            home_team_form = self.data.get("team_form", {}).get(self.home_team, {}).get("stats", {})
            away_team_form = self.data.get("team_form", {}).get(self.away_team, {}).get("stats", {})
            
            if home_team_form and away_team_form:
                # Comparar estatísticas em casa do mandante vs fora do visitante
                home_comparison = {
                    "home_win_percentage": home_team_form.get("win_percentage", {}).get("home", 0),
                    "away_win_percentage": away_team_form.get("win_percentage", {}).get("away", 0),
                    "home_goals_scored": home_team_form.get("goals_scored_per_game", {}).get("home", 0),
                    "away_goals_scored": away_team_form.get("goals_scored_per_game", {}).get("away", 0),
                    "home_goals_conceded": home_team_form.get("goals_conceded_per_game", {}).get("home", 0),
                    "away_goals_conceded": away_team_form.get("goals_conceded_per_game", {}).get("away", 0),
                    "home_xG": home_team_form.get("xG", {}).get("home", 0),
                    "away_xG": away_team_form.get("xG", {}).get("away", 0),
                    "home_xGC": home_team_form.get("xGC", {}).get("home", 0),
                    "away_xGC": away_team_form.get("xGC", {}).get("away", 0)
                }
                
                processed_positions["direct_comparison"] = home_comparison
        
        return processed_positions
    
    def process_predictions(self) -> Dict[str, Any]:
        """
        Processa os dados de prognósticos.
        
        Returns:
            Dict[str, Any]: Dados processados de prognósticos
        """
        predictions_data = self.data.get("predictions", {})
        if not predictions_data:
            return {}
        
        # Processar prognósticos gerais
        general_predictions = predictions_data.get("general", {})
        
        # Calcular diferenças em relação à média da liga
        if general_predictions:
            general_predictions["over_2_5_vs_league"] = general_predictions.get("over_2_5_percentage", 0) - general_predictions.get("over_2_5_league_avg", 0)
            general_predictions["over_1_5_vs_league"] = general_predictions.get("over_1_5_percentage", 0) - general_predictions.get("over_1_5_league_avg", 0)
            general_predictions["btts_vs_league"] = general_predictions.get("btts_percentage", 0) - general_predictions.get("btts_league_avg", 0)
            general_predictions["goals_vs_league"] = general_predictions.get("goals_per_game", 0) - general_predictions.get("goals_per_game_league_avg", 0)
            general_predictions["cards_vs_league"] = general_predictions.get("cards_per_game", 0) - general_predictions.get("cards_per_game_league_avg", 0)
            general_predictions["corners_vs_league"] = general_predictions.get("corners_per_game", 0) - general_predictions.get("corners_per_game_league_avg", 0)
        
        # Processar prognósticos detalhados de gols
        goals_detailed = predictions_data.get("goals_detailed", {})
        
        # Processar prognósticos de cantos
        corners = predictions_data.get("corners", {})
        
        # Processar prognósticos de cartões
        cards = predictions_data.get("cards", {})
        
        # Processar prognósticos de primeiro tempo/segundo tempo
        halftime_fulltime = predictions_data.get("halftime_fulltime", {})
        
        # Processar prognósticos de quem marca primeiro
        first_goal = predictions_data.get("first_goal", {})
        
        # Criar estrutura de dados processados
        processed_predictions = {
            "gpt_analysis": predictions_data.get("gpt_analysis", ""),
            "general": general_predictions,
            "goals_detailed": goals_detailed,
            "corners": corners,
            "cards": cards,
            "halftime_fulltime": halftime_fulltime,
            "first_goal": first_goal
        }
        
        return processed_predictions
    
    def process_all_data(self) -> Dict[str, Any]:
        """
        Processa todos os dados extraídos.
        
        Returns:
            Dict[str, Any]: Todos os dados processados
        """
        processed_h2h = self.process_head_to_head()
        processed_form = self.process_team_form()
        processed_positions = self.process_table_positions()
        processed_predictions = self.process_predictions()
        
        return {
            "basic_info": self.data.get("basic_info", {}),
            "head_to_head": processed_h2h,
            "team_form": processed_form,
            "table_positions": processed_positions,
            "predictions": processed_predictions
        }
