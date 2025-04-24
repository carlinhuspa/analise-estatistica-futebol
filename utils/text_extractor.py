#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para extração de dados do texto de estatísticas de futebol.
"""

import re
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional

class FootballStatsExtractor:
    """
    Classe para extrair dados estatísticos de futebol a partir de texto.
    """
    
    def __init__(self, text: str):
        """
        Inicializa o extrator com o texto a ser analisado.
        
        Args:
            text (str): Texto completo da página de estatísticas
        """
        self.text = text
        self.home_team = ""
        self.away_team = ""
        self.match_date = ""
        self.stadium = ""
        
    def extract_basic_info(self) -> Dict[str, str]:
        """
        Extrai informações básicas da partida (times, data, estádio).
        
        Returns:
            Dict[str, str]: Dicionário com informações básicas
        """
        # Extrair times
        match_pattern = r"(\d{2}/\d{2} \d{4} - \d{2}:\d{2}).*?\n(.*?) x (.*?)\n"
        match = re.search(match_pattern, self.text)
        
        if match:
            self.match_date = match.group(1)
            self.home_team = match.group(2)
            self.away_team = match.group(3)
        
        # Extrair estádio
        stadium_pattern = r"Estádio - (.*?) \("
        stadium_match = re.search(stadium_pattern, self.text)
        if stadium_match:
            self.stadium = stadium_match.group(1)
        
        return {
            "match_date": self.match_date,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "stadium": self.stadium
        }
    
    def extract_head_to_head(self) -> Dict[str, Any]:
        """
        Extrai dados de confrontos diretos entre as equipes.
        
        Returns:
            Dict[str, Any]: Dicionário com estatísticas de confrontos diretos
        """
        # Padrão para extrair o resumo de confrontos diretos
        h2h_pattern = r"O histórico de confrontos diretos entre (.*?) e (.*?) mostra que, dos (\d+) jogos disputados, (.*?) venceu (\d+) vezes e (.*?) venceu (\d+) vezes. Houve (\d+) empates"
        h2h_match = re.search(h2h_pattern, self.text)
        
        if not h2h_match:
            return {}
        
        total_matches = int(h2h_match.group(3))
        team1_wins = int(h2h_match.group(5))
        team2_wins = int(h2h_match.group(7))
        draws = int(h2h_match.group(8))
        
        # Extrair estatísticas de gols nos confrontos
        goals_pattern = r"Mais de 1.5\n(\d+) / (\d+) Jogos\n(\d+)%Mais de 2.5\n(\d+) / (\d+) Jogos\n(\d+)%Mais de 3.5\n(\d+) / (\d+) Jogos\n(\d+)%AM\n(\d+) / (\d+) Jogos"
        goals_match = re.search(goals_pattern, self.text)
        
        goals_stats = {}
        if goals_match:
            goals_stats = {
                "over_1_5_matches": int(goals_match.group(1)),
                "over_1_5_total": int(goals_match.group(2)),
                "over_1_5_percent": int(goals_match.group(3)),
                "over_2_5_matches": int(goals_match.group(4)),
                "over_2_5_total": int(goals_match.group(5)),
                "over_2_5_percent": int(goals_match.group(6)),
                "over_3_5_matches": int(goals_match.group(7)),
                "over_3_5_total": int(goals_match.group(8)),
                "over_3_5_percent": int(goals_match.group(9)),
                "btts_matches": int(goals_match.group(10)),
                "btts_total": int(goals_match.group(11)),
                "btts_percent": int(goals_match.group(3))
            }
        
        # Extrair últimos 5 confrontos diretos
        last_matches_pattern = r"(.*?) x (.*?) Resultados anteriores\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n"
        last_matches_section = re.search(last_matches_pattern, self.text, re.DOTALL)
        
        last_matches = []
        if last_matches_section:
            matches_text = last_matches_section.group(0)
            match_lines = matches_text.strip().split('\n')[2:7]  # Pegar as 5 linhas após o cabeçalho
            
            for line in match_lines:
                date_match = re.search(r"(\d{2}/\d{2} \d{4})", line)
                score_match = re.search(r"(\d+)\n(.*?)(\d+)", line)
                
                if date_match and score_match:
                    date = date_match.group(1)
                    team1_score = score_match.group(1)
                    team2_score = score_match.group(3)
                    
                    last_matches.append({
                        "date": date,
                        "home_team": self.home_team if line.startswith(self.home_team) else self.away_team,
                        "away_team": self.away_team if line.startswith(self.home_team) else self.home_team,
                        "home_score": int(team1_score),
                        "away_score": int(team2_score)
                    })
        
        return {
            "total_matches": total_matches,
            "home_team_wins": team1_wins if h2h_match.group(4) == self.home_team else team2_wins,
            "away_team_wins": team2_wins if h2h_match.group(4) == self.home_team else team1_wins,
            "draws": draws,
            "home_win_percentage": round((team1_wins if h2h_match.group(4) == self.home_team else team2_wins) / total_matches * 100),
            "away_win_percentage": round((team2_wins if h2h_match.group(4) == self.home_team else team1_wins) / total_matches * 100),
            "draw_percentage": round(draws / total_matches * 100),
            "goals_stats": goals_stats,
            "last_matches": last_matches
        }
    
    def extract_team_form(self) -> Dict[str, Dict[str, Any]]:
        """
        Extrai dados sobre a forma recente das equipes.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dicionário com estatísticas de forma recente para cada equipe
        """
        teams_form = {}
        
        # Padrão para extrair a forma recente (últimos 5 jogos)
        for team in [self.home_team, self.away_team]:
            form_pattern = rf"{team}\n(.*?)\nCasa\n(.*?)\nFora\n(.*?)\n"
            form_match = re.search(form_pattern, self.text, re.DOTALL)
            
            if not form_match:
                continue
            
            general_form = form_match.group(1).strip()
            home_form = form_match.group(2).strip()
            away_form = form_match.group(3).strip()
            
            # Extrair resultados dos últimos jogos
            last_matches_pattern = rf"{team} logo{team} está.*?\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n"
            last_matches_section = re.search(last_matches_pattern, self.text, re.DOTALL)
            
            last_matches = []
            if last_matches_section:
                for i in range(1, 6):
                    match_line = last_matches_section.group(i).strip()
                    teams_match = re.search(r"(.*?)\n(\d+) - (\d+)\n(.*)", match_line)
                    
                    if teams_match:
                        home = teams_match.group(1).strip()
                        home_score = int(teams_match.group(2))
                        away_score = int(teams_match.group(3))
                        away = teams_match.group(4).strip()
                        
                        last_matches.append({
                            "home_team": home,
                            "away_team": away,
                            "home_score": home_score,
                            "away_score": away_score,
                            "result": "V" if (home == team and home_score > away_score) or 
                                           (away == team and away_score > home_score) else
                                      "D" if (home == team and home_score < away_score) or 
                                           (away == team and away_score < home_score) else "E"
                        })
            
            # Extrair estatísticas gerais
            stats_pattern = rf"{team}\nInglaterra - Premier League.*?\nEstat\.GeralCasaFora\nVitória %(\d+)%(\d+)%(\d+)%\nMGJ([\d\.]+)([\d\.]+)([\d\.]+)\nMarcaram([\d\.]+)([\d\.]+)([\d\.]+)\nSofreram([\d\.]+)([\d\.]+)([\d\.]+)\nAM(\d+)%(\d+)%(\d+)%\nClean Sheets(\d+)%(\d+)%(\d+)%\nFTS(\d+)%(\d+)%(\d+)%\nxG([\d\.]+)([\d\.]+)([\d\.]+)\nxGC([\d\.]+)([\d\.]+)([\d\.]+)"
            stats_match = re.search(stats_pattern, self.text)
            
            stats = {}
            if stats_match:
                stats = {
                    "win_percentage": {
                        "overall": int(stats_match.group(1)),
                        "home": int(stats_match.group(2)),
                        "away": int(stats_match.group(3))
                    },
                    "goals_per_game": {
                        "overall": float(stats_match.group(4)),
                        "home": float(stats_match.group(5)),
                        "away": float(stats_match.group(6))
                    },
                    "goals_scored_per_game": {
                        "overall": float(stats_match.group(7)),
                        "home": float(stats_match.group(8)),
                        "away": float(stats_match.group(9))
                    },
                    "goals_conceded_per_game": {
                        "overall": float(stats_match.group(10)),
                        "home": float(stats_match.group(11)),
                        "away": float(stats_match.group(12))
                    },
                    "btts_percentage": {
                        "overall": int(stats_match.group(13)),
                        "home": int(stats_match.group(14)),
                        "away": int(stats_match.group(15))
                    },
                    "clean_sheets_percentage": {
                        "overall": int(stats_match.group(16)),
                        "home": int(stats_match.group(17)),
                        "away": int(stats_match.group(18))
                    },
                    "failed_to_score_percentage": {
                        "overall": int(stats_match.group(19)),
                        "home": int(stats_match.group(20)),
                        "away": int(stats_match.group(21))
                    },
                    "xG": {
                        "overall": float(stats_match.group(22)),
                        "home": float(stats_match.group(23)),
                        "away": float(stats_match.group(24))
                    },
                    "xGC": {
                        "overall": float(stats_match.group(25)),
                        "home": float(stats_match.group(26)),
                        "away": float(stats_match.group(27))
                    }
                }
            
            teams_form[team] = {
                "general_form": general_form,
                "home_form": home_form,
                "away_form": away_form,
                "last_matches": last_matches,
                "stats": stats
            }
        
        return teams_form
    
    def extract_table_positions(self) -> Dict[str, Dict[str, Any]]:
        """
        Extrai dados sobre as posições das equipes nas tabelas.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dicionário com posições nas tabelas para cada equipe
        """
        positions = {}
        
        # Padrão para extrair posição na tabela geral
        for team in [self.home_team, self.away_team]:
            position_pattern = rf"{team}\nInglaterra - Premier League\nPos Liga\. (\d+) / (\d+)"
            position_match = re.search(position_pattern, self.text)
            
            if not position_match:
                continue
            
            general_position = int(position_match.group(1))
            total_teams = int(position_match.group(2))
            
            # Extrair posição na tabela casa/fora
            home_away_tables = re.findall(r"Tabela em Casa / Tabela Fora.*?(\d+)\n\n (.*?)\n(\d+)\n\n(\d+)%\n\n(\d+)\n\n(\d+)\n\n(\d+)\n\n(\d+)\n\n([\d\.]+)", self.text, re.DOTALL)
            
            home_position = None
            away_position = None
            
            for entry in home_away_tables:
                if team in entry[1]:
                    # Verificar se é tabela casa ou fora
                    if "Tabela em Casa" in self.text[:self.text.find(entry[0])]:
                        home_position = int(entry[0])
                    else:
                        away_position = int(entry[0])
            
            positions[team] = {
                "general_position": general_position,
                "total_teams": total_teams,
                "home_position": home_position,
                "away_position": away_position
            }
        
        return positions
    
    def extract_predictions(self) -> Dict[str, Any]:
        """
        Extrai dados sobre prognósticos e previsões.
        
        Returns:
            Dict[str, Any]: Dicionário com prognósticos e previsões
        """
        predictions = {}
        
        # Extrair análise do GPT4
        gpt_analysis_pattern = r"ChatGPT LogoGPT4 AI Análise\n(.*?)\n\* Este resumo foi gerado pelo GPT4"
        gpt_analysis_match = re.search(gpt_analysis_pattern, self.text, re.DOTALL)
        
        if gpt_analysis_match:
            predictions["gpt_analysis"] = gpt_analysis_match.group(1).strip()
        
        # Extrair prognósticos gerais
        general_predictions_pattern = r"Todos os Prognósticos- .*?\n(\d+)%Mais de 2.5\nMédia da Liga : (\d+)%\n(\d+)%Mais de 1.5\nMédia da Liga : (\d+)%\n(\d+)%AM\nMédia da Liga : (\d+)%\n([\d\.]+)Golos / Jogo\nMédia da Liga : ([\d\.]+)\n([\d\.]+)Cartões \nMédia da Liga : ([\d\.]+)\n([\d\.]+)Cantos \nMédia da Liga : ([\d\.]+)"
        general_match = re.search(general_predictions_pattern, self.text)
        
        if general_match:
            predictions["general"] = {
                "over_2_5_percentage": int(general_match.group(1)),
                "over_2_5_league_avg": int(general_match.group(2)),
                "over_1_5_percentage": int(general_match.group(3)),
                "over_1_5_league_avg": int(general_match.group(4)),
                "btts_percentage": int(general_match.group(5)),
                "btts_league_avg": int(general_match.group(6)),
                "goals_per_game": float(general_match.group(7)),
                "goals_per_game_league_avg": float(general_match.group(8)),
                "cards_per_game": float(general_match.group(9)),
                "cards_per_game_league_avg": float(general_match.group(10)),
                "corners_per_game": float(general_match.group(11)),
                "corners_per_game_league_avg": float(general_match.group(12))
            }
        
        # Extrair prognósticos detalhados de gols
        goals_predictions_pattern = r"Mais de 0.5\n(\d+)%\n(\d+)%\n(\d+)%\nMais de 1.5\n(\d+)%\n(\d+)%\n(\d+)%\nMais de 2.5\n(\d+)%\n(\d+)%\n(\d+)%\nMais de 3.5\n(\d+)%\n(\d+)%\n(\d+)%\nMais de 4.5\n(\d+)%\n(\d+)%\n(\d+)%\nAM\n(\d+)%\n(\d+)%\n(\d+)%"
        goals_match = re.search(goals_predictions_pattern, self.text)
        
        if goals_match:
            predictions["goals_detailed"] = {
                "over_0_5": {
                    "home": int(goals_match.group(1)),
                    "away": int(goals_match.group(2)),
                    "average": int(goals_match.group(3))
                },
                "over_1_5": {
                    "home": int(goals_match.group(4)),
                    "away": int(goals_match.group(5)),
                    "average": int(goals_match.group(6))
                },
                "over_2_5": {
                    "home": int(goals_match.group(7)),
                    "away": int(goals_match.group(8)),
                    "average": int(goals_match.group(9))
                },
                "over_3_5": {
                    "home": int(goals_match.group(10)),
                    "away": int(goals_match.group(11)),
                    "average": int(goals_match.group(12))
                },
                "over_4_5": {
                    "home": int(goals_match.group(13)),
                    "away": int(goals_match.group(14)),
                    "average": int(goals_match.group(15))
                },
                "btts": {
                    "home": int(goals_match.group(16)),
                    "away": int(goals_match.group(17)),
                    "average": int(goals_match.group(18))
                }
            }
        
        # Extrair prognósticos de cantos
        corners_predictions_pattern = r"Cantos / jogo\n\* Média de Cantos por jogo entre .*?\n\n([\d\.]+)/ jogo\nCantos Ganhos\n\n([\d\.]+)/ jogo\nCantos Ganhos\n\nTotal Cantos1P/2P\nCantos no Jogo\n.*?\n.*?\nMédia\nMais 6\n(\d+)%\n(\d+)%\n(\d+)%\nMais 7\n(\d+)%\n(\d+)%\n(\d+)%\nMais 8\n(\d+)%\n(\d+)%\n(\d+)%\nMais 9\n(\d+)%\n(\d+)%\n(\d+)%\nMais 10\n(\d+)%\n(\d+)%\n(\d+)%"
        corners_match = re.search(corners_predictions_pattern, self.text)
        
        if corners_match:
            predictions["corners"] = {
                "corners_per_game": float(corners_match.group(1)),
                "home_corners_per_game": float(corners_match.group(2)),
                "away_corners_per_game": float(corners_match.group(3)),
                "over_6_corners_percentage": int(corners_match.group(4)),
                "over_7_corners_percentage": int(corners_match.group(7)),
                "over_8_corners_percentage": int(corners_match.group(10)),
                "over_9_corners_percentage": int(corners_match.group(13)),
                "over_10_corners_percentage": int(corners_match.group(16))
            }
        
        # Extrair prognósticos de cartões
        cards_predictions_pattern = r"Cartões\n([\d\.]+)\nTotal de Cartões / jogo\n\n\* Soma de cartões por jogo entre .*?\n\n([\d\.]+)Cartões\n/ jogo\n.*?\n([\d\.]+)Cartões\n/ jogo\n.*?\nTotal de CartõesCartões por Equipa\nCartões no Jogo\n.*?\n.*?\nMédia\nMais de 2.5\n(\d+)%\n(\d+)%\n(\d+)%\nMais de 3.5\n(\d+)%\n(\d+)%\n(\d+)%\nMais de 4.5\n(\d+)%\n(\d+)%\n(\d+)%"
        cards_match = re.search(cards_predictions_pattern, self.text)
        
        if cards_match:
            predictions["cards"] = {
                "cards_per_game": float(cards_match.group(1)),
                "home_cards_per_game": float(cards_match.group(2)),
                "away_cards_per_game": float(cards_match.group(3)),
                "over_2_5_cards_percentage": int(cards_match.group(6)),
                "over_3_5_cards_percentage": int(cards_match.group(9)),
                "over_4_5_cards_percentage": int(cards_match.group(12))
            }
        
        # Extrair prognósticos de primeiro tempo/segundo tempo
        halftime_predictions_pattern = r"1P/2P Forma\n.*?\n.*?\nVitórias 1P\n(\d+)%\n(\d+)%\nVitórias 2P\n(\d+)%\n(\d+)%\nEmpates 1P\n(\d+)%\n(\d+)%\nEmpates 2P\n(\d+)%\n(\d+)%\nDerrotas 1P\n(\d+)%\n(\d+)%\nDerrotas 2P\n(\d+)%\n(\d+)%"
        halftime_match = re.search(halftime_predictions_pattern, self.text)
        
        if halftime_match:
            predictions["halftime_fulltime"] = {
                "home_win_1h": int(halftime_match.group(1)),
                "away_win_1h": int(halftime_match.group(2)),
                "home_win_2h": int(halftime_match.group(3)),
                "away_win_2h": int(halftime_match.group(4)),
                "home_draw_1h": int(halftime_match.group(5)),
                "away_draw_1h": int(halftime_match.group(6)),
                "home_draw_2h": int(halftime_match.group(7)),
                "away_draw_2h": int(halftime_match.group(8)),
                "home_loss_1h": int(halftime_match.group(9)),
                "away_loss_1h": int(halftime_match.group(10)),
                "home_loss_2h": int(halftime_match.group(11)),
                "away_loss_2h": int(halftime_match.group(12))
            }
        
        # Extrair prognósticos de quem marca primeiro
        first_goal_pattern = r"Quem vai marcar primeiro\?\n.*?  \n.*?\n(\d+)%\n\nMarcou primeiro em (\d+) / (\d+) jogos\n\n.*?  \n.*?\n(\d+)%\n\nMarcou primeiro em (\d+) / (\d+) jogos"
        first_goal_match = re.search(first_goal_pattern, self.text)
        
        if first_goal_match:
            predictions["first_goal"] = {
                "home_first_goal_percentage": int(first_goal_match.group(1)),
                "home_first_goal_matches": int(first_goal_match.group(2)),
                "home_total_matches": int(first_goal_match.group(3)),
                "away_first_goal_percentage": int(first_goal_match.group(4)),
                "away_first_goal_matches": int(first_goal_match.group(5)),
                "away_total_matches": int(first_goal_match.group(6))
            }
        
        return predictions
    
    def extract_all_data(self) -> Dict[str, Any]:
        """
        Extrai todos os dados disponíveis no texto.
        
        Returns:
            Dict[str, Any]: Dicionário completo com todos os dados extraídos
        """
        basic_info = self.extract_basic_info()
        head_to_head = self.extract_head_to_head()
        team_form = self.extract_team_form()
        table_positions = self.extract_table_positions()
        predictions = self.extract_predictions()
        
        return {
            "basic_info": basic_info,
            "head_to_head": head_to_head,
            "team_form": team_form,
            "table_positions": table_positions,
            "predictions": predictions
        }
