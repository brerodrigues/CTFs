#!/usr/bin/env python2

from z3 import *
from random import randint

banner = """ +-+-+-+-+-+-+-+-+
 |K|e|y|g|e|n|m|e|
 +-+-+-+-+-+-+-+-+
 |T|a|m|u| |C|T|F|
 +-+-+-+-+-+-+-+-+
   |K|e|y|g|e|n|
   +-+-+-+-+-+-+
   """

def main():
	print banner

	try:
		keygens = int(raw_input("Tell me how many keys do you want: "))
		while (keygens > 0):
			print keygen()
			keygens = keygens - 1
	except ValueError:
		print ("Thanks for the invalid number. I'm only give you one key.")
		print keygen()

def keygen():
    # Pedaco da funcao que encoda input do usuario e compara com chave: [OIonU2_<__nK<Ks
    # unsigned int acumulador = 72;
    # int contador = 0;
    #
    # tamanhoSerial = strlen(serial);
    #
    # while(contador < tamanhoSerial) {
    #     serial[contador] = ((serial[contador] + 12) * acumulador + 17) % 70 + 48;
    #     acumulador = serial[contador];
    #     contador++;
    # }
    #
    # return serial;

    # Acumulador inicial + unicode([OIonU2_<__nK<Ks)
    keys = [72, 91, 79, 73, 111, 110, 85, 50, 95, 60, 95, 95, 110, 75, 60, 75, 115]
    valid_serial = ""

    # varre a lista de keys em busca de valores que satisfacam a expressao de codificacao de serial
    for index, key in enumerate(keys):
        serial = Int('x')

        if index + 1 >= len(keys):
            result = key
        else:
            result = keys[index+1]

		# constrains para gerar valor unicode valido 'digitavel' (> 32 && < 126)
		# constrain com expressao que encoda o input do usuario para comparacao com chave
        constraints = [serial > 32, serial < 126, ((serial + 12) * key + 17) % 70 + 48 == result]
        # pega no maximo 15 solucoes possiveis pq 15 eh legal
        solutions = get_models(constraints, 15)

        # pega uma solucao qualquer
        number_solutions = len(solutions)
        random_solution = randint(0, number_solutions-1)

        # converte valor z3 da solucao para um caracter
        valid_serial = valid_serial + str(unichr(get_int_value_from_model(solutions[random_solution], serial)))

    # apenas sendo preguicoso
    return valid_serial[:-1]

# https://www.cs.tau.ac.il/~msagiv/courses/asv/z3py/guide-examples.htm
# pega todas solucoes possiveis
# basicamente roda o solver, pega a solucao encontrada, adiciona essa solucao como uma nova constraint
# e tenta rodar o solver novamente ate que o solver nao encontre mais nada
# melhor explicado em: https://stackoverflow.com/questions/11867611/z3py-checking-all-solutions-for-equation
def get_models(constraints, quantity):
    result = []
    solver = Solver()
    solver.add(constraints)
    
    while len(result) < quantity and solver.check() == sat:
        model = solver.model()
        result.append(model)
        # Create a new constraint the blocks the current model
        block = []
        
        for declaration in model:
            constant = declaration()
            block.append(constant != model[declaration])
            solver.add(Or(block))
        
    return result

# uma gambiarra que fiz para pegar o valor do model do z3
def get_int_value_from_model(model, z3_value):
    return model.eval(z3_value).as_long()

if __name__ == '__main__':
    main()
