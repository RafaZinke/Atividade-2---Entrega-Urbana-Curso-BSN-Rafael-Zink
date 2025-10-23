Desenvolvido por: Rafael Zink
O que faz?
Esse programa calcula quanto custa fazer uma entrega na cidade. Ele considera:

A zona de destino (zona1, zona2, zona3 ou zona4)
O peso do pacote
O volume do pacote
Se precisa entrega rápida (janela crítica)

 Como rodar:

clone com o comando git clone https://github.com/RafaZinke/Atividade-2---Entrega-Urbana-Curso-BSN-Rafael-Zink.git

Tenha o Python instalado (versão 3.7+)
Baixe o arquivo entrega_urbana.py
Abra o terminal/prompt na pasta do arquivo
Digite: python main.py
Responda as perguntas que aparecerem

Ou tenha uma IDE que possa executar o arquivo main.py

Pronto! O programa vai calcular e mostrar o custo total.
 Exemplo de uso
Você digita:
Zona de destino: zona2
Peso do pacote (kg): 15
Volume do pacote (m³): 0.8
Janela de entrega crítica? (s/n): s
O programa mostra:
Custo Base (Zona):        R$      25.00
Pedágio:                  R$       5.50
Sobretaxa Peso:           R$      12.50  (5kg a mais × R$2,50)
Sobretaxa Volume:         R$       0.90  (0,3m³ a mais × R$3,00)
Custo Janela Crítica:     R$      15.00
─────────────────────────────────────────
TOTAL:                    R$      58.90
 Programação Funcional usada
1. Funções Puras
Todas as funções sempre retornam o mesmo resultado para a mesma entrada. 

2. Imutabilidade
Nunca modificamos os dados originais, sempre criamos novos:

3. Map, Filter e Reduce
Map - Aplica função em cada item da lista
Filter - Filtra só o que interessa
Reduce - Junta tudo em um valor só

Regras de Preço

Preço base: varia de R$15 a R$50 conforme a zona
Pedágio: de R$0 a R$12 conforme a zona
Peso extra: R$2,50 por kg acima de 10kg
Volume extra: R$3,00 por m³ acima de 0,5m³
Janela crítica: +R$15,00

 Validações
O programa verifica se:

Os números são positivos
A zona existe
A soma dos custos bate com o total (invariante)

Se algo estiver errado, mostra uma mensagem explicando o erro.