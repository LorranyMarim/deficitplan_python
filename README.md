# DeficitPlan - Calorie Deficit Calculator & Weight Loss Planner

Select Language / Selecione o Idioma:
* [Português (Brasil)](#-português-brasil)
* [English](#-english)

---

## 🇧🇷 Português (Brasil)

### 📄 Sobre o Projeto
O **DeficitPlan** é um sistema desktop baseado na arquitetura **MVC (Model-View-Controller)** desenvolvido em Python utilizando a biblioteca gráfica **Tkinter** e estilizado com o tema profissional `aquativo` (`ttkthemes`).

O software foi originalmente concebido como um sistema de uso pessoal em **2022** e passou por uma refatoração completa em **2026**, com o objetivo de limpar o código, implementar validações rigorosas de entrada de dados, adicionar tratamento de *placeholders*, automatizar dicas visuais (*tooltips*) e otimizar o algoritmo de combinação de treinos.

### 🔬 Embasamento Científico
Todos os cálculos matemáticos e parâmetros biológicos adotados no sistema foram extraídos de **artigos e estudos científicos consolidados** e amplamente conhecidos na área da saúde, nutrição e educação física. Isso inclui:
* **Índice de Massa Corporal (IMC):** Classificação oficial baseada nos parâmetros da Organização Mundial da Saúde (OMS).
* **Taxa Metabólica Basal (TMB) e Gasto Energético Diário Total (TDEE):** Fórmulas consolidadas de cálculo metabólico ajustadas pelos fatores de atividade física descritos na literatura médica.
* **Equivalente Metabólico da Tarefa (MET):** Valores de queima calórica baseados no Compêndio de Atividades Físicas mundial.
* **Faixa Segura de Emagrecimento Semanal (0,5 kg a 1,5 kg):** Range estipulado com base em consensos médicos que definem o limite saudável para perda de peso sustentável, evitando riscos à saúde ou perda excessiva de massa magra.

### 🛠️ Funcionalidades Principais
* **Análise Corporal Completa:** Obtém dados de IMC, Categoria de Peso, Taxa Metabólica Basal (TMB) e Gasto Diário Total de Energia (TDEE).
* **Planejamento de Perda de Peso:** Permite definir o peso total a ser perdido e a meta semanal desejada (dentro da faixa segura de 0,5 kg a 1,5 kg).
* **Déficit e Consumo Calórico:** Calcula automaticamente o déficit diário necessário e o consumo calórico alvo seguro (respeitando os limites mínimos de segurança biológica).
* **Perfil de Exercícios Tabular:** Sugere combinações dinâmicas de até 2 exercícios do banco de dados (`data.py`) que melhor atendem à queima calórica necessária por sessão, respeitando a quantidade de dias que o usuário deseja treinar e limitando o tempo total a 90 minutos.
* **Cópia Rápida:** Botão integrado com ícone para copiar o plano de exercícios gerado diretamente para a área de transferência.

### 🎓 Foco Educacional e Comunidade
O foco principal deste projeto é open-source e educacional. O sistema foi estruturado para que **estudantes e iniciantes em Python e Tkinter** possam baixar, usar e aprimorar o código. 

Ele serve como uma excelente base de estudos para:
1. Praticar a escrita de **testes automatizados**.
2. Estudar e aplicar técnicas avançadas de **refatoração de código**.
3. Modificar ou experimentar novas **estruturas arquiteturais** (como evoluir o MVC).
4. Praticar a **portabilidade de plataformas**, servindo de protótipo para transformar este sistema desktop em uma aplicação **Web** ou **Mobile**.

---

### 🚀 Como Instalar e Executar

#### 1. Baixar e Instalar o Python
Caso não possua o Python instalado, baixe a versão estável mais recente (Python 3.10 ou superior) no site oficial: [python.org](https://www.python.org/). Certifique-se de marcar a opção **"Add Python to PATH"** durante a instalação.

#### 2. Instalar as Dependências
Abra o terminal ou o Prompt de Comando (CMD) na pasta raiz do projeto e instale as bibliotecas necessárias executando:
```bash
pip install -r requirements.txt
´´´

#### 3. Executar o Sistema
Para rodar a aplicação, vá até a pasta raiz do projeto, abra o seu Prompt de Comando (CMD) ou terminal e execute o comando:

```bash
python main.py
´´´

### 📄 Licença
Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para mais detalhes. O uso educacional e a refatoração são encorajados, desde que mantida a atribuição de autoria.

## 🇺🇸 English
### 📄 About the Project
**DeficitPlan** is a desktop system based on the MVC (Model-View-Controller) architecture, developed in Python using the Tkinter graphical library and styled with the professional aquativo theme (ttkthemes).

The software was originally conceived as a personal-use system in 2022 and underwent a complete refactoring in 2026 to improve code quality, implement strict input validation, add native placeholder handling, automate visual tooltips, and optimize the training combination algorithm.

### 🔬 Scientific Grounding
All mathematical calculations and biological parameters used in this system are derived from consolidated scientific articles and peer-reviewed studies widely known in the fields of health, nutrition, and sports science. This includes:

Body Mass Index (BMI): Official classification based on World Health Organization (WHO) standards.

Basal Metabolic Rate (BMR) & Total Daily Energy Expenditure (TDEE): Established metabolic formulas adjusted by physical activity multipliers described in medical literature.

Metabolic Equivalent of Task (MET): Caloric burn rates based on the global Compendium of Physical Activities.

Safe Weekly Weight Loss Range (0.5 kg to 1.5 kg): A range established by medical consensus as the safe threshold for sustainable weight loss without health risks or severe lean mass depletion.

### 🛠️ Key Features
Comprehensive Body Analysis: Evaluates BMI, Weight Category, Basal Metabolic Rate (BMR), and Total Daily Energy Expenditure (TDEE).

Weight Loss Planning: Allows defining the total weight to lose and the desired weekly target (within the safe range of 0.5 kg to 1.5 kg).

Deficit & Caloric Intake: Automatically calculates the required daily deficit and the safe target caloric intake.

Tabular Exercise Profile: Suggests dynamic combinations of up to 2 exercises from the database (data.py) that best meet the required session burn, according to the user's chosen training frequency, keeping workouts under a 90-minute limit.

Quick Copy: Integrated button with an icon to copy the generated exercise plan directly to the clipboard.

### 🎓 Educational Focus and Community
The main purpose of this project is open-source and educational. The system has been structured so that students and beginners in Python and Tkinter can download, use, and improve the codebase.

It serves as an excellent sandbox to:

Practice writing automated tests.

Study and apply advanced code refactoring techniques.

Modify or experiment with new architectural structures (e.g., evolving the current MVC).

Practice cross-platform migration, using it as a blueprint to transform this desktop app into a Web or Mobile application.

### 🚀 Installation and Execution
1. Download and Install Python
If you do not have Python installed, download the latest stable version (Python 3.10 or higher) from the official website: python.org. Make sure to check the option "Add Python to PATH" during installation.

2. Install Dependencies
Open your terminal or Command Prompt (CMD) in the project's root folder and install the required packages by running:

Bash
pip install -r requirements.txt

### 3. Run the System
To run the application, navigate to the project's root folder, open your Command Prompt (CMD) or terminal, and execute the following command:

Bash
python main.py

### 📄 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details. Educational use and refactoring are encouraged, provided authorship attribution is maintained.