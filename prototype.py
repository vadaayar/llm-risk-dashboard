from load_data import load_supplier_data, load_delay_data

suppliers = load_supplier_data()
delays = load_delay_data()
print(suppliers.head())

