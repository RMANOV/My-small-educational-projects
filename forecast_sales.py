sales = {1: 100, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600}


# create initial forecast for next 12 months
# get actual sales for previous 1 month
# calculate forecast for next 12 months against actual sales

# create initial forecast for next 12 months using moving average of previous 3 months
for i in range(sales.__len__(), sales.__len__() + 12):
    sales[i + 1] = (sales[i - 2] + sales[i - 1] + sales[i]) / 3
# keys should be in following format Nf - where N is month number and f is forecast number - for example forecast = {7: 700, 8: 800, 9: 900, 10: 1000, 11: 1100, 12: 1200, 1: 1300}
# get actual sales for previous 1 month
# correct old forecast for 12 months against actual sales and calculate forecast for next 1 month

while True:
    # get actual sales for next 1 month
    actual_sales = int(input("Enter actual sales for next month " + str(sales.__len__() -11) + ": "))
    sales[sales.__len__() + 1] = actual_sales

    # correct old forecast for 12 months against actual sales and calculate forecast for next 1 month
    # keys should following the order of months in sales{} dictionary - for example sales = {1: 100, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600} - forecast = {7: 700, 8: 800, 9: 900, 10: 1000, 11: 1100, 12: 1200, 1: 1300}
    for i in range(sales.__len__(), 0, -1):
        if i < 4:
            sales[i] = sales[i]
        else:
            sales[i] = (sales[i - 3] + sales[i - 2] + sales[i - 1]) / 3
    
    print(sales)





# while True:
#     # get actual sales for next 1 month
#     actual_sales = int(input("Enter actual sales for next month: "))
#     sales[sales.__len__() + 1] = actual_sales

#     # correct old forecast for 12 months against actual sales and calculate forecast for next 1 month
#     # keys should following the order of months in sales{} dictionary - for example sales = {1: 100, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600} - forecast = {7: 700, 8: 800, 9: 900, 10: 1000, 11: 1100, 12: 1200, 1: 1300}
#     # for i in range(sales.__len__(), 0, -1):
#     #     if i < 4:
#     #         forecast[i] = sales[i]
#     #     else:
#     #         forecast[i] = (sales[i - 3] + sales[i - 2] + sales[i - 1]) / 3
    
#     # print(forecast)
#     for i in range(sales.__len__(), 0, -1):
#         if i < 4:
#             sales_and_forecast[i] = sales[i]
#         else:
#             sales_and_forecast[i] = (sales[i - 3] + sales[i - 2] + sales[i - 1]) / 3
#     print(sales_and_forecast)
