from tehran_stocks import download, Stocks, db

SAIPA = "44891482026867833"

stock1 = Stocks.query.filter_by(code='46348559193224090').first() # find by code on tsetmc url
stock = Stocks.query.filter(Stocks.name.like('%فولاد%')).first() 
stock.update() 
print(Stocks.df)
stock1.df.to_csv('price.csv')

class TestNames:
    def test_id_from_group(self):
        ids = download.get_stock_ids(34)
        assert ids, "no id available"

    def test_saipa_in_that(self):
        ids = download.get_stock_ids(34)

        assert SAIPA in ids, "Saipa is not in group"

    def test_get_groups(self):
        groups = download.get_stock_groups()
        size = len(groups)
        assert size > 10, "there is a problem during downloading groups"


class TestStockDetail:
    def test_get_detail(self):
        data = download.get_stock_detail(SAIPA, 34)
        if isinstance(data, dict):
            assert data["code"] == SAIPA
        if isinstance(data, str):
            assert data == "exist"

    def test_error_get_detail(self):
        FAKE = 278496000000000
        be_false = download.get_stock_detail(FAKE, 23)
        assert not be_false, "it saves data that is not valid"
