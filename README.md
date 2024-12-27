# Hospital Patient Locator

Ce projet est une application distribuée permettant de localiser les patients dans un hôpital. L'architecture comprend plusieurs microservices basés sur Spring Boot et un conteneur MongoDB pour le stockage des données.

---

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- **Docker** et **Docker Compose**
- **Java 17** ou supérieur
- **Maven**
- **Node.js** et **npm** (pour le frontend web et mobile)

---

## Architecture des Services

### Backend
- **eureka-server** : Serveur de registre pour la découverte des services.
- **gateway-server** : Passerelle pour acheminer les requêtes vers les services appropriés.
- **health-data-service** : Gestion des données de santé des patients.
- **hallway-detection-service** : Détection des mouvements des patients dans les couloirs.
- **notification-service** : Envoi de notifications en cas d'événements importants.
- **patient-location-service** : Localisation en temps réel des patients.
- **user-service** : Gestion des utilisateurs et de l'authentification.

### Frontend
- **mobile** : Application mobile pour accéder aux informations de localisation.
- **web** : Application web pour les administrateurs et le personnel hospitalier.

---

## Instructions pour exécuter les services

### 1. Démarrer la base de données MongoDB

Créez un fichier `docker-compose.yml` dans le répertoire racine du projet avec le contenu suivant :

```yaml
version: '3.8'

services:
  mongodb_container:
    image: mongo:latest
    container_name: mongodb_container
    environment:
      MONGO_INITDB_DATABASE: hospital
    ports:
      - 27017:27017
    volumes:
      - mongodb_data_container:/data/db

volumes:
  mongodb_data_container:

Ensuite, exécutez la commande suivante pour démarrer MongoDB :

docker-compose up -d

### 2. Démarrer le serveur Eureka
Naviguez dans le dossier eureka-server et exécutez les commandes suivantes :
mvn clean install
java -jar target/eureka-server-0.0.1-SNAPSHOT.jar

### 3. Démarrer le Gateway Server
Naviguez dans le dossier gateway-server et exécutez les commandes suivantes:
```yaml
mvn clean install
java -jar target/gateway-server-0.0.1-SNAPSHOT.jar







