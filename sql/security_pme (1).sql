-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3307
-- Généré le : ven. 31 juil. 2026 à 18:50
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
(10, 2, '2026-07-28 11:11:40', 44.00, 'Moyen'),
(11, 3, '2026-07-29 19:06:08', 28.00, 'Faible'),
(12, 2, '2026-07-30 12:25:11', 44.00, 'Moyen'),
(13, 2, '2026-07-30 22:28:58', 56.00, 'Moyen'),
(14, 2, '2026-07-30 22:31:12', 40.00, 'Moyen'),
(15, 2, '2026-07-30 22:36:40', 44.00, 'Moyen'),
(16, 2, '2026-07-31 12:00:36', 52.00, 'Moyen'),
(17, 2, '2026-07-31 12:06:50', 60.00, 'Moyen'),
(18, 2, '2026-07-31 12:12:22', 20.00, 'Faible'),
(19, 2, '2026-07-31 12:16:52', 24.00, 'Faible'),
(20, 2, '2026-07-31 12:32:33', 40.00, 'Moyen'),
(21, 2, '2026-07-31 13:01:08', 60.00, 'Moyen'),
(22, 2, '2026-07-31 13:03:09', 48.00, 'Moyen'),
(23, 2, '2026-07-31 17:46:31', 64.00, 'Moyen');

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
(2, 'ALTEN', 'alten@gmail', '$2b$12$TGhfyZo3cE2nYjZRjpcTu.mE1r8RhtkXZ8N3tMzu8AUdWOslHOmEW', '', 'Al-Houceima', '2026-07-27 13:51:03'),
(3, 'ALTEN', 'alten@gmail.com', '$2b$12$M5vA//kY0Y16bnvlmVpie.Ljh.eEcvz9hwVfpfSwdElskoqLXKHNK', '', 'Al-Houceima', '2026-07-29 19:04:45');

-- --------------------------------------------------------

--
-- Structure de la table `question`
--
-- Erreur de lecture de structure pour la table security_pme.question : #1932 - Table 'security_pme.question' doesn't exist in engine
-- Erreur de lecture des données pour la table security_pme.question : #1064 - Erreur de syntaxe près de 'FROM `security_pme`.`question`' à la ligne 1

-- --------------------------------------------------------

--
-- Structure de la table `recommandation`
--

