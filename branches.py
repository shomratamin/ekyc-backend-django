import csv
from bank.models import *


bank = Bank.objects.filter(is_default=True)
bank = bank.first()
total_match = 0
__all = Branch.objects.all()
for a in __all:
    a.visible_in_form = False
    print(a.name)
    a.save()

with open('branches.csv',mode='r', encoding='utf-8') as csvfile:
    branch_list = csv.reader(csvfile)

    for branch in branch_list:
        branch_model = Branch.objects.filter(bank=bank, code=branch[2])
        if branch_model.count() < 1:
            branch_model = Branch(bank=bank)
        else:
            branch_model = branch_model.first()
            total_match = total_match + 1
        branch_model.name = branch[1]
        branch_model.branch_index = int(branch[0])
        branch_model.code = branch[2]
        branch_model.visible_in_form = True
        branch_model.save()
        print(branch_model.name, branch_model.code)
        print('total_match', total_match)