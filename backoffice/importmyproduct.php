<?php
set_time_limit(30000);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
    // Check if _PS_ADMIN_DIR_ is defined
    if (!defined('_PS_ADMIN_DIR_')) {
        // if _PS_ADMIN_DIR_ is not defined, define.
        define('_PS_ADMIN_DIR_', getcwd());
    }
    // Setup connection with config.inc.php (required for database connection, ...)
    include(_PS_ADMIN_DIR_.'/../config/config.inc.php');
    $secure_key = 'ed3fa1ce558e1c2528cfbaa3f99403';

    // Check if the client use the correct secure_key, url to use: www.yourstore.com/yourbackoffice/importmyproduct.php?secure_key=ed3fa1ce558e1c2528cfbaa3f99403
    if(!Tools::getValue('secure_key') || Tools::getValue('secure_key') != $secure_key) {
        // If the secure_key is not set our not equal the php page will stop running.
        die('UNAUTHORIZED: We dont want you on this page!');
    }
    echo 'Welcome, the secure_key you have used is correct. Now we can start adding product programmatically ... <br>';
   
    function addProduct($ean13, $ref, $name, $qty, $text, $features, $price, $imgUrl, $category_id) {
        $product = new Product();              // Create new product in prestashop
        // $product->ean13 = $ean13;

        if (!empty($ref)){
            // $product->reference = $ref;
            $product->meta_description = htmlspecialchars($ref);
            $product->meta_title = htmlspecialchars($ref);
            $product->description_short = htmlspecialchars($ref);
        }
        $product->name = createMultiLangField($name);
        $product->description = htmlspecialchars($text);
        $product->description_short = htmlspecialchars($ref);
        $product->id_category_default = $category_id;
        $product->redirect_type = '301';

        if ($price > 0){
            $product->price = number_format(fdiv($price, 1.23), 6, '.', '');
            $product->show_price = 1;

        }

        else {
            var_dump($price);
            $product->price = '0.0' ;
            $product->show_price = 0;
            $qty = 0;
        }
        var_dump($price);

        $product->id_tax_rules_group = 1;
        $product->minimal_quantity = 1;
        $product->on_sale = 0;
        $product->online_only = 0;
        $product->link_rewrite = createMultiLangField(Tools::str2url($name)); 
        try {
            $product->add();                // Submit new product
        }            
                    
        catch (Exception $e) {
            echo 'Caught exception: ',  $e->getMessage(), "\n";
        }
        StockAvailable::setQuantity($product->id, null, $qty); // id_product, id_product_attribute, quantity
        $product->addToCategories(array($category_id));     // After product is submitted insert all categories
        // Insert "feature name" and "feature value"
        if (is_array($features)) {
            $array_kv = array();
            $keys = array_keys($features);

            for($i=0;$i<count($features);$i++)
            {
                $temp =  array("name" => $keys[$i], "value" => $features[$keys[$i]]);
                array_push($array_kv,$temp);
            }

            foreach ($array_kv as $feature) {
                $attributeName = $feature['name'];
                $attributeValue = $feature['value'];

                // 1. Check if 'feature name' exist already in database
                $FeatureNameId = Db::getInstance()->getValue('SELECT id_feature FROM ' . _DB_PREFIX_ . 'feature_lang WHERE name = "' . pSQL($attributeName) . '"');
                // If 'feature name' does not exist, insert new.
                if (empty($FeatureNameId)) {
                    Db::getInstance()->execute('INSERT INTO `' . _DB_PREFIX_ . 'feature` (`id_feature`,`position`) VALUES (0, 0)');
                    $FeatureNameId = Db::getInstance()->Insert_ID(); // Get id of "feature name" for insert in product
                    Db::getInstance()->execute('INSERT INTO `' . _DB_PREFIX_ . 'feature_shop` (`id_feature`,`id_shop`) VALUES (' . $FeatureNameId . ', 1)');
                    Db::getInstance()->execute('INSERT INTO `' . _DB_PREFIX_ . 'feature_lang` (`id_feature`,`id_lang`, `name`) VALUES (' . $FeatureNameId . ', ' . Context::getContext()->language->id . ', "' . pSQL($attributeName) . '")');
                }

                // 1. Check if 'feature value name' exist already in database
                $FeatureValueId = Db::getInstance()->getValue('SELECT id_feature_value FROM ' . _DB_PREFIX_ . 'feature_value WHERE id_feature_value IN (SELECT id_feature_value FROM `' . _DB_PREFIX_ . 'feature_value_lang` WHERE value = "' . pSQL($attributeValue) . '") AND id_feature = ' . $FeatureNameId);
                // If 'feature value name' does not exist, insert new.
                if (empty($FeatureValueId)) {
                    Db::getInstance()->execute('INSERT INTO `' . _DB_PREFIX_ . 'feature_value` (`id_feature_value`,`id_feature`,`custom`) VALUES (0, ' . $FeatureNameId . ', 0)');
                    $FeatureValueId = Db::getInstance()->Insert_ID();
                    Db::getInstance()->execute('INSERT INTO `' . _DB_PREFIX_ . 'feature_value_lang` (`id_feature_value`,`id_lang`,`value`) VALUES (' . $FeatureValueId . ', ' . Context::getContext()->language->id . ', "' . pSQL($attributeValue) . '")');
                }
                Db::getInstance()->execute('INSERT INTO `' . _DB_PREFIX_ . 'feature_product` (`id_feature`, `id_product`, `id_feature_value`) VALUES (' . $FeatureNameId . ', ' . $product->id . ', ' . $FeatureValueId . ')');
            }
        }

        // add product image.
        $shops = Shop::getShops(true, null, true);
        $image = new Image();
        $image->id_product = $product->id;
        $image->position = Image::getHighestPosition($product->id) + 1;
        $image->cover = true;
        if (($image->validateFields(false, true)) === true && ($image->validateFieldsLang(false, true)) === true && $image->add()) {
            $image->associateTo($shops);
            if (!uploadImage($product->id, $image->id, $imgUrl)) {
                $image->delete();
            }
        }
        echo 'Product added successfully (ID: ' . $product->id . ')';
    }

    function createMultiLangField($field) {
        $res = array();
        foreach (Language::getIDs(false) as $id_lang) {
            $res[$id_lang] = $field;
        }
        return $res;
    }

    function uploadImage($id_entity, $id_image = null, $imgUrl) {
        $tmpfile = tempnam(_PS_TMP_IMG_DIR_, 'ps_import');
        $watermark_types = explode(',', Configuration::get('WATERMARK_TYPES'));
        $image_obj = new Image((int)$id_image);
        $path = $image_obj->getPathForCreation();
        $imgUrl = str_replace(' ', '%20', trim($imgUrl));
        // Evaluate the memory required to resize the image: if it's too big we can't resize it.
        if (!ImageManager::checkImageMemoryLimit($imgUrl)) {
            return false;
        }
        if (@copy($imgUrl, $tmpfile)) {
            ImageManager::resize($tmpfile, $path . '.jpg');
            $images_types = ImageType::getImagesTypes('products');
            foreach ($images_types as $image_type) {
                ImageManager::resize($tmpfile, $path . '-' . stripslashes($image_type['name']) . '.jpg', $image_type['width'], $image_type['height']);
                if (in_array($image_type['id_image_type'], $watermark_types)) {
                Hook::exec('actionWatermark', array('id_image' => $id_image, 'id_product' => $id_entity));
                }
            }
        } else {
            unlink($tmpfile);
            return false;
        }
        unlink($tmpfile);
        return true;
    }

    function array_multi_search($needle,$haystack){
        foreach($haystack as $key=>$data){            
            if(in_array($needle,$data)){
                return $key;
            }
        }
    }


    function file_get_contents_utf8($fn) {
        $content = file_get_contents($fn);
         return mb_convert_encoding($content, 'UTF-8',
             mb_detect_encoding($content, 'UTF-8, ISO-8859-1', true));
   }

   function addCategory($category, $categories, $id_parrent){
       // Temporary not used - useful when displaying categories names
        $categories_names = array(
            'zarowki'  => 'Żarówki',
            'tasmy-led' => "Tasmy LED",
            'oprawy-najazdowe' => 'Oprawy najazdowe',
            'oprawy-wpuszczane'  => "Oprawy wpuszczane",
            'kinkiety' => "Kinkiety",
            'lampy-stojace' => "Lampy Stojące",
            'lampy-wiszace-i-zyrandole'  => "Lampy wiszące i żyrandole",
            'wentylatory' => "Wentylatory",
            'plafony-zewnetrzne' => "Plafony zewnętrzne",
            'lampy-ogrodowe-stojace'  => "Lampy ogrodowe stojące",
            'lampy-zewnetrzne-wiszace' => "Lampy zewnętrzne wiszące",
            'Oswietlenie' => "Oswietlenie",
            'Do ogrodu' => "Do ogrodu",
            'Do wnetrz' => "Do wnetrz"
        );
        $object = new Category();
        $link = Tools::link_rewrite($category);

        $object->name = array();
        $object->link_rewrite = array();

        foreach (Language::getLanguages(false) as $lang){
            $object->name[$lang['id_lang']] = $category ;
            // $object->name[$lang['id_lang']] = $categories_names[$category] ;

            $object->link_rewrite[$lang['id_lang']] = $link;
        }
        $object->id_parent = $id_parrent;
        $object->add();
        echo 'Category added successfully (ID: ' . $object->id . ')';
        return array('name' => $category, 'id' => $object->id);
   }


   $categories = array(
                        array('Oswietlenie', array('zarowki', 'tasmy-led', 'oprawy-najazdowe', 'oprawy-wpuszczane')),
                        array('Do wnetrz', array('kinkiety', 'lampy-stojace', 'lampy-wiszace-i-zyrandole', 'wentylatory')),
                        array('Do ogrodu', array('plafony-zewnetrzne', 'lampy-ogrodowe-stojace', 'lampy-zewnetrzne-wiszace'))
                        );



    $string = file_get_contents_utf8("/var/www/html/products_un.json");
    $json_a = json_decode($string, true);
    $categories_id = array();
    
    // Clear categories, products, features
    Db::getInstance()->execute('TRUNCATE TABLE ps_product;');
    Db::getInstance()->execute('TRUNCATE TABLE ps_product_shop;');
    Db::getInstance()->execute('TRUNCATE TABLE ps_product_lang;');

    Db::getInstance()->execute('TRUNCATE TABLE ps_image;');
    Db::getInstance()->execute('TRUNCATE TABLE ps_image_shop;');
    Db::getInstance()->execute('TRUNCATE TABLE ps_image_lang;');


    Db::getInstance()->execute('TRUNCATE TABLE ps_feature;');
    Db::getInstance()->execute('TRUNCATE TABLE ps_feature_shop;');
    Db::getInstance()->execute('TRUNCATE TABLE ps_feature_lang;');

    Db::getInstance()->execute('TRUNCATE TABLE ps_feature_value;');
    Db::getInstance()->execute('TRUNCATE TABLE ps_feature_value_lang;');
    Db::getInstance()->execute('TRUNCATE TABLE ps_feature_product;');

    Db::getInstance()->execute('DELETE FROM ps_category WHERE id_category>2;');
    foreach ($categories as $i => $value) {
        $parrent_id = Configuration::get('PS_HOME_CATEGORY');
        $id_name_array = addCategory($value[0], $categories, $parrent_id);
        array_push($categories_id, $id_name_array);
        $parrent_id = $id_name_array['id'];
        foreach ($value[1] as $j => $category) {
            $id_name_array = addCategory($category, $categories, $parrent_id);
            array_push($categories_id, $id_name_array);
        }
    }

    // $array=$clusters[$key];

    foreach ($json_a as $product_item => $product_i) {
        $key=array_multi_search($product_i['category'], $categories_id);

        addProduct(
            '1234567891234',                         // Product EAN13
            trim($product_i['short_about']),                         // Product reference
            $product_i['name'],                               // Product name
            5,                                       // Product quantity
            $product_i['description'],              // Product description
            $product_i['attributes'],
            str_replace(' ', '', str_replace(',', '.', $product_i['price'])),                                // Product price
            $product_i['img'],       // Product image
            $categories_id[$key]['id'],                                       // Product default category
        );
    }
    

