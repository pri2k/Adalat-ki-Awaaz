# Adalat ki Awaaz

Adalat ki Awaaz is an autonomous AI agent designed to search, summarize, optimize, and publish news content on Indian law and judicial rulings. It ensures SEO-optimized, structured, and multilingual content delivery with fully automated publishing.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

Adalat ki Awaaz is built to autonomously aggregate, process, and publish news articles. It employs advanced AI techniques to fetch articles, generate structured summaries, optimize content for search engines, and publish seamlessly without human intervention. This project focuses on automation, multilingual support, and SEO optimization.

## Features

- **Automated Web Crawling & Data Extraction**: Fetches news articles from reliable sources and classifies them into sub-topics.
- **Summarization & Content Generation**: Uses BART for summarization to create concise, well-structured articles.
- **SEO Optimization**: Enhances discoverability with keyword extraction, metadata generation, and readability improvements using NLTK.
- **Metadata Extraction & Tagging**: Tokenizes articles to extract keywords and generates structured key-value metadata pairs for tagging.
- **Multilingual Support**: Uses NLLB to translate summaries into Hindi, Bangla, and Telugu for wider accessibility.
- **Automated Publishing**: Publishes articles to WordPress autonomously via `wordpress_xmlrpc`, ensuring seamless content deployment.
- **Scalability & Modular Architecture**: Easily extendable for additional features like analytics and user engagement tracking.

## Technologies

- **Python**: Core language for development.
- **Django**: Backend framework for API and data handling.
- **Hugging Face Transformers**: Model deployment for summarization and translation.
- **NLTK**: Keyword extraction and search optimization.
- **BART**: Used for article summarization.
- **NLLB**: Enables multilingual translations.
- **WordPress XML-RPC**: Automates article publishing.

## Installation

### Prerequisites

- Python 3.x
- Git

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/pri2k/Adalat-ki-Awaaz.git
   ```

2. **Navigate to the Project Directory:**

   ```bash
   cd Adalat-ki-Awaaz
   ```

3. **Set Up a Virtual Environment (Optional but Recommended):**

   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the autonomous agent, run:

```bash
python main.py
```

The system will automatically fetch news, summarize content, optimize for SEO, translate, and publish articles to WordPress.

## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

Please open an issue before making major changes to discuss ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For updates and details, visit: [Adalat ki Awaaz](https://adalatkiawaaz.wordpress.com).
