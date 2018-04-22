# Network description syntax
This is the syntax description for the network files which are used by MASLAB-UFRGS.

Here we also have some examples of the most commonly used networks.

To read these network files, we already have an example code on how to read it [here](https://github.com/maslab-ufrgs/ksp/blob/master/KSP.py#L93).

## Especificação
Um arquivo de rede é definido pelos seguintes elementos:
* function (e piecewise): descreve uma função de custo ou uma função de custo piecewise.
* node: descreve um vértice da rede.
* edge (e dedge): descreve um link não-direcionado (edge) ou direcionado (dedge) e suas propriedades.
* od: descreve um par OD e sua demanda (quantidade de veículos).

Os elementos devem ser declarados nesta mesma ordem, ou seja, primeiro funções, depois vértices, depois links e, por último, pares OD. 
Comentários podem ser feitos com o caractere #. 
A sintaxe de cada elemento é definida a seguir. Vale ressaltar que apenas espaços simples são aceitos para separar os campos de cada elemento.

## Síntaxe function
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

## Síntaxe node
A sintaxe de um vértice é a seguinte:
```
node name
```

Onde ''name'' descreve o nome do vértice.

## Síntaxe edge
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

## Sintaxe od
A sintaxe de um par OD é a seguinte:
```
od name origin destination flow
```

Onde:
* ''name'' descreve o nome do par OD. No caso dos pares OD, o nome deve ser composto pelo nome dos links envolvidos separados pelo caractere pipe (|).
* ''origin'' refere-se ao vértice de origem.
* ''destination'' refere-se ao vértice de destino.
* ''flow'' corresponde ao número de veículos (demanda) utilizando o par OD em questão.
