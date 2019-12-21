from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)


movies = [
    {
        'id': 1,
        'title': 'Once upon a time in Hollywood...',
        'description': 'Brand new movie by Quentin Tarantino',
        'yearOfRelease': '2019'
    },
    {
        'id': 2,
        'title': 'The Witcher',
        'description': 'Netflix original series based on a series of novel by Andrzej Sapkovsky',
        'yearOfRelease': '2019'
    }
]


@app.route('/api/movies', methods=['GET'])
def get_movies():
    return jsonify({'movies': movies})

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = list(filter(lambda t: t['id'] == movie_id, movies))[0]
    if len(movies) == 0:
        abort(404)
    return jsonify({'movie': movie})

@app.route('/api/movies', methods=['POST'])
def create_movie():
    if not request.json or not 'title' in request.json:
        abort(400)
    movie = {
        'id': movies[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'yearOfRelease': request.json.get('yearOfRelease', "")
    }
    movies.append(movie)
    return jsonify({'movie': movie}), 201

@app.route('/api/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = list(filter(lambda t: t['id'] == movie_id, movies))
    if len(movie) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'yearOfRelease' in request.json and type(request.json['yearOfRelease']) is not unicode:
        abort(400)
    movie[0]['title'] = request.json.get('title', movie[0]['title'])
    movie[0]['description'] = request.json.get('description', movie[0]['description'])
    movie[0]['unicode'] = request.json.get('unicode', movie[0]['done'])
    return jsonify({'movie': movie[0]})

@app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = filter(lambda t: t['id'] == movie_id, movies)
    if len(movie) == 0:
        abort(404)
    movies.remove(movie[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)