from flask import render_template

def add_index_route(main_bp):
    @main_bp.route('/')
    def index():
        return render_template('index.html')
