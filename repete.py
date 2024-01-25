# Lista original de IDs
original_ids = [
    2194, 2384, 2184, 2204, 2224, 2234, 2244, 2264, 2284, 2304, 
    2324, 2334, 2354, 2364, 2374, 2394, 2214, 2254, 2314, 2454, 
    2464, 2274, 2344, 2294
]

# Lista de IDs adicionais
additional_ids = [
    2454, 2464, 2384, 2184, 2204, 2224, 2234, 2244, 2264, 2284, 
    2304, 2324, 2334, 2354, 2364, 2374, 2394, 2214, 2254, 2314, 
    2454, 2464, 2274, 2344, 2294
]

# Convertendo as listas para conjuntos
original_set = set(original_ids)
additional_set = set(additional_ids)

# Encontrando a diferença simétrica entre os conjuntos
unique_ids = original_set.symmetric_difference(additional_set)

# Mostrando o ID que não se repete
print("ID que não se repete:", unique_ids.pop())
