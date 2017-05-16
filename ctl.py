# -*- coding: utf-8 -*-
import sys

#DONE
##########################################################
##########################################################

def simpleImplication(expression):

	for i in range(len(expression)):
		if expression[i] == '->':
			changes = True
			expression[i] = '|'
			expression.insert(i, ')')
			expression.insert(1, '(')
			expression.insert(1, '!')

			break

	return expression

#DONE
##########################################################
##########################################################

def convertAX(expression):

	for i in range(len(expression)):
		if expression[i] == 'AX':
			expression = convertGeneral(expression, 'EX', i)
			break

	return expression

#DONE
##########################################################
##########################################################

def convertEF(expression):

	for i in range(len(expression)):
		if expression[i] == 'EF':
			expression[i] = 'EU'
			expression.insert(i+1, '(')
			expression.insert(len(expression)-1, ')')
			expression.insert(i+2, ',')
			expression.insert(i+2, 'true')

			break

	return expression

#DONE
##########################################################
##########################################################

def convertAG(expression):

	changes = False

	for i in range(len(expression)):
		if expression[i] == 'AG':
			expression = convertGeneral(expression, 'EF', i)
			break

	return convertEF(expression)

#DONE
##########################################################
##########################################################

def convertEG(expression):

	for i in range(len(expression)):
		if expression[i] == 'EG':
			expression = convertGeneral(expression, 'AF', i)
			break

	return expression

##########################################################
##########################################################

def convertGeneral (expression, term, i):

	expression[i] = term
	#changing interior
	expression.insert(i+1, '!')
	expression.insert(i+1, '(')
	expression.insert(len(expression)-1, ')')
	#changing exterior
	expression.insert(0, '!')
	expression.insert(0, '(')
	expression.insert(len(expression)-1, ')')

	return expression


##########################################################
##########################################################

def convertAU(expression):

	changes = False

	begin = 0
	middle = 0
	end = len(expression) - 2

	lElements = []
	rElements = []

	for i in range(len(expression)):
		if expression[i] == 'AU':
			begin = i+2
			changes = True
		if expression[i] == ',':
			middle = i

	if (changes == True):
		lElements = expression[begin:middle]
		rElements = expression[middle+1:end]

		blockEG = ['(', '!', '(', 'EG', '(', '!', '('] + rElements + [')', ')', ')', ')']
		blockEG = convertEG(blockEG)

		blockEU = ['EU', '(', '!', '('] + rElements + [')', ',', '!', '('] + lElements + ['&', '(', '!', '('] + rElements + [')', ')', ')']

		return ['('] + blockEG + ['&', '(', '!', '('] + blockEU + [')', ')', ')', ')']

	else:
		return expression

##########################################################
##########################################################

def callAll(expression):

	#print(expression)
	expression = simpleImplication(expression)
	# print('1')
	# print(''.join(expression))
	expression = convertAX(expression)
	# print('2')	ARRUMAR
	# print(''.join(expression))
	expression = convertEF(expression)
	# print('3')
	# print(''.join(expression))
	expression = convertAG(expression)
	# print('4')
	# print(''.join(expression))
	expression = convertEG(expression)
	# print('5')
	# print(''.join(expression))
	expression = convertAU(expression)
	# print('6')
	# print(''.join(expression))

	return expression

##########################################################
##########################################################

def convertCTL(expression):

	openP = []
	i=0

	while (i < len(expression)):

		if expression[i] == '(':
			openP.append(i)
		
		if expression[i] == ')':
			oldSize = len(expression)
			left = openP[len(openP)-1]
			right = i+1
			del openP[len(openP)-1]
			expression = expression[:left] + callAll(expression[left:right])  + expression[right:]
			newSize = len(expression)    
			i += newSize - oldSize
			#print(''.join(expression))

		i += 1

	return expression


expression = '( EG ( ( EX ( q ) ) & ( EX ( ! ( p ) ) ) ) )'
expression = expression.split()
print('1')
print(''.join(convertCTL(expression)))

expression = '( AF ( EX ( q ) -> ( AX ( q ) ) ) )'
expression = expression.split()
print('2')
print(''.join(convertCTL(expression)))

expression = '( EU ( p , q & ( r ) ) )'
expression = expression.split()
print('3')
print(''.join(convertCTL(expression)))

#ARRUMAR
expression = '( AU ( ! ( p ) , ! ( q ) ) )'
expression = expression.split()
print('4')
print(''.join(convertCTL(expression)))

expression = '( p -> ! ( q ) )'
expression = expression.split()
print('5')
print(''.join(convertCTL(expression)))

expression = '( AU ( ! ( h ) , c ) )'
expression = expression.split()
print('6')
print(''.join(convertCTL(expression)))

expression = '( AG ( s -> ( AF ( h ) ) ) )'
expression = expression.split()
print('7')
print(''.join(convertCTL(expression)))

expression = '( AG ( e -> ( AF ( ! ( e ) ) ) ) )' 
expression = expression.split()
print('8')
print(''.join(convertCTL(expression)))