
![Assistify](https://i.imgur.com/lHkmErl.png)

# **Assistify - Your AI Powered Helper!**

[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Benji1155/Assistify)](https://img.shields.io/github/v/release/Benji1155/Assistify)
[![GitHub last commit](https://img.shields.io/github/last-commit/Benji1155/Assistify)](https://img.shields.io/github/last-commit/Benji1155/Assistify)
[![GitHub issues](https://img.shields.io/github/issues-raw/Benji1155/Assistify)](https://img.shields.io/github/issues-raw/Benji1155/Assistify)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Benji1155/Assistify)](https://img.shields.io/github/issues-pr/Benji1155/Assistify)
[![GitHub](https://img.shields.io/github/license/Benji1155/Assistify)](https://img.shields.io/github/license/Benji1155/Assistify)

**Introduction**

This assessment explores the development of a natural language processing (NLP)-based dialog chatbot named Assistify. Designed as a personal assistant replacement, Assistify offers various practical features, including:

- Wikipedia Integration: Learn about topics with ease.
- Weather Reports: Stay informed to ensure the weather doesn’t disrupt your day.
- Meeting Scheduler: Keep track of your meetings effortlessly.

These features make Assistify a valuable tool for busy individuals to organize their day and handle unexpected events. Unlike casual conversational chatbots, Assistify focuses on practicality and work-oriented tasks. By leveraging NLP and other techniques, it ensures a smooth user experience. Furthermore, Assistify is free and accessible anytime, anywhere unlike a traditional personal assistant.

**NLP Techniques**

Assistify utilizes several NLP techniques. A critical decision during development was choosing between a deep learning approach and a rule-based system:

- Deep Learning: Ideal for handling unexpected or conversational inputs. With proper training, it can mimic human-like interactions. However, it requires significant data, time, and tuning.
- Rule-Based System: Selected for this project due to its simplicity and suitability for predefined use cases. It provides consistent and precise responses within its scope.

**Input Cleaning**

To ensure accurate responses, user inputs are cleaned by:

- Removing punctuation.
- Converting text to lowercase.

This preprocessing improves message consistency and response accuracy.
Extracting Locations for Weather Updates

Determining the user's location for weather updates posed a unique challenge. Listing all possible place names was inefficient. Instead, a smarter approach was implemented:

-  Use a library to categorize words as nouns, verbs, locations, etc.
    Identify location names by cycling through these categorized words.
    Supplement this with a custom list of New Zealand’s most populous cities (as the library might lack local names).

While not 100% accurate, this method covers most scenarios effectively.
Storage

**Storage**

A key aspect of Assistify is its ability to store login credentials and meeting information. To ensure data separation for different users, a login system was introduced. User-specific information, such as names, is stored in a MySQL database, enabling:

- Personalization of the chatbot experience.
- Easy data syncing across devices due to its online nature.

Although a local database could have sufficed, a MySQL database was chosen for its versatility and ability to support multi-user functionality. This ensures seamless data storage and retrieval.

**Front-End**

Creating an intuitive and user-friendly interface was a priority. A graphical user interface (GUI) was developed using Tkinter, chosen for its simplicity and ease of integration.
Key Features:

- Chatbox: Facilitates sending and receiving messages seamlessly.
- Buttons: Guide users intuitively through available actions.

Unlike console-based chatbots, the Tkinter GUI provides a modern and accessible interface that aligns with user expectations for contemporary applications.
