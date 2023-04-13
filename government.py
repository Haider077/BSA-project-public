
class Govt():
    def __init__(self, name, taxRate, illegalProducts):
        self.name = name
        self.taxRate = taxRate
        self.illegalProducts = illegalProducts


    # getters
    def get_name(self):
        return self.name

    def get_taxRate(self):
        return self.taxRate

    def get_illegalProducts(self):
        return self.illegalProducts


    # setters
    def set_taxRate(self, newRate):
        self.taxRate = newRate

    def set_name(self, name):
        self.name = name

    def set_illegalProducts(self, illegalProducts):
        self.illegalProducts = illegalProducts


    # checks if a product is banned by this govt, returns true if banned, false if not
    def product_is_banned(self, product):

        in_list = False

        for banned in self.illegalProducts:
                if banned == product:
                    in_list = True

        return in_list


    # checks if a product is already banned, if a product is already on the list, does nothing
    # otherwise adds product to the list of illegal products
    def ban_product(self, product):

        if self.product_is_banned(product) == False:
            self.illegalProducts.append(product)
        else:
            pass


    # checks if product is in the list, and removes it if present, otherwise does nothing
    def legalize_product(self, product):

        if self.product_is_banned(product):
            self.illegalProducts.remove(product)
        else:
            pass

        