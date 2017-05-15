# EX EU AF
from ctl.models.tree import TreeNode
from tabulate import tabulate

# test cases
expressions = {
    # "1": "(((a)&(b))&(c))",
    # "2": "((a)&((b)&(c)))",
    # "3": "((EU((e),(q)))&(c))",
    "4": "(AF((e)))",
    "5": "(AF(((e)&(b))))",
    # "6": "(a)",
    "7": "(!(EU((true),(!((!(e))|(AF((!(e)))))))))",
    "8": "(EU((true),(!((!(e))|(AF((!(e))))))))"
}

def parseExpression(expression):

    # print("parsing {0}".format(expression))
    # this stack store indices of opening and closing parenthesis of a subexpression
    if expression == None:
        return None

    rightExpression = None
    leftExpression = None
    operator = None
    prop = None

    count = 1
    left = 2
    it = 2

    if not (expression[1] == '('):
        if (expression[1]) == '!':
            operator = '!'
            it = 1
            leftExpression = expression[2:-1]
        # Cuidao com o length!!!!!!
        elif expression[1:4].upper() in ["AF(","EX("]:
            operator = expression[1:3]
            it = 1
            leftExpression = expression[4:-2]
            
        elif expression[1:4].upper() in ["EU("]:
            operator = expression[1:3]
            it = 1
            newExpression = expression[4:-2]
            leftExpression, rightExpression = newExpression.split(',')
            # print(newExpression, leftExpression, rightExpression)
        else:
            # nao tem operator!
            prop = expression[1:len(expression) - 1]
    else:
        while count != 0:
            if expression[it] == '(':
                count = count + 1
            elif expression[it] == ')':
                count = count - 1
            it = it + 1

        rightExpression = expression[it + 1:-1]
        leftExpression = expression[1:it]
        operator = expression[it]
        print(operator, leftExpression, rightExpression, prop)

    root = TreeNode(expression, 0, operator=operator, prop=prop)
    root.left = parseExpression(leftExpression)
    root.right = parseExpression(rightExpression)

    return root

def dfs(root):
    if root == None:
        return

    dfs(root.left)
    print(root, end="\n\n")
    dfs(root.right)

def main():
    for key in sorted(expressions):

        result = parseExpression(expressions[key])
        dfs(result)
        print("---------------------------", end="\n\n")


if __name__ == '__main__':
    main()