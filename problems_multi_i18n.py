"""French and Spanish text for the multi-language problem bank.

Kept out of problems_multi.py so the problem definitions stay readable and a
new language is one dict away. English and German live next to the problems
themselves; anything missing here falls back to English.

Each entry: {problem id: {lang: {title, statement, hints, notes}}}
"""

EXTRA: dict[str, dict[str, dict]] = {

# ===========================================================================
"m_sum_range": {
 "fr": {
  "title": "Sommer une liste",
  "statement": """Renvoyez la somme de tous les nombres de la liste. Une liste vide donne 0.

  sum_range([1, 2, 3]) -> 6
  sum_range([])        -> 0

Cet exercice existe pour vous familiariser avec l'éditeur et l'exécution des
tests dans un nouveau langage avant d'attaquer les vrais problèmes.""",
  "hints": ["Partez d'un accumulateur à 0 et ajoutez chaque élément",
            "La plupart des langages ont une fonction intégrée — essayez les deux"]},
 "es": {
  "title": "Sumar una lista",
  "statement": """Devuelve la suma de todos los números de la lista. Una lista vacía suma 0.

  sum_range([1, 2, 3]) -> 6
  sum_range([])        -> 0

Este ejercicio está para que te acostumbres al editor y a la ejecución de
pruebas en un lenguaje nuevo antes de empezar con los problemas de verdad.""",
  "hints": ["Empieza con un acumulador en 0 y suma cada elemento",
            "La mayoría de lenguajes lo trae de serie — prueba las dos formas"]},
},

"m_contains_duplicate": {
 "fr": {
  "title": "Contient des doublons",
  "statement": """Renvoyez true si une valeur apparaît au moins deux fois, false si toutes sont
distinctes.

  contains_duplicate([1, 2, 3, 1]) -> true
  contains_duplicate([1, 2, 3, 4]) -> false

Les tests cachés contiennent un grand tableau : une double boucle sur toutes
les paires sera trop lente. Utilisez un ensemble (ou triez d'abord).""",
  "hints": ["L'appartenance à un ensemble de hachage est en O(1), à une liste en O(n)",
            "Renvoyez dès que vous voyez une valeur pour la deuxième fois",
            "Comparer la taille de l'ensemble à la longueur marche aussi"],
  "notes": "LeetCode 217. La première question où la réponse naïve dépasse le temps."},
 "es": {
  "title": "Contiene duplicados",
  "statement": """Devuelve true si algún valor aparece al menos dos veces, false si todos son
distintos.

  contains_duplicate([1, 2, 3, 1]) -> true
  contains_duplicate([1, 2, 3, 4]) -> false

Las pruebas ocultas incluyen un arreglo grande, así que un bucle anidado sobre
todos los pares será demasiado lento. Usa un conjunto (o ordena primero).""",
  "hints": ["Pertenecer a un conjunto hash es O(1); a una lista, O(n)",
            "Devuelve en cuanto veas un valor por segunda vez",
            "Comparar el tamaño del conjunto con la longitud también sirve"],
  "notes": "LeetCode 217. La primera pregunta donde la respuesta ingenua se pasa de tiempo."},
},

"m_max_subarray": {
 "fr": {
  "title": "Somme maximale d'un sous-tableau (Kadane)",
  "statement": """Renvoyez la plus grande somme d'une suite contiguë et non vide de nombres.

  max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) -> 6      (la suite 4, -1, 2, 1)
  max_subarray([-1])                            -> -1

Attention : le tableau peut être entièrement négatif, donc initialiser le
meilleur résultat à 0 est faux. C'est l'algorithme de Kadane : un seul
passage, O(n).""",
  "hints": ["À chaque élément, décidez : prolonger la suite ou repartir d'ici",
            "courant = max(valeur, courant + valeur)",
            "Initialisez best ET courant avec le premier élément, pas avec 0"],
  "notes": "LeetCode 53 et le MaxSliceSum de Codility. Deux lignes à connaître par cœur."},
 "es": {
  "title": "Suma máxima de subarreglo (Kadane)",
  "statement": """Devuelve la mayor suma de una secuencia contigua y no vacía de números.

  max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) -> 6      (la secuencia 4, -1, 2, 1)
  max_subarray([-1])                            -> -1

Cuidado: el arreglo puede ser todo negativo, así que empezar el mejor valor en
0 es incorrecto. Este es el algoritmo de Kadane: una sola pasada, O(n).""",
  "hints": ["En cada elemento decide: extender la secuencia o empezar de nuevo aquí",
            "actual = max(valor, actual + valor)",
            "Inicializa best Y actual con el primer elemento, no con 0"],
  "notes": "LeetCode 53 y el MaxSliceSum de Codility. Dos líneas que hay que saber de memoria."},
},

"m_two_sum": {
 "fr": {
  "title": "Deux sommes",
  "statement": """Renvoyez les indices des deux nombres dont la somme vaut target, sous forme
de liste [i, j] avec i < j. Il existe exactement une solution et vous ne
pouvez pas réutiliser le même élément.

  two_sum([2, 7, 11, 15], 9) -> [0, 1]
  two_sum([3, 3], 6)         -> [0, 1]

La double boucle imbriquée est en O(n²). Faites-le en un passage avec une
table valeur -> indice : c'est la réponse attendue en entretien.""",
  "hints": ["Stockez valeur -> indice au fur et à mesure",
            "Pour chaque valeur, demandez si target - valeur a déjà été vue",
            "Insérez APRÈS la recherche, sinon un élément se marie avec lui-même"],
  "notes": "LeetCode 1 — la question d'entretien la plus posée qui soit."},
 "es": {
  "title": "Dos sumandos",
  "statement": """Devuelve los índices de los dos números que suman target, como una lista
[i, j] con i < j. Existe exactamente una solución y no puedes usar el mismo
elemento dos veces.

  two_sum([2, 7, 11, 15], 9) -> [0, 1]
  two_sum([3, 3], 6)         -> [0, 1]

El doble bucle anidado es O(n²). Hazlo en una pasada con un mapa de valor a
índice: esa es la respuesta que se espera en la entrevista.""",
  "hints": ["Guarda valor -> índice mientras recorres",
            "Para cada valor pregunta si target - valor ya se vio",
            "Inserta DESPUÉS de consultar, o un elemento se emparejará consigo mismo"],
  "notes": "LeetCode 1 — la pregunta de entrevista más frecuente que existe."},
},

"m_valid_palindrome": {
 "fr": {
  "title": "Palindrome valide",
  "statement": """En ignorant la casse et tout caractère qui n'est ni une lettre ni un chiffre,
le texte se lit-il pareil dans les deux sens ?

  is_palindrome("A man, a plan, a canal: Panama") -> true
  is_palindrome("race a car")                     -> false
  is_palindrome(" ")                              -> true

La chaîne vide compte comme un palindrome.""",
  "hints": ["Soit vous nettoyez la chaîne, soit vous avancez deux pointeurs vers "
            "l'intérieur en sautant le reste",
            "Comparez les caractères en minuscules",
            "La version à deux pointeurs ne demande aucune mémoire supplémentaire"],
  "notes": "LeetCode 125."},
 "es": {
  "title": "Palíndromo válido",
  "statement": """Ignorando mayúsculas y todo carácter que no sea letra ni dígito, ¿el texto se
lee igual en ambos sentidos?

  is_palindrome("A man, a plan, a canal: Panama") -> true
  is_palindrome("race a car")                     -> false
  is_palindrome(" ")                              -> true

La cadena vacía cuenta como palíndromo.""",
  "hints": ["O limpias la cadena primero, o avanzas dos punteros hacia dentro "
            "saltando lo demás",
            "Compara los caracteres en minúscula",
            "La versión con dos punteros no necesita memoria extra"],
  "notes": "LeetCode 125."},
},

"m_fizzbuzz": {
 "fr": {
  "title": "FizzBuzz",
  "statement": """Renvoyez une liste de chaînes pour les nombres de 1 à n :

  * multiples de 3 et de 5 -> "FizzBuzz"
  * multiples de 3         -> "Fizz"
  * multiples de 5         -> "Buzz"
  * tout le reste          -> le nombre lui-même, en texte

  fizzbuzz(5) -> ["1", "2", "Fizz", "4", "Buzz"]
  fizzbuzz(0) -> []

Testez le cas 15 en premier, sinon il ne peut jamais se produire.""",
  "hints": ["i % 15 == 0 couvre les deux conditions d'un coup",
            "Chaque entrée est une chaîne, y compris les nombres",
            "n = 0 doit donner une liste vide, pas une erreur"]},
 "es": {
  "title": "FizzBuzz",
  "statement": """Devuelve una lista de cadenas para los números del 1 al n:

  * múltiplos de 3 y de 5 -> "FizzBuzz"
  * múltiplos de 3        -> "Fizz"
  * múltiplos de 5        -> "Buzz"
  * todo lo demás         -> el número mismo, como texto

  fizzbuzz(5) -> ["1", "2", "Fizz", "4", "Buzz"]
  fizzbuzz(0) -> []

Comprueba el caso del 15 primero, o nunca podrá ocurrir.""",
  "hints": ["i % 15 == 0 cubre ambas condiciones de una vez",
            "Cada entrada es una cadena, también los números",
            "n = 0 debe dar una lista vacía, no un error"]},
},

"m_binary_search": {
 "fr": {
  "title": "Recherche binaire",
  "statement": """`nums` est trié par ordre croissant. Renvoyez l'indice de target, ou -1 s'il
n'y est pas. Doit s'exécuter en O(log n).

  binary_search([-1, 0, 3, 5, 9, 12], 9) -> 4
  binary_search([-1, 0, 3, 5, 9, 12], 2) -> -1
  binary_search([], 1)                   -> -1

Réécrivez-la de mémoire jusqu'à ce que les erreurs d'un cran disparaissent.""",
  "hints": ["low, high = 0, len - 1 et boucle tant que low <= high",
            "mid = low + (high - low) / 2 évite le dépassement dans les langages "
            "à entiers bornés",
            "Allez vers mid + 1 ou mid - 1, jamais vers mid, sinon vous bouclez sans fin"],
  "notes": "LeetCode 704."},
 "es": {
  "title": "Búsqueda binaria",
  "statement": """`nums` está ordenado de forma ascendente. Devuelve el índice de target, o -1 si
no está. Debe ejecutarse en O(log n).

  binary_search([-1, 0, 3, 5, 9, 12], 9) -> 4
  binary_search([-1, 0, 3, 5, 9, 12], 2) -> -1
  binary_search([], 1)                   -> -1

Escríbela de memoria hasta que dejen de aparecer los errores por uno.""",
  "hints": ["low, high = 0, len - 1 y bucle mientras low <= high",
            "mid = low + (high - low) / 2 evita el desbordamiento en lenguajes "
            "con enteros acotados",
            "Muévete a mid + 1 o mid - 1, nunca a mid, o el bucle no termina"],
  "notes": "LeetCode 704."},
},

"m_reverse_words": {
 "fr": {
  "title": "Inverser les mots",
  "statement": """Inversez l'ORDRE des mots d'une phrase. Les mots sont séparés par des espaces ;
réduisez toute suite d'espaces à un seul et supprimez ceux des extrémités.

  reverse_words("the sky  is blue") -> "blue is sky the"
  reverse_words("  hello world  ")   -> "world hello"
  reverse_words("")                  -> ""

Chaque mot reste tel quel — seul leur ordre change.""",
  "hints": ["Découper sur les espaces élimine déjà les morceaux vides",
            "Inversez la liste de mots, puis rassemblez avec un seul espace",
            "Attention aux espaces de début et de fin"]},
 "es": {
  "title": "Invertir las palabras",
  "statement": """Invierte el ORDEN de las palabras de una frase. Las palabras se separan por
espacios; reduce cualquier serie de espacios a uno y recorta los extremos.

  reverse_words("the sky  is blue") -> "blue is sky the"
  reverse_words("  hello world  ")   -> "world hello"
  reverse_words("")                  -> ""

Cada palabra se queda igual — solo cambia su orden.""",
  "hints": ["Dividir por espacios ya descarta los trozos vacíos",
            "Invierte la lista de palabras y únelas con un solo espacio",
            "Cuidado con los espacios al principio y al final"]},
},

"m_move_zeroes": {
 "fr": {
  "title": "Déplacer les zéros",
  "statement": """Déplacez chaque 0 à la fin de la liste en conservant l'ordre des valeurs non
nulles. Renvoyez la liste obtenue.

  move_zeroes([0, 1, 0, 3, 12]) -> [1, 3, 12, 0, 0]
  move_zeroes([0])              -> [0]
  move_zeroes([])               -> []""",
  "hints": ["Récupérez les valeurs non nulles dans l'ordre",
            "Complétez le reste du résultat avec des zéros",
            "Dans les langages à tableaux fixes, un pointeur d'écriture fait les deux"],
  "notes": "LeetCode 283."},
 "es": {
  "title": "Mover los ceros",
  "statement": """Mueve cada 0 al final de la lista conservando el orden de los valores distintos
de cero. Devuelve la lista resultante.

  move_zeroes([0, 1, 0, 3, 12]) -> [1, 3, 12, 0, 0]
  move_zeroes([0])              -> [0]
  move_zeroes([])               -> []""",
  "hints": ["Recoge los valores distintos de cero en orden",
            "Rellena el resto del resultado con ceros",
            "En lenguajes con arreglos fijos, un puntero de escritura hace ambas cosas"],
  "notes": "LeetCode 283."},
},

"m_max_profit": {
 "fr": {
  "title": "Meilleur moment pour acheter et vendre",
  "statement": """prices[i] est le cours d'une action au jour i. Achetez un jour et vendez un
jour PLUS TARD. Renvoyez le plus grand profit possible, ou 0 si aucune
transaction n'est rentable.

  max_profit([7, 1, 5, 3, 6, 4]) -> 5      (acheter à 1, vendre à 6)
  max_profit([7, 6, 4, 3, 1])    -> 0
  max_profit([])                 -> 0

Un seul passage : retenez le cours le plus bas rencontré jusqu'ici.""",
  "hints": ["Suivez le prix minimum vu jusqu'à présent",
            "Chaque jour, la meilleure vente vaut prix - minimum",
            "Ne laissez jamais le profit descendre sous 0"],
  "notes": "LeetCode 121 et le MaxProfit de Codility."},
 "es": {
  "title": "Mejor momento para comprar y vender",
  "statement": """prices[i] es la cotización de una acción el día i. Compra un día y vende un día
POSTERIOR. Devuelve el mayor beneficio posible, o 0 si ninguna operación gana
dinero.

  max_profit([7, 1, 5, 3, 6, 4]) -> 5      (comprar a 1, vender a 6)
  max_profit([7, 6, 4, 3, 1])    -> 0
  max_profit([])                 -> 0

Una sola pasada: recuerda el precio más bajo visto hasta ahora.""",
  "hints": ["Lleva el precio mínimo visto hasta el momento",
            "Cada día, la mejor venta vale precio - mínimo",
            "Nunca dejes que el beneficio baje de 0"],
  "notes": "LeetCode 121 y el MaxProfit de Codility."},
},

"m_row_sums": {
 "fr": {
  "title": "Sommes des lignes",
  "statement": """L'entrée est une grille — une liste de lignes, chaque ligne étant une liste de
nombres. Renvoyez la somme de chaque ligne.

  row_sums([[1, 2], [3, 4], [5, 6]]) -> [3, 7, 11]
  row_sums([])                       -> []

C'est l'échauffement de tout problème en deux dimensions : se familiariser avec
l'indexation imbriquée dans un nouveau langage.""",
  "hints": ["Parcourez les lignes, puis les valeurs à l'intérieur",
            "Le résultat a une entrée par ligne",
            "Une grille vide donne un résultat vide"]},
 "es": {
  "title": "Sumas de filas",
  "statement": """La entrada es una cuadrícula — una lista de filas, cada fila una lista de
números. Devuelve la suma de cada fila.

  row_sums([[1, 2], [3, 4], [5, 6]]) -> [3, 7, 11]
  row_sums([])                       -> []

Este es el calentamiento de todo problema bidimensional: acostumbrarse a los
índices anidados en un lenguaje nuevo.""",
  "hints": ["Recorre las filas y dentro de ellas los valores",
            "El resultado tiene una entrada por fila",
            "Una cuadrícula vacía da un resultado vacío"]},
},

"m_count_vowels": {
 "fr": {
  "title": "Compter les voyelles",
  "statement": """Comptez combien de voyelles (a, e, i, o, u) le texte contient. Majuscules et
minuscules comptent toutes les deux ; tout le reste est ignoré.

  count_vowels("Hello World") -> 3
  count_vowels("xyz")         -> 0
  count_vowels("")            -> 0""",
  "hints": ["Mettez le caractère en minuscule avant de le tester",
            "Tester l'appartenance à la chaîne \"aeiou\" est le test le plus court"]},
 "es": {
  "title": "Contar las vocales",
  "statement": """Cuenta cuántas vocales (a, e, i, o, u) contiene el texto. Mayúsculas y
minúsculas cuentan igual; todo lo demás se ignora.

  count_vowels("Hello World") -> 3
  count_vowels("xyz")         -> 0
  count_vowels("")            -> 0""",
  "hints": ["Pasa el carácter a minúscula antes de comprobarlo",
            "Comprobar si está en la cadena \"aeiou\" es la prueba más corta"]},
},

"m_reverse_list": {
 "fr": {
  "title": "Inverser une liste",
  "statement": """Renvoyez la liste dans l'ordre inverse, sous forme de nouvelle liste.

  reverse_list([1, 2, 3]) -> [3, 2, 1]
  reverse_list([])        -> []

La plupart des langages le font nativement, mais écrivez la boucle avec indices
au moins une fois — parcourir depuis les deux extrémités est un motif que vous
réutiliserez sans cesse.""",
  "hints": ["Parcourez l'entrée à l'envers, ou écrivez la sortie à l'envers",
            "out[i] = nums[len - 1 - i]"]},
 "es": {
  "title": "Invertir una lista",
  "statement": """Devuelve la lista en orden inverso, como una lista nueva.

  reverse_list([1, 2, 3]) -> [3, 2, 1]
  reverse_list([])        -> []

Casi todos los lenguajes lo traen de serie, pero escribe el bucle con índices
al menos una vez — recorrer desde ambos extremos es un patrón que reutilizarás
constantemente.""",
  "hints": ["Recorre la entrada al revés, o escribe la salida al revés",
            "out[i] = nums[len - 1 - i]"]},
},

"m_single_number": {
 "fr": {
  "title": "Le nombre solitaire",
  "statement": """Chaque valeur de la liste apparaît exactement deux fois, sauf une qui apparaît
une seule fois. Trouvez-la.

  single_number([4, 1, 2, 1, 2]) -> 4
  single_number([7])             -> 7

Un ensemble le résout avec O(n) de mémoire. La réponse attendue utilise O(1) :
faites le XOR de toutes les valeurs. x ^ x vaut 0 et x ^ 0 vaut x, donc toutes
les paires s'annulent quel que soit leur ordre d'arrivée.""",
  "hints": ["L'opérateur XOR s'écrit ^ dans tous les langages ici",
            "Partez de 0 et repliez toute la liste dedans",
            "L'ordre n'a pas d'importance — le XOR est commutatif"],
  "notes": "LeetCode 136 et l'OddOccurrencesInArray de Codility."},
 "es": {
  "title": "El número solitario",
  "statement": """Cada valor de la lista aparece exactamente dos veces, salvo uno que aparece una
sola vez. Encuéntralo.

  single_number([4, 1, 2, 1, 2]) -> 4
  single_number([7])             -> 7

Un conjunto lo resuelve con O(n) de memoria. La respuesta esperada usa O(1):
haz XOR de todos los valores. x ^ x es 0 y x ^ 0 es x, así que todas las
parejas se cancelan sin importar el orden.""",
  "hints": ["El operador XOR se escribe ^ en todos estos lenguajes",
            "Empieza en 0 y pliega la lista entera dentro",
            "El orden da igual — XOR es conmutativo"],
  "notes": "LeetCode 136 y el OddOccurrencesInArray de Codility."},
},

"m_majority_element": {
 "fr": {
  "title": "Élément majoritaire",
  "statement": """Une valeur apparaît dans PLUS de la moitié des cases. Renvoyez-la. La liste
n'est jamais vide et une telle valeur existe toujours.

  majority_element([3, 2, 3])             -> 3
  majority_element([2, 2, 1, 1, 1, 2, 2]) -> 2

Compter dans une table coûte O(n) de mémoire. Le vote de Boyer-Moore le fait en
O(1) : gardez un candidat et un compteur, +1 quand la valeur correspond, -1
sinon, et adoptez un nouveau candidat dès que le compteur tombe à zéro.""",
  "hints": ["Énoncez d'abord la version qui compte en O(n) de mémoire, puis améliorez",
            "Gardez un candidat et un compteur de voix",
            "Réinitialisez le candidat dès que le compteur atteint zéro"],
  "notes": "LeetCode 169 et le Dominator de Codility."},
 "es": {
  "title": "Elemento mayoritario",
  "statement": """Un valor aparece en MÁS de la mitad de las posiciones. Devuélvelo. La lista
nunca está vacía y ese valor siempre existe.

  majority_element([3, 2, 3])             -> 3
  majority_element([2, 2, 1, 1, 1, 2, 2]) -> 2

Contar en un mapa cuesta O(n) de memoria. El voto de Boyer-Moore lo hace en
O(1): mantén un candidato y un contador, +1 cuando el valor coincide, -1 cuando
no, y adopta un nuevo candidato en cuanto el contador llegue a cero.""",
  "hints": ["Di primero la versión que cuenta con O(n) de memoria y luego mejórala",
            "Mantén un candidato y un contador de votos",
            "Reinicia el candidato en cuanto el contador llegue a cero"],
  "notes": "LeetCode 169 y el Dominator de Codility."},
},

"m_gcd": {
 "fr": {
  "title": "Plus grand commun diviseur",
  "statement": """Renvoyez le PGCD de deux entiers positifs ou nuls.

  gcd(84, 36) -> 12
  gcd(7, 13)  -> 1
  gcd(5, 0)   -> 5

Utilisez l'algorithme d'Euclide : remplacez (a, b) par (b, a % b) jusqu'à ce
que b soit nul, et ce qui reste dans a est la réponse. Ne bouclez pas depuis 1 —
les entrées montent jusqu'au milliard.""",
  "hints": ["tant que b != 0 : (a, b) devient (b, a % b)",
            "À la fin de la boucle, a contient la réponse",
            "pgcd(x, 0) vaut x, ce que la boucle gère déjà"],
  "notes": "Le cœur du ChocolatesByNumbers de Codility, entre autres."},
 "es": {
  "title": "Máximo común divisor",
  "statement": """Devuelve el MCD de dos enteros no negativos.

  gcd(84, 36) -> 12
  gcd(7, 13)  -> 1
  gcd(5, 0)   -> 5

Usa el algoritmo de Euclides: sustituye (a, b) por (b, a % b) hasta que b sea
cero, y lo que quede en a es la respuesta. No hagas un bucle desde 1 — las
entradas llegan a los mil millones.""",
  "hints": ["mientras b != 0: (a, b) pasa a ser (b, a % b)",
            "Al acabar el bucle, a contiene la respuesta",
            "mcd(x, 0) es x, y el bucle ya lo resuelve"],
  "notes": "El núcleo del ChocolatesByNumbers de Codility, entre otros."},
},

"m_is_anagram": {
 "fr": {
  "title": "Anagramme valide",
  "statement": """Renvoyez true si les deux chaînes utilisent exactement les mêmes lettres, le
même nombre de fois.

  is_anagram("anagram", "nagaram") -> true
  is_anagram("rat", "car")         -> false
  is_anagram("", "")               -> true

Des longueurs différentes donnent false immédiatement. Trier les deux est en
O(n log n) et tout à fait acceptable ; compter les caractères est en O(n) et
donc mieux.""",
  "hints": ["Comparez d'abord les longueurs et sortez tôt",
            "Trier les deux et comparer, c'est la version en deux lignes",
            "Compter en montant pour l'une et en descendant pour l'autre donne le O(n)"],
  "notes": "LeetCode 242."},
 "es": {
  "title": "Anagrama válido",
  "statement": """Devuelve true si ambas cadenas usan exactamente las mismas letras, el mismo
número de veces.

  is_anagram("anagram", "nagaram") -> true
  is_anagram("rat", "car")         -> false
  is_anagram("", "")               -> true

Longitudes distintas dan false de inmediato. Ordenar ambas es O(n log n) y es
perfectamente aceptable; contar caracteres es O(n) y mejor.""",
  "hints": ["Compara primero las longitudes y sal pronto",
            "Ordenar ambas y comparar es la versión de dos líneas",
            "Contar hacia arriba en una y hacia abajo en la otra da el O(n)"],
  "notes": "LeetCode 242."},
},

"m_merge_sorted": {
 "fr": {
  "title": "Fusionner deux listes triées",
  "statement": """Les deux listes sont déjà triées par ordre croissant. Fusionnez-les en une
seule liste triée.

  merge_sorted([1, 2, 4], [1, 3, 4]) -> [1, 1, 2, 3, 4, 4]
  merge_sorted([], [0])              -> [0]
  merge_sorted([], [])               -> []

Concaténer puis trier fonctionne, mais gaspille le fait qu'elles sont déjà
triées. Faites la vraie fusion avec deux indices — O(n + m), et c'est l'étape
au cœur du tri fusion.""",
  "hints": ["Un indice par liste, tous deux à 0",
            "Prenez la plus petite tête à chaque tour et n'avancez que cet indice",
            "Quand une liste est épuisée, ajoutez tout le reste de l'autre"],
  "notes": "LeetCode 21."},
 "es": {
  "title": "Fusionar dos listas ordenadas",
  "statement": """Ambas listas ya están ordenadas de forma ascendente. Fusiónalas en una sola
lista ordenada.

  merge_sorted([1, 2, 4], [1, 3, 4]) -> [1, 1, 2, 3, 4, 4]
  merge_sorted([], [0])              -> [0]
  merge_sorted([], [])               -> []

Concatenar y ordenar funciona, pero desaprovecha que ya están ordenadas. Haz la
fusión de verdad con dos índices — O(n + m), y es el paso que está en el
corazón del ordenamiento por mezcla.""",
  "hints": ["Un índice por lista, ambos empezando en 0",
            "Toma la cabeza menor en cada ronda y avanza solo ese índice",
            "Cuando una lista se agote, añade todo el resto de la otra"],
  "notes": "LeetCode 21."},
},

"m_climb_stairs": {
 "fr": {
  "title": "Monter les marches",
  "statement": """Vous montez un escalier de n marches en faisant des pas de 1 ou 2 marches.
Combien de façons distinctes y a-t-il d'arriver en haut ?

  climb_stairs(2)  -> 2      (1+1, 2)
  climb_stairs(3)  -> 3      (1+1+1, 1+2, 2+1)
  climb_stairs(0)  -> 1      (une façon : ne rien faire)

n va jusqu'à 45, donc la récursion naïve est beaucoup trop lente. Remarquez que
façons(n) = façons(n-1) + façons(n-2) — c'est Fibonacci déguisé. Deux variables
qui roulent suffisent, pas besoin de tableau.""",
  "hints": ["façons(n) = façons(n-1) + façons(n-2) — vous veniez d'une ou deux "
            "marches plus bas",
            "Itérez vers le haut avec deux variables qui roulent",
            "n = 0 et n = 1 ont chacun exactement une façon"],
  "notes": "LeetCode 70 — la porte d'entrée de toute question de programmation dynamique."},
 "es": {
  "title": "Subir escaleras",
  "statement": """Subes una escalera de n escalones dando pasos de 1 o 2 escalones. ¿Cuántas
formas distintas hay de llegar arriba?

  climb_stairs(2)  -> 2      (1+1, 2)
  climb_stairs(3)  -> 3      (1+1+1, 1+2, 2+1)
  climb_stairs(0)  -> 1      (una forma: no hacer nada)

n llega hasta 45, así que la recursión simple es demasiado lenta. Fíjate en que
formas(n) = formas(n-1) + formas(n-2) — esto es Fibonacci disfrazado. Bastan dos
variables rodantes, no hace falta un arreglo.""",
  "hints": ["formas(n) = formas(n-1) + formas(n-2) — llegaste desde uno o dos "
            "escalones más abajo",
            "Itera hacia arriba con dos variables rodantes",
            "n = 0 y n = 1 tienen exactamente una forma cada uno"],
  "notes": "LeetCode 70 — la puerta de entrada a toda pregunta de programación dinámica."},
},

"m_longest_common_prefix": {
 "fr": {
  "title": "Plus long préfixe commun",
  "statement": """Renvoyez la plus longue chaîne par laquelle commencent tous les mots de la
liste. Renvoyez une chaîne vide s'il n'y en a pas, ou si la liste est vide.

  longest_common_prefix(["flower", "flow", "flight"]) -> "fl"
  longest_common_prefix(["dog", "racecar", "car"])    -> ""
  longest_common_prefix([])                           -> ""

La réponse ne peut jamais être plus longue que le mot le plus court, ce qui
borne toute la recherche.""",
  "hints": ["Prenez le premier mot comme préfixe candidat",
            "Raccourcissez-le contre chaque autre mot jusqu'à ce que tous soient d'accord",
            "Une liste vide et un mot vide donnent tous deux une réponse vide"],
  "notes": "LeetCode 14."},
 "es": {
  "title": "Prefijo común más largo",
  "statement": """Devuelve la cadena más larga con la que empiezan todas las palabras de la
lista. Devuelve una cadena vacía si no hay ninguna, o si la lista está vacía.

  longest_common_prefix(["flower", "flow", "flight"]) -> "fl"
  longest_common_prefix(["dog", "racecar", "car"])    -> ""
  longest_common_prefix([])                           -> ""

La respuesta nunca puede ser más larga que la palabra más corta, y eso acota
toda la búsqueda.""",
  "hints": ["Toma la primera palabra como prefijo candidato",
            "Recórtalo contra cada palabra restante hasta que todas coincidan",
            "Una lista vacía y una palabra vacía dan las dos una respuesta vacía"],
  "notes": "LeetCode 14."},
},

"m_rotate_array": {
 "fr": {
  "title": "Faire tourner un tableau",
  "statement": """Faites tourner la liste de k pas vers la DROITE et renvoyez le résultat.

  rotate_array([1, 2, 3, 4, 5, 6, 7], 3) -> [5, 6, 7, 1, 2, 3, 4]
  rotate_array([], 3)                    -> []

k peut dépasser la longueur de la liste. Prenez d'abord k modulo la longueur —
et méfiez-vous de la liste vide, car ce modulo diviserait par zéro.""",
  "hints": ["k %= longueur supprime les tours complets inutiles",
            "La valeur d'indice i se retrouve à l'indice (i + k) % longueur",
            "Traitez la liste vide avant le modulo"],
  "notes": "LeetCode 189 et la CyclicRotation de Codility."},
 "es": {
  "title": "Rotar un arreglo",
  "statement": """Rota la lista k pasos a la DERECHA y devuelve el resultado.

  rotate_array([1, 2, 3, 4, 5, 6, 7], 3) -> [5, 6, 7, 1, 2, 3, 4]
  rotate_array([], 3)                    -> []

k puede ser mayor que la lista. Toma primero k módulo la longitud — y ojo con
la lista vacía, porque ese módulo dividiría por cero.""",
  "hints": ["k %= longitud elimina las vueltas completas sobrantes",
            "El valor del índice i acaba en el índice (i + k) % longitud",
            "Trata la lista vacía antes del módulo"],
  "notes": "LeetCode 189 y la CyclicRotation de Codility."},
},

"m_longest_run": {
 "fr": {
  "title": "Plus longue suite de valeurs égales",
  "statement": """Renvoyez la longueur de la plus longue suite de valeurs IDENTIQUES consécutives.

  longest_run([1, 1, 2, 2, 2, 3]) -> 3
  longest_run([1, 2, 3])          -> 1
  longest_run([])                 -> 0

Un seul passage, un seul compteur, aucune boucle imbriquée.""",
  "hints": ["Suivez la suite en cours et la meilleure suite",
            "Si la valeur égale la précédente, prolongez ; sinon repartez à 1",
            "Mettez le meilleur à jour à chaque étape"]},
 "es": {
  "title": "Racha más larga de valores iguales",
  "statement": """Devuelve la longitud de la racha más larga de valores IDÉNTICOS consecutivos.

  longest_run([1, 1, 2, 2, 2, 3]) -> 3
  longest_run([1, 2, 3])          -> 1
  longest_run([])                 -> 0

Una sola pasada, un solo contador, sin bucles anidados.""",
  "hints": ["Lleva la racha actual y la mejor racha",
            "Si el valor es igual al anterior, extiende; si no, vuelve a 1",
            "Actualiza el mejor en cada paso"]},
},

"m_equilibrium_index": {
 "fr": {
  "title": "Indice d'équilibre",
  "statement": """Un indice d'équilibre est une position où tout ce qui est à GAUCHE a la même
somme que tout ce qui est à DROITE. L'élément lui-même ne compte pour aucun
des deux côtés.

Renvoyez le PLUS PETIT de ces indices, ou -1 s'il n'y en a aucun.

  equilibrium_index([-1, 3, -4, 5, 1, -6, 2, 1]) -> 1
  equilibrium_index([1, 2, 3])                   -> -1
  equilibrium_index([])                          -> -1

Doit être en O(n) : calculez le total une fois, gardez une somme de gauche
courante et déduisez la droite comme total - gauche - courant.""",
  "hints": ["total = somme(nums), calculé une seule fois avant la boucle",
            "À l'indice i, le côté droit vaut total - gauche - nums[i]",
            "Comparez d'abord, puis ajoutez nums[i] à gauche — dans cet ordre"],
  "notes": "Le TapeEquilibrium de Codility sous un autre déguisement."},
 "es": {
  "title": "Índice de equilibrio",
  "statement": """Un índice de equilibrio es una posición donde todo lo que queda a la IZQUIERDA
suma lo mismo que todo lo que queda a la DERECHA. El elemento en sí no cuenta
para ninguno de los dos lados.

Devuelve el MENOR de esos índices, o -1 si no hay ninguno.

  equilibrium_index([-1, 3, -4, 5, 1, -6, 2, 1]) -> 1
  equilibrium_index([1, 2, 3])                   -> -1
  equilibrium_index([])                          -> -1

Debe ser O(n): calcula el total una vez, lleva una suma izquierda acumulada y
deduce la derecha como total - izquierda - actual.""",
  "hints": ["total = suma(nums), calculado una sola vez antes del bucle",
            "En el índice i, el lado derecho es total - izquierda - nums[i]",
            "Compara primero y luego suma nums[i] a la izquierda — en ese orden"],
  "notes": "El TapeEquilibrium de Codility con otro disfraz."},
},

"m_binary_gap": {
 "fr": {
  "title": "Écart binaire",
  "statement": """Un écart binaire est une suite de ZÉROS consécutifs entourée d'un un des DEUX
côtés dans l'écriture binaire de n.

  binary_gap(9)    -> 2      9 s'écrit 1001
  binary_gap(529)  -> 4      529 s'écrit 1000010001, écarts de 4 et 3
  binary_gap(20)   -> 1      20 s'écrit 10100 — le zéro final ne compte pas
  binary_gap(15)   -> 0      1111 n'a aucun écart
  binary_gap(32)   -> 0      100000 — jamais refermé par un autre un

Renvoyez la longueur du plus grand écart, ou 0 s'il n'y en a pas. Le piège, ce
sont les zéros de la fin : ils ne sont pas entourés, donc ils ne comptent pas.""",
  "hints": ["Parcourez les bits avec n & 1 et n >>= 1",
            "Ne commencez à compter les zéros qu'APRÈS avoir vu votre premier un",
            "Une suite ne compte que si un autre un la referme"],
  "notes": "Codility leçon 1 — le premier exercice que la plupart y rencontrent."},
 "es": {
  "title": "Hueco binario",
  "statement": """Un hueco binario es una serie de CEROS consecutivos rodeada por un uno a AMBOS
lados en la representación binaria de n.

  binary_gap(9)    -> 2      9 es 1001
  binary_gap(529)  -> 4      529 es 1000010001, huecos de 4 y 3
  binary_gap(20)   -> 1      20 es 10100 — el cero final no cuenta
  binary_gap(15)   -> 0      1111 no tiene hueco
  binary_gap(32)   -> 0      100000 — nunca lo cierra otro uno

Devuelve la longitud del hueco más largo, o 0 si no hay ninguno. La trampa son
los ceros del final: no están rodeados, así que no cuentan.""",
  "hints": ["Recorre los bits con n & 1 y n >>= 1",
            "Empieza a contar ceros solo DESPUÉS de ver tu primer uno",
            "Una serie solo cuenta si otro uno la cierra"],
  "notes": "Codility lección 1 — el primer ejercicio con el que se topa casi todo el mundo."},
},

"m_passing_cars": {
 "fr": {
  "title": "Voitures qui se croisent",
  "statement": """La liste ne contient que des 0 et des 1 : 0 est une voiture qui roule vers
l'EST, 1 une voiture qui roule vers l'OUEST. Un couple (P, Q) se croise quand
P < Q, a[P] vaut 0 et a[Q] vaut 1.

Renvoyez le nombre de couples de ce type.

  passing_cars([0, 1, 0, 1, 1]) -> 5
  passing_cars([1, 1, 1])       -> 0
  passing_cars([])              -> 0

Compter chaque couple est en O(n²). Faites plutôt un seul balayage : gardez le
compte des 0 déjà vus, et chaque 1 rencontré s'apparie d'un coup avec tous.""",
  "hints": ["Balayez de gauche à droite en comptant les 0 déjà passés",
            "Chaque 1 s'apparie d'un seul coup avec tous ces 0",
            "Ce motif « combien de l'autre sorte sont passés avant » mérite d'être retenu"],
  "notes": "Codility leçon 5."},
 "es": {
  "title": "Coches que se cruzan",
  "statement": """La lista solo contiene 0 y 1: 0 es un coche que va hacia el ESTE, 1 uno que va
hacia el OESTE. Una pareja (P, Q) se cruza cuando P < Q, a[P] es 0 y a[Q] es 1.

Devuelve cuántas parejas de ese tipo hay.

  passing_cars([0, 1, 0, 1, 1]) -> 5
  passing_cars([1, 1, 1])       -> 0
  passing_cars([])              -> 0

Contar cada pareja es O(n²). Haz una sola pasada: lleva la cuenta de los 0 ya
vistos, y cada 1 que aparezca se empareja de golpe con todos ellos.""",
  "hints": ["Recorre de izquierda a derecha contando los 0 que ya pasaron",
            "Cada 1 se empareja de una vez con todos esos 0",
            "Este patrón de «cuántos del otro tipo vinieron antes» vale la pena recordarlo"],
  "notes": "Codility lección 5."},
},

"m_min_subarray_len": {
 "fr": {
  "title": "Plus court sous-tableau de somme donnée",
  "statement": """Renvoyez la longueur du PLUS COURT sous-tableau contigu dont la somme vaut au
moins target. Renvoyez 0 s'il n'en existe pas. Toutes les valeurs sont
positives.

  min_subarray_len(7, [2, 3, 1, 2, 4, 3]) -> 2      ([4, 3])
  min_subarray_len(11, [1, 1, 1])         -> 0
  min_subarray_len(4, [1, 4, 4])          -> 1

Agrandissez une fenêtre vers la droite tant que la somme est trop petite, puis
rétrécissez-la par la gauche tant qu'elle reste valide. Chaque indice entre et
sort une seule fois : malgré la boucle interne, l'ensemble est en O(n).""",
  "hints": ["Agrandissez avec l'indice droit, rétrécissez avec le gauche",
            "Notez la longueur tant que la fenêtre est valide, avant de rétrécir",
            "best reste à 0 si la fenêtre n'est jamais assez grande"],
  "notes": "LeetCode 209 — le modèle de la fenêtre glissante à taille variable."},
 "es": {
  "title": "Subarreglo más corto con suma mínima",
  "statement": """Devuelve la longitud del subarreglo contiguo MÁS CORTO cuya suma sea al menos
target. Devuelve 0 si no existe ninguno. Todos los valores son positivos.

  min_subarray_len(7, [2, 3, 1, 2, 4, 3]) -> 2      ([4, 3])
  min_subarray_len(11, [1, 1, 1])         -> 0
  min_subarray_len(4, [1, 4, 4])          -> 1

Haz crecer una ventana hacia la derecha mientras la suma sea pequeña, y luego
redúcela por la izquierda mientras siga siendo válida. Cada índice entra y sale
una vez: pese al bucle interior, todo es O(n).""",
  "hints": ["Crece con el índice derecho, reduce con el izquierdo",
            "Anota la longitud mientras la ventana es válida, antes de reducir",
            "best se queda en 0 si la ventana nunca llega a ser suficiente"],
  "notes": "LeetCode 209 — la plantilla de la ventana deslizante de tamaño variable."},
},

"m_count_primes": {
 "fr": {
  "title": "Compter les nombres premiers",
  "statement": """Comptez combien de nombres premiers sont strictement INFÉRIEURS à n.

  count_primes(10)  -> 4      (2, 3, 5, 7)
  count_primes(2)   -> 0
  count_primes(0)   -> 0

Tester chaque nombre séparément est trop lent. Utilisez le crible
d'Ératosthène : marquez chaque multiple d'un premier comme composé, et ne
commencez à barrer qu'à p*p, car tout ce qui est en dessous l'est déjà.""",
  "hints": ["Allouez un tableau de booléens de taille n et barrez les composés",
            "Commencez à barrer à p*p, pas à 2*p",
            "Tout ce qui est encore non marqué quand vous l'atteignez est premier"],
  "notes": "LeetCode 204. Le crible mérite d'être su par cœur."},
 "es": {
  "title": "Contar números primos",
  "statement": """Cuenta cuántos números primos son estrictamente MENORES que n.

  count_primes(10)  -> 4      (2, 3, 5, 7)
  count_primes(2)   -> 0
  count_primes(0)   -> 0

Comprobar cada número por separado es demasiado lento. Usa la criba de
Eratóstenes: marca cada múltiplo de un primo como compuesto, y empieza a tachar
solo en p*p, porque todo lo de debajo ya está tachado.""",
  "hints": ["Reserva un arreglo de booleanos de tamaño n y tacha los compuestos",
            "Empieza a tachar en p*p, no en 2*p",
            "Todo lo que siga sin marcar cuando llegues a él es primo"],
  "notes": "LeetCode 204. La criba vale la pena sabérsela de memoria."},
},

"m_transpose": {
 "fr": {
  "title": "Transposer une matrice",
  "statement": """Renvoyez la grille transposée : les lignes deviennent des colonnes et les
colonnes des lignes.

  transpose([[1, 2, 3], [4, 5, 6]]) -> [[1, 4], [2, 5], [3, 6]]
  transpose([[1]])                  -> [[1]]
  transpose([])                     -> []

L'entrée est rectangulaire. Le résultat a une ligne par colonne d'entrée :
attention aux dimensions, une grille r par c devient c par r.""",
  "hints": ["out[c][r] = grid[r][c] — cette seule ligne est toute l'opération",
            "Allouez d'abord le résultat avec les dimensions échangées",
            "Une grille vide donne un résultat vide, avant de toucher à grid[0]"],
  "notes": "LeetCode 867."},
 "es": {
  "title": "Transponer una matriz",
  "statement": """Devuelve la cuadrícula transpuesta: las filas pasan a ser columnas y las
columnas, filas.

  transpose([[1, 2, 3], [4, 5, 6]]) -> [[1, 4], [2, 5], [3, 6]]
  transpose([[1]])                  -> [[1]]
  transpose([])                     -> []

La entrada es rectangular. El resultado tiene una fila por cada columna de
entrada: cuidado con las dimensiones, una cuadrícula r por c pasa a ser c por r.""",
  "hints": ["out[c][r] = grid[r][c] — esa única línea es toda la operación",
            "Reserva primero el resultado con las dimensiones intercambiadas",
            "Una cuadrícula vacía da un resultado vacío, antes de tocar grid[0]"],
  "notes": "LeetCode 867."},
},
}
