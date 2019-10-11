# Projeto 1 MegaDados
### Gabriel Monteiro e Rafael Vieira

## Dicionário de dados - ENTREGA 1

### Tabelas:

#### Usuários:
 - Id INT, AUTO INCREMENT (PK) - É um valor inteiro que identifica cada usuário
 - Nome VARCHAR(50) - Nome do usuário
 - Email VARCHAR(80) - Endereço de email do usuário
 - Cidade VARCHAR(50) - Endereço físico do usuário

#### Posts:
 - Id INT, AUTO INCREMENT (PK) - É um valor inteiro que identifica cada post
 - User Id INT (FK) - É o id do usuário que fez o post
 - Título VARCHAR(50), NOT NULL - Título do post, que não pode ser vazio
 - Texto VARCHAR(300) - Texto do post, com no máximo 300 charactéres
 - Imagem VARCHAR(100) - Endereço url de uma imagem associada ao post
 - Ativo BOOLEAN - Indica se o post está ativo ou não

#### Pássaros:
 - Espécie VARCHAR(50) (PK) - É o nome da espécie de pássaro que identifica ela

#### Preferência:
 - User Id INT (PK, FK) - É um valor inteiro que identifica a preferência do usuário por seu pássaro favorito
 - Pássaro Id INT (PK, FK) - É um valor inteiro que identifica o pássaro preferido do usuário em questão

#### Menciona Pássaros:
 - Post Id INT (PK, FK) - É um valor inteiro que identifica o post que possui uma marcação de algum pássaro 
 - Pássaro Id INT (PK, FK) - É um valor inteiro que identifica o pássaro que foi mencionado no post em questão
 - Ativo BOOLEAN - Indica se o post em questão está ativo ou não

#### Menciona Usuário:
 - Post Id INT (PK, FK) - É um valor inteiro que identifica o post que possui um shout de algum usuário
 - User Id INT (PK, FK) - É um valor inteiro que identifica o usuário que foi mencionado no post em questão
 - Ativo BOOLEAN - Indica se o post em questão está ativo ou não
 
#### Views:
 - User Id INT (PK, FK) - É um valor inteiro que identifica o usuário que visualizou o post em questão
 - Post Id INT (PK, FK) - É um valor inteiro que identifica o post que foi visualizado
 - Aparelho VARCHAR(20) - Indica em qual aparelho o post foi visualizado
 - Browser VARCHAR(20) - Indica em qual browser o post foi acessado
 - IP VARCHAR(50) - Indica qual o IP que visualizou o post
 - Horário DATETIME - Indica o horário de visualização do post


