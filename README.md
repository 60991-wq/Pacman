# Pac-Man Multi-Agent Lab

![Python](https://img.shields.io/badge/Python-3-3776AB)

Projet Python basé sur le framework Pac-Man de UC Berkeley, pour comparer plusieurs façons de faire décider Pac-Man de son prochain coup : réagir à l'instant présent, anticiper le pire cas face aux fantômes, ou raisonner sur des probabilités.

---

##  Stack technique

- Python 3
- Tkinter (interface graphique)

---

## Agents implémentés

| Agent | Logique |
|---|---|
| **ReflexAgent** | Choisit le meilleur coup immédiat, sans anticipation |
| **MinimaxAgent** | Anticipe plusieurs coups en supposant que les fantômes jouent toujours au pire pour Pac-Man |
| **AlphaBetaAgent** | Même logique que Minimax, mais élague les branches inutiles pour aller plus vite |
| **ExpectimaxAgent** | Anticipe en supposant que les fantômes agissent de façon incertaine plutôt que toujours au pire |

D'autres fonctionnalités : fonction d'évaluation tenant compte de la nourriture, des capsules et des fantômes ; fantômes aléatoires ou qui poursuivent activement ; plusieurs plans de labyrinthe (`smallClassic`, `mediumClassic`, `minimaxClassic`, `trickyClassic`) ; mode graphique, texte ou silencieux ; enregistrement et relecture de parties.

---

##  Structure

```
└── pacman_multiagent/
	├── pacman.py             
	├── multiAgents.py        
	├── pacmanAgents.py      
	├── ghostAgents.py       
	├── game.py              
	├── layout.py             
	├── graphicsDisplay.py    
	├── textDisplay.py        
	├── graphicsUtils.py      
	├── util.py               
	└── layouts/               
└── ...
```

---

## Lancer le projet

Depuis la racine, dans un terminal Windows :

```bash
cd pacman_multiagent
python pacman.py
```

### Tester un agent en particulier

```bash
python pacman.py -p ReflexAgent -l smallClassic
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=2
python pacman.py -p AlphaBetaAgent -l minimaxClassic -a depth=2
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=2
```

### Options utiles

| Option | Rôle |
|---|---|
| `-p AGENT` | Agent à utiliser |
| `-l LAYOUT` | Plan de labyrinthe |
| `-a depth=N` | Profondeur de recherche |
| `-n N` | Nombre de parties |
| `-q` | Sans graphismes (pour des tests rapides) |
| `-f` | Graine aléatoire fixe (résultats reproductibles) |

---

## Résultats

Mesures obtenues avec `-n 10 -q -f` (10 parties)

| Agent | Plan | Victoires | Score moyen |
|---|---|---|---|
| ReflexAgent | smallClassic | 7/10 (0.70) | 600.0 |
| MinimaxAgent | minimaxClassic (depth 2) | 5/10 (0.50) | 9.3 |
| AlphaBetaAgent | minimaxClassic (depth 2) | 5/10 (0.50) | 9.3 |
| ExpectimaxAgent | minimaxClassic (depth 2) | 7/10 (0.70) | 207.7 |

**Observations :**
- AlphaBeta donne exactement les mêmes résultats que Minimax — logique, puisque l'élagage alpha-bêta ne change jamais la décision finale, il accélère juste la recherche.
- Expectimax fait nettement mieux que Minimax sur ce plan (0.70 contre 0.50 de win rate) : les fantômes par défaut se déplaçant en partie aléatoirement, le modèle probabiliste d'Expectimax colle mieux à leur comportement réel que l'hypothèse pessimiste de Minimax.
- 10 parties restent un échantillon limité — les scores très variables de Minimax/AlphaBeta (de -498 à +515) montrent qu'il faudrait davantage de parties pour des conclusions plus solides.

---

##  Contexte

Moteur de jeu et structure issus du framework pédagogique de UC Berkeley. Les agents sont écrits à la main (règles, fonctions d'évaluation, recherche classique) —

---

## Auteur

 Abla Aninia Negue — 60991
