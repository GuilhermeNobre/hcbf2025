# Projeto Biofy - 2º Hackathon Biofy

Este projeto foi desenvolvido durante o 2º Hackathon Biofy, focado em soluções inovadoras para a área de biotecnologia e saúde. O projeto consiste em uma aplicação web que utiliza inteligência artificial para detecção e classificação de bactérias, com uma interface interativa e funcionalidades de visualização de dados.

## 🚀 Funcionalidades

- Detecção e classificação de bactérias usando YOLOv8
- Interface web interativa construída com Streamlit
- Visualização de dados e métricas
- Sistema de armazenamento e gerenciamento de imagens
- Análise temporal dos dados

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- YOLOv8 para detecção de objetos
- Streamlit para interface web
- OpenCV para processamento de imagens
- Pandas para manipulação de dados
- SQLite para armazenamento de dados

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

## 🔧 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/hcbf2025.git
cd hcbf2025
```

2. Instale as dependências:

```bash
cd streamlit-test-hc
pip install -r requirements.txt
```

3. Baixe os modelos pré-treinados:

- Os modelos YOLOv8 já estão incluídos no diretório `bacteria-project/`

## 🎮 Como Executar

1. Navegue até o diretório da aplicação:

```bash
cd streamlit-test-hc
```

2. Execute a aplicação Streamlit:

```bash
streamlit run main.py
```

3. A aplicação estará disponível em `http://localhost:8501`

## 📁 Estrutura do Projeto

- `bacteria-project/`: Contém os modelos YOLOv8 e notebooks de treinamento
- `streamlit-test-hc/`: Aplicação web principal
  - `main.py`: Arquivo principal da aplicação
  - `image_page.py`: Página de processamento de imagens
  - `timelife.py`: Análise temporal dos dados
  - `dom_file.py`: Gerenciamento de arquivos
  - `map_stream.py`: Visualização de dados em mapa

## 🤝 Contribuição

Este projeto foi desenvolvido durante o 2º Hackathon Biofy. Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- Equipe do 2º Hackathon Biofy

## 🙏 Agradecimentos

- Biofy por organizar o hackathon
- Todos os mentores e participantes que contribuíram com o projeto
