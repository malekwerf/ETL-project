from pyspark.sql import SparkSession
from pyspark.sql import functions as F   # Pour des fonctions SQL
from pyspark.sql.types import *          # Pour les types de données Spark
import os

os.environ['java.library.path'] = "D:/sqljdbc_auth.dll"

# Définir le chemin vers le fichier .jar JDBC
jar_path = "C:/Users/DeLL/Desktop/sqljdbc_4.2/enu/jre8/sqljdbc42.jar"

# Créer la session Spark
spark = SparkSession.builder \
    .appName("Mini Data Warehouse") \
    .config("spark.master", "local") \
    .config("spark.driver.extraClassPath", jar_path) .getOrCreate()
    
    
sales_df = spark.read.option("header", True).csv("data/raw/sales.csv")
customers_df = spark.read.option("header", True).csv("data/raw/customers.csv")

sales_df.write.mode("overwrite").parquet("output/bronze/sales")
customers_df.write.mode("overwrite").parquet("output/bronze/customers")
#Vérifier les données brutes lues

print("Données brutes des ventes :")
sales_df.show()

print("Données brutes des clients :")
customers_df.show()



# Nettoyage des données pour la couche Silver
sales_clean_df = sales_df.select("CustomerID","OrderID", "ProductID", "Quantity", "UnitPrice")
#sales_df = sales_df.withColumnRenamed("OrderID", "OrderID0")
customers_clean_df = customers_df.select("CustomerID", "ContactName", "Address")



# Afficher un échantillon des données nettoyées
print("Données nettoyées des ventes :")
sales_clean_df.show()

print("Données nettoyées des clients :")
customers_clean_df.show()

# Sauvegarder les données nettoyées dans la couche Silver
sales_clean_df.write.mode("overwrite").parquet("output/silver/sales_clean")
customers_clean_df.write.mode("overwrite").parquet("output/silver/customers_clean")
# Jointure des ventes et des clients
enriched_df = sales_clean_df.join(customers_clean_df, "CustomerID", "inner")

# Afficher un échantillon de la table enrichie
print("Table enrichie des ventes :")
enriched_df.show()

# Sauvegarder la table enrichie dans la couche Gold
enriched_df.write.mode("overwrite").parquet("output/gold/enriched_sales")


# Créer une vue temporaire pour interroger les données
enriched_df.createOrReplaceTempView("enriched_sales")

# Requête SQL pour calculer le revenu total par produit
result = spark.sql(""" 
    SELECT ProductID, SUM(Quantity * UnitPrice) AS TotalRevenue 
    FROM enriched_sales 
    GROUP BY ProductID 
""")

# Afficher les résultats
print("Revenu total par produit :")
result.show()

                                                           #l'authentification Windows
jdbc_url = "jdbc:sqlserver://localhost:1433;databaseName=master;integratedSecurity=true"
jdbc_properties = {
    "user": "DESKTOP-F60H8N1/DeLL",
    "password": "",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# Exporter la table enrichie vers SQL Server
enriched_df.write.jdbc(url=jdbc_url, table="p", mode="overwrite", properties=jdbc_properties)

spark.stop()