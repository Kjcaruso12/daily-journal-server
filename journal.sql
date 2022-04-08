CREATE TABLE `JournalEntries` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept`	TEXT NOT NULL,
	`entry`	TEXT NOT NULL,
    `date` CURRENT_DATE NOT NULL,
    `mood_id` INTEGER NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Moods`(`id`)
);

CREATE TABLE `Moods` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label`    TEXT NOT NULL
);

CREATE TABLE `EntryTags` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`entry_id` INTEGER NOT NULL,
	`tag_id` INTEGER,
	FOREIGN KEY(`entry_id`) REFERENCES `JournalEntries`(`id`),
	FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE `Tags` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`subject`	TEXT NOT NULL
);

INSERT INTO `JournalEntries` VALUES (null, 'Javascript', "I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.", "Wed Sep 15 2021 10:10:47 ", 1);
INSERT INTO `JournalEntries` VALUES (null, 'Python', "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake", "Wed Sep 15 2021 10:11:33 ", 4);
INSERT INTO `JournalEntries` VALUES (null, 'Python', "Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks", "Wed Sep 15 2021 10:13:11 ", 3);
INSERT INTO `JournalEntries` VALUES (null, 'Javascript', "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.", "Wed Sep 15 2021 10:14:05 ", 3);

INSERT INTO `Moods` VALUES (null, "Happy");
INSERT INTO `Moods` VALUES (null, "Sad");
INSERT INTO `Moods` VALUES (null, "Angry");
INSERT INTO `Moods` VALUES (null, "Ok");

INSERT INTO `Tags` VALUES (null, "Loop");
INSERT INTO `Tags` VALUES (null, "Conditional");
INSERT INTO `Tags` VALUES (null, "Nonsense");

INSERT INTO `EntryTags` VALUES (null, 1, 1);
INSERT INTO `EntryTags` VALUES (null, 3, 2);
INSERT INTO `EntryTags` VALUES (null, 2, 3);

SELECT * FROM `JournalEntries` WHERE entry LIKE "Python%";