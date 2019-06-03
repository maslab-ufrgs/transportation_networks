# Transportation networks
This repository features several transportation networks to be used for traffic simulation. 
These networks were created by [maslab-ufrgs](https://github.com/maslab-ufrgs) based on the literature (references are given with networks files), but following a novel and more flexible syntax (defined by our group). 

In this document, we present (only in Portuguese): 
* the specification of the network files, 
* the list of network files available in this repository, and 
* the script files that can be used to manipulate the network files.

## Especificação de arquivos de rede
Um arquivo de rede é definido pelos seguintes elementos:
* function (e piecewise): descreve uma função de custo ou uma função de custo piecewise.
* node: descreve um vértice da rede.
* edge (e dedge): descreve um link não-direcionado (edge) ou direcionado (dedge) e suas propriedades.
* od: descreve um par OD e sua demanda (quantidade de veículos).

Os elementos devem ser declarados nesta mesma ordem, ou seja, primeiro funções, depois vértices, depois links e, por último, pares OD. 
Comentários podem ser feitos com o caractere #. 
A sintaxe de cada elemento é definida a seguir. Vale ressaltar que apenas espaços simples são aceitos para separar os campos de cada elemento.

### Sintaxe do elemento 'function'
A sintaxe de uma função comum é a seguinte:
```
function name (args) formula
```

Onde:
* "name" é o nome da função.
* "args" é a lista de argumentos da função. No caso de múltiplos argumentos, eles devem ser separados por vírgulas, sem espaços. A lista deve ser delimitada por parênteses. 
* "formula" é a fórmula matemática da função. A fórmula pode ser descrita através de números, variáveis e operações matemáticas. Idealmente, os argumentos devem aparecer na fórmula.

A partir da fórmula e argumentos, é definida uma lista de constantes. Toda e qualquer variável da fórmula que não for definida como um argumento será considerada uma constante. Desta forma, junto da definição dos links (ver seção correspondente) é preciso informar os valores das constantes da função definida (obviamente, estes valores variam de um link para o outro). '''Importante!''' A ordem que as constantes são definidas na função é a mesma que deve ser utilizada na definição de seus valores junto dos links.

No caso da função piecewise, a sintaxe sofre algumas modificações:
```
piecewise name (args) piecewise_formula
```

Onde "name" e "args" seguem a mesma especificação que em "function". 
O termo "piecewise_formula" descreve uma série de segmentos separados pelo caractere pipe (|). Um segmento, por sua vez, é uma tupla contendo uma fórmula (seguindo a mesma especificação que em "function") e um intervalo, separados por vírgula. Não há limite no número de intervalos. A única restrição é que o último segmento não deve ter um intervalo definido. Desta forma, a definição de "piecewise_formula" pode ser descrito como:
a definição é a seguinte:
```
formula,intervalo|formula,intervalo|formula
```

Onde:
* "formula" segue a mesma especificação que em "function".
* "intervalo" representa uma expressão lógica (idealmente envolvendo as variáveis da fórmula).

### Sintaxe do elemento 'node'
A sintaxe de um vértice é a seguinte:
```
node name
```

Onde ''name'' descreve o nome do vértice.

### Sintaxe do elemento 'edge'
A sintaxe de um link é a seguinte:
```
edge name origin destination function constants
```

Onde:
* ''name'' descreve o nome do link. O nome de um link deve ser composto pelo nome dos links envolvidos separados por um hífen (-).
* ''origin'' refere-se ao vértice de origem.
* ''destination'' refere-se ao vértice de destino.
* ''function'' corresponde ao nome da função de custo utilizada por este link.
* ''constants'' descreve os valores a serem atribuídos às constantes da função especificada. Os valores devem ser separados por espaços simples e '''não''' devem ser delimitados por parênteses. A ordem que as constantes são definidas na função é a mesma que deve ser utilizada aqui na definição de seus valores. 

A distinção entre os elementos ''edge'' e ''dedge'' é que o primeiro cria um link não-direcionado, ao passo que o segundo cria um link direcionado. Em termos práticos, o ''dedge'' cria dois links: um conforme a definição (origem para destino) e um adicional invertido (destino para origem).

### Sintaxe do elemento 'od'
A sintaxe de um par OD é a seguinte:
```
od name origin destination flow
```

Onde:
* ''name'' descreve o nome do par OD. No caso dos pares OD, o nome deve ser composto pelo nome dos links envolvidos separados pelo caractere pipe (|).
* ''origin'' refere-se ao vértice de origem.
* ''destination'' refere-se ao vértice de destino.
* ''flow'' corresponde ao número de veículos (demanda) utilizando o par OD em questão.

## Redes inclusas

As redes disponíveis neste repositório são as seguintes:
* *Albany*, por [Liu, Abouzeid & Julius (2017). Traffic Flow in Vehicular Communication Networks. In: 2017 American Control Conference (ACC).](http://www.doi.org/10.23919/ACC.2017.7963812) (figure 4)
* *OW*, por [Ortúzar & Willumsen (2011). Modelling transport (4th ed.).](https://books.google.com/books?id=qWa5MyS4CiwC) (example 10.1)
* *Pigou*, por [Pigou (1932). The Economics of Welfare (4th ed.).](http://oll.libertyfund.org/titles/1410)
* *ND* e *ND_bpr1*, por [Nguyen, S., & Dupuis, C. (1984). An efficient method for computing traffic equilibria in networks with asymmetric transportation costs. Transportation Science, 18(2), 185-202.](https://pubsonline.informs.org/doi/abs/10.1287/trsc.18.2.185) e [Yin, Y., Madanat, S. M., & Lu, X. Y. (2009). Robust improvement schemes for road networks under demand uncertainty. European Journal of Operational Research, 198(2), 470-479.](https://www.sciencedirect.com/science/article/pii/S0377221708007558), respectivamente.
* *Braess graphs*, representando expansões do grafo original do Braess paradox, por Stefanello & Bazzan (2016). Traffic Assignment Problem - Extending Braess Paradox. 
  - *Braess_1_4200_10_c1*
  - *Braess_2_4200_10_c1*
  - *Braess_3_4200_10_c1*
  - *Braess_4_4200_10_c1*
  - *Braess_5_4200_10_c1*
  - *Braess_6_4200_10_c1*
  - *Braess_7_4200_10_c1*
  - *Braess_8_4200_10_c1*
  - *BBraess_1_2100_10_c1_2100*
  - *BBraess_3_2100_10_c1_900*
  - *BBraess_5_2100_10_c1_900*
  - *BBraess_7_2100_10_c1_900*
* Bar-Gera TNTP: instâncias selecionadas do repositório do [Bar-Gera](https://github.com/bstabler/TransportationNetworks).
  - *Anaheim*
  - *Berlin-Friedrichshain*
  - *Berlin-Mitte-Center*
  - *Berlin-Mitte-Prenzlauerberg-Friedrichshain-Center*
  - *Berlin-Prenzlauerberg-Center*
  - *Berlin-Tiergarten*
  - *SiouxFalls*

## Scripts inclusos

Além das redes e da especificação em si, este repositório também disponibliza os seguintes scripts:
* convert_bargera.py: converte um arquivo de rede no formato do [Bar-Gera](https://github.com/bstabler/TransportationNetworks) para o formato do presente repositório. 
* python_example.py: fornece um exemplo de como manipular os arquivos de rede, ou seja, de como criar um grafo a partir do arquivo e como utilizá-lo.
* validator.py: verifica erros em um arquivo de rede.
