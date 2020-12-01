import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='ecommerce',
                                         user='root',
                                         password='')

    stop=False
    while stop==False:
        product_id = input("Product ID: ")
        product_name = input("Product Name: ")
        product_price = input("Product Price: ")
        # product_Digital = input("Is Digital?(True/False): ") 
        product_Digital = False 
        

        #F:\Downloads\VS CODE\python\ProductImages
        
        final_image = "F:\Downloads\VS CODE\python\ecommerce\Product_Database_Images".replace("\\",r'/')

        mySql_insert_query = f"""INSERT INTO store_product (id, name, price, digital, image) 
                            VALUES 
                            ({product_id},'{product_name}', {product_price}, {product_Digital}, '{final_image}') """

        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        connection.commit()

        print(cursor.rowcount, "Record inserted successfully into Products table")
        cursor.close()


        add_another_product = input("Add another product? Y/N: ")
        if add_another_product == "Y" or "y":
            stop=False



except mysql.connector.Error as error:
    print("Failed to insert record into Products table {}".format(error))

finally:
    if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")
                                          