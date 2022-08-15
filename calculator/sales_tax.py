from datetime import datetime
import json
from xml.etree.ElementInclude import include
from . import init as getClientConection
from avalara.transaction_builder import TransactionBuilder

tax_document = { 
    'addresses': {'SingleLocation': None}, #required
    'commit': False,
    'companyCode': 'DEFAULT', 
    'customerCode': None, #required
    'email': None,
    'date': f"{datetime.utcnow().date()}", #requried
    'description': 'Test transaction', 
    'lines': None, #required
    # 'purchaseOrderNo': f"TEST-{datetime.now()}", 
    'type': 'SalesInvoice', # requried for the transaction to show up in Avalara
    'include': "SummaryOnly"
}


def get_sales_tax(client = None):

    try:
        #if client is None: client = getClientConection()
        wo = json.load(open("ir_workorder.json"))
        lines = []
        
        # map customer
        customerName =  wo["order"]["customer"]["firstName"]
        customerName += " " + wo["order"]["customer"]["lastName"]
        tax_document["customerCode"] = customerName

        customerEmail =  wo["order"]["customer"]["email"]
        tax_document["email"] = customerEmail

        # map wo line items
        for item in wo["order"]["lineItems"]:
             lines.append({"amount": item["price"], "quantity": item["quantity"], "description": item["description"]})

        tax_document["lines"] = lines

        # map wo shippingAddress
        shippingAddress = {
            'city': wo["order"]["shippingAddress"]["city"], 
            'country':  'US',
            'line1':wo["order"]["shippingAddress"]["address1"],
            'postalCode':wo["order"]["shippingAddress"]["zip"],
            'region':wo["order"]["shippingAddress"]["state"]
        }
        
        tax_document["addresses"]["SingleLocation"] = shippingAddress

        response = client.create_transaction(model=tax_document, include="SummaryOnly")
        response = response.json()
        

        print("Total Amount:", response["totalAmount"])
        print("Total Tax", response["totalTax"])
        print("Total Taxable:", response["totalTaxable"])
        print("Summary:", response["summary"])
        totalTaxRate = 0
        for tax in response["summary"]:
            totalTaxRate += tax["rate"]
        # add total rate to WO data(taxRate)
        print("Total Tax Rate:", totalTaxRate)
        # complete the workflow as usual 

    except Exception as e:
        print(e)

    #avatax.create_transaction(tax_document)