CREATE TABLE `recommandation` (
  `id` int(11) NOT NULL,
  `diagnostic_id` int(11) NOT NULL,
  `contenu` text NOT NULL,
  `date_generation` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `recommandation`
--

INSERT INTO `recommandation` (`id`, `diagnostic_id`, `contenu`, `date_generation`) VALUES
(1, 12, '**Résumé de la situation**\nL\'entreprise ALTEN a obtenu un score de maturité cybersécurité de 44,0/100, ce qui indique un niveau de maturité moyen. Les résultats du diagnostic ont mis en évidence certaines catégories qui nécessitent une attention particulière, notamment la gouvernance, l\'organisation et la sensibilisation à la cybersécurité. Il est essentiel de mettre en place un plan d\'action correctif pour améliorer la cybersécurité de l\'entreprise et protéger ses actifs numériques.\n\n**Priorités d\'action**\n1. **Définition d\'un plan d\'action pour réduire les risques** : Il est crucial de désigner une personne ou une équipe responsable de la cybersécurité pour évaluer les risques et mettre en place un plan d\'action pour les réduire. C\'est important car cela permettra d\'identifier les vulnérabilités et de prendre des mesures pour les atténuer, ce qui réduira le risque d\'attaques ou de pertes de données.\n2. **Sensibilisation et formation du personnel** : Organiser des séances de sensibilisation et de formation en cybersécurité pour le personnel est essentiel pour prévenir les erreurs humaines qui peuvent compromettre la sécurité de l\'entreprise. C\'est important car un personnel informé et vigilant peut aider à prévenir les attaques et à réagir rapidement en cas d\'incident.\n3. **Evaluation des risques avant l\'intégration de nouveaux logiciels ou équipements** : Il est vital de mettre en place une procédure pour évaluer les risques avant l\'intégration de nouveaux logiciels, équipements ou services informatiques. C\'est important car cela permettra de détecter les vulnérabilités potentielles et de prendre des mesures pour les atténuer avant qu\'elles ne puissent causer des problèmes.\n\n**Recommandation d\'organisation**\nIl est recommandé de désigner un responsable de la cybersécurité en interne, qui sera chargé de mettre en place et de suivre le plan d\'action correctif. Ce responsable devra travailler en étroite collaboration avec les équipes informatiques et de direction pour assurer que les mesures de cybersécurité soient intégrées dans les processus de l\'entreprise. Avec des ressources limitées, il est important de prioriser les actions et de commencer par les plus urgentes, en cherchant éventuellement des ressources externes ou des formations pour aider à renforcer les capacités internes en cybersécurité.', '2026-07-30 12:25:14'),
(2, 22, '**Résumé de la situation**\nL\'entreprise ALTEN présente un score global de maturité en cybersécurité de 48,0/100, ce qui indique un niveau de maturité moyen. Les catégories nécessitant une attention particulière incluent la gestion des risques, la gouvernance et la sensibilisation à la cybersécurité. Les résultats du diagnostic mettent en évidence la nécessité d\'améliorer la gestion des risques et la mise en place d\'une politique de cybersécurité efficace.\n\n**Priorités d\'action**\n1. **Définir une procédure de gestion des incidents de cybersécurité** : Il est essentiel de mettre en place une procédure claire pour signaler et traiter les incidents de cybersécurité, tels que les virus, le phishing et la perte de données. Cela est important pour minimiser les impacts d\'une attaque et assurer la continuité des activités.\n2. **Élaborer une politique de cybersécurité** : La création d\'une politique de cybersécurité est cruciale pour définir les règles et les responsabilités en matière de cybersécurité au sein de l\'entreprise. Cela aidera à sensibiliser les employés et à prévenir les incidents de cybersécurité.\n3. **Désigner un responsable de la cybersécurité** : Il est vital de désigner une personne ou une équipe responsable de la cybersécurité pour assurer le suivi et la mise en œuvre des mesures de cybersécurité. Cela permettra de garantir que les actions correctives soient mises en œuvre de manière efficace.\n\n**Recommandation générale d\'organisation**\nIl est recommandé de créer un comité de cybersécurité composé de membres de l\'équipe de direction et de représentants des différents départements de l\'entreprise. Ce comité sera chargé de superviser la mise en œuvre des mesures de cybersécurité, de suivre les progrès et de prendre des décisions éclairées pour améliorer la cybersécurité de l\'entreprise. Cette approche permettra de mobiliser les ressources nécessaires et de garantir que la cybersécurité soit une prioritée au sein de l\'entreprise.', '2026-07-31 13:03:12'),
(3, 23, '**Résumé de la situation**\nL\'entreprise ALTEN a obtenu un score global de maturité en cybersécurité de 64,0/100, ce qui indique un niveau de maturité moyen. Les catégories de développement sécurisé et protection des données, ainsi que de gestion des risques, nécessitent une attention particulière. Il est essentiel de prendre des mesures correctives pour améliorer la cybersécurité de l\'entreprise et protéger ses actifs.\n\n**Priorités d\'action**\n\n1. **Définir une procédure de gestion des incidents de cybersécurité** : Créer un plan d\'urgence pour gérer les incidents tels que les virus, le phishing et la perte de données. C\'est important car cela permettra à l\'entreprise de réagir rapidement et de minimiser les dégâts en cas d\'incident.\n2. **Protéger les données sensibles** : Mettre en place des mesures de protection des données telles que le chiffrement, les mots de passe forts et les sauvegardes régulières. C\'est important car les données sensibles sont souvent la cible des cyberattaques et leur perte peut avoir des conséquences graves.\n3. **Identifier et documenter les risques** : Réaliser une analyse des risques pour identifier les menaces potentielles et documenter les résultats dans un registre de risques. C\'est important car cela permettra à l\'entreprise de prendre des mesures proactives pour atténuer les risques et prévenir les incidents de cybersécurité.\n\n**Recommandation générale d\'organisation**\nIl est recommandé de désigner un responsable de la cybersécurité au sein de l\'entreprise pour coordonner les efforts de sécurité et assurer la mise en œuvre des mesures correctives. Cela permettra de garantir que les actions priority sont mises en œuvre de manière efficace et que la cybersécurité devient une préoccupation permanente au sein de l\'entreprise.', '2026-07-31 17:46:33');

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
(20, 10, 'cat4_q7', 0),
(21, 11, 'cat1_q1', 0),
(22, 11, 'cat1_q2', 0),
(23, 11, 'cat1_q3', 1),
(24, 11, 'cat1_q4', 1),
(25, 11, 'cat2_q4', 0),
(26, 11, 'cat2_q3', 0),
(27, 11, 'cat2_q2', 2),
(28, 11, 'cat2_q1', 1),
(29, 11, 'cat3_q4', 0),
(30, 11, 'cat3_q3', 0),
(31, 11, 'cat3_q2', 0),
(32, 11, 'cat3_q1', 0),
(33, 11, 'cat4_q3', 0),
(34, 11, 'cat4_q2', 1),
(35, 11, 'cat4_q1', 1),
(36, 11, 'cat4_q5', 0),
(37, 11, 'cat4_q4', 0),
(38, 11, 'cat4_q6', 0),
(39, 11, 'cat4_q7', 0),
(40, 11, 'cat4_q8', 0),
(41, 12, 'cat1_q1', 0),
(42, 12, 'cat1_q2', 0),
(43, 12, 'cat1_q3', 1),
(44, 12, 'cat1_q4', 0),
(45, 12, 'cat2_q2', 2),
(46, 12, 'cat2_q3', 1),
(47, 12, 'cat2_q4', 1),
(48, 12, 'cat2_q1', 0),
(49, 12, 'cat3_q3', 0),
(50, 12, 'cat3_q4', 0),
(51, 12, 'cat3_q2', 1),
(52, 12, 'cat3_q1', 1),
(53, 12, 'cat4_q3', 0),
(54, 12, 'cat4_q4', 1),
(55, 12, 'cat4_q5', 1),
(56, 12, 'cat4_q6', 1),
(57, 12, 'cat4_q8', 0),
(58, 12, 'cat4_q2', 0),
(59, 12, 'cat4_q1', 1),
(60, 12, 'cat4_q7', 0),
(61, 13, 'cat1_q1', 0),
(62, 13, 'cat1_q2', 1),
(63, 13, 'cat1_q3', 0),
(64, 13, 'cat1_q4', 0),
(65, 13, 'cat2_q4', 1),
(66, 13, 'cat2_q3', 1),
(67, 13, 'cat2_q2', 1),
(68, 13, 'cat2_q1', 1),
(69, 13, 'cat3_q4', 1),
(70, 13, 'cat3_q3', 0),
(71, 13, 'cat3_q2', 0),
(72, 13, 'cat3_q1', 1),
(73, 13, 'cat4_q3', 1),
(74, 13, 'cat4_q4', 1),
(75, 13, 'cat4_q5', 1),
(76, 13, 'cat4_q6', 1),
(77, 13, 'cat4_q7', 1),
(78, 13, 'cat4_q8', 0),
(79, 13, 'cat4_q1', 1),
(80, 13, 'cat4_q2', 1),
(81, 14, 'cat1_q1', 2),
(82, 14, 'cat1_q2', 2),
(83, 14, 'cat1_q4', 1),
(84, 14, 'cat1_q3', 1),
(85, 14, 'cat2_q3', 0),
(86, 14, 'cat2_q2', 1),
(87, 14, 'cat2_q1', 0),
(88, 14, 'cat2_q4', 0),
(89, 14, 'cat3_q4', 0),
(90, 14, 'cat3_q3', 1),
(91, 14, 'cat3_q2', 1),
(92, 14, 'cat3_q1', 0),
(93, 14, 'cat4_q3', 1),
(94, 14, 'cat4_q4', 0),
(95, 14, 'cat4_q5', 0),
(96, 14, 'cat4_q7', 0),
(97, 14, 'cat4_q6', 0),
(98, 14, 'cat4_q8', 0),
(99, 14, 'cat4_q2', 0),
(100, 14, 'cat4_q1', 0),
(101, 15, 'cat1_q1', 1),
(102, 15, 'cat1_q2', 2),
(103, 15, 'cat1_q4', 2),
(104, 15, 'cat1_q3', 1),
(105, 15, 'cat2_q1', 0),
(106, 15, 'cat2_q2', 0),
(107, 15, 'cat2_q3', 1),
(108, 15, 'cat2_q4', 1),
(109, 15, 'cat3_q4', 0),
(110, 15, 'cat3_q3', 0),
(111, 15, 'cat3_q2', 0),
(112, 15, 'cat3_q1', 0),
(113, 15, 'cat4_q1', 0),
(114, 15, 'cat4_q2', 0),
(115, 15, 'cat4_q3', 0),
(116, 15, 'cat4_q4', 0),
(117, 15, 'cat4_q5', 1),
(118, 15, 'cat4_q6', 1),
(119, 15, 'cat4_q7', 1),
(120, 15, 'cat4_q8', 0),
(121, 16, 'cat1_q1', 0),
(122, 16, 'cat1_q2', 1),
(123, 16, 'cat1_q3', 1),
(124, 16, 'cat1_q4', 0),
(125, 16, 'cat2_q4', 1),
(126, 16, 'cat2_q3', 1),
(127, 16, 'cat2_q2', 2),
(128, 16, 'cat2_q1', 0),
(129, 16, 'cat3_q3', 0),
(130, 16, 'cat3_q4', 0),
(131, 16, 'cat3_q2', 1),
(132, 16, 'cat3_q1', 1),
(133, 16, 'cat4_q1', 1),
(134, 16, 'cat4_q2', 1),
(135, 16, 'cat4_q3', 0),
(136, 16, 'cat4_q4', 1),
(137, 16, 'cat4_q6', 0),
(138, 16, 'cat4_q5', 0),
(139, 16, 'cat4_q7', 1),
(140, 16, 'cat4_q8', 1),
(141, 17, 'cat1_q1', 0),
(142, 17, 'cat1_q2', 0),
(143, 17, 'cat1_q3', 2),
(144, 17, 'cat1_q4', 2),
(145, 17, 'cat2_q1', 1),
(146, 17, 'cat2_q2', 2),
(147, 17, 'cat2_q3', 0),
(148, 17, 'cat2_q4', 1),
(149, 17, 'cat3_q3', 0),
(150, 17, 'cat3_q4', 1),
(151, 17, 'cat3_q2', 0),
(152, 17, 'cat3_q1', 1),
(153, 17, 'cat4_q3', 1),
(154, 17, 'cat4_q4', 1),
(155, 17, 'cat4_q5', 0),
(156, 17, 'cat4_q6', 0),
(157, 17, 'cat4_q7', 1),
(158, 17, 'cat4_q8', 1),
(159, 17, 'cat4_q1', 1),
(160, 17, 'cat4_q2', 0),
(161, 18, 'cat1_q2', 0),
(162, 18, 'cat1_q1', 0),
(163, 18, 'cat1_q4', 0),
(164, 18, 'cat1_q3', 1),
(165, 18, 'cat2_q4', 1),
(166, 18, 'cat2_q3', 0),
(167, 18, 'cat2_q2', 0),
(168, 18, 'cat2_q1', 0),
(169, 18, 'cat3_q2', 0),
(170, 18, 'cat3_q3', 0),
(171, 18, 'cat3_q1', 1),
(172, 18, 'cat3_q4', 1),
(173, 18, 'cat4_q1', 0),
(174, 18, 'cat4_q2', 0),
(175, 18, 'cat4_q3', 0),
(176, 18, 'cat4_q5', 0),
(177, 18, 'cat4_q4', 0),
(178, 18, 'cat4_q6', 0),
(179, 18, 'cat4_q8', 0),
(180, 18, 'cat4_q7', 1),
(181, 19, 'cat1_q1', 0),
(182, 19, 'cat1_q2', 0),
(183, 19, 'cat1_q3', 0),
(184, 19, 'cat1_q4', 1),
(185, 19, 'cat2_q3', 0),
(186, 19, 'cat2_q4', 0),
(187, 19, 'cat2_q2', 0),
(188, 19, 'cat2_q1', 1),
(189, 19, 'cat3_q4', 1),
(190, 19, 'cat3_q3', 0),
(191, 19, 'cat3_q1', 1),
(192, 19, 'cat3_q2', 0),
(193, 19, 'cat4_q1', 0),
(194, 19, 'cat4_q2', 1),
(195, 19, 'cat4_q4', 0),
(196, 19, 'cat4_q3', 0),
(197, 19, 'cat4_q6', 0),
(198, 19, 'cat4_q5', 0),
(199, 19, 'cat4_q7', 1),
(200, 19, 'cat4_q8', 0),
(201, 20, 'cat1_q2', 0),
(202, 20, 'cat1_q1', 0),
(203, 20, 'cat1_q3', 0),
(204, 20, 'cat1_q4', 0),
(205, 20, 'cat2_q4', 0),
(206, 20, 'cat2_q3', 0),
(207, 20, 'cat2_q2', 2),
(208, 20, 'cat2_q1', 1),
(209, 20, 'cat3_q4', 1),
(210, 20, 'cat3_q3', 1),
(211, 20, 'cat3_q2', 0),
(212, 20, 'cat3_q1', 1),
(213, 20, 'cat4_q1', 0),
(214, 20, 'cat4_q2', 1),
(215, 20, 'cat4_q3', 0),
(216, 20, 'cat4_q4', 1),
(217, 20, 'cat4_q5', 1),
(218, 20, 'cat4_q6', 1),
(219, 20, 'cat4_q7', 0),
(220, 20, 'cat4_q8', 0),
(221, 21, 'cat1_q1', 0),
(222, 21, 'cat1_q2', 1),
(223, 21, 'cat1_q3', 2),
(224, 21, 'cat1_q4', 2),
(225, 21, 'cat2_q4', 0),
(226, 21, 'cat2_q3', 0),
(227, 21, 'cat2_q2', 1),
(228, 21, 'cat2_q1', 0),
(229, 21, 'cat3_q4', 1),
(230, 21, 'cat3_q2', 1),
(231, 21, 'cat3_q3', 1),
(232, 21, 'cat3_q1', 1),
(233, 21, 'cat4_q4', 0),
(234, 21, 'cat4_q3', 0),
(235, 21, 'cat4_q2', 0),
(236, 21, 'cat4_q1', 1),
(237, 21, 'cat4_q5', 1),
(238, 21, 'cat4_q6', 1),
(239, 21, 'cat4_q7', 1),
(240, 21, 'cat4_q8', 1),
(241, 22, 'cat1_q1', 0),
(242, 22, 'cat1_q2', 1),
(243, 22, 'cat1_q3', 1),
(244, 22, 'cat1_q4', 1),
(245, 22, 'cat2_q3', 0),
(246, 22, 'cat2_q4', 0),
(247, 22, 'cat2_q1', 1),
(248, 22, 'cat2_q2', 2),
(249, 22, 'cat3_q1', 0),
(250, 22, 'cat3_q2', 0),
(251, 22, 'cat3_q3', 1),
(252, 22, 'cat3_q4', 1),
(253, 22, 'cat4_q1', 1),
(254, 22, 'cat4_q2', 1),
(255, 22, 'cat4_q3', 1),
(256, 22, 'cat4_q4', 1),
(257, 22, 'cat4_q6', 0),
(258, 22, 'cat4_q5', 0),
(259, 22, 'cat4_q7', 0),
(260, 22, 'cat4_q8', 0),
(261, 23, 'cat1_q1', 2),
(262, 23, 'cat1_q3', 2),
(263, 23, 'cat1_q4', 2),
(264, 23, 'cat1_q2', 2),
(265, 23, 'cat2_q1', 0),
(266, 23, 'cat2_q2', 0),
(267, 23, 'cat2_q3', 0),
(268, 23, 'cat2_q4', 0),
(269, 23, 'cat3_q1', 0),
(270, 23, 'cat3_q2', 0),
(271, 23, 'cat3_q3', 0),
(272, 23, 'cat3_q4', 0),
(273, 23, 'cat4_q3', 1),
(274, 23, 'cat4_q2', 1),
(275, 23, 'cat4_q4', 1),
(276, 23, 'cat4_q5', 1),
(277, 23, 'cat4_q6', 1),
(278, 23, 'cat4_q7', 1),
(279, 23, 'cat4_q8', 1),
(280, 23, 'cat4_q1', 1);

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
(40, 10, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 62.50),
(41, 11, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 25.00),
(42, 11, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 60.00),
(43, 11, 'cat3_gestion_des_risques', 'Gestion des risques', 0.00),
(44, 11, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 25.00),
(45, 12, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 12.50),
(46, 12, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 80.00),
(47, 12, 'cat3_gestion_des_risques', 'Gestion des risques', 50.00),
(48, 12, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 50.00),
(49, 13, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 12.50),
(50, 13, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 80.00),
(51, 13, 'cat3_gestion_des_risques', 'Gestion des risques', 50.00),
(52, 13, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 87.50),
(53, 14, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 75.00),
(54, 14, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 20.00),
(55, 14, 'cat3_gestion_des_risques', 'Gestion des risques', 50.00),
(56, 14, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 12.50),
(57, 15, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 75.00),
(58, 15, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 40.00),
(59, 15, 'cat3_gestion_des_risques', 'Gestion des risques', 0.00),
(60, 15, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 37.50),
(61, 16, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 25.00),
(62, 16, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 80.00),
(63, 16, 'cat3_gestion_des_risques', 'Gestion des risques', 50.00),
(64, 16, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 62.50),
(65, 17, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 50.00),
(66, 17, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 80.00),
(67, 17, 'cat3_gestion_des_risques', 'Gestion des risques', 50.00),
(68, 17, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 62.50),
(69, 18, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 12.50),
(70, 18, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 20.00),
(71, 18, 'cat3_gestion_des_risques', 'Gestion des risques', 50.00),
(72, 18, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 12.50),
(73, 19, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 12.50),
(74, 19, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 20.00),
(75, 19, 'cat3_gestion_des_risques', 'Gestion des risques', 50.00),
(76, 19, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 25.00),
(77, 20, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 0.00),
(78, 20, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 60.00),
(79, 20, 'cat3_gestion_des_risques', 'Gestion des risques', 75.00),
(80, 20, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 50.00),
(81, 21, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 62.50),
(82, 21, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 20.00),
(83, 21, 'cat3_gestion_des_risques', 'Gestion des risques', 100.00),
(84, 21, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 62.50),
(85, 22, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 37.50),
(86, 22, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 60.00),
(87, 22, 'cat3_gestion_des_risques', 'Gestion des risques', 50.00),
(88, 22, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 50.00),
(89, 23, 'cat1_contexte_et_criticite_du_syste', 'Contexte et criticité du système d\'information', 100.00),
(90, 23, 'cat2_developpement_securise_et_prot', 'Développement sécurisé et protection des données', 0.00),
(91, 23, 'cat3_gestion_des_risques', 'Gestion des risques', 0.00),
(92, 23, 'cat4_gouvernance_organisation_et_se', 'Gouvernance, organisation et sensibilisation à la cybersécurité', 100.00);

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
-- Index pour la table `recommandation`
--
ALTER TABLE `recommandation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `diagnostic_id` (`diagnostic_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT pour la table `pme`
--
ALTER TABLE `pme`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `recommandation`
--
ALTER TABLE `recommandation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `reponse`
--
ALTER TABLE `reponse`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=281;

--
-- AUTO_INCREMENT pour la table `score_categorie`
--
ALTER TABLE `score_categorie`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `diagnostic`
--
ALTER TABLE `diagnostic`
  ADD CONSTRAINT `diagnostic_ibfk_1` FOREIGN KEY (`pme_id`) REFERENCES `pme` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `recommandation`
--
ALTER TABLE `recommandation`
  ADD CONSTRAINT `recommandation_ibfk_1` FOREIGN KEY (`diagnostic_id`) REFERENCES `diagnostic` (`id`) ON DELETE CASCADE;

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
