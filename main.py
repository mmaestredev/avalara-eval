import calculator
from calculator import sales_tax

client = calculator.init()

sales_tax.get_sales_tax(client=client)