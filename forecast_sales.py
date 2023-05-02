sales = {1: 100, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600}



def forecast_sales(sales):
    sales_and_forecast = {}
    for i in range(sales.__len__(), 0, -1):
        if i < 4:
            sales_and_forecast[i] = sales[i]
        else:
            sales_and_forecast[i] = round((sales[i - 3] + sales[i - 2] + sales[i - 1]) / 3)
    return sales_and_forecast


def get_actual_sales(sales):
    actual_sales = int(input("Enter actual sales for next month: "))
    sales[sales.__len__() + 1] = actual_sales
    return sales


def main():
    sales = {1: 100, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600}
    while True:
        sales = get_actual_sales(sales)
        sales = forecast_sales(sales)
        print(sales)


if __name__ == "__main__":
    main()
