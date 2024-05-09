
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from imdb import IMDb

class Genre: 
    def __init__(self, name):
        self.name = name  
        self.movies = [] 

    def add_movie(self, movie):
        self.movies.append(movie) 

    def list_movies(self):
        if not self.movies:
            print("No movies in this genre yet.")
        for movie in self.movies: 
            print(f"- {movie['title']} ({movie.get('rating', 'NR')}/10)")

class MovieApp: 
    def __init__(self):
        self.imdb = IMDb() 
        self.genres = {
            "Action": Genre("Action"),
            "Comedy": Genre("Comedy"),
            "Drama": Genre("Drama"),
            "Horror": Genre("Horror"),
            "Romance": Genre("Romance"),
            "Thriller": Genre("Thriller")
        }

    def search_and_add_movie(self, genre_name):

        title = input("Enter movie title to search: ")
        results = self.imdb.search_movie(title) 
        if results:
            print("Select the movie you want to add:")
            for i, result in enumerate(results[:10]):
                print(f"{i + 1}. {result['title']} ({result.get('year', 'Unknown year')})")

            choice = int(input("Choose a number (or 0 to cancel): ")) 
            if choice:
                selected_movie = results[choice - 1]
                self.imdb.update(selected_movie)
                self.genres[genre_name].add_movie(selected_movie) 
                print(f"Added {selected_movie['title']} to {genre_name} genre.") 
        else:
            print("No results found.")

    def rate_movie(self, genre):

        for i, movie in enumerate(genre.movies): 
            print(f"{i+1}. {movie['title']}")

        movie_choice = int(input("Enter movie number (or 0 to cancel): ")) 
        if 0 < movie_choice <= len(genre.movies):
            rating = int(input("Enter rating (1-10): ")) 
            if 1 <= rating <= 10:
                genre.movies[movie_choice - 1]['rating'] = rating 
                print(f"Rating updated for {genre.movies[movie_choice - 1]['title']}") 
            else:
                print("Invalid rating. Please enter a number between 1 and 10.") 
        else:
            print("No valid selection made.") 

    def main(self): 

        while True:
            print("Generalize Movie App")
            print("1. List Genres")
            print("2. View Movies in a Genre")
            print("3. Add Movie to a Genre")
            print("4. Rate a Movie in a Genre")
            print("5. Exit")
            choice = input("Enter your choice: ") 

            if choice == "1":
                for name in self.genres:
                    print(f"- {name}")

            elif choice == "2":
                genre_name = input("Enter genre name: ").title()
                if genre_name in self.genres:
                    self.genres[genre_name].list_movies()
                else:
                    print(f"Genre '{genre_name}' not found.")

            elif choice == "3":
                genre_name = input("Enter genre name for adding movie: ").title()
                if genre_name in self.genres:
                    self.search_and_add_movie(genre_name) 
                else:
                    print(f"Genre '{genre_name}' not found.")

            elif choice == "4":
                genre_name = input("Enter genre name for rating movie: ").title()
                if genre_name in self.genres:
                    self.rate_movie(self.genres[genre_name])
                else:
                    print(f"Genre '{genre_name}' not found.")

            elif choice == "5":
                print("Exiting Generalize Movie App.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = MovieApp()
    app.main()




class TestGenre(unittest.TestCase):
    def test_add_movie(self):
        genre = Genre("Action")
        movie = {"title": "The Dark Knight", "rating": 9}
        genre.add_movie(movie)
        self.assertIn(movie, genre.movies)

    def test_list_movies(self):
        genre = Genre("Action")
        movie1 = {"title": "The Dark Knight", "rating": 9}
        movie2 = {"title": "Inception", "rating": 8}
        genre.add_movie(movie1)
        genre.add_movie(movie2)
        expected_output = "- The Dark Knight (9/10)\n- Inception (8/10)\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            genre.list_movies()
            self.assertEqual(fake_out.getvalue(), expected_output)


class TestMovieApp(unittest.TestCase):
    def setUp(self):
        self.movie_app = MovieApp()

    @patch('builtins.input', side_effect=['1'])
    def test_list_genres(self, mock_input):
        expected_output = "- Action\n- Comedy\n- Drama\n- Horror\n- Romance\n- Thriller\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.movie_app.main()
            self.assertEqual(fake_out.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['2', 'Action'])
    def test_view_movies(self, mock_input):
        expected_output = "No movies in this genre yet.\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.movie_app.main()
            self.assertEqual(fake_out.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['3', 'Action', 'The Dark Knight'])
    @patch('imdb.IMDb.search_movie', return_value=[{"title": "The Dark Knight", "rating": 9}])
    def test_add_movie(self, mock_search_movie, mock_input):
        expected_output = "Added The Dark Knight to Action genre.\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.movie_app.main()
            self.assertEqual(fake_out.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['4', 'Action'])
    def test_rate_movie(self, mock_input):
        genre = Genre("Action")
        genre.add_movie({"title": "The Dark Knight"})
        with patch('builtins.input', side_effect=['1', '10']), \
             patch('sys.stdout', new=StringIO()) as fake_out:
            self.movie_app.rate_movie(genre)
            self.assertEqual(genre.movies[0]['rating'], 10)
            self.assertEqual(fake_out.getvalue(), "Rating updated for The Dark Knight\n")

    @patch('builtins.input', side_effect=['5'])
    def test_exit(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.movie_app.main()
            self.assertEqual(fake_out.getvalue(), "Exiting Generalize Movie App.\n")


if __name__ == '__main__':
    unittest.main()