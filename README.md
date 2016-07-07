Projeto Final TR2 
==================================================
Matheus Rosendo Pedreira(11/0017749)
Cayke Prudente(11/0112491)
Igor Miranda(11/0013255)
---------------------------------


# Índice
1. [Introdução](#introducao)
2. [Classes](#classes)
  2.1 [main](#main)
  2.2 [UIGenerator](#uigenerator)
  2.3 [ServerRequests](#serverrequests)
  2.4 [ClientInterface](#clientInterface)
  2.5 [Define](#define)
  2.6 [masterServer](#masterserver)
  2.7 [dht](#dht)
3. [Limitações](#limitacoes)
  3.1 [Windows](#windows)
  3.2 [Tamanho de arquvo](#tamanho-de-arquivo)
  3.3 [Renomear](#renomear)
4. [Utilizando o programa](#utilizando-o-programa)
  4.1 [Server Master](#server-master)
  4.2 [Cliente](#cliente)
  4.3 [Navegação](#navegacao)


#Introdução  
O objetivo do sistema era realizar o gerenciamento de dados de multiusuários em sistema distribuido em um estilo parecido com o dropbox onde cada usuário pode gerenciar os próprios arquivos na rede e baixar os arquivos de qualquer usuário.
No entanto o sistema possui uma diferença onde o server pode replicar os arquivos dentro dos clientes para gerar cópias de segurança utilizando o algoritmo DHT para gerenciar o balanceamento desses arquivos.

#Classes
##main
Essa classe é responsável por gerenciar o HTML e iniciar a classes de servidor do cliente (ClientInterface) e de requisições com o servidor (ServerRequests). Para gerenciar o HMTL essa classe ainda utiliza métodos da classe UIGenerator para criar HTML dinâmico. 
Para criar o HTML essa classe utiliza os arquivos na pasta (/templates) e se comunica com estes através de métodos http POST e GET e através de urls definidos no init do arquivo.
##UIGenerator
Essa classe é responsável por gerar HTMLs dinâmico caso uma página precise ser gerada de tal forma.
##ServerRequests
Essa classe é responsável por realizar a comunicação com o servidor local do cliente para que este gerencie a comunicação com o master.
##ClientInterface
Essa classe é responsável pela comunicação com o servidor master e disponibilizar o download dos arquivos fora do server master.
##Define
Esse arquivo define os códigos para requisições do servidor e para mensagens de erro gerados pelo servidor. 
##masterServer
Classe responsavel por inicializar o servidor master. Ela recebe todas as requests vinda dos clientes. Para cada cliente é criada uma thread e um socket TCP. Nessa classe tambem é feito o parse da request e entao se encaminha para o metodo da classe DHT responsavel por gerir a request em questao.
##dht
Classe responsavel por todo processamento do servidor master. Ela guarda todas as referencias a usuarios, arquivos, distribuicao de arquivos, redistribuicao de carga. Tambem implementa os metodos responsaveis por toda a parte de adicao,edicao,remocao de arquivos, diretorios e usuarios. Para mais informacoes consulte o pdf do projeto do sistema.

#Limitações
##Windows
O servidor master não pode ser rodado em máquinas windows por problemas de diferença de construção de diretório, no entanto, o cliente roda 100% em qualquer máquina.
##Tamanho de arquivo
Os arquivos utilizados em upload no sistema devem ser arquivos de texto e não podem exceder o tamanho de 2Kb pois o tamanho do socket foi limitado em 2048 bytes.
##Renomear
Um cliente não deve renomear a sua pasta raiz ou a pasta raiz do sistema para que não ocorram conflitos. Isso se deve ao fato da pasta da raiz do cliente ser o identificador deste na rede.

#Utilizando o programa
Para utilizar o sistema é necessário se conectar a uma rede, seja ela localhost ou a um roteador. Após decidida a rede que ocorrerá a conexão é necessário descobrir o IP em que o server master irá rodar.
Após isso selecionar uma porta entre 5000 e 5200.
Para utilizar o sistema utilizar o python 2.7.9 ou superior contanto que este seja da vesão 2 e não da 3.
## Server Master
Para rodar o masterServer é necessário modificar o a variável ```HOST``` para o IP da rede utilizada e a variável ```PORT``` para a porta desejada.
Após isso é só rodar o masterServer.py:
```python runserver.py```
## Cliente
Para rodar o cliente é necessário modificar o a variável ```__IP``` para o IP do servidor master na rede utilizada e a variável ```__PORTSERVER``` para a porta desejada.
Após isso é só rodar o arquivo main.py
```python main.py```

## Navegação
Para utilizar o sistema é só utilizar um navegador e entrar na url ```localhost:8000```. Caso o usuário em algum momento deseje voltar para uma tela anterior é utilizar o botão de voltar do navegador.