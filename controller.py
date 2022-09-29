import os
from flask import Flask, render_template
from flask import request
from sqlalchemy import Time, create_engine
import pandas as pd
import model

app = Flask(__name__)

@app.route("/")
def index():    
    filtrar = model.Dashboard()
    regiões = filtrar.opçãodefiltroregião()
    bus = filtrar.opçãodefiltrobu()
    return render_template("index.html", regiões = regiões, bus = bus)

        
if __name__ == "__main__":
    app.run(debug= True)