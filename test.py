from selenium import webdriver
import md5
import random
import string


#random string generation
def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def testmd5(depth, debug=False, debug_pairs=5):
    # Pairs of random strings and their calculated md5 digests
    if debug: print("Calculating pairs...")
    random_pairs = []
    for i in range(0, int(depth)):
        tmp = id_generator()
        hash_tmp = md5.new(tmp).hexdigest()
        random_pairs.append([tmp, hash_tmp])


    if debug:
        print("First 5 pairs:")
        print(random_pairs[:int(debug_pairs)])

    driver = webdriver.Chrome("/var/www/html/chromedriver")


    # Test each random string and compare the digests with using the python library and the javascript function
    successful_pairs = 0
    for pair in random_pairs:
        driver.get("http://localhost/md5-hasher.html")
        input_field = driver.find_element_by_id("input")
        submit_btn = driver.find_element_by_id("mainbutton")
        input_field.send_keys(pair[0])
        submit_btn.click()
        try:
            assert str(pair[1]) in driver.page_source
        except:
            continue
        successful_pairs += 1

    driver.close()

    #Statistics
    print(str(successful_pairs) + "/" + str(len(random_pairs)) + " Successful")
    print(str(successful_pairs*100/len(random_pairs)) + "%")


testmd5(20, debug=True)
