# ctl-model-checking

## Trabalho 1 - Implementação de CTL model checking

### Especificação
Implementar uma ferramenta de verificação de modelos (i.e. model checking) usando lógica de árvore de computação (Computational Tree Logic - CTL).

A ferramenta deve ser capaz de verificar propriedades expressadas com os seguintes operadores CTL:
### Operadores básicos
* Negação !
* Operador AND &
* Operator OU |
* Implicação ->
* Se e somente se <->

### Operadores CTL
* AX
* EX
* AF
* EF
* AG
* EG
* AU
* EU

### Funcionalidades Adicionais
* Carregar máquinas de estados expressadas seguindo o formato KISS em arquivo texto puro, tal como descrito abaixo.
1. Primeira linha tem um valor totLinhas do tipo inteiro não nulo descrevendo o total de estados da máquina de estados
2. As próximas totLinhas linhas consecutivas terão os seguintes elementos separados por espaço
2.1. Identificador único do estado (tipo inteiro)
2.2. Total totProps de propriedades (tipo inteiro)
2.3. Sequência de totProps strings representando os rótulos das propriedades dados como identificadores válidos, separadas por espaço
2.4. Total de próximos totProxEstad estados (tipo inteiro)
2.5. Sequência de totProxEstad identificadores válidos dos próximos estados, separados por espaço
3. Na última linha deverá constar a propriedade CTL a ser verificada.
3.1. Verificar expressões com qualquer combinação válida de operadores;
3.2. Considerar expressões contendo parênteses;
3.3. Notificar propriedades mal-formadas;

#### A ferramenta também deve notificar máquinas de estados mal-formadas (e.g. rótulo de próximos estados inválidos)