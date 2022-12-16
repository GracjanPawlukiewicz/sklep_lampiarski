import re
import json
import pymysql

PRODUCTS_PATH = '/var/www/html/prestashop/products.json'

def group_attr_to_add(products):
    attr = {}

    # Group by attributes to add
    for prod in products:
        attr_name = prod['selector_description']
        if not attr_name:
            continue

        attr_sel = [sel.replace('\t', ' ') for sel in prod['selection']
                    if '--wybierz' not in sel]  

        if attr_name in attr:
            attr[attr_name] = list(set(attr[attr_name] + attr_sel))
        else:
            attr[attr_name] = attr_sel
    
    return attr

def add_attributes(products, cur):
    attr = group_attr_to_add(products)

    # get last position
    cur.execute('SELECT position FROM ps_attribute_group ORDER BY position DESC LIMIT 1;')
    last_pos = int(cur.fetchall()[0][0])

    for idx, (name, sels) in enumerate(attr.items()):
        cur.execute(f"INSERT INTO ps_attribute_group (is_color_group,group_type,position) VALUES (0,'select',{last_pos+idx});")
        grp_id = cur.lastrowid
        cur.execute(f"INSERT INTO ps_attribute_group_lang VALUES ({grp_id},2,'{name}','{name}');")
        cur.execute(f"INSERT INTO ps_attribute_group_shop VALUES ({grp_id},1);")

        for idx, sel in enumerate(sels):
            cur.execute(f"INSERT INTO ps_attribute (id_attribute_group,position) VALUES ({grp_id},{idx});")
            att_id = cur.lastrowid
            cur.execute(f"INSERT INTO ps_attribute_lang VALUES ({att_id},2,'{sel}');")
            cur.execute(f"INSERT INTO ps_attribute_shop VALUES ({att_id},1);")

def assign_attr_to_prod(products, cur):
    for prod in products:
        if not prod['selector_description']:
            continue
        
        name = prod['name']
        try:
            cur.execute(f"SELECT pl.id_product FROM ps_product_lang AS pl JOIN ps_stock_available AS ps ON ps.id_product=pl.id_product WHERE pl.name='{name}' AND ps.quantity!=0;")
            res = cur.fetchall()
            if len(res) == 1:
                prod_id = int(res[0][0])
            else: continue
        except: 
            continue

        print(name, prod_id)

        attr_sel = [sel.replace('\t', ' ') for sel in prod['selection']
                    if '--wybierz' not in sel]
        
        for idx, sel in enumerate(attr_sel):
            print(f'\t{sel}')

            cur.execute(f"SELECT id_attribute FROM ps_attribute_lang WHERE name='{sel}';")
            att_id = int(cur.fetchall()[0][0])

            default_on = '1' if idx == 0 else 'NULL'
            cur.execute(f"INSERT INTO ps_product_attribute (id_product,quantity,default_on) VALUES ({prod_id},1000,{default_on});")
            patt_id = cur.lastrowid
            
            cur.execute(f"INSERT INTO ps_product_attribute_combination VALUES ({att_id},{patt_id});")
            cur.execute(f"INSERT INTO ps_product_attribute_shop (id_product,id_product_attribute,id_shop,default_on) VALUES ({prod_id},{patt_id},1,{default_on});")

            cur.execute(f"INSERT INTO ps_stock_available (id_product,id_product_attribute,id_shop,quantity,out_of_stock) VALUES ({prod_id},{patt_id},1,1000,2);")
        
        cur.execute(f'UPDATE ps_stock_available SET quantity={1000*len(sel)} WHERE id_product={prod_id} AND id_product_attribute=0')


def main():
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = 'biznes',
        db='prestashop',
    )
    cur = conn.cursor()

    with open(PRODUCTS_PATH) as fp:
        products = json.load(fp)

    #add_attributes(products, cur)

    assign_attr_to_prod(products, cur)

    conn.commit()

if __name__ == '__main__':
    main()
