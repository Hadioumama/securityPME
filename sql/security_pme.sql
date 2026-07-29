-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3307
-- Généré le : mar. 28 juil. 2026 à 19:21
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `security_pme`
--

-- --------------------------------------------------------

--
-- Structure de la table `categorie`
--
-- Erreur de lecture de structure pour la table security_pme.categorie : #1932 - Table 'security_pme.categorie' doesn't exist in engine
-- Erreur de lecture des données pour la table security_pme.categorie : #1064 - Erreur de syntaxe près de 'FROM `security_pme`.`categorie`' à la ligne 1

-- --------------------------------------------------------

--
-- Structure de la table `diagnostic`
--

CREATE TABLE `diagnostic` (
  `id` int(11) NOT NULL,
  `pme_id` int(11) NOT NULL,
  `date_diagnostic` datetime DEFAULT current_timestamp(),
  `score_global` decimal(5,2) NOT NULL,
  `niveau` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `diagnostic`
--

INSERT INTO `diagnostic` (`id`, `pme_id`, `date_diagnostic`, `score_global`, `niveau`) VALUES
(1, 2, '2026-07-27 18:37:17', 64.00, 'Moyen'),
(2, 2, '2026-07-27 18:38:09', 64.00, 'Moyen'),
(3, 2, '2026-07-27 18:39:28', 48.00, 'Moyen'),
(4, 2, '2026-07-27 18:43:07', 56.00, 'Moyen'),
(5, 2, '2026-07-27 18:47:41', 56.00, 'Moyen'),
(6, 2, '2026-07-27 18:51:46', 56.00, 'Moyen'),
(7, 2, '2026-07-28 11:03:37', 44.00, 'Moyen'),
(8, 2, '2026-07-28 11:04:31', 44.00, 'Moyen'),
(9, 2, '2026-07-28 11:08:06', 44.00, 'Moyen'),
(10, 2, '2026-07-28 11:11:40', 44.00, 'Moyen');

-- --------------------------------------------------------

--
-- Structure de la table `pme`
--

CREATE TABLE `pme` (
  `id` int(11) NOT NULL,
  `nom` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `secteur` varchar(100) DEFAULT NULL,
  `ville` varchar(100) DEFAULT NULL,
  `date_creation` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `pme`
--

INSERT INTO `pme` (`id`, `nom`, `email`, `mot_de_passe`, `secteur`, `ville`, `date_creation`) VALUES
(2, 'ALTEN', 'alten@gmail', '$2b$12$TGhfyZo3cE2nYjZRjpcTu.mE1r8RhtkXZ8N3tMzu8AUdWOslHOmEW', '', 'Al-Houceima', '2026-07-27 13:51:03');

-- --------------------------------------------------------

--
-- Structure de la table `question`
--
-- Erreur de lecture de structure pour la table security_pme.question : #1932 - Table 'security_pme.question' doesn't exist in engine
-- Erreur de lecture des données pour la table security_pme.question : #1064 - Erreur de syntaxe près de 'FROM `security_pme`.`question`' à la ligne 1

-- --------------------------------------------------------

--
-- Structure de la table `reponse`
--

CREATE TABLE `reponse` (
  `id` int(11) NOT NULL,
  `diagnostic_id` int(11) NOT NULL,
  `question_id` varchar(50) NOT NULL,
  `score_obtenu` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `reponse`
--

INSERT INTO `reponse` (`id`, `diagnostic_id`, `question_id`, `score_obtenu`) VALUES
(1, 10, 'cat1_q1', 1),
(2, 10, 'cat1_q3', 0),
(3, 10, 'cat1_q4', 0),
(5, 10, 'cat2_q3', 1),
(6, 10, 'cat2_q4', 0),
(7, 10, 'cat2_q2', 0),
(8, 10, 'cat2_q1', 0),
(9, 10, 'cat3_q4', 0),
(10, 10, 'cat3_q3', 1),
(11, 10, 'cat3_q2', 1),
(12, 10, 'cat3_q1', 1),
(13, 10, 'cat4_q1', 0),
(14, 10, 'cat4_q2', 1),
(15, 10, 'cat4_q3', 1),
(16, 10, 'cat4_q4', 1),
(17, 10, 'cat4_q5', 1),
(18, 10, 'cat4_q6', 1),
(19, 10, 'cat4_q8', 0),
(20, 10, 'cat4_q7', 0);

-- --------------------------------------------------------

--
-- Structure de la table `score_categorie`
--

CREATE TABLE `score_categorie` (
  `id` int(11) NOT NULL,
  `diagnostic_id` int(11) NOT NULL,
  `categorie_id` varchar(100) NOT NULL,
  `categorie_nom` varchar(200) NOT NULL,
  `score` decimal(5,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `score_categorie`
--

INSERT INTO `score_categorie` (`id`, `diagnostic_id`, `categorie_id`, `categorie_nom`, `score`) VALUES
(37, 10, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 25.00),
(38, 10, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 20.00),
(39, 10, 'cat3_gestion_des_risques', 'Gestion des risques', 75.00),
(40, 10, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 62.50);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `diagnostic`
--
ALTER TABLE `diagnostic`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_diagnostic_pme` (`pme_id`);

--
-- Index pour la table `pme`
--
ALTER TABLE `pme`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Index pour la table `reponse`
--
ALTER TABLE `reponse`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_reponse_diagnostic` (`diagnostic_id`);

--
-- Index pour la table `score_categorie`
--
ALTER TABLE `score_categorie`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_score_categorie_evaluation` (`diagnostic_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `diagnostic`
--
ALTER TABLE `diagnostic`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT pour la table `pme`
--
ALTER TABLE `pme`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `reponse`
--
ALTER TABLE `reponse`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT pour la table `score_categorie`
--
ALTER TABLE `score_categorie`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `diagnostic`
--
ALTER TABLE `diagnostic`
  ADD CONSTRAINT `diagnostic_ibfk_1` FOREIGN KEY (`pme_id`) REFERENCES `pme` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `reponse`
--
ALTER TABLE `reponse`
  ADD CONSTRAINT `reponse_ibfk_1` FOREIGN KEY (`diagnostic_id`) REFERENCES `diagnostic` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `score_categorie`
--
ALTER TABLE `score_categorie`
  ADD CONSTRAINT `score_categorie_ibfk_1` FOREIGN KEY (`diagnostic_id`) REFERENCES `diagnostic` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
