# Mini Data Warehouse with PySpark, Spark SQL, and SQL Server

## Description

Ce projet consiste à construire un mini Data Warehouse à l'aide de PySpark et Spark SQL. L'objectif est de lire des données à partir de fichiers CSV, de les transformer via un pipeline ETL, et de les charger dans SQL Server à l'aide d'un driver JDBC. Le projet utilise une architecture multi-couches (bronze, silver, gold) pour structurer les différentes étapes de nettoyage et de transformation des données.

---

## Structure du Projet

Voici la structure des dossiers pour le projet :

spark_project/
├── data/
│   ├── raw/             # Fichiers CSV bruts
│   │   ├── sales.csv
│   │   └── customers.csv
├── notebooks/           # Notebooks Jupyter pour les tests interactifs
│   └── etl.ipynb
├── scripts/             # Scripts Python exécutant les tâches ETL
│   └── etl.py
├── output/              # Données transformées à chaque étape (Bronze, Silver, Gold)
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── README.md            # Fichier d'instructions pour le projet
├── requirements.txt     # Fichier contenant les dépendances Python
└── .gitignore           # Fichiers à ignorer par Git
## Prérequis

Avant de démarrer,  j'assure que mon environnement dispose des éléments suivants :

- **Python 3.8+**
- **Java 8** (pour Spark)
- **PySpark 3.3.0**
- **SQL Server** (installé localement ou sur un serveur)
- **SQL Server Management Studio**
- **Driver JDBC pour SQL Server**
- **Hadoop**

## Installer les dépendances 
pip install -r requirements.txt

## configuration

**Étape 1 : Configurer les variables d'environnement**
Définissez le chemin vers le fichier sqljdbc_auth.dll si vous utilisez l'authentification Windows
import os
os.environ['java.library.path'] = "D:/sqljdbc_auth.dll"
**Étape 2 : Configurer la session PySpark**
Dans votre code PySpark, spécifiez le chemin du fichier .jar du pilote JDBC SQL Server.
from pyspark.sql import SparkSession

# Chemin vers le fichier JAR du pilote JDBC
jar_path = "C:/Users/DeLL/Desktop/sqljdbc_4.2/enu/jre8/sqljdbc42.jar"

# Créer la session Spark
spark = SparkSession.builder \
    .appName("Mini Entrepôt de Données") \
    .config("spark.master", "local") \
    .config("spark.driver.extraClassPath", jar_path) \
    .getOrCreate()

# Vérifier la configuration de Spark
print(spark.sparkContext.getConf().getAll())

**Étape 3 : Connexion à SQL Server**
Pour  connecter à SQL Server via JDBC, il faut définir l'URL de connexion et les propriétés correctes :
jdbc_url = "jdbc:sqlserver://localhost:1433;databaseName=master;integratedSecurity=true"

jdbc_properties = {
    "user": "DESKTOP-F60H8N1/DeLL",
    "password": "",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# Exemple de lecture de données à partir d'une table SQL Server
df = spark.read.jdbc(url=jdbc_url, table="your_table", properties=jdbc_properties)
df.show()

**Étape 4 : Exécution du processus ETL**

 L'execution du processus ETL via le script etl.py. Ce script effectuera les opérations suivantes :

1-Chargement des données brutes depuis les fichiers CSV.
2-Transformations à l'aide de PySpark.
3-Écriture des données transformées dans SQL Server ou sauvegarde dans le répertoire de sortie.

# Dépendances
pyspark==3.3.0

# Résolution des problèmes
**Pilote JDBC non trouvé :** Vérifiez que le chemin vers le fichier .jar du pilote JDBC est correctement défini dans spark.driver.extraClassPath.
**Erreur d'authentification :**Si vous utilisez l'authentification Windows, assurez-vous que le fichier sqljdbc_auth.dll est correctement placé et que son chemin est défini dans les variables d'environnement.

**Problème lié à la connexion TCP avec SQL Server:**
Si vous rencontrez des erreurs de connexion TCP lors de la tentative de connexion à SQL Server, cela peut être dû à divers problèmes, tels que le firewall, la configuration du serveur SQL, ou une mauvaise configuration du JDBC.

# Vérifiez que SQL Server accepte les connexions TCP/IP
Par défaut, SQL Server peut ne pas accepter les connexions TCP/IP. Pour l'activer :

**Ouvrez SQL Server Configuration Manager.**
Allez dans SQL Server Network Configuration > Protocols for [Your SQL Instance].
Vérifiez que TCP/IP est activé. Si ce n'est pas le cas, faites un clic droit et sélectionnez Enable.
Redémarrez le service SQL Server.
 **Configurer le port TCP/IP**
SQL Server utilise par défaut le port 1433 pour les connexions TCP/IP. Assurez-vous que ce port est ouvert et non bloqué par un firewall.

Toujours dans SQL Server Configuration Manager, faites un clic droit sur TCP/IP dans Protocols for [Your SQL Instance] et sélectionnez Properties.
Sous l'onglet IP Addresses, assurez-vous que le port 1433 est bien spécifié pour TCP Port sous IPAll.

**Vérifier le firewall**
Assurez-vous que le firewall de votre machine ou du serveur autorise les connexions entrantes sur le port 1433.

Si vous utilisez Windows Firewall, accédez aux paramètres du firewall et autorisez les connexions entrantes pour SQL Server (port 1433).
 **Vérifier la chaîne de connexion JDBC**
La chaîne de connexion JDBC doit être correctement configurée avec le bon port et les bons paramètres de connexion. Voici un exemple pour SQL Server :
jdbc_url = "jdbc:sqlserver://localhost:1433;databaseName=your_database"
jdbc_properties = {
    "user": "your_username",
    "password": "your_password",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}
# Conclusion


### Points clés expliqués :
1. **Structure du projet** : Décrit les dossiers et fichiers du projet.
2. **Prérequis** : Liste les outils et bibliothèques nécessaires.
3. **Configuration** : Étapes détaillées pour configurer les variables d'environnement, PySpark, et les connexions JDBC.
4. **Processus ETL** : Montre comment charger les données, les transformer et les écrire dans SQL Server.
5. **Dépendances** : Liste des packages Python requis pour le projet.
6. **Résolution des problèmes** : Aide à résoudre les problèmes courants.
