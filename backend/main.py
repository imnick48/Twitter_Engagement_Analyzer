from flask import Flask, request
from fetchtweet import getSentiment,count_occ
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
@app.route("/getSentiment",methods=["GET"])
def sentiment():
    link=request.args.get("link")
    res=count_occ(getSentiment(link))
    return {"result":res}
if __name__ == "__main__":
    app.run(debug=True)