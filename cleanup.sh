#!/bin/bash

RESOURCE_GROUP="rg-mlops"

echo "=========================================="
echo "Nettoyage des ressources Azure"
echo "=========================================="

read -p "Voulez-vous vraiment supprimer toutes les ressources ? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Operation annulee."
    exit 0
fi

echo "\nRessources a supprimer:"
az resource list --resource-group $RESOURCE_GROUP --output table

echo "\nSuppression en cours..."
az group delete --name $RESOURCE_GROUP --yes --no-wait

echo "\nSuppression lancee (prend 5-10 minutes)"
echo "Verifiez sur : https://portal.azure.com"