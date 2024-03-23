# CERBERUS

Projeto desenvolvido para a disciplina de Aprendizagem de Máquina em Sistemas Embarcados (2023.2) do curso de Engenharia de Computação da Universidade Federal de Alagoas (UFAL).

#### Professor
- Erick de Andrade Barboza

#### Alunos 
- Bruno Lemos de Lima
- José Ferreira Leite Neto
- Karla Sophia Santana da Cruz

## Sumário

Clique nos links abaixo para acessar rapidamente a seção desejada:

- [Sobre](#sobre)
- [Principais Funcionalidades](#principais-funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Dependências [device]](#dependências-device)
- [Dependências [server]](#dependências-server)
- [Como executar [device]](#como-executar-device)
- [Como executar [server]](#como-executar-server)
- [Licença](#licença)
- [Agradecimentos](#agradecimentos)

## Sobre
Este projeto tem como objetivo desenvolver um sistema de reconhecimento facial utilizando um dispositivo embarcado (Arduino Nano 33 BLE Sense) e um servidor para armazenamento e processamento dos dados. O sistema é composto por duas partes: o dispositivo embarcado, que captura a imagem do rosto do usuário e a envia para o servidor, e o servidor, que recebe a imagem, extrai os embeddings do rosto e compara com os embeddings armazenados no banco de dados. O sistema foi desenvolvido utilizando Python e as bibliotecas OpenCV, DeepFace e FastAPI. A comunicação entre o dispositivo embarcado e o servidor é feita por Serial.

## Principais Funcionalidades

- **Cadastro de usuário [SIGN UP]**
  O usuário pode se cadastrar no sistema fornecendo seu nome e um e-mail válido. O sistema verifica se o e-mail já está cadastrado e, caso não esteja, ele extrai por meio da imagem tirada pelo dispositivo embarcado o rosto do usuário e armazena os embeddings do rosto no banco de dados.

- **Login de usuário [SIGN IN]**
  O usuário pode fazer login no sistema fornecendo seu e-mail. O sistema verifica se o e-mail está cadastrado e, caso esteja, ele extrai por meio da imagem tirada pelo dispositivo embarcado o rosto do usuário e compara com os embeddings armazenados no banco de dados.

- **Captura de imagem [CAPTURE]**
  O dispositivo embarcado captura uma imagem do rosto do usuário e a envia para o servidor. O servidor recebe e envia para o Cliente, que exibe a imagem capturada.

- **Sair [EXIT]**
  O usuário pode sair do sistema a qualquer momento, fechando a página do Cliente.

## Estrutura do Projeto

O projeto está estruturado da seguinte forma:

```
Socket
│   LICENSE
│   README.md
└───device
│   └───include
│       │   device_settings.h
│       │   image_provider.h
│       │   model_settings.h
│       │   person_detect_model_data.h
│       │   person_detection.h
│   └───device_settings.cpp
│   └───device.ino
│   └───image_provider.cpp
│   └───model_settings.cpp
│   └───person_detect_model_data.cpp
│   └───person_detection.cpp
└───server
│   └───static
│       └───css
│           │   main.css
│           │   sweetalert2.css
│       └───img
│           │   icon.png
│       └───js
│           │   main.js
│   └───templates
│       │   index.html
│   └───utils
│       │   hex.py
│       │   ports.py
│   │   .env.example
│   │   .gitignore
│   │   app.py
│   │   communication.py
│   │   config.py
│   │   database.py
│   │   logger.py
│   │   main.py
│   │   requirements.txt
```

- Na raiz do projeto, podem ser encontrados: ``LICENSE`` (licença padrão MIT), ``README.md`` (este README) e as pastas ``device`` e ``server``.
- A pasta ``device`` contém os arquivos necessários para a execução do projeto no dispositivo embarcado (Arudino Nano 33 BLE Sense), com os arquivos de código-fonte e de configuração.
- A pasta ``server`` contém os arquivos necessários para a execução do projeto no servidor, com os arquivos de código-fonte, arquivos estáticos (CSS, JS e imagens) e templates HTML, além de arquivos de configuração e utilitários.

## Dependências Device

As dependências necessárias para a execução do projeto no dispositivo embarcado são: 

- Arduino IDE
- Arduino Mbed OS Nano Boards (Versão Latest)
- Biblioteca TinyMLx (Versão 1.1.0 Alpha)
- Biblioteca LSM9DS1 (Versão 1.1.0)
- Biblioteca TensorFlowLite (Versão 2.4.0 Alpha)

Todas as dependências, exceto a biblioteca TensorFlowLite, podem ser instaladas por meio do gerenciador de bibliotecas da Arduino IDE, bastando pesquisar pelo nome da biblioteca e instalar a versão indicada. A biblioteca TensorFlowLite deve ser instalada manualmente, seguindo os passos abaixo:

1. Baixe a biblioteca [TensorFlowLite (Versão 2.4.0 Alpha)](https://downloads.arduino.cc/libraries/github.com/bcmi-labs/Arduino_TensorFlowLite-2.4.0-ALPHA.zip).
2. Abra a Arduino IDE.
3. Vá em Sketch > Include Library > Add .ZIP Library.
4. Selecione o arquivo baixado e clique em "Abrir".

Feito isso, todas as dependências necessárias estarão instaladas e o projeto poderá ser executado no dispositivo embarcado.

## Dependências Server

As dependências necessárias para a execução do projeto no servidor são:

- Jinja2 (Versão 3.1.3)
- loguru (Versão 0.7.2)
- pyserial (Versão 3.5)
- uvicorn (Versão 0.29.0)
- fastapi (Versão 0.110.0)
- deepface (Versão 0.0.89)
- tf-keras (Versão 2.16.0)
- python-dotenv (Versão 1.0.1)
- opencv-python (Versão 4.9.0.80)

Todas as dependências podem ser instaladas por meio do gerenciador de pacotes do Python, bastando executar o comando abaixo na pasta ``server``:

```bash
    $ pip install -r requirements.txt
```

## Como executar Device

Para executar o projeto no dispositivo embarcado, basta seguir os passos abaixo:

1. Abra o arquivo ``device.ino`` na Arduino IDE.
2. Compile o código e faça o upload para o dispositivo embarcado.

## Como executar Server

Para executar o projeto no servidor, basta seguir os passos abaixo:

1. Abra um terminal na raiz do projeto.
2. Navegue até a pasta ``server``.
3. Instale as dependências necessárias.
4. Copie o arquivo ``.env.example`` e renomeie para ``.env``.
5. Execute o servidor com o comando abaixo:

```bash
    $ python main.py
```

O servidor estará disponível em ``http://localhost:8000``.

## Licença
A licença do projeto é MIT. Para mais informações, acesse o arquivo ``LICENSE``.

## Agradecimentos
Agradecemos ao professor Erick de Andrade Barboza pela orientação e apoio durante o desenvolvimento do projeto.