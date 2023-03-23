from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import sqlite3

app = Flask(__name__)
api = Api(app)

class VegetablePrices(Resource):
    def get(self,name):
        # get query parameter
        #name = request.args.get('name')
        
        # validate query parameter
        if not name:
            return {"message": "กรุณาพิมพ์อีกครั้งครับ."}, 400
        
        # fetch data from database
        conn = sqlite3.connect('VEGETABLEPRICES.db')
        c = conn.cursor()
        query = f"SELECT * FROM prices WHERE name='{name}'"
        c.execute(query)
        rows = c.fetchall()
        
        # format and return data
        if rows:
            result = []
            for row in rows:
                result.append({
                    "date": row[0],
                    "name": row[1],
                    "min_price": row[2],
                    "max_price": row[3],
                    "avg_price": row[4],
                    "unit": row[5]
                })
            return {"data": result}, 200
        else:
            return {"message": f"ไม่พบข้อมูล {name}. ครับ"}, 404

# call
api.add_resource(VegetablePrices, "/vegetable/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)
