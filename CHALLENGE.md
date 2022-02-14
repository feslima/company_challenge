Olá, obrigado pelo interesse em fazer parte da nossa equipe.

Nós encorajamos você a exagerar na solução para mostrar do que você é capaz.

Considere um cenário em que você precisa cadastrar sua empresa para uma plataforma SaaS.

Você PODE e DEVE usar bibliotecas de terceiros, usando o framework DJANGO. Lembre-se, um desenvolvedor eficaz sabe o que construir e o que reutilizar.

Na entrevista de "code review", esteja preparado para responder algumas
perguntas sobre essas bibliotecas, como e por que você as escolheu e com quais outras alternativas você está familiarizado, serão algumas dessas perguntas.

Como este é um processo de "code review", evite adicionar código gerado ao
projeto (ex: venv).

**Obs:** Para realizar esse teste crie um repositório público mas **não utilize ou mencione** o nome da Empresa, porque esse desafio é compartilhado apenas com pessoas que estamos entrevistando e gostaríamos que permanecesse assim.

## **Instruções para o fluxo da aplicação:**

## **Endpoints**

1. **Cadastro de Usuário** → Endpoint para cadastro de novos acessos (primeiro nome, sobrenome, email e senha)
2. **Cadastro de Empresa** → Endpoint para cadastro de Empresas (usuário, CNPJ, Razão Social e Nome Fantasia). Esse endpoint deve vincular um usuário com uma empresa. Um usuário pode estar em multiplas empresas.
3. **Login do usuário** → Endpoint para Login (o login precisa ser feito através do e-mail do usuário).
4. **Cadastro de membros na empresa** → Endpoint para cadastrar novos membros na empresa (ID usuário e ID empresa)
5. **Listagem de todas as empresas do usuário logado** → Endpoint para trazer todas as empresas pertencentes ao usuário **ESPECÍFICO**.
6. **Listagem de membros de uma empresa** → Endpoint para trazer todos os membros de uma empresa **ESPECÍFICA**.

### Serviços:

No nosso sistema, todas as empresas possuem dados da receita federal, portanto, devemos sempre atualiza-los mensalmente.

Após 30 dias da criação de uma empresa, deve-se acessar `https://receitaws.com.br/v1/cnpj/{CNPJ}` e atualizar algumas informações, sendo:

- Razão Social
- Nome Fantasia
- Status / Situação

Lembrando que: nosso sistema atualiza as informações **MENSALMENTE** e o dia da atualização varia de empresa para empresa.

Essa atualização deverá ser executada em workers assíncronos baseados em eventos e/ou filas para não bloquear a `thread` principal.

**OBS:** A api utilizada é pública, portanto, possui limite de requisições. Será usada apenas para fins de testes.

<aside>
💡 Um dos principais objetivos deste projeto é ver como você preenche ambiguidades de maneira criativa. Não existe um projeto perfeito aqui, apenas interpretações das instruções acima; portanto, seja criativo em sua abordagem.

</aside>

### Requisitos mínimos para o teste:

- Código testável e demonstrar isso escrevendo testes (testes unitários)
- O banco de dados escolhido deve ser relacional (Postgres, MySQL, SQLite e etc)
- API seguindo os padrões REST

Você NÃO precisa desenvolver um "frontend" (telas) para esse teste

### Pontos que consideramos um bônus

- Utilizar uma arquitetura de cache
- Suas respostas durante o code review
- Utilização de criptografia
- Uma boa descrição do que foi feito na sua "pull request"
- Melhores práticas para segurança de APIs e dados
- Utilizar docker
- Histórico do seus commits, com mensagens descritivas do que está
sendo desenvolvido
- Um bom README

### Enviando o teste para avaliação

- Faça os commits diretamente na master
- Faça o push para um repositório publico no github
- Compartilhe o link do repositório conosco