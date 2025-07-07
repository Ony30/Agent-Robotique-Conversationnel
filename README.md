# Agent_robotique_conversationnel

## Description

Ce projet implémente un agent robotique capable de mener des conversations en langage naturel en utilisant CamemBERT, un modèle de langage français, intégré avec un robot NAO.

## Structure du Projet

Le projet est divisé en deux composants principaux, chacun nécessitant son propre environnement :

```
agent_robotique_conversationnel/
├── LLM/
│   ├── context/
│   ├── app.py
│   ├── requirements_conda.txt
│   ├── requirements_pip.txt
│   └── scrapt.py
└── Robot/
    ├── dialog.py
    ├── requirements_conda.txt
    └── requirements_pip.txt
```

## Prérequis
- Conda (Miniconda ou Anaconda)
- Robot NAO
- GPU

## Installation

Apres avoir cloné le projet, l'installation se fait en deux parties, une pour chaque composant du projet.

### 1. Installation de l'environnement LLM

```bash
# Création de l'environnement conda pour LLM
cd LLM
conda create -n llm_env
conda activate llm_env

# Installation des dépendances
conda install --file requirements_conda.txt
pip install -r requirements_pip.txt
```

### 2. Installation de l'environnement Robot

```bash
# Création de l'environnement conda pour Robot
cd ../Robot
conda create -n robot_env
conda activate robot_env

# Installation des dépendances
conda install --file requirements_conda.txt
pip install -r requirements_pip.txt
```

## Architecture et Communication

Le projet utilise une architecture client-serveur :

### Composant LLM (Serveur)
- Implémenté avec FastAPI
- Héberge le modèle CamemBERT pour le question-answering
- Expose une API REST sur le port 8000
- Point d'entrée principal : `/predict` (POST)
- Utilise un contexte fixe pour le modèle chargé depuis `madagascar_wikipedia.txt`

### Composant Robot (Client)
- Gère l'interface avec le robot NAO
- Communique avec le serveur LLM via des requêtes HTTP

### Flux de Communication
1. Le robot NAO capte une question via son système de dialogue
2. Le module Robot envoie une requête POST à l'API du LLM
3. Le LLM traite la question avec le contexte prédéfini
4. La réponse est renvoyée au robot qui la prononce via son système text-to-speech


## Configuration

### Configuration du LLM
- Le modèle utilise par défaut le GPU
- Le contexte est chargé depuis `context/madagascar_wikipedia.txt`

### Configuration du Robot
- Modifier les variables dans `dialog.py` :
  ```python
  self.nao_ip = "192.168.1.100"  # IP du robot
  self.nao_port = 9559           # Port du robot
  self.api_url = "http://192.168.1.103:8000/predict"  # URL de l'API
  ```

## Utilisation

1. Démarrage du service LLM :
```bash
conda activate llm_env
cd LLM
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

2. Dans un nouveau terminal, démarrage du Robot :
```bash
conda activate robot_env
cd Robot
python dialog.py
```
Note : Cette implémentation est conçue pour un environnement de développement local.

## Architecture

Le projet utilise une architecture à deux composants :
- **LLM** : Gère le traitement du langage naturel et la génération des réponses
- **Robot** : Gère l'interface avec le robot et le dialogue

## Structure des Fichiers
```
agent_robotique_conversationnel/
├── README.md               # Ce fichier
├── LLM/
│   ├── context/
│   │   └── madagascar_wikipedia.txt    # Contexte pour le modèle
│   ├── app.py                         # Serveur FastAPI
│   ├── requirements_conda.txt         # Dépendances conda
│   ├── requirements_pip.txt          # Dépendances pip
│   └── scrapt.py                     # Script de scraping
└── Robot/
    ├── dialog.py                     # Interface robot NAO
    ├── requirements_conda.txt        # Dépendances conda
    └── requirements_pip.txt         # Dépendances pip
```

## Support

Pour obtenir de l'aide ou signaler un problème :

- **Email** : [Contact](mailto:email@example.com)

Pour les questions spécifiques au robot NAO :
- Consultez la [documentation officielle de NAO](http://doc.aldebaran.com/2-1/home_nao.html)

## Auteurs et Remerciements

Ce projet a été développé dans le cadre du Master 2 en Mathematique Informatique pour le Big Data à l'Université de Pau et des Pays de l'Adour (UPPA).

### Encadrement
Nous tenons à remercier sincèrement :

- **M. Eric Gouardères** - Pour sa direction et ses conseils précieux
- **M. Mauro Gaio** - Pour son accompagnement et sa supervision
- **M. Tafer Abdelkrim** - Pour sa contribution et son support

### Développement
- **Onintsoa Fitiavana ANDRIANANDRAINA** - Développement principal
- **M. Eric Gouardères** - Configuration de reseau