#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para implementação de modelos matemáticos para predições de futebol.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from scipy.stats import poisson
from sklearn.linear_model import LogisticRegression

class FootballPredictionModels:
    """
    Classe para implementar modelos matemáticos para predições de futebol.
    """
    
    def __init__(self, processed_data: Dict[str, Any]):
        """
        Inicializa os modelos com os dados processados.
        
        Args:
            processed_data (Dict[str, Any]): Dados processados
        """
        self.data = processed_data
        self.home_team = processed_data["basic_info"]["home_team"]
        self.away_team = processed_data["basic_info"]["away_team"]
        
        # Extrair dados relevantes para os modelos
        self.h2h_data = processed_data.get("head_to_head", {})
        self.team_form = processed_data.get("team_form", {})
        self.table_positions = processed_data.get("table_positions", {})
        self.predictions = processed_data.get("predictions", {})
    
    def poisson_model(self) -> Dict[str, Any]:
        """
        Implementa o modelo de Poisson para predição de resultados.
        
        Returns:
            Dict[str, Any]: Resultados do modelo de Poisson
        """
        # Extrair dados de forma recente para estimar força de ataque e defesa
        home_team_data = self.team_form.get(self.home_team, {})
        away_team_data = self.team_form.get(self.away_team, {})
        
        if not home_team_data or not away_team_data:
            return {"error": "Dados insuficientes para o modelo de Poisson"}
        
        # Obter estatísticas de gols
        home_stats = home_team_data.get("stats", {})
        away_stats = away_team_data.get("stats", {})
        
        if not home_stats or not away_stats:
            return {"error": "Estatísticas de gols insuficientes para o modelo de Poisson"}
        
        # Estimar força de ataque e defesa
        home_attack = home_stats.get("goals_scored_per_game", {}).get("home", 0)
        home_defense = home_stats.get("goals_conceded_per_game", {}).get("home", 0)
        
        away_attack = away_stats.get("goals_scored_per_game", {}).get("away", 0)
        away_defense = away_stats.get("goals_conceded_per_game", {}).get("away", 0)
        
        # Calcular médias da liga (se disponíveis)
        league_avg_home_goals = 1.5  # Valor padrão se não disponível
        league_avg_away_goals = 1.2  # Valor padrão se não disponível
        
        general_predictions = self.predictions.get("general", {})
        if general_predictions:
            league_avg_goals = general_predictions.get("goals_per_game_league_avg", 0)
            if league_avg_goals > 0:
                league_avg_home_goals = league_avg_goals * 0.55  # Aproximadamente 55% dos gols são marcados pelos mandantes
                league_avg_away_goals = league_avg_goals * 0.45  # Aproximadamente 45% dos gols são marcados pelos visitantes
        
        # Calcular expectativa de gols
        home_expected_goals = home_attack * away_defense / league_avg_away_goals
        away_expected_goals = away_attack * home_defense / league_avg_home_goals
        
        # Ajustar com fator casa
        home_advantage_factor = 1.2  # Fator de vantagem em casa
        home_expected_goals *= home_advantage_factor
        
        # Calcular probabilidades de gols usando distribuição de Poisson
        max_goals = 10  # Máximo de gols a considerar
        
        home_probs = [poisson.pmf(i, home_expected_goals) for i in range(max_goals)]
        away_probs = [poisson.pmf(i, away_expected_goals) for i in range(max_goals)]
        
        # Calcular matriz de probabilidades de placar
        score_matrix = np.zeros((max_goals, max_goals))
        for i in range(max_goals):
            for j in range(max_goals):
                score_matrix[i, j] = home_probs[i] * away_probs[j]
        
        # Calcular probabilidades de resultados
        home_win_prob = np.sum(np.tril(score_matrix, -1))
        draw_prob = np.sum(np.diag(score_matrix))
        away_win_prob = np.sum(np.triu(score_matrix, 1))
        
        # Calcular probabilidades de over/under
        over_0_5_prob = 1.0 - score_matrix[0, 0]
        over_1_5_prob = 1.0 - (score_matrix[0, 0] + score_matrix[1, 0] + score_matrix[0, 1])
        over_2_5_prob = 1.0 - np.sum(score_matrix[:2, :]) - np.sum(score_matrix[2:, :2]) + score_matrix[1, 1]
        over_3_5_prob = 1.0 - np.sum(score_matrix[:3, :]) - np.sum(score_matrix[3:, :3]) + np.sum(score_matrix[1:3, 1:3])
        
        # Calcular probabilidade de ambas equipes marcarem (BTTS)
        btts_prob = 1.0 - home_probs[0] - away_probs[0] + home_probs[0] * away_probs[0]
        
        # Encontrar os 5 placares mais prováveis
        top_scores = []
        for i in range(max_goals):
            for j in range(max_goals):
                top_scores.append(((i, j), score_matrix[i, j]))
        
        top_scores.sort(key=lambda x: x[1], reverse=True)
        top_5_scores = top_scores[:5]
        
        return {
            "home_expected_goals": home_expected_goals,
            "away_expected_goals": away_expected_goals,
            "home_win_prob": home_win_prob * 100,
            "draw_prob": draw_prob * 100,
            "away_win_prob": away_win_prob * 100,
            "over_0_5_prob": over_0_5_prob * 100,
            "over_1_5_prob": over_1_5_prob * 100,
            "over_2_5_prob": over_2_5_prob * 100,
            "over_3_5_prob": over_3_5_prob * 100,
            "btts_prob": btts_prob * 100,
            "top_5_scores": [{"score": f"{score[0][0]}-{score[0][1]}", "probability": score[1] * 100} for score in top_5_scores],
            "score_matrix": score_matrix.tolist()
        }
    
    def adjusted_poisson_model(self) -> Dict[str, Any]:
        """
        Implementa o modelo de Poisson ajustado com histórico de confrontos diretos.
        
        Returns:
            Dict[str, Any]: Resultados do modelo de Poisson ajustado
        """
        # Obter resultados do modelo de Poisson básico
        poisson_results = self.poisson_model()
        
        if "error" in poisson_results:
            return {"error": "Não foi possível executar o modelo de Poisson ajustado"}
        
        # Extrair dados de confrontos diretos
        if not self.h2h_data:
            return poisson_results  # Retornar modelo não ajustado se não houver dados de confrontos diretos
        
        last_matches = self.h2h_data.get("last_5_matches", {}).get("matches", [])
        
        if not last_matches:
            return poisson_results  # Retornar modelo não ajustado se não houver dados de confrontos diretos
        
        # Calcular médias de gols nos confrontos diretos
        home_goals = []
        away_goals = []
        
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
        
        # Calcular médias
        h2h_home_avg = np.mean(home_goals) if home_goals else 0
        h2h_away_avg = np.mean(away_goals) if away_goals else 0
        
        # Ajustar expectativa de gols com base nos confrontos diretos
        home_expected_goals = poisson_results["home_expected_goals"]
        away_expected_goals = poisson_results["away_expected_goals"]
        
        # Peso para o histórico de confrontos diretos (50%)
        h2h_weight = 0.5
        form_weight = 1.0 - h2h_weight
        
        adjusted_home_expected_goals = (form_weight * home_expected_goals + h2h_weight * h2h_home_avg)
        adjusted_away_expected_goals = (form_weight * away_expected_goals + h2h_weight * h2h_away_avg)
        
        # Recalcular probabilidades com os valores ajustados
        max_goals = 10  # Máximo de gols a considerar
        
        home_probs = [poisson.pmf(i, adjusted_home_expected_goals) for i in range(max_goals)]
        away_probs = [poisson.pmf(i, adjusted_away_expected_goals) for i in range(max_goals)]
        
        # Calcular matriz de probabilidades de placar
        score_matrix = np.zeros((max_goals, max_goals))
        for i in range(max_goals):
            for j in range(max_goals):
                score_matrix[i, j] = home_probs[i] * away_probs[j]
        
        # Calcular probabilidades de resultados
        home_win_prob = np.sum(np.tril(score_matrix, -1))
        draw_prob = np.sum(np.diag(score_matrix))
        away_win_prob = np.sum(np.triu(score_matrix, 1))
        
        # Calcular probabilidades de over/under
        over_0_5_prob = 1.0 - score_matrix[0, 0]
        over_1_5_prob = 1.0 - (score_matrix[0, 0] + score_matrix[1, 0] + score_matrix[0, 1])
        over_2_5_prob = 1.0 - np.sum(score_matrix[:2, :]) - np.sum(score_matrix[2:, :2]) + score_matrix[1, 1]
        over_3_5_prob = 1.0 - np.sum(score_matrix[:3, :]) - np.sum(score_matrix[3:, :3]) + np.sum(score_matrix[1:3, 1:3])
        
        # Calcular probabilidade de ambas equipes marcarem (BTTS)
        btts_prob = 1.0 - home_probs[0] - away_probs[0] + home_probs[0] * away_probs[0]
        
        # Encontrar os 5 placares mais prováveis
        top_scores = []
        for i in range(max_goals):
            for j in range(max_goals):
                top_scores.append(((i, j), score_matrix[i, j]))
        
        top_scores.sort(key=lambda x: x[1], reverse=True)
        top_5_scores = top_scores[:5]
        
        return {
            "home_expected_goals": adjusted_home_expected_goals,
            "away_expected_goals": adjusted_away_expected_goals,
            "home_win_prob": home_win_prob * 100,
            "draw_prob": draw_prob * 100,
            "away_win_prob": away_win_prob * 100,
            "over_0_5_prob": over_0_5_prob * 100,
            "over_1_5_prob": over_1_5_prob * 100,
            "over_2_5_prob": over_2_5_prob * 100,
            "over_3_5_prob": over_3_5_prob * 100,
            "btts_prob": btts_prob * 100,
            "top_5_scores": [{"score": f"{score[0][0]}-{score[0][1]}", "probability": score[1] * 100} for score in top_5_scores],
            "score_matrix": score_matrix.tolist(),
            "h2h_adjustment": {
                "h2h_home_avg": h2h_home_avg,
                "h2h_away_avg": h2h_away_avg,
                "h2h_weight": h2h_weight
            }
        }
    
    def logistic_regression_model(self) -> Dict[str, Any]:
        """
        Implementa um modelo simplificado de regressão logística para predição de resultados.
        
        Returns:
            Dict[str, Any]: Resultados do modelo de regressão logística
        """
        # Extrair dados para o modelo
        home_team_data = self.team_form.get(self.home_team, {})
        away_team_data = self.team_form.get(self.away_team, {})
        
        if not home_team_data or not away_team_data:
            return {"error": "Dados insuficientes para o modelo de regressão logística"}
        
        # Obter estatísticas relevantes
        home_stats = home_team_data.get("stats", {})
        away_stats = away_team_data.get("stats", {})
        
        if not home_stats or not away_stats:
            return {"error": "Estatísticas insuficientes para o modelo de regressão logística"}
        
        # Extrair features para o modelo
        home_win_pct = home_stats.get("win_percentage", {}).get("home", 0) / 100
        away_win_pct = away_stats.get("win_percentage", {}).get("away", 0) / 100
        
        home_goals_scored = home_stats.get("goals_scored_per_game", {}).get("home", 0)
        home_goals_conceded = home_stats.get("goals_conceded_per_game", {}).get("home", 0)
        
        away_goals_scored = away_stats.get("goals_scored_per_game", {}).get("away", 0)
        away_goals_conceded = away_stats.get("goals_conceded_per_game", {}).get("away", 0)
        
        # Extrair posições na tabela
        home_position_data = self.table_positions.get(self.home_team, {})
        away_position_data = self.table_positions.get(self.away_team, {})
        
        home_position = home_position_data.get("general_position", 0)
        away_position = away_position_data.get("general_position", 0)
        total_teams = home_position_data.get("total_teams", 20)
        
        # Normalizar posições (quanto menor o valor, melhor a equipe)
        home_position_norm = 1 - (home_position / total_teams) if total_teams > 0 else 0.5
        away_position_norm = 1 - (away_position / total_teams) if total_teams > 0 else 0.5
        
        # Criar features para o modelo
        features = np.array([
            home_win_pct, away_win_pct,
            home_goals_scored, home_goals_conceded,
            away_goals_scored, away_goals_conceded,
            home_position_norm, away_position_norm
        ]).reshape(1, -1)
        
        # Pesos para cada feature (simplificação de um modelo treinado)
        # Ordem: home_win_pct, away_win_pct, home_goals_scored, home_goals_conceded, 
        #        away_goals_scored, away_goals_conceded, home_position_norm, away_position_norm
        home_win_weights = np.array([0.3, -0.2, 0.15, -0.15, -0.1, 0.1, 0.2, -0.2])
        draw_weights = np.array([-0.1, -0.1, -0.05, 0.05, -0.05, 0.05, -0.1, -0.1])
        away_win_weights = np.array([-0.2, 0.3, -0.1, 0.15, 0.15, -0.15, -0.2, 0.2])
        
        # Calcular probabilidades (simplificação usando produto escalar e softmax)
        home_win_logit = np.dot(features, home_win_weights)
        draw_logit = np.dot(features, draw_weights)
        away_win_logit = np.dot(features, away_win_weights)
        
        # Aplicar softmax para obter probabilidades
        logits = np.array([home_win_logit, draw_logit, away_win_logit]).flatten()
        exp_logits = np.exp(logits)
        probs = exp_logits / np.sum(exp_logits)
        
        home_win_prob, draw_prob, away_win_prob = probs
        
        # Estimar expectativa de gols
        home_expected_goals = home_goals_scored * 0.7 + away_goals_conceded * 0.3
        away_expected_goals = away_goals_scored * 0.7 + home_goals_conceded * 0.3
        
        # Calcular probabilidades de over/under e BTTS
        total_expected_goals = home_expected_goals + away_expected_goals
        
        over_0_5_prob = 1.0 - np.exp(-total_expected_goals)
        over_1_5_prob = 1.0 - np.exp(-total_expected_goals) * (1 + total_expected_goals)
        over_2_5_prob = 1.0 - np.exp(-total_expected_goals) * (1 + total_expected_goals + (total_expected_goals ** 2) / 2)
        over_3_5_prob = 1.0 - np.exp(-total_expected_goals) * (1 + total_expected_goals + (total_expected_goals ** 2) / 2 + (total_expected_goals ** 3) / 6)
        
        btts_prob = (1 - np.exp(-home_expected_goals)) * (1 - np.exp(-away_expected_goals))
        
        return {
            "home_expected_goals": home_expected_goals,
            "away_expected_goals": away_expected_goals,
            "home_win_prob": home_win_prob * 100,
            "draw_prob": draw_prob * 100,
            "away_win_prob": away_win_prob * 100,
            "over_0_5_prob": over_0_5_prob * 100,
            "over_1_5_prob": over_1_5_prob * 100,
            "over_2_5_prob": over_2_5_prob * 100,
            "over_3_5_prob": over_3_5_prob * 100,
            "btts_prob": btts_prob * 100,
            "features": {
                "home_win_pct": home_win_pct,
                "away_win_pct": away_win_pct,
                "home_goals_scored": home_goals_scored,
                "home_goals_conceded": home_goals_conceded,
                "away_goals_scored": away_goals_scored,
                "away_goals_conceded": away_goals_conceded,
                "home_position_norm": home_position_norm,
                "away_position_norm": away_position_norm
            }
        }
    
    def ensemble_model(self) -> Dict[str, Any]:
        """
        Implementa um modelo ensemble combinando os resultados dos outros modelos.
        
        Returns:
            Dict[str, Any]: Resultados do modelo ensemble
        """
        # Executar os modelos individuais
        poisson_results = self.poisson_model()
        adjusted_poisson_results = self.adjusted_poisson_model()
        logistic_results = self.logistic_regression_model()
        
        # Verificar se algum modelo falhou
        models_ok = []
        if "error" not in poisson_results:
            models_ok.append("poisson")
        if "error" not in adjusted_poisson_results:
            models_ok.append("adjusted_poisson")
        if "error" not in logistic_results:
            models_ok.append("logistic")
        
        if not models_ok:
            return {"error": "Todos os modelos falharam"}
        
        # Definir pesos para cada modelo
        model_weights = {
            "poisson": 0.3,
            "adjusted_poisson": 0.5,
            "logistic": 0.2
        }
        
        # Normalizar pesos para os modelos disponíveis
        total_weight = sum(model_weights[model] for model in models_ok)
        normalized_weights = {model: model_weights[model] / total_weight for model in models_ok}
        
        # Combinar probabilidades de resultados
        home_win_prob = 0.0
        draw_prob = 0.0
        away_win_prob = 0.0
        
        if "poisson" in models_ok:
            home_win_prob += poisson_results["home_win_prob"] * normalized_weights["poisson"]
            draw_prob += poisson_results["draw_prob"] * normalized_weights["poisson"]
            away_win_prob += poisson_results["away_win_prob"] * normalized_weights["poisson"]
        
        if "adjusted_poisson" in models_ok:
            home_win_prob += adjusted_poisson_results["home_win_prob"] * normalized_weights["adjusted_poisson"]
            draw_prob += adjusted_poisson_results["draw_prob"] * normalized_weights["adjusted_poisson"]
            away_win_prob += adjusted_poisson_results["away_win_prob"] * normalized_weights["adjusted_poisson"]
        
        if "logistic" in models_ok:
            home_win_prob += logistic_results["home_win_prob"] * normalized_weights["logistic"]
            draw_prob += logistic_results["draw_prob"] * normalized_weights["logistic"]
            away_win_prob += logistic_results["away_win_prob"] * normalized_weights["logistic"]
        
        # Combinar probabilidades de over/under e BTTS
        over_0_5_prob = 0.0
        over_1_5_prob = 0.0
        over_2_5_prob = 0.0
        over_3_5_prob = 0.0
        btts_prob = 0.0
        
        if "poisson" in models_ok:
            over_0_5_prob += poisson_results["over_0_5_prob"] * normalized_weights["poisson"]
            over_1_5_prob += poisson_results["over_1_5_prob"] * normalized_weights["poisson"]
            over_2_5_prob += poisson_results["over_2_5_prob"] * normalized_weights["poisson"]
            over_3_5_prob += poisson_results["over_3_5_prob"] * normalized_weights["poisson"]
            btts_prob += poisson_results["btts_prob"] * normalized_weights["poisson"]
        
        if "adjusted_poisson" in models_ok:
            over_0_5_prob += adjusted_poisson_results["over_0_5_prob"] * normalized_weights["adjusted_poisson"]
            over_1_5_prob += adjusted_poisson_results["over_1_5_prob"] * normalized_weights["adjusted_poisson"]
            over_2_5_prob += adjusted_poisson_results["over_2_5_prob"] * normalized_weights["adjusted_poisson"]
            over_3_5_prob += adjusted_poisson_results["over_3_5_prob"] * normalized_weights["adjusted_poisson"]
            btts_prob += adjusted_poisson_results["btts_prob"] * normalized_weights["adjusted_poisson"]
        
        if "logistic" in models_ok:
            over_0_5_prob += logistic_results["over_0_5_prob"] * normalized_weights["logistic"]
            over_1_5_prob += logistic_results["over_1_5_prob"] * normalized_weights["logistic"]
            over_2_5_prob += logistic_results["over_2_5_prob"] * normalized_weights["logistic"]
            over_3_5_prob += logistic_results["over_3_5_prob"] * normalized_weights["logistic"]
            btts_prob += logistic_results["btts_prob"] * normalized_weights["logistic"]
        
        # Combinar expectativa de gols
        home_expected_goals = 0.0
        away_expected_goals = 0.0
        
        if "poisson" in models_ok:
            home_expected_goals += poisson_results["home_expected_goals"] * normalized_weights["poisson"]
            away_expected_goals += poisson_results["away_expected_goals"] * normalized_weights["poisson"]
        
        if "adjusted_poisson" in models_ok:
            home_expected_goals += adjusted_poisson_results["home_expected_goals"] * normalized_weights["adjusted_poisson"]
            away_expected_goals += adjusted_poisson_results["away_expected_goals"] * normalized_weights["adjusted_poisson"]
        
        if "logistic" in models_ok:
            home_expected_goals += logistic_results["home_expected_goals"] * normalized_weights["logistic"]
            away_expected_goals += logistic_results["away_expected_goals"] * normalized_weights["logistic"]
        
        # Calcular placares mais prováveis usando o modelo de Poisson com os valores esperados combinados
        max_goals = 10  # Máximo de gols a considerar
        
        home_probs = [poisson.pmf(i, home_expected_goals) for i in range(max_goals)]
        away_probs = [poisson.pmf(i, away_expected_goals) for i in range(max_goals)]
        
        # Calcular matriz de probabilidades de placar
        score_matrix = np.zeros((max_goals, max_goals))
        for i in range(max_goals):
            for j in range(max_goals):
                score_matrix[i, j] = home_probs[i] * away_probs[j]
        
        # Encontrar os 5 placares mais prováveis
        top_scores = []
        for i in range(max_goals):
            for j in range(max_goals):
                top_scores.append(((i, j), score_matrix[i, j]))
        
        top_scores.sort(key=lambda x: x[1], reverse=True)
        top_5_scores = top_scores[:5]
        
        return {
            "home_expected_goals": home_expected_goals,
            "away_expected_goals": away_expected_goals,
            "home_win_prob": home_win_prob,
            "draw_prob": draw_prob,
            "away_win_prob": away_win_prob,
            "over_0_5_prob": over_0_5_prob,
            "over_1_5_prob": over_1_5_prob,
            "over_2_5_prob": over_2_5_prob,
            "over_3_5_prob": over_3_5_prob,
            "btts_prob": btts_prob,
            "top_5_scores": [{"score": f"{score[0][0]}-{score[0][1]}", "probability": score[1] * 100} for score in top_5_scores],
            "models_used": models_ok,
            "model_weights": normalized_weights
        }
    
    def run_all_models(self) -> Dict[str, Any]:
        """
        Executa todos os modelos e retorna os resultados.
        
        Returns:
            Dict[str, Any]: Resultados de todos os modelos
        """
        poisson_results = self.poisson_model()
        adjusted_poisson_results = self.adjusted_poisson_model()
        logistic_results = self.logistic_regression_model()
        ensemble_results = self.ensemble_model()
        
        return {
            "poisson": poisson_results,
            "adjusted_poisson": adjusted_poisson_results,
            "logistic_regression": logistic_results,
            "ensemble": ensemble_results
        }
    
    def generate_insights(self) -> Dict[str, Any]:
        """
        Gera insights baseados nos resultados dos modelos.
        
        Returns:
            Dict[str, Any]: Insights dos modelos
        """
        # Executar o modelo ensemble
        ensemble_results = self.ensemble_model()
        
        if "error" in ensemble_results:
            return {"error": "Não foi possível gerar insights dos modelos"}
        
        # Extrair dados relevantes
        home_win_prob = ensemble_results["home_win_prob"]
        draw_prob = ensemble_results["draw_prob"]
        away_win_prob = ensemble_results["away_win_prob"]
        
        over_0_5_prob = ensemble_results["over_0_5_prob"]
        over_1_5_prob = ensemble_results["over_1_5_prob"]
        over_2_5_prob = ensemble_results["over_2_5_prob"]
        over_3_5_prob = ensemble_results["over_3_5_prob"]
        
        btts_prob = ensemble_results["btts_prob"]
        
        home_expected_goals = ensemble_results["home_expected_goals"]
        away_expected_goals = ensemble_results["away_expected_goals"]
        
        top_5_scores = ensemble_results["top_5_scores"]
        
        # Gerar insights principais
        insights = []
        
        # Insight sobre o resultado mais provável
        most_likely_result = None
        most_likely_prob = 0.0
        
        if home_win_prob > draw_prob and home_win_prob > away_win_prob:
            most_likely_result = f"Vitória do {self.home_team}"
            most_likely_prob = home_win_prob
        elif away_win_prob > home_win_prob and away_win_prob > draw_prob:
            most_likely_result = f"Vitória do {self.away_team}"
            most_likely_prob = away_win_prob
        else:
            most_likely_result = "Empate"
            most_likely_prob = draw_prob
        
        insights.append(f"Resultado mais provável: {most_likely_result} ({most_likely_prob:.2f}%).")
        
        # Insight sobre o placar mais provável
        most_likely_score = top_5_scores[0]["score"]
        most_likely_score_prob = top_5_scores[0]["probability"]
        
        insights.append(f"Placar mais provável: {most_likely_score} ({most_likely_score_prob:.2f}%).")
        
        # Insight sobre expectativa de gols
        total_expected_goals = home_expected_goals + away_expected_goals
        
        insights.append(f"Expectativa de gols: {home_expected_goals:.2f} para {self.home_team}, " +
                       f"{away_expected_goals:.2f} para {self.away_team} (total: {total_expected_goals:.2f}).")
        
        # Insight sobre over/under
        over_under_insight = None
        if over_2_5_prob >= 65:
            over_under_insight = f"Alta probabilidade de Over 2.5 gols ({over_2_5_prob:.2f}%)."
        elif over_2_5_prob <= 35:
            over_under_insight = f"Alta probabilidade de Under 2.5 gols ({100 - over_2_5_prob:.2f}%)."
        else:
            over_under_insight = f"Probabilidade equilibrada para Over/Under 2.5 gols ({over_2_5_prob:.2f}% para Over)."
        
        insights.append(over_under_insight)
        
        # Insight sobre BTTS
        btts_insight = None
        if btts_prob >= 65:
            btts_insight = f"Alta probabilidade de ambas equipes marcarem ({btts_prob:.2f}%)."
        elif btts_prob <= 35:
            btts_insight = f"Baixa probabilidade de ambas equipes marcarem ({btts_prob:.2f}%)."
        else:
            btts_insight = f"Probabilidade equilibrada para ambas equipes marcarem ({btts_prob:.2f}%)."
        
        insights.append(btts_insight)
        
        # Insight sobre outros placares prováveis
        other_scores = ", ".join([f"{score['score']} ({score['probability']:.2f}%)" for score in top_5_scores[1:3]])
        insights.append(f"Outros placares prováveis: {other_scores}.")
        
        # Insight sobre modelos utilizados
        models_used = ensemble_results.get("models_used", [])
        model_weights = ensemble_results.get("model_weights", {})
        
        models_description = ", ".join([f"{model} ({model_weights[model]*100:.0f}%)" for model in models_used])
        insights.append(f"Modelos utilizados: {models_description}.")
        
        return {
            "ensemble_results": ensemble_results,
            "insights": insights
        }
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """
        Executa uma análise completa com todos os modelos.
        
        Returns:
            Dict[str, Any]: Análise completa dos modelos
        """
        return self.generate_insights()
