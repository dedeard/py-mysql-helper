from dotenv import load_dotenv
from DB import DB

load_dotenv()

DB.DB.get_instance() \
    .update("users") \
    .set_values({"name": "abg"}) \
    .where() \
    .equal('id', 5) \
    .exec()

DB.DB.get_instance() \
    .delete("users") \
    .where() \
    .equal('id', 5) \
    .exec()

res = DB.DB.get_instance() \
    .select("users") \
    .set_column(["*"]) \
    .where() \
    .not_like('name', "%r%") \
    .order_by(["id"], 'asc') \
    .exec()

if not res.error():
    print(res.results())
else:
    print(res.error())
